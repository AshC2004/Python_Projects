# Gemini Migration Notes

This document summarizes all updates made to migrate the LinkedIn Sales Automation project from **OpenAI GPT** to **Google Gemini (Pro)**.

## 1. Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Your Google AI Studio Gemini key `AIza...` | ✅ |
| `AI_PROVIDER` | Set to `gemini` (default) or `openai` for fallback | ✅ |
| `OPENAI_API_KEY` | (Deprecated) Leave empty unless fallback needed | ❌ |

Example `.env`:
```ini
GEMINI_API_KEY=AIza-your-gemini-key
AI_PROVIDER=gemini
# OPENAI_API_KEY=
```

## 2. Dependencies

`backend/requirements.txt` now contains:
```
google-generativeai==0.5.2
# openai==1.3.5   # commented out
```
Run:
```bash
docker-compose build web worker
```

## 3. Code Changes

### `/backend/app/gemini_service.py`
New module wrapping Gemini Python SDK with asynchronous helpers:
- `analyze_prospect_profile()`
- `generate_personalized_messages()`

### `/backend/app/ai_service.py`
Now acts as a **provider switch**. Reads `AI_PROVIDER` env and routes calls to Gemini (default) or to OpenAI for fallback/testing.

### `campaign_service.py`
Still imports `ai_service`, so no further edits needed—runtime switch handles the calls.

## 4. Docker Compose

Added variables to `web`, `worker` services:
```yaml
environment:
  - GEMINI_API_KEY=${GEMINI_API_KEY}
  - AI_PROVIDER=${AI_PROVIDER}
```
Removed `OPENAI_API_KEY`.

## 5. Front-End Labels

`index.html` settings panel now displays **Gemini API Key** instead of **OpenAI API Key**.

## 6. Documentation Updated

- `README.md`—references now say *Gemini* instead of *OpenAI*.
- `API-KEYS-SETUP.md`—added Google AI Studio steps.
- **New**: `Gemini Migration Notes` (this file).

## 7. Quick Smoke Test

```bash
export GEMINI_API_KEY=AIza-your-key
export AI_PROVIDER=gemini

docker-compose down -v
docker-compose up -d --build

# Test health
curl http://localhost:8000/health

# Test Gemini direct
docker-compose exec web python - << 'PY'
import os, asyncio, google.generativeai as genai
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-pro-latest')
print(model.generate_content('Hello from Gemini!').text)
PY
```

If you see a greeting, the migration is successful.

---

**You can now proceed with normal campaign creation, prospect analysis, and message generation—all powered by Google Gemini.**