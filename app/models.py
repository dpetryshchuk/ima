from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from database import Base

# One conversation = one database row
class Conversation(Base):
    __tablename__ = "conversations"

    session_id = Column(String, primary_key=True)  # Unique ID for each chat session
    messages = Column(JSONB, default=[])  # Array of {role, content} objects
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
