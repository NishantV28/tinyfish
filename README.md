# Scout — A Privacy-First AI Personal Browser (Powered by TinyFish)

**Scout** is an AI-powered personal browser that understands plain-language requests, sends specialized agents to perform live web automation via **TinyFish**, and protects user privacy using dynamic email alias generation, breach detection ("Catch the Leaker"), and automated two-step account deletion.

---

## Repository Structure

```
.
├── create_scout_project.py       # One-click generator script to rebuild scaffold & zip archive
├── scout-browser.zip             # Downloadable/distributable complete project archive
└── scout-browser/                # Project root
    ├── supabase/
    │   └── schema.sql            # PostgreSQL schema with UUIDs, accounts, aliases, leaks & tasks
    ├── cloudflare-worker/
    │   ├── email_worker.js       # Edge email catch-all worker with leak detection webhook
    │   └── wrangler.toml         # Cloudflare Worker configuration
    ├── backend/
    │   ├── config.py             # Pydantic environment settings
    │   ├── models.py             # FastAPI request/response schemas
    │   ├── main.py               # FastAPI server entry point
    │   ├── requirements.txt      # Python dependencies
    │   ├── services/
    │   │   └── tinyfish.py       # TinyFish Search, Fetch, SSE Agent & Browser Profiles client
    │   └── agents/
    │       ├── orchestrator.py   # Intent classification and workflow coordinator
    │       ├── privacy_agent.py  # Alias Shield, Catch the Leaker, 2-Step Deletion Map
    │       └── specialized_agents.py # Search, Research, Shopping, Monitor, Web Task Agents
    ├── frontend/
    │   ├── package.json          # Next.js 14 frontend dependencies
    │   ├── tsconfig.json         # TypeScript configuration
    │   ├── next.config.mjs       # Next.js configuration
    │   └── src/app/
    │       ├── globals.css       # Dark mode theme styles
    │       ├── layout.tsx        # Next.js root layout
    │       └── page.tsx          # Chat command bar, 2-min demo triggers & live stream viewer
    ├── .env.example              # Environment variables template
    └── README.md                 # Scout browser documentation
```

---

## Quick Start

### 1. Backend (FastAPI + TinyFish Layer + 9 Agents)
```bash
cd scout-browser/backend
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On macOS / Linux:
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. Frontend (Next.js Command Bar & Live Browser Stream)
```bash
cd scout-browser/frontend
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to access the UI and test the 4 pre-configured demo scenarios.

### 3. Database & Cloudflare Worker
- Execute `scout-browser/supabase/schema.sql` inside your Supabase SQL editor.
- Deploy `scout-browser/cloudflare-worker/email_worker.js` with `npx wrangler deploy`.
