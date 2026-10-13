"""Creates any missing database tables, e.g. on a fresh Neon database."""

from app import app, db

with app.app_context():
    db.create_all()
    print(f"Tables created on {db.engine.url.render_as_string()}")
