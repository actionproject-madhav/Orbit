"""User model helpers for MongoDB."""

from datetime import datetime, timezone
from typing import Optional


def create_user_doc(
    email: str,
    is_guest: bool = False,
    name: str = "",
    password_hash: str = "",
) -> dict:
    """Create a new user document for MongoDB."""
    return {
        "email": email,
        "password_hash": password_hash,
        "is_guest": is_guest,
        "name": name,
        "dob": None,
        "birth_time": None,
        "birth_location": None,
        "phone": None,
        "instagram": None,
        "hobbies": [],
        "year": None,          # "freshman" | "sophomore" | "junior" | "senior" | "grad" | "other"
        "vibe_answers": {},     # {"weekend": "out", "love_language": "time", "red_flag": "flaky"}
        "looking_for": None,   # "friend" | "date" | "both"
        "gender": None,
        "interested_in": [],
        "zodiac": {
            "sun": None,
            "moon": None,
            "rising": None,
        },
        "school": "rollins",
        "onboarding_complete": False,
        "verification_code": None,
        "email_verified": is_guest,  # guests skip verification
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }


def serialize_user(user: dict) -> dict:
    """Convert MongoDB user doc to JSON-safe dict."""
    if not user:
        return None
    return {
        "id": str(user["_id"]),
        "email": user.get("email", ""),
        "is_guest": user.get("is_guest", False),
        "name": user.get("name", ""),
        "dob": user.get("dob"),
        "birth_time": user.get("birth_time"),
        "birth_location": user.get("birth_location"),
        "phone": user.get("phone"),
        "instagram": user.get("instagram"),
        "hobbies": user.get("hobbies", []),
        "year": user.get("year"),
        "vibe_answers": user.get("vibe_answers", {}),
        "looking_for": user.get("looking_for"),
        "gender": user.get("gender"),
        "interested_in": user.get("interested_in", []),
        "zodiac": user.get("zodiac", {}),
        "school": user.get("school", "rollins"),
        "onboarding_complete": user.get("onboarding_complete", False),
        "email_verified": user.get("email_verified", False),
        "created_at": user.get("created_at", "").isoformat() if user.get("created_at") else None,
    }
