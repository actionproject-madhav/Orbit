"""LLM wrapper for generating cosmic compatibility descriptions."""

import os
from openai import OpenAI


def generate_cosmic_description(user1: dict, user2: dict, score: int) -> str:
    """
    Use OpenAI to generate a fun, goofy cosmic compatibility blurb.
    Falls back to template if API key not set.
    """
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return _template_description(user1, user2, score)

    client = OpenAI(api_key=api_key)

    zodiac1 = user1.get("zodiac", {})
    zodiac2 = user2.get("zodiac", {})
    hobbies1 = ", ".join(user1.get("hobbies", []))
    hobbies2 = ", ".join(user2.get("hobbies", []))

    prompt = f"""You are the goofy campus astrologer for Orbit, a Valentine's matching app at Rollins College.
Write a fun, playful, Gen-Z-friendly 2-3 sentence cosmic compatibility blurb for these two people.

Person 1: {user1.get('name', 'Star Child 1')}
  Sun: {zodiac1.get('sun', 'Unknown')} | Moon: {zodiac1.get('moon', 'Unknown')} | Rising: {zodiac1.get('rising', 'Unknown')}
  Vibes: {hobbies1 or 'mysterious'}

Person 2: {user2.get('name', 'Star Child 2')}
  Sun: {zodiac2.get('sun', 'Unknown')} | Moon: {zodiac2.get('moon', 'Unknown')} | Rising: {zodiac2.get('rising', 'Unknown')}
  Vibes: {hobbies2 or 'mysterious'}

Compatibility: {score}%

Rules:
- Reference real astrology (elements, ruling planets, house placements)
- Keep it light, goofy, campus vibes — like a friend texting you about your crush
- Make it feel personal and specific to their signs
- Include one playful prediction about what they'd do together on campus
- Do NOT use generic dating app language. Be creative and cosmic.
- Keep it under 60 words."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a witty, Gen-Z campus astrologer who writes cosmic compatibility blurbs."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.9,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return _template_description(user1, user2, score)


def _template_description(user1: dict, user2: dict, score: int) -> str:
    """Fallback template-based descriptions."""
    sun1 = user1.get("zodiac", {}).get("sun", "Cosmic")
    sun2 = user2.get("zodiac", {}).get("sun", "Cosmic")

    templates = [
        f"When a {sun1} meets a {sun2}, the campus literally shakes. "
        f"At {score}% cosmic alignment, you two were basically written in the stars. "
        f"Expect spontaneous library study sessions that turn into deep talks about life.",

        f"A {sun1} and {sun2} combo? The planets have been gossiping about this. "
        f"Your {score}% compatibility means the universe did NOT put you in the same orbit by accident. "
        f"The stars predict a late-night campus walk that changes everything.",

        f"The {sun1}-{sun2} energy is giving main character duo vibes. "
        f"{score}% cosmically matched means even Mercury retrograde can't mess this up. "
        f"The stars say your first hangout involves food and unhinged laughter.",
    ]

    # Pick based on score range
    if score >= 80:
        return templates[0]
    elif score >= 60:
        return templates[1]
    else:
        return templates[2]
