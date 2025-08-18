
    import os, json, asyncio
    from typing import Dict, Any, List

    PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower()

    if PROVIDER == "openai":
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")

        async def analyze_prospect_profile(linkedin_data: Dict[str, Any]) -> Dict[str, Any]:
            prompt = f"Analyze this LinkedIn profile and return structured JSON insights:
{json.dumps(linkedin_data, indent=2)}"
            completion = await openai.ChatCompletion.acreate(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return json.loads(completion.choices[0].message.content)

        async def generate_personalized_messages(prospect_data: Dict[str, Any], campaign_config: Dict[str, Any], message_type: str) -> List[Dict[str, Any]]:
            prompt = f"Generate 3 {message_type} messages under 300 characters... Prospect: {json.dumps(prospect_data)} Campaign: {json.dumps(campaign_config)}"
            completion = await openai.ChatCompletion.acreate(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
            )
            return json.loads(completion.choices[0].message.content)

    else:  # default Gemini
        import google.generativeai as genai
        API_KEY = os.getenv("GEMINI_API_KEY")
        if not API_KEY:
            raise RuntimeError("GEMINI_API_KEY environment variable missing")
        genai.configure(api_key=API_KEY)
        MODEL = genai.GenerativeModel("gemini-1.5-pro-latest")

        async def analyze_prospect_profile(linkedin_data: Dict[str, Any]) -> Dict[str, Any]:
            prompt = f"You are a B2B sales analyst. Analyse this profile JSON and return JSON insights.
{json.dumps(linkedin_data, indent=2)}"
            response = await asyncio.to_thread(MODEL.generate_content, prompt)
            return json.loads(response.text)

        async def generate_personalized_messages(prospect_data: Dict[str, Any], campaign_config: Dict[str, Any], message_type: str) -> List[Dict[str, Any]]:
            prompt = f"Generate 3 {message_type} LinkedIn messages under 300 chars. Prospect: {json.dumps(prospect_data)} Campaign: {json.dumps(campaign_config)}"
            response = await asyncio.to_thread(MODEL.generate_content, prompt)
            return json.loads(response.text)
