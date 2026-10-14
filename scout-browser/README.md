# Scout — A Privacy-First AI Personal Browser

**One Line:** Scout is an AI-powered personal browser that understands plain-language requests, sends the right specialised agent to do the work on the live web via **TinyFish**, and protects the user's identity while it does: every signup gets its own email alias, so Scout can catch the app that leaked your data and delete you from it.

## Quick Start

### 1. Backend (FastAPI + Orchestrator + 9 Agents + TinyFish Layer)
```bash
cd backend
python -m venv venv
# Windows: .\venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. Frontend (Next.js Command Bar + Live TinyFish Browser View)
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:3000 and click through the 2-Minute Live Demo Bar at the top of the browser!

### 3. Database & Edge Email Routing
- Run `supabase/schema.sql` in your Supabase SQL Editor.
- Deploy `cloudflare-worker/email_worker.js` using `npx wrangler deploy`.
