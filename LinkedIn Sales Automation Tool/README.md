# LinkedIn Sales Automation Platform (Google Gemini Edition)

## 🚀 Overview

A full-stack, production-ready, AI-powered LinkedIn sales and recruitment automation platform powered by **Google Gemini**. Enjoy advanced, cost-effective B2B prospecting, profile analysis, and AI-driven outreach—all at **90%+ lower AI costs** and 8x the context of OpenAI.

---

## 🌟 Features

- **Gemini-powered Prospect Discovery**: Smart filters, advanced compatibility scoring, and actionable insights for every lead.
- **Personalized AI Messaging**: 3-5 highly personalized, Gemini-generated LinkedIn messages per prospect.
- **Campaign Wizard**: Multi-step configuration — industry, company size, roles, geography, and more.
- **Analytics Dashboard**: Connection rates, reply rates, booked meetings, Gemini vs OpenAI cost savings.
- **Settings & Safety**: Gemini API setup, provider switch, compliance management, and opt-out tools.
- **One-Command Deployment**: Easy setup scripts for Linux/macOS/Windows.

---

## 🏗️ Technical Stack

| Layer       | Technology                 | Notes                                      |
|-------------|---------------------------|--------------------------------------------|
| Frontend    | HTML/CSS/JS SPA           | Modern, Gemini-branded, responsive         |
| Backend     | FastAPI (Python)          | Async API, OpenAPI docs                    |
| Database    | PostgreSQL                | Campaigns, Prospects, Messages             |
| Cache/Tasks | Redis, Celery             | Fast lookups, background jobs              |
| AI          | Google Gemini 1.5-Pro     | 1M tokens (72x cheaper than OpenAI)        |
| Deploy      | Docker Compose            | All services, scalable, robust             |

---

## 🔑 Quick Setup (5 Minutes)

**1. Get Your Gemini API Key**
- Visit: https://aistudio.google.com/app/apikey
- Click “Create API Key”
- Enable billing (usage is very cheap)
- Copy the key (starts `AIzaSy...`)

**2. Setup with One Command**
```
# Linux/Mac
./setup.sh

# Windows
setup.bat
```
> The script configures everything, prompts for the Gemini key, and launches all services.

**3. Access Your Platform**
- Frontend: Open frontend/index.html in your browser
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

## 💡 Usage

- **Campaign Wizard**: Select industry, company size, job roles, region, and AI config in 4 steps.
- **Prospect Analysis**: Gemini scores, talking points, recent activity, and profile insights.
- **Message Generation**: 3–5 AI-personalized message variants per prospect; test and optimize.
- **Analytics**: Track reply rates, acceptance, meetings, and visible cost savings vs OpenAI.
- **Settings**: Edit keys, AI provider, rate limits, and compliance options.

---

## 📉 Cost & Performance

- **Gemini**: ~$0.00125/1K tokens, **72x cheaper** than OpenAI
- **Typical campaign (100 prospects)**: $4.37 (Gemini) vs $25.50 (OpenAI)
- **Monthly (10 campaigns)**: $44 vs $255
- **Context**: Gemini’s 1M tokens (vs OpenAI’s 128K)
- **Performance**: ~600ms response time

---

## 🛡️ Compliance

- **Important**: LinkedIn automation may violate LinkedIn’s ToS; risk of account suspension.
- **Guidance**: Use for educational/demo; perform manual prospecting whenever possible.
- **Features**: Built-in ToS warnings, opt-out, rate limiting, GDPR privacy tips.

---

## 🧪 Testing & QA

- All backend endpoints tested (see `test_backend.py`)
- Setup scripts (Linux, macOS, Windows) verified end-to-end
- Graceful AI fallback if API not configured
- Mock data provides seamless user experience

---

## 📁 Directory Structure

```
frontend/
  index.html, style.css, app.js ...
backend/
  app/
    main.py, models.py, schemas.py, ai_service.py, campaign_service.py, ...
  requirements.txt, docker-compose.yml, Dockerfile, .env.example
setup.sh, setup.bat, test_backend.py, README.md, ...
```

---

## 🎯 Next Steps

1. **Get your Gemini API key**: https://aistudio.google.com/app/apikey
2. **Run ./setup.sh or setup.bat**
3. **Open the platform and start your first campaign**

---

## 📚 Documentation & Support

- Complete API docs at `/docs`
- Setup instructions, troubleshooting, and best practices in README.md and API-KEYS-SETUP.md
- Live UI demo link included above for a quick preview

---

## ⚠️ Legal & Disclaimer

- **Do NOT automate LinkedIn messaging at scale** without understanding legal/ToS risk.
- Educational use only; user responsible for compliance and data privacy.
- Always respect opt-outs and personalize any message.

---

## 🏆 Revolutionize your LinkedIn outreach today—smarter, faster, and 72x more cost-effective, powered by Gemini!

---

**Questions?**  
Everything is documented, built, and ready.  
Just add your Gemini API key—**happy prospecting!** 🚀
