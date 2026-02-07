"""User profile routes."""

from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId

from app import mongo
from app.models.user import serialize_user
from app.utils.zodiac_compat import get_sun_sign, SIGN_DESCRIPTIONS, SIGN_EMOJIS

users_bp = Blueprint("users", __name__)


@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    """Get current user profile."""
    user_id = get_jwt_identity()
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user": serialize_user(user)}), 200


@users_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_me():
    """Update user profile (used during onboarding and profile edits)."""
    user_id = get_jwt_identity()
    data = request.get_json()

    # Allowed fields to update
    allowed_fields = [
        "name", "dob", "birth_time", "birth_location",
        "phone", "instagram", "hobbies", "looking_for",
        "gender", "interested_in",
    ]

    update = {}
    for field in allowed_fields:
        if field in data:
            update[field] = data[field]

    # Calculate zodiac signs if DOB is provided
    if "dob" in data and data["dob"]:
        try:
            dob = datetime.strptime(data["dob"], "%Y-%m-%d")
            sun_sign = get_sun_sign(dob.month, dob.day)
            update["zodiac"] = update.get("zodiac", {})
            update["zodiac"] = {"sun": sun_sign, "moon": None, "rising": None}

            # If birth_time and location provided, try to calculate moon/rising
            birth_time = data.get("birth_time") or None
            birth_location = data.get("birth_location") or None

            if birth_time and birth_location:
                try:
                    from app.services.astrology import calculate_natal_chart
                    chart = calculate_natal_chart(
                        name=data.get("name", "User"),
                        year=dob.year,
                        month=dob.month,
                        day=dob.day,
                        hour=int(birth_time.split(":")[0]),
                        minute=int(birth_time.split(":")[1]),
                        city=birth_location,
                    )
                    if chart:
                        update["zodiac"] = chart
                except Exception as e:
                    print(f"Natal chart calculation failed: {e}")
                    # Fall back to sun sign only
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    # Check if onboarding is complete
    if data.get("onboarding_complete"):
        update["onboarding_complete"] = True

    update["updated_at"] = datetime.now(timezone.utc)

    mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update}
    )

    # Return updated user
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return jsonify({"user": serialize_user(user)}), 200


@users_bp.route("/me/cosmic", methods=["GET"])
@jwt_required()
def get_cosmic_profile():
    """Get detailed zodiac profile for the user."""
    user_id = get_jwt_identity()
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        return jsonify({"error": "User not found"}), 404

    zodiac = user.get("zodiac", {})
    sun = zodiac.get("sun")

    profile = {
        "sun_sign": sun,
        "moon_sign": zodiac.get("moon"),
        "rising_sign": zodiac.get("rising"),
        "sun_description": SIGN_DESCRIPTIONS.get(sun, ""),
        "sun_emoji": SIGN_EMOJIS.get(sun, ""),
        "name": user.get("name", ""),
    }

    return jsonify({"cosmic_profile": profile}), 200
