"""Configures the Flask app."""

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, ".env"))

# Set to 1 in the Docker image so the app behaves itself on Cloud Run
PRODUCTION = os.environ.get("PRODUCTION") == "1"

# Fail on startup rather than run half broken
if PRODUCTION:
    missing = [key for key in ("DATABASE_URL", "SECRET_KEY", "TMDB_KEY")
               if not os.environ.get(key)]
    if missing:
        raise RuntimeError(f"Missing environment variables: {missing}")

# Use Postgres (Neon) if a URL is given, otherwise fall back to local SQLite
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    # SQLAlchemy needs the driver in the scheme, Neon gives postgresql://
    for prefix in ("postgres://", "postgresql://"):
        if DATABASE_URL.startswith(prefix):
            DATABASE_URL = "postgresql+psycopg://" + \
                DATABASE_URL[len(prefix):]
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
else:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")

# Neon drops idle connections so check them before use
SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 300}
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = os.environ.get("SECRET_KEY")
WTF_CSRF_ENABLED = True

# Only send cookies over HTTPS in production
SESSION_COOKIE_SECURE = PRODUCTION
REMEMBER_COOKIE_SECURE = PRODUCTION

TMDB_KEY = os.environ.get("TMDB_KEY")
