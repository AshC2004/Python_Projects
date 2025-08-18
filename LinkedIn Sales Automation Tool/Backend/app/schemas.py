from pydantic import BaseModel, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class CampaignGoal(str, Enum):
    BOOK_DEMO = "Book a Demo"
    SCHEDULE_CALL = "Schedule a Call"
    DOWNLOAD_CONTENT = "Download Content"
    TRIAL_SIGNUP = "Trial Signup"
    PARTNERSHIP = "Partnership Discussion"
    HIRING = "Hiring/Recruitment"

class BrandVoice(str, Enum):
    PROFESSIONAL = "Professional & Formal"
    FRIENDLY = "Friendly & Approachable"
    ENTHUSIASTIC = "Enthusiastic & Energetic"
    CONSULTATIVE = "Consultative & Expert"

class CompanySize(str, Enum):
    STARTUP = "Startup (1-50)"
    SME = "SME (51-200)"
    MID_MARKET = "Mid-Market (201-1000)"
    ENTERPRISE = "Enterprise (1000+)"

class AIProvider(str, Enum):
    GEMINI = "gemini"
    OPENAI = "openai"

# Base schemas
class CampaignBase(BaseModel):
    name: str
    target_industry: str
    company_size: CompanySize
    location: str
    job_roles: List[str]
    campaign_goal: CampaignGoal
    brand_voice: BrandVoice
    triggers: Optional[List[str]] = None

class CampaignCreate(CampaignBase):
    pass

class Campaign(CampaignBase):
    id: int
    status: str
    ai_provider: Optional[str] = "gemini"
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ProspectBase(BaseModel):
    name: str
    title: str
    company: str
    location: str
    linkedin_url: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class ProspectCreate(ProspectBase):
    campaign_id: int

class Prospect(ProspectBase):
    id: int
    campaign_id: int
    compatibility_score: Optional[float]
    recent_activity: Optional[str]
    talking_points: Optional[List[str]]
    profile_insights: Optional[str]
    personalization_opportunities: Optional[List[str]]
    status: str
    ai_analyzed: Optional[bool] = False
    created_at: datetime

    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    message_type: str
    template: str
    personalized_content: str

class MessageCreate(MessageBase):
    campaign_id: int
    prospect_id: int

class Message(MessageBase):
    id: int
    campaign_id: int
    prospect_id: int
    personalization_score: Optional[float]
    sent_at: Optional[datetime]
    status: str
    ai_generated: Optional[bool] = True
    created_at: datetime

    class Config:
        orm_mode = True

class MessageGenerationRequest(BaseModel):
    prospect_data: Dict[str, Any]
    campaign_config: Dict[str, Any]
    message_type: str

class APIKeysUpdate(BaseModel):
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    ai_provider: Optional[AIProvider] = AIProvider.GEMINI

class CampaignAnalytics(BaseModel):
    campaign_id: int
    prospects_found: int
    prospects_analyzed: int
    connection_requests_sent: int
    connection_acceptance_rate: float
    messages_sent: int
    reply_rate: float
    meetings_booked: int
    ai_cost: float
    cost_savings_vs_openai: float
    date: datetime

    class Config:
        orm_mode = True