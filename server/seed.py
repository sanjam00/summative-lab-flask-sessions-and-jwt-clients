from app import app
from config import db
from models import User, JournalEntry

with app.app_context():

    print("Clearing database...")
    JournalEntry.query.delete()
    User.query.delete()

    print("Seeding users...")

    user1 = User(
        username="alex"
    )
    user1.password_hash = "password123"

    user2 = User(
        username="sam"
    )
    user2.password_hash = "password456"
    
    db.session.add_all([user1, user2])
    db.session.commit()

    print("Seeding journal entries...")

    entry1 = JournalEntry(
        title="First Entry",
        body="Today I started my journal app.",
        user_id=user1.id
    )
    entry2 = JournalEntry(
        title="Workout Notes",
        body="Went climbing today.",
        user_id=user1.id
    )
    entry3 = JournalEntry(
        title="Vacation Ideas",
        body="Thinking about Arizona road trips.",
        user_id=user2.id
    )

    db.session.add_all([entry1, entry2, entry3])
    db.session.commit()

    print("Done seeding!")