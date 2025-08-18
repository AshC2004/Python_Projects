from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
import logging

from . import models, schemas, ai_service

logger = logging.getLogger(__name__)

class CampaignService:
    def __init__(self):
        self.ai_service = ai_service

    def create_campaign(self, db: Session, campaign: schemas.CampaignCreate) -> models.Campaign:
        """Create a new campaign"""
        db_campaign = models.Campaign(**campaign.dict())
        db.add(db_campaign)
        db.commit()
        db.refresh(db_campaign)
        logger.info(f"Created campaign: {db_campaign.name} (ID: {db_campaign.id})")
        return db_campaign

    def get_campaigns(self, db: Session) -> List[models.Campaign]:
        """Get all campaigns"""
        return db.query(models.Campaign).order_by(models.Campaign.created_at.desc()).all()

    def get_campaign(self, db: Session, campaign_id: int) -> Optional[models.Campaign]:
        """Get a specific campaign"""
        return db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()

    async def start_prospect_search(self, db: Session, campaign_id: int, search_criteria: Dict[str, Any]):
        """Start searching for prospects for a campaign"""
        try:
            logger.info(f"Starting prospect search for campaign {campaign_id}")

            # Generate mock prospects based on criteria
            prospects_data = self._generate_mock_prospects(search_criteria)

            for prospect_data in prospects_data:
                # Create prospect record
                db_prospect = models.Prospect(
                    campaign_id=campaign_id,
                    name=prospect_data['name'],
                    title=prospect_data['title'],
                    company=prospect_data['company'],
                    location=prospect_data['location'],
                    linkedin_url=prospect_data.get('linkedin_url', ''),
                    compatibility_score=prospect_data.get('compatibility_score', 85),
                    recent_activity=prospect_data.get('recent_activity', ''),
                    status='discovered'
                )
                db.add(db_prospect)

                # Generate AI analysis for the prospect
                try:
                    analysis = await self.ai_service.analyze_prospect_profile(prospect_data)
                    db_prospect.profile_insights = analysis.get('best_approach', '')
                    db_prospect.talking_points = analysis.get('talking_points', [])
                    db_prospect.compatibility_score = analysis.get('compatibility_score', 85)
                    db_prospect.personalization_opportunities = analysis.get('personalization_opportunities', [])
                    db_prospect.ai_analyzed = True
                    logger.info(f"AI analysis completed for prospect: {prospect_data['name']}")
                except Exception as e:
                    logger.error(f"AI analysis failed for prospect {prospect_data['name']}: {e}")
                    db_prospect.ai_analyzed = False

            db.commit()

            # Update campaign analytics
            self._update_campaign_analytics(db, campaign_id, len(prospects_data))

            logger.info(f"Prospect search completed for campaign {campaign_id}. Found {len(prospects_data)} prospects.")

        except Exception as e:
            logger.error(f"Prospect search failed for campaign {campaign_id}: {e}")

    def get_campaign_prospects(self, db: Session, campaign_id: int) -> List[models.Prospect]:
        """Get all prospects for a campaign"""
        return db.query(models.Prospect).filter(models.Prospect.campaign_id == campaign_id).all()

    def get_all_prospects(self, db: Session) -> List[models.Prospect]:
        """Get all prospects across all campaigns"""
        return db.query(models.Prospect).order_by(models.Prospect.created_at.desc()).limit(50).all()

    def get_prospect(self, db: Session, prospect_id: int) -> Optional[models.Prospect]:
        """Get a specific prospect"""
        return db.query(models.Prospect).filter(models.Prospect.id == prospect_id).first()

    async def analyze_prospect(self, db: Session, prospect_id: int) -> Dict[str, Any]:
        """Run AI analysis on a specific prospect"""
        prospect = self.get_prospect(db, prospect_id)
        if not prospect:
            raise ValueError("Prospect not found")

        prospect_data = {
            "name": prospect.name,
            "title": prospect.title,
            "company": prospect.company,
            "location": prospect.location,
            "recent_activity": prospect.recent_activity
        }

        analysis = await self.ai_service.analyze_prospect_profile(prospect_data)

        # Update prospect with analysis
        prospect.profile_insights = analysis.get('best_approach', prospect.profile_insights)
        prospect.talking_points = analysis.get('talking_points', prospect.talking_points)
        prospect.compatibility_score = analysis.get('compatibility_score', prospect.compatibility_score)
        prospect.personalization_opportunities = analysis.get('personalization_opportunities', [])
        prospect.ai_analyzed = True

        db.commit()

        return analysis

    def get_campaign_analytics(self, db: Session, campaign_id: int) -> Dict[str, Any]:
        """Get analytics for a campaign"""
        # Get latest analytics record
        analytics = db.query(models.CampaignAnalytics).filter(
            models.CampaignAnalytics.campaign_id == campaign_id
        ).order_by(models.CampaignAnalytics.date.desc()).first()

        # Get prospect counts
        total_prospects = db.query(models.Prospect).filter(models.Prospect.campaign_id == campaign_id).count()
        analyzed_prospects = db.query(models.Prospect).filter(
            models.Prospect.campaign_id == campaign_id,
            models.Prospect.ai_analyzed == True
        ).count()

        if not analytics:
            # Create default analytics
            return {
                "prospects_found": total_prospects,
                "prospects_analyzed": analyzed_prospects,
                "connection_requests_sent": 0,
                "connection_acceptance_rate": 0.0,
                "messages_sent": 0,
                "reply_rate": 0.0,
                "meetings_booked": 0,
                "ai_cost": 0.0,
                "cost_savings_vs_openai": 0.0,
                "roi": 0.0
            }

        return {
            "prospects_found": total_prospects,
            "prospects_analyzed": analyzed_prospects,
            "connection_requests_sent": analytics.connection_requests_sent,
            "connection_acceptance_rate": analytics.connection_acceptance_rate,
            "messages_sent": analytics.messages_sent,
            "reply_rate": analytics.reply_rate,
            "meetings_booked": analytics.meetings_booked,
            "ai_cost": analytics.ai_cost,
            "cost_savings_vs_openai": analytics.cost_savings_vs_openai,
            "roi": self._calculate_roi(analytics)
        }

    def _update_campaign_analytics(self, db: Session, campaign_id: int, prospects_found: int):
        """Update campaign analytics"""
        today = datetime.utcnow().date()

        # Check if analytics record exists for today
        analytics = db.query(models.CampaignAnalytics).filter(
            models.CampaignAnalytics.campaign_id == campaign_id,
            func.date(models.CampaignAnalytics.date) == today
        ).first()

        if not analytics:
            analytics = models.CampaignAnalytics(
                campaign_id=campaign_id,
                prospects_found=prospects_found,
                prospects_analyzed=prospects_found,
                ai_cost=prospects_found * 0.01,  # Estimated Gemini cost
                cost_savings_vs_openai=prospects_found * 0.72  # 72x savings
            )
            db.add(analytics)
        else:
            analytics.prospects_found += prospects_found
            analytics.prospects_analyzed += prospects_found
            analytics.ai_cost += prospects_found * 0.01
            analytics.cost_savings_vs_openai += prospects_found * 0.72

        db.commit()

    def _calculate_roi(self, analytics: models.CampaignAnalytics) -> float:
        """Calculate ROI based on meetings booked"""
        if analytics.meetings_booked == 0:
            return 0.0

        # Assume average deal value of $5000 and 20% close rate
        estimated_revenue = analytics.meetings_booked * 5000 * 0.2
        estimated_cost = 1000  # Estimated campaign cost

        if estimated_cost == 0:
            return 0.0

        return ((estimated_revenue - estimated_cost) / estimated_cost) * 100

    def _generate_mock_prospects(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate mock prospects based on search criteria"""
        base_prospects = [
            {
                "name": "Anjali Mehta",
                "title": "HR Director",
                "company": "TechFlow Solutions",
                "location": "Mumbai, India",
                "linkedin_url": "https://linkedin.com/in/anjali-mehta-hr",
                "recent_activity": "Posted about AI transformation in HR",
                "compatibility_score": 94
            },
            {
                "name": "Rahul Kumar",
                "title": "CTO",
                "company": "StartupForge",
                "location": "Bangalore, India",
                "linkedin_url": "https://linkedin.com/in/rahul-kumar-cto",
                "recent_activity": "Shared insights on cloud-native architecture",
                "compatibility_score": 91
            },
            {
                "name": "Priya Sharma",
                "title": "VP Marketing",
                "company": "GrowthLabs",
                "location": "Delhi, India",
                "linkedin_url": "https://linkedin.com/in/priya-sharma-vp",
                "recent_activity": "Celebrated 200% growth in Q3",
                "compatibility_score": 89
            },
            {
                "name": "Arjun Patel",
                "title": "Sales Director",
                "company": "CloudVenture",
                "location": "Pune, India",
                "linkedin_url": "https://linkedin.com/in/arjun-patel-sales",
                "recent_activity": "Announced expansion to Southeast Asia",
                "compatibility_score": 87
            },
            {
                "name": "Meera Gupta",
                "title": "Head of Marketing",
                "company": "InnovateTech",
                "location": "Chennai, India",
                "linkedin_url": "https://linkedin.com/in/meera-gupta-marketing",
                "recent_activity": "Published whitepaper on B2B marketing trends",
                "compatibility_score": 88
            }
        ]

        # Filter based on criteria (simple matching)
        filtered_prospects = []
        for prospect in base_prospects:
            if self._matches_criteria(prospect, criteria):
                filtered_prospects.append(prospect)

        return filtered_prospects[:5]  # Limit to 5 prospects for demo

    def _matches_criteria(self, prospect: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """Check if prospect matches search criteria"""
        # Simple matching logic for demo
        location = criteria.get('location', '').lower()
        if location and location != 'global' and location not in prospect['location'].lower():
            return False

        job_roles = criteria.get('job_roles', [])
        if job_roles:
            title_lower = prospect['title'].lower()
            for role in job_roles:
                if any(word in title_lower for word in role.lower().split()):
                    return True
            return False

        return True

# Create service instance
campaign_service = CampaignService()