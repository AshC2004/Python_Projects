
    import google.generativeai as genai
    from typing import Dict, List, Any
    import os, json, asyncio

    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        raise RuntimeError("GEMINI_API_KEY missing in environment")

    genai.configure(api_key=API_KEY)
    MODEL = genai.GenerativeModel("gemini-1.5-pro-latest")

    async def analyze_prospect_profile(linkedin_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze LinkedIn profile using Gemini and return insights"""
        prompt = f"""
        You are a senior B2B sales analyst. Analyze this LinkedIn profile JSON and return JSON with:
        1. compatibility_score (0-100)
        2. talking_points (3-5 strings)
        3. recent_activity (string)
        4. best_approach (string)
        5. personalization_opportunities (list)
        LinkedIn Profile:
{json.dumps(linkedin_data, indent=2)}
        """
        response = await asyncio.to_thread(MODEL.generate_content, prompt)
        return json.loads(response.text)

    async def generate_personalized_messages(prospect_data: Dict[str, Any], campaign_config: Dict[str, Any], message_type: str) -> List[Dict[str, Any]]:
        """Generate personalized LinkedIn messages using Gemini"""
        prompt = f"""
        Generate 3 {message_type} LinkedIn messages under 300 characters with a clear CTA. Use this brand voice: {campaign_config.get('brand_voice', 'Professional')}.
        Prospect Data:
{json.dumps(prospect_data, indent=2)}
        Campaign Config:
{json.dumps(campaign_config, indent=2)}
        Return JSON list with fields: content, personalization_points, estimated_response_rate
        """
        response = await asyncio.to_thread(MODEL.generate_content, prompt)
        return json.loads(response.text)
