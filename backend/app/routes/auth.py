"""Authentication routes: register, verify, login, guest."""

import uuid
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from bson.objectid import ObjectId
import bcrypt

from app import mongo
from app.models.user import create_user_doc, serialize_user
from app.utils.email import validate_school_email, generate_verification_code, send_verification_email

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register with school email. Sends a verification code."""
    data = request.get_json()
    email = data.get("email", "").strip().lower()

    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Validate school email domain
    allowed_domains = current_app.config.get("ALLOWED_EMAIL_DOMAINS", ["rollins.edu"])
    if not validate_school_email(email, allowed_domains):
        return jsonify({"error": f"Please use your school email (@{', @'.join(allowed_domains)})"}), 400

    # Check if user already exists
    existing = mongo.db.users.find_one({"email": email})
    if existing and existing.get("email_verified"):
        return jsonify({"error": "Account already exists. Please log in."}), 409

    # Generate verification code
    code = generate_verification_code()

    if existing:
        # Update verification code for unverified user
        mongo.db.users.update_one(
            {"_id": existing["_id"]},
            {"$set": {"verification_code": code}}
        )
    else:
        # Create new user
        password = data.get("password", "")
        password_hash = ""
        if password:
            password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        user_doc = create_user_doc(email=email, password_hash=password_hash)
        user_doc["verification_code"] = code
        mongo.db.users.insert_one(user_doc)

    # Send verification email (for MVP, code is in response)
    send_verification_email(email, code)

    return jsonify({
        "message": "Verification code sent",
        "email": email,
        # Include code in dev mode for testing
        "dev_code": code,
    }), 201


@auth_bp.route("/verify", methods=["POST"])
def verify():
    """Verify email with code. Returns JWT token."""
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    code = data.get("code", "").strip()

    if not email or not code:
        return jsonify({"error": "Email and code are required"}), 400

    user = mongo.db.users.find_one({"email": email})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.get("verification_code") != code:
        return jsonify({"error": "Invalid verification code"}), 400

    # Mark as verified
    mongo.db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"email_verified": True, "verification_code": None}}
    )

    # Generate JWT
    token = create_access_token(identity=str(user["_id"]))

    user["email_verified"] = True
    return jsonify({
        "token": token,
        "user": serialize_user(user),
    }), 200


@auth_bp.route("/login", methods=["POST"])
def login():
    """Login with email. Sends verification code (passwordless)."""
    data = request.get_json()
    email = data.get("email", "").strip().lower()

    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = mongo.db.users.find_one({"email": email})
    if not user:
        return jsonify({"error": "No account found. Please register first."}), 404

    # Send new verification code for passwordless login
    code = generate_verification_code()
    mongo.db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"verification_code": code}}
    )
    send_verification_email(email, code)

    return jsonify({
        "message": "Verification code sent",
        "email": email,
        "dev_code": code,
    }), 200


@auth_bp.route("/guest", methods=["POST"])
def guest():
    """Create a guest account. Returns JWT immediately."""
    guest_id = f"guest_{uuid.uuid4().hex[:8]}"
    guest_email = f"{guest_id}@orbit.guest"

    user_doc = create_user_doc(email=guest_email, is_guest=True)
    result = mongo.db.users.insert_one(user_doc)

    token = create_access_token(identity=str(result.inserted_id))

    user_doc["_id"] = result.inserted_id
    return jsonify({
        "token": token,
        "user": serialize_user(user_doc),
    }), 201
