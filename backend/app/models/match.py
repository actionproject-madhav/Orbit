"""Match model helpers for MongoDB."""

from datetime import datetime, timezone


def create_match_doc(
    user1_id,
    user2_id,
    compatibility_score: int,
    astro_breakdown: dict,
    cosmic_description: str,
    match_type: str = "valentine",
    reveal_date: str = None,
) -> dict:
    """Create a new match document."""
    return {
        "user1_id": user1_id,
        "user2_id": user2_id,
        "compatibility_score": compatibility_score,
        "astro_breakdown": astro_breakdown,
        "cosmic_description": cosmic_description,
        "match_type": match_type,
        "revealed": False,
        "reveal_date": reveal_date,
        "created_at": datetime.now(timezone.utc),
    }


def serialize_match(match: dict, partner: dict = None) -> dict:
    """Convert MongoDB match doc to JSON-safe dict."""
    if not match:
        return None

    result = {
        "id": str(match["_id"]),
        "compatibility_score": match.get("compatibility_score", 0),
        "astro_breakdown": match.get("astro_breakdown", {}),
        "cosmic_description": match.get("cosmic_description", ""),
        "match_type": match.get("match_type", "valentine"),
        "revealed": match.get("revealed", False),
        "reveal_date": match.get("reveal_date"),
        "created_at": match.get("created_at", "").isoformat() if match.get("created_at") else None,
    }

    if partner:
        result["partner"] = {
            "name": partner.get("name", ""),
            "zodiac": partner.get("zodiac", {}),
            "hobbies": partner.get("hobbies", []),
            "instagram": partner.get("instagram"),
            "phone": partner.get("phone"),
        }

    return result
