"""
12x12 Zodiac Sign Compatibility Matrix
Scores from 0-100 based on traditional astrological compatibility.
"""

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Compatibility matrix (symmetric) - traditional astrology based
# Same sign, trine (4 apart), sextile (2 apart) = high
# Square (3 apart) = tension/passion, Opposition (6 apart) = attraction/challenge
_MATRIX = [
    #  Ari  Tau  Gem  Can  Leo  Vir  Lib  Sco  Sag  Cap  Aqu  Pis
    [  75,  55,  78,  42,  93,  50,  72,  48,  93,  47,  78,  67],  # Aries
    [  55,  75,  60,  85,  55,  90,  62,  88,  40,  95,  58,  85],  # Taurus
    [  78,  60,  75,  55,  80,  62,  88,  48,  78,  50,  93,  55],  # Gemini
    [  42,  85,  55,  75,  50,  78,  42,  92,  40,  62,  48,  95],  # Cancer
    [  93,  55,  80,  50,  75,  55,  85,  58,  93,  48,  65,  50],  # Leo
    [  50,  90,  62,  78,  55,  75,  55,  82,  48,  92,  50,  68],  # Virgo
    [  72,  62,  88,  42,  85,  55,  75,  60,  72,  48,  85,  55],  # Libra
    [  48,  88,  48,  92,  58,  82,  60,  75,  55,  78,  50,  90],  # Scorpio
    [  93,  40,  78,  40,  93,  48,  72,  55,  75,  50,  85,  62],  # Sagittarius
    [  47,  95,  50,  62,  48,  92,  48,  78,  50,  75,  55,  70],  # Capricorn
    [  78,  58,  93,  48,  65,  50,  85,  50,  85,  55,  75,  58],  # Aquarius
    [  67,  85,  55,  95,  50,  68,  55,  90,  62,  70,  58,  75],  # Pisces
]

# Build lookup dict for fast access
ZODIAC_MATRIX = {}
for i, sign1 in enumerate(SIGNS):
    ZODIAC_MATRIX[sign1] = {}
    for j, sign2 in enumerate(SIGNS):
        ZODIAC_MATRIX[sign1][sign2] = _MATRIX[i][j]


def get_compatibility(sign1: str, sign2: str) -> int:
    """Get compatibility score between two zodiac signs (0-100)."""
    s1 = sign1.capitalize()
    s2 = sign2.capitalize()
    if s1 in ZODIAC_MATRIX and s2 in ZODIAC_MATRIX[s1]:
        return ZODIAC_MATRIX[s1][s2]
    return 50  # default


def get_sun_sign(month: int, day: int) -> str:
    """Determine sun sign from birth month and day."""
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    else:
        return "Pisces"


SIGN_DESCRIPTIONS = {
    "Aries": "The Ram - Bold, ambitious, and ready to charge into anything",
    "Taurus": "The Bull - Grounded, loyal, and unapologetically stubborn",
    "Gemini": "The Twins - Witty, curious, and never boring",
    "Cancer": "The Crab - Nurturing, intuitive, and emotionally deep",
    "Leo": "The Lion - Confident, dramatic, and impossible to ignore",
    "Virgo": "The Maiden - Analytical, helpful, and detail-obsessed",
    "Libra": "The Scales - Charming, fair, and aesthetically gifted",
    "Scorpio": "The Scorpion - Intense, magnetic, and fiercely loyal",
    "Sagittarius": "The Archer - Adventurous, optimistic, and brutally honest",
    "Capricorn": "The Goat - Disciplined, ambitious, and surprisingly funny",
    "Aquarius": "The Water Bearer - Innovative, independent, and wonderfully weird",
    "Pisces": "The Fish - Dreamy, empathetic, and creatively gifted",
}

SIGN_EMOJIS = {
    "Aries": "♈",
    "Taurus": "♉",
    "Gemini": "♊",
    "Cancer": "♋",
    "Leo": "♌",
    "Virgo": "♍",
    "Libra": "♎",
    "Scorpio": "♏",
    "Sagittarius": "♐",
    "Capricorn": "♑",
    "Aquarius": "♒",
    "Pisces": "♓",
}
