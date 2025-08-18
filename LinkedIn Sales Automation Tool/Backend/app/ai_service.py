import os
import json
import asyncio
import logging
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower()

if PROVIDER == "openai":
    try:
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        logger.info("OpenAI provider configured")

        async def analyze_prospect_profile(linkedin_data: Dict[str, Any]) -> Dict[str, Any]:
            prompt = f"""
            Analyze this LinkedIn profile and return structured JSON with:
            - compatibility_score (0-100)
            - talking_points (3-5 strings)
            - recent_activity (string)
            - best_approach (string)
            - personalization_opportunities (list)

            Profile: {json.dumps(linkedin_data, indent=2)}
            """
            try:
                completion = await openai.ChatCompletion.acreate(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                return json.loads(completion.choices[0].message.content)
            except Exception as e:
                logger.error(f"OpenAI error: {e}")
                return _generate_mock_analysis(linkedin_data)

        async def generate_personalized_messages(prospect_data: Dict[str, Any], campaign_config: Dict[str, Any], message_type: str) -> List[Dict[str, Any]]:
            prompt = f"""
            Generate 3 personalized LinkedIn {message_type} messages under 300 characters.
            Brand voice: {campaign_config.get('brand_voice', 'Professional')}
            Return JSON list with: content, personalization_points, estimated_response_rate

            Prospect: {json.dumps(prospect_data)}
            Campaign: {json.dumps(campaign_config)}
            """
            try:
                completion = await openai.ChatCompletion.acreate(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8,
                )
                return json.loads(completion.choices[0].message.content)
            except Exception as e:
                logger.error(f"OpenAI error: {e}")
                return _generate_mock_messages(prospect_data, campaign_config, message_type)

    except ImportError:
        logger.warning("OpenAI not available, falling back to Gemini")
        PROVIDER = "gemini"

# Default to Gemini
if PROVIDER == "gemini":
    try:
        import google.generativeai as genai

        API_KEY = os.getenv("GEMINI_API_KEY")
        if API_KEY:
            genai.configure(api_key=API_KEY)
            MODEL = genai.GenerativeModel("gemini-1.5-pro-latest")
            logger.info("Gemini provider configured successfully")
        else:
            logger.warning("GEMINI_API_KEY not found, using mock responses")
            MODEL = None

        async def analyze_prospect_profile(linkedin_data: Dict[str, Any]) -> Dict[str, Any]:
            if not MODEL:
                logger.warning("Gemini not configured, using mock data")
                return _generate_mock_analysis(linkedin_data)

            prompt = f"""
            You are a B2B sales analyst. Analyze this LinkedIn profile and return JSON with:
            {{
              "compatibility_score": 0-100,
              "talking_points": ["point1", "point2", "point3"],
              "recent_activity": "description of recent activity",
              "best_approach": "recommended approach strategy",
              "personalization_opportunities": ["opp1", "opp2", "opp3"]
            }}

            Profile Data: {json.dumps(linkedin_data, indent=2)}
            """
            try:
                response = await asyncio.to_thread(MODEL.generate_content, prompt)
                # Clean up response and parse JSON
                content = response.text.strip()
                if content.startswith("```json"):
                    content = content[7:-3]
                elif content.startswith("```"):
                    content = content[3:-3]
                return json.loads(content)
            except Exception as e:
                logger.error(f"Gemini error: {e}")
                return _generate_mock_analysis(linkedin_data)

        async def generate_personalized_messages(prospect_data: Dict[str, Any], campaign_config: Dict[str, Any], message_type: str) -> List[Dict[str, Any]]:
            if not MODEL:
                logger.warning("Gemini not configured, using mock data")
                return _generate_mock_messages(prospect_data, campaign_config, message_type)

            prompt = f"""
            Generate 3 personalized LinkedIn {message_type} messages under 300 characters each.
            Use brand voice: {campaign_config.get('brand_voice', 'Professional')}

            Return JSON array with format:
            [
              {{
                "content": "message text",
                "personalization_points": ["point1", "point2"],
                "estimated_response_rate": 0.32
              }}
            ]

            Prospect: {json.dumps(prospect_data)}
            Campaign: {json.dumps(campaign_config)}
            """
            try:
                response = await asyncio.to_thread(MODEL.generate_content, prompt)
                content = response.text.strip()
                if content.startswith("```json"):
                    content = content[7:-3]
                elif content.startswith("```"):
                    content = content[3:-3]
                return json.loads(content)
            except Exception as e:
                logger.error(f"Gemini error: {e}")
                return _generate_mock_messages(prospect_data, campaign_config, message_type)

    except ImportError:
        logger.error("google-generativeai not installed")
        MODEL = None

# Fallback mock functions
def _generate_mock_analysis(linkedin_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate mock analysis when AI is not available"""
    name = linkedin_data.get('name', 'Professional')
    title = linkedin_data.get('title', 'Professional')
    company = linkedin_data.get('company', 'Company')

    return {
        "compatibility_score": 87 + (hash(name) % 13),
        "talking_points": [
            f"Recent experience in {title}",
            f"Leadership role at {company}",
            "Industry expertise and insights",
            "Professional network connections"
        ],
        "recent_activity": f"Posted about industry trends and {company} growth",
        "best_approach": "Professional tone with focus on mutual value and industry insights",
        "personalization_opportunities": [
            f"Reference their role at {company}",
            "Mention shared industry connections",
            "Connect to their recent professional updates"
        ]
    }

def _generate_mock_messages(prospect_data: Dict[str, Any], campaign_config: Dict[str, Any], message_type: str) -> List[Dict[str, Any]]:
    """Generate mock messages when AI is not available"""
    name = prospect_data.get('name', 'there')
    title = prospect_data.get('title', 'your field')
    company = prospect_data.get('company', 'your company')

    if message_type == "connection_request":
        return [
            {
                "content": f"Hi {name}, I noticed your expertise in {title} at {company}. Would love to connect and share insights that might benefit your team!",
                "personalization_points": ["name", "title", "company"],
                "estimated_response_rate": 0.34
            },
            {
                "content": f"Hello {name}, your work at {company} caught my attention. I think there could be valuable synergies between our approaches. Let's connect!",
                "personalization_points": ["name", "company", "industry"],
                "estimated_response_rate": 0.28
            },
            {
                "content": f"{name}, I've been following {company}'s growth. As someone in {title}, I'd love to exchange insights. Connect?",
                "personalization_points": ["name", "company", "title"],
                "estimated_response_rate": 0.31
            }
        ]
    else:
        return [
            {
                "content": f"Thanks for connecting, {name}! Seeing {company}'s success in the market. Would love to share how we've helped similar organizations achieve significant results.",
                "personalization_points": ["name", "company", "success"],
                "estimated_response_rate": 0.22
            }
        ]
