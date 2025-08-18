from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    target_industry = Column(String)
    company_size = Column(String)
    location = Column(String)
    job_roles = Column(JSON)  # Store as JSON array
    campaign_goal = Column(String)
    brand_voice = Column(String)
    triggers = Column(JSON)  # Optional triggers
    status = Column(String, default="active")
    ai_provider = Column(String, default="gemini")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    prospects = relationship("Prospect", back_populates="campaign", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="campaign", cascade="all, delete-orphan")

class Prospect(Base):
    __tablename__ = "prospects"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    name = Column(String)
    title = Column(String)
    company = Column(String)
    location = Column(String)
    linkedin_url = Column(String)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    compatibility_score = Column(Float)
    recent_activity = Column(Text)
    talking_points = Column(JSON)
    profile_insights = Column(Text)
    personalization_opportunities = Column(JSON)
    status = Column(String, default="discovered")  # discovered, contacted, replied, converted
    ai_analyzed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    campaign = relationship("Campaign", back_populates="prospects")
    messages = relationship("Message", back_populates="prospect", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    prospect_id = Column(Integer, ForeignKey("prospects.id"))
    message_type = Column(String)  # connection_request, follow_up_1, follow_up_2, etc.
    template = Column(Text)
    personalized_content = Column(Text)
    personalization_score = Column(Float)
    sent_at = Column(DateTime, nullable=True)
    status = Column(String, default="draft")  # draft, scheduled, sent, delivered, read, replied
    ai_generated = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    campaign = relationship("Campaign", back_populates="messages")
    prospect = relationship("Prospect", back_populates="messages")

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, unique=True)  # gemini, openai, etc.
    encrypted_key = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CampaignAnalytics(Base):
    __tablename__ = "campaign_analytics"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    date = Column(DateTime, default=datetime.utcnow)
    prospects_found = Column(Integer, default=0)
    prospects_analyzed = Column(Integer, default=0)
    connection_requests_sent = Column(Integer, default=0)
    connection_acceptance_rate = Column(Float, default=0.0)
    messages_sent = Column(Integer, default=0)
    reply_rate = Column(Float, default=0.0)
    meetings_booked = Column(Integer, default=0)
    ai_cost = Column(Float, default=0.0)
    cost_savings_vs_openai = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)