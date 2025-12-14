# /app/app/models/prompts.py
from sqlalchemy import Column, String, DateTime, Boolean, JSON, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PromptVersionDB(Base):
    __tablename__ = "prompt_versions"
    
    # Composite primary key: version + strategy
    version = Column(String, nullable=False)
    strategy = Column(String, nullable=False)
    
    # Other fields
    name = Column(String, nullable=False)
    system_prompt = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String, default="system")
    changelog = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    performance_metrics = Column(JSON, default=dict)
    
    # Define composite primary key
    __table_args__ = (
        PrimaryKeyConstraint('version', 'strategy'),
    )