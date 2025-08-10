from app import app, db
from app import Notice, Comment

# Create tables
with app.app_context():
    # Drop the existing table
    db.drop_all()
    # Create new table with updated schema
    db.create_all()
    print("Database tables created successfully!")
