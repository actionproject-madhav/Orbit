"""Astrology calculation service using kerykeion for natal charts."""

from app.utils.zodiac_compat import get_sun_sign


def calculate_natal_chart(name: str, year: int, month: int, day: int,
                          hour: int, minute: int, city: str) -> dict:
    """
    Calculate a full natal chart (sun, moon, rising) using kerykeion.
    Returns dict with sun, moon, rising signs.
    Falls back to sun-sign only if kerykeion fails.
    """
    try:
        from kerykeion import AstrologicalSubject

        subject = AstrologicalSubject(
            name=name,
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            city=city,
        )

        return {
            "sun": subject.sun.get("sign", get_sun_sign(month, day)),
            "moon": subject.moon.get("sign"),
            "rising": subject.first_house.get("sign"),
        }
    except Exception as e:
        print(f"Kerykeion natal chart failed: {e}")
        # Fallback to manual sun sign calculation
        return {
            "sun": get_sun_sign(month, day),
            "moon": None,
            "rising": None,
        }


def get_element(sign: str) -> str:
    """Get the element for a zodiac sign."""
    elements = {
        "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
        "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
        "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
        "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water",
    }
    return elements.get(sign, "Unknown")


def get_modality(sign: str) -> str:
    """Get the modality for a zodiac sign."""
    modalities = {
        "Aries": "Cardinal", "Cancer": "Cardinal", "Libra": "Cardinal", "Capricorn": "Cardinal",
        "Taurus": "Fixed", "Leo": "Fixed", "Scorpio": "Fixed", "Aquarius": "Fixed",
        "Gemini": "Mutable", "Virgo": "Mutable", "Sagittarius": "Mutable", "Pisces": "Mutable",
    }
    return modalities.get(sign, "Unknown")
