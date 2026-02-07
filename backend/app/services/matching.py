"""Matching algorithm: pairs users based on zodiac + hobbies + intent."""

from bson.objectid import ObjectId
from app import mongo
from app.utils.zodiac_compat import get_compatibility
from app.models.match import create_match_doc
from app.services.llm import generate_cosmic_description


def calculate_pair_score(user1: dict, user2: dict) -> tuple:
    """
    Calculate compatibility score between two users.
    Returns (total_score, breakdown_dict).
    """
    zodiac1 = user1.get("zodiac", {})
    zodiac2 = user2.get("zodiac", {})

    # 1. Sun sign compatibility (40% weight)
    sun1 = zodiac1.get("sun", "")
    sun2 = zodiac2.get("sun", "")
    sun_score = get_compatibility(sun1, sun2) if sun1 and sun2 else 50
    weighted_sun = sun_score * 0.40

    # 2. Moon sign compatibility (25% weight)
    moon1 = zodiac1.get("moon")
    moon2 = zodiac2.get("moon")
    if moon1 and moon2:
        moon_score = get_compatibility(moon1, moon2)
    else:
        moon_score = sun_score  # fallback
    weighted_moon = moon_score * 0.25

    # 3. Hobby overlap (20% weight)
    hobbies1 = set(user1.get("hobbies", []))
    hobbies2 = set(user2.get("hobbies", []))
    common_hobbies = len(hobbies1 & hobbies2)
    hobby_score = min(common_hobbies / 3 * 100, 100) if hobbies1 or hobbies2 else 50
    weighted_hobby = hobby_score * 0.20

    # 4. Looking-for alignment (15% weight)
    lf1 = user1.get("looking_for", "both")
    lf2 = user2.get("looking_for", "both")
    alignment_score = _intent_compatibility(lf1, lf2)
    weighted_intent = alignment_score * 0.15

    total = round(weighted_sun + weighted_moon + weighted_hobby + weighted_intent)

    breakdown = {
        "sun_compat": sun_score,
        "moon_compat": moon_score,
        "hobby_overlap": common_hobbies,
        "hobby_score": round(hobby_score),
        "intent_score": alignment_score,
    }

    return total, breakdown


def _intent_compatibility(lf1: str, lf2: str) -> int:
    """Score how well two users' intents align."""
    if lf1 == lf2:
        return 100
    if "both" in (lf1, lf2):
        return 80
    # friend vs date mismatch
    return 40


def run_matching() -> dict:
    """
    Run the matching algorithm for all onboarded users.
    Each user gets their single best cosmic Valentine match.
    Uses a greedy approach: pair highest-scoring pairs first.
    """
    # Get all onboarded users
    users = list(mongo.db.users.find({"onboarding_complete": True}))

    if len(users) < 2:
        return {"matches_created": 0, "users_matched": 0}

    # Clear existing matches
    mongo.db.matches.delete_many({})

    # Calculate all pair scores
    pair_scores = []
    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            u1, u2 = users[i], users[j]

            # Basic gender/interest filtering
            if not _gender_compatible(u1, u2):
                continue

            score, breakdown = calculate_pair_score(u1, u2)
            pair_scores.append({
                "user1": u1,
                "user2": u2,
                "score": score,
                "breakdown": breakdown,
            })

    # Sort by score descending
    pair_scores.sort(key=lambda x: x["score"], reverse=True)

    # Greedy matching: pair highest scores first, each user matched once
    matched_ids = set()
    matches_created = 0

    for pair in pair_scores:
        u1_id = pair["user1"]["_id"]
        u2_id = pair["user2"]["_id"]

        if u1_id in matched_ids or u2_id in matched_ids:
            continue

        # Generate LLM cosmic description
        try:
            description = generate_cosmic_description(
                pair["user1"], pair["user2"], pair["score"]
            )
        except Exception as e:
            print(f"LLM description failed: {e}")
            description = _fallback_description(pair["user1"], pair["user2"], pair["score"])

        # Create match document
        match_doc = create_match_doc(
            user1_id=u1_id,
            user2_id=u2_id,
            compatibility_score=pair["score"],
            astro_breakdown=pair["breakdown"],
            cosmic_description=description,
            match_type="valentine",
        )
        mongo.db.matches.insert_one(match_doc)

        matched_ids.add(u1_id)
        matched_ids.add(u2_id)
        matches_created += 1

    return {
        "matches_created": matches_created,
        "users_matched": len(matched_ids),
    }


def _gender_compatible(u1: dict, u2: dict) -> bool:
    """Check if two users are compatible based on gender preferences."""
    g1 = u1.get("gender")
    g2 = u2.get("gender")
    int1 = u1.get("interested_in", [])
    int2 = u2.get("interested_in", [])

    # If no preferences set, allow match
    if not int1 and not int2:
        return True
    if not int1:
        return g1 in int2 if g1 else True
    if not int2:
        return g2 in int1 if g2 else True

    return (g2 in int1 if g2 else True) and (g1 in int2 if g1 else True)


def _fallback_description(user1: dict, user2: dict, score: int) -> str:
    """Generate a simple fallback description without LLM."""
    sun1 = user1.get("zodiac", {}).get("sun", "mysterious")
    sun2 = user2.get("zodiac", {}).get("sun", "mysterious")
    return (
        f"A {sun1} and a {sun2} walk onto campus... "
        f"The stars say you're {score}% cosmically aligned. "
        f"The universe clearly has plans for you two."
    )
