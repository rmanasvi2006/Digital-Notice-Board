from app import app, db
from app import Notice

with app.app_context():
    # Drop the existing table
    db.drop_all()
    # Create new table with updated schema
    db.create_all()
