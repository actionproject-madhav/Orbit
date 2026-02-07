"""Email validation and verification utilities."""

import random
import string
from typing import Optional


def validate_school_email(email: str, allowed_domains: list) -> bool:
    """Check if email belongs to an allowed school domain."""
    if not email or "@" not in email:
        return False
    domain = email.split("@")[1].lower()
    return domain in [d.lower() for d in allowed_domains]


def generate_verification_code(length: int = 6) -> str:
    """Generate a random numeric verification code."""
    return "".join(random.choices(string.digits, k=length))


def send_verification_email(email: str, code: str) -> bool:
    """
    Send verification code to email.
    For MVP, we'll store the code and verify it directly.
    In production, integrate with SendGrid/Mailgun/etc.
    """
    # TODO: Integrate actual email service
    # For MVP/testing, the code is returned in the API response
    print(f"[DEV] Verification code for {email}: {code}")
    return True
