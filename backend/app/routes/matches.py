"""Match routes: generate matches, get user's match."""

from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId

from app import mongo
from app.models.match import serialize_match

matches_bp = Blueprint("matches", __name__)


@matches_bp.route("/generate", methods=["POST"])
def generate_matches():
    """
    Admin endpoint: Generate matches for all onboarded users.
    In production, protect with admin auth. For MVP, use a simple secret.
    """
    data = request.get_json() or {}
    admin_secret = data.get("admin_secret", "")

    if admin_secret != current_app.config.get("SECRET_KEY"):
        return jsonify({"error": "Unauthorized"}), 401

    from app.services.matching import run_matching

    try:
        results = run_matching()
        return jsonify({
            "message": "Matching complete",
            "matches_created": results["matches_created"],
            "users_matched": results["users_matched"],
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@matches_bp.route("/me", methods=["GET"])
@jwt_required()
def get_my_match():
    """Get the current user's Valentine match."""
    user_id = get_jwt_identity()
    user_oid = ObjectId(user_id)

    # Find match where user is either user1 or user2
    match = mongo.db.matches.find_one({
        "$or": [
            {"user1_id": user_oid},
            {"user2_id": user_oid},
        ]
    })

    if not match:
        return jsonify({
            "match": None,
            "status": "waiting",
            "message": "Your cosmic match is being aligned by the stars...",
        }), 200

    # Determine reveal status
    reveal_date_str = current_app.config.get("MATCH_REVEAL_DATE", "2026-02-13T20:00:00")
    reveal_date = datetime.fromisoformat(reveal_date_str).replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)

    is_revealed = now >= reveal_date or match.get("revealed", False)

    if not is_revealed:
        # Return teaser without partner details
        return jsonify({
            "match": {
                "id": str(match["_id"]),
                "compatibility_score": match.get("compatibility_score", 0),
                "match_type": match.get("match_type", "valentine"),
                "revealed": False,
                "reveal_date": reveal_date_str,
            },
            "status": "countdown",
            "message": "Your cosmic match will be revealed on Valentine's Eve!",
        }), 200

    # Full reveal - get partner info
    partner_id = match["user2_id"] if match["user1_id"] == user_oid else match["user1_id"]
    partner = mongo.db.users.find_one({"_id": partner_id})

    # Mark as revealed
    if not match.get("revealed"):
        mongo.db.matches.update_one(
            {"_id": match["_id"]},
            {"$set": {"revealed": True}}
        )

    return jsonify({
        "match": serialize_match(match, partner),
        "status": "revealed",
        "message": "The stars have aligned!",
    }), 200
