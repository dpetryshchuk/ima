from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from config import DATABASE_URL

# Create base class for our models
Base = declarative_base()

# Create engine (connection to database)
engine = create_engine(DATABASE_URL)

# Create session factory (for talking to database)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_message(session_id: str, role: str, content: str):
    """Add a new message to a conversation"""
    db = SessionLocal()

    # Get existing conversation or create new one
    conversation = db.query(Conversation).filter(Conversation.session_id == session_id).first()

    if not conversation:
        # Create new conversation with first message
        conversation = Conversation(
            session_id=session_id,
            messages=[{"role": role, "content": content}]
        )
        db.add(conversation)
    else:
        # Append message to existing conversation
        # We must re-assign the list to force SQLAlchemy to detect the change on JSONB
        conversation.messages = conversation.messages + [{"role": role, "content": content}]
        conversation.updated_at = datetime.utcnow()

    db.commit()
    db.close()

def get_history(session_id: str):
    """Get all messages for a session"""
    db = SessionLocal()
    conversation = db.query(Conversation).filter(Conversation.session_id == session_id).first()
    db.close()

    if conversation:
        return conversation.messages
    return []

def clear_history(session_id: str):
    """Clear all messages for a session"""
    db = SessionLocal()
    conversation = db.query(Conversation).filter(Conversation.session_id == session_id).first()
    if conversation:
        db.delete(conversation)
    db.commit()
    db.close()

# Import models and create tables
from models import Conversation
Base.metadata.create_all(bind=engine)
