from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Agent(Base):
    __tablename__ = "sup_agents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    agent_id = Column(String, unique=True, nullable=False)
    user_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
