import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "orbit-dev-secret-key-change-me")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/orbit")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "orbit-jwt-secret-change-me")
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24 * 30  # 30 days
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ALLOWED_EMAIL_DOMAINS = ["rollins.edu"]
    MATCH_REVEAL_DATE = os.getenv("MATCH_REVEAL_DATE", "2026-02-13T20:00:00")
