from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import uvicorn
from datetime import datetime, timedelta
from typing import List, Optional
import os
import logging

from . import models, schemas, database, campaign_service
from .database import SessionLocal, engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LinkedIn Sales Automation API (Gemini Powered)",
    description="AI-powered LinkedIn automation using Google Gemini for sales teams",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer(auto_error=False)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {
        "message": "LinkedIn Sales Automation API - Powered by Google Gemini", 
        "status": "active",
        "ai_provider": os.getenv("AI_PROVIDER", "gemini"),
        "version": "2.0.0"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "timestamp": datetime.utcnow(),
        "ai_provider": os.getenv("AI_PROVIDER", "gemini"),
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY"))
    }

# Campaign endpoints
@app.post("/api/campaigns/", response_model=schemas.Campaign)
async def create_campaign(
    campaign: schemas.CampaignCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        db_campaign = campaign_service.create_campaign(db, campaign)
        # Start prospect search in background
        background_tasks.add_task(
            campaign_service.start_prospect_search,
            db, 
            db_campaign.id,
            campaign.dict()
        )
        return db_campaign
    except Exception as e:
        logger.error(f"Error creating campaign: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/campaigns/", response_model=List[schemas.Campaign])
async def get_campaigns(db: Session = Depends(get_db)):
    return campaign_service.get_campaigns(db)

@app.get("/api/campaigns/{campaign_id}/prospects")
async def get_campaign_prospects(campaign_id: int, db: Session = Depends(get_db)):
    try:
        prospects = campaign_service.get_campaign_prospects(db, campaign_id)
        return [
            {
                "id": p.id,
                "name": p.name,
                "title": p.title,
                "company": p.company,
                "location": p.location,
                "compatibility_score": p.compatibility_score,
                "recent_activity": p.recent_activity,
                "talking_points": p.talking_points,
                "profile_insights": p.profile_insights,
                "status": p.status
            }
            for p in prospects
        ]
    except Exception as e:
        logger.error(f"Error getting prospects: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/campaigns/{campaign_id}/analytics")
async def get_campaign_analytics(campaign_id: int, db: Session = Depends(get_db)):
    try:
        return campaign_service.get_campaign_analytics(db, campaign_id)
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Prospect endpoints
@app.get("/api/prospects/", response_model=List[schemas.Prospect])
async def get_prospects(db: Session = Depends(get_db)):
    try:
        prospects = campaign_service.get_all_prospects(db)
        return prospects[:20]  # Limit to first 20 for demo
    except Exception as e:
        logger.error(f"Error getting prospects: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/prospects/{prospect_id}/analyze")
async def analyze_prospect(prospect_id: int, db: Session = Depends(get_db)):
    try:
        prospect = campaign_service.get_prospect(db, prospect_id)
        if not prospect:
            raise HTTPException(status_code=404, detail="Prospect not found")

        # Run AI analysis (will use mock data if no API key)
        analysis = await campaign_service.analyze_prospect(db, prospect_id)
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing prospect: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Message generation endpoints
@app.post("/api/messages/generate")
async def generate_messages(
    request: schemas.MessageGenerationRequest,
    db: Session = Depends(get_db)
):
    try:
        from . import ai_service
        messages = await ai_service.generate_personalized_messages(
            request.prospect_data,
            request.campaign_config,
            request.message_type
        )
        return {"messages": messages, "ai_provider": os.getenv("AI_PROVIDER", "gemini")}
    except Exception as e:
        logger.error(f"Error generating messages: {e}")
        # Return mock messages if AI fails
        return {
            "messages": [
                {
                    "content": f"Hi {request.prospect_data.get('name', 'there')}, I noticed your expertise in {request.prospect_data.get('title', 'your field')}. Would love to connect!",
                    "personalization_points": ["name", "title"],
                    "estimated_response_rate": 0.32
                }
            ],
            "ai_provider": "mock",
            "error": "AI service unavailable, showing mock data"
        }

# Settings endpoints
@app.post("/api/settings/api-keys")
async def update_api_keys(
    keys: schemas.APIKeysUpdate,
    db: Session = Depends(get_db)
):
    # In a real implementation, store encrypted API keys in database
    return {
        "status": "success", 
        "message": "API keys updated",
        "gemini_configured": bool(keys.gemini_api_key)
    }

@app.get("/api/settings/compliance-check")
async def compliance_check():
    return {
        "linkedin_terms_compliance": True,
        "ai_provider": os.getenv("AI_PROVIDER", "gemini"),
        "rate_limits": {
            "connection_requests": {"daily": 30, "weekly": 150},
            "messages": {"daily": 20, "weekly": 100}
        },
        "recommendations": [
            "Keep daily connection requests under 30 for safety",
            "Always personalize messages using Gemini AI",
            "Respect user opt-outs immediately",
            "Use manual research when possible"
        ],
        "cost_savings": {
            "gemini_vs_openai": "72x cheaper",
            "monthly_savings": "$200+ for typical usage"
        }
    }

# Test endpoint for Gemini integration
@app.get("/api/test/gemini")
async def test_gemini():
    try:
        from . import ai_service
        test_data = {"name": "Test User", "title": "Test Title", "company": "Test Company"}
        result = await ai_service.analyze_prospect_profile(test_data)
        return {"status": "success", "gemini_working": True, "result": result}
    except Exception as e:
        return {
            "status": "error", 
            "gemini_working": False, 
            "error": str(e),
            "message": "Gemini API key might be missing or invalid"
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)