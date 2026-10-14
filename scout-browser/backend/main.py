from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import CommandRequest, ApprovalRequest, InboundEmailWebhook, PreferenceApprovalRequest
from agents.orchestrator import orchestrator
from agents.privacy_agent import privacy_agent
from config import settings

app = FastAPI(
    title="Scout — Privacy-First AI Personal Browser API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEMO_ACCOUNTS = [
    {
        "id": "acc_1",
        "app_name": "QuickPhoto Editor",
        "domain": "quickphoto.io",
        "category": "utility",
        "browser_profile_id": "tf_prof_u1_quickphoto",
        "risk_score": 96,
        "has_wallet_balance": False,
        "has_active_orders": False,
        "has_active_sub": False,
        "reason": "Leaked your alias to instant-cash-loans24.biz + unused for 9 months",
    },
    {
        "id": "acc_2",
        "app_name": "FlashDealz Kart",
        "domain": "flashdealzkart.com",
        "category": "shopping",
        "browser_profile_id": "tf_prof_u1_flashdealz",
        "risk_score": 82,
        "has_wallet_balance": False,
        "has_active_orders": False,
        "has_active_sub": False,
        "reason": "One-time purchase in 2024; site had a known credential breach",
    },
    {
        "id": "acc_3",
        "app_name": "HDFC NetBanking",
        "domain": "hdfcbank.com",
        "category": "finance",
        "browser_profile_id": "tf_prof_u1_hdfc",
        "risk_score": 0,
        "has_wallet_balance": True,
        "has_active_orders": False,
        "has_active_sub": False,
    },
    {
        "id": "acc_4",
        "app_name": "Google Workspace / Gmail",
        "domain": "google.com",
        "category": "email_provider",
        "browser_profile_id": "tf_prof_u1_google",
        "risk_score": 0,
        "has_wallet_balance": False,
        "has_active_orders": False,
        "has_active_sub": True,
    },
]

APPROVED_PREFERENCES = {
    "budgets": {"laptop": "$1,500"},
    "preferred_sources": ["arxiv.org", "notebookcheck.net"],
    "interests": ["Agentic AI", "Privacy Tech"],
}

@app.post("/api/command")
async def handle_command(req: CommandRequest):
    result = await orchestrator.execute_workflow(
        prompt=req.prompt,
        current_url=req.current_page_url,
        open_tabs=req.open_tabs,
        user_preferences=APPROVED_PREFERENCES,
        sample_accounts=DEMO_ACCOUNTS,
    )
    return result

@app.post("/api/approve-deletion-run2")
async def approve_deletion_run_2(req: ApprovalRequest):
    if not req.approved:
        return {"status": "cancelled_by_user", "message": "Deletion aborted safely."}

    target_account = DEMO_ACCOUNTS[0]
    run2 = await privacy_agent.execute_deletion_run_2(
        account=target_account,
        route_used={
            "deletion_url": f"https://{target_account['domain']}/settings/account/delete",
            "menu_steps": ["Settings", "Account", "Delete Account"],
            "grace_period_days": 30,
        },
    )
    return run2

@app.post("/api/privacy/inbound-email")
async def receive_inbound_email(
    payload: InboundEmailWebhook,
    x_scout_webhook_secret: str = Header(default=""),
):
    if x_scout_webhook_secret != settings.WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="Invalid webhook secret")

    report = await privacy_agent.inspect_inbound_email(
        alias_record={
            "alias_email": payload.alias_email,
            "assigned_app_name": "QuickPhoto Editor",
            "assigned_domain": "quickphoto.io",
            "known_partner_domains": [],
        },
        from_email=payload.from_email,
        from_domain=payload.from_domain,
        subject=payload.subject,
    )
    return {
        "allow_forward": report["allow_forward"],
        "real_user_email": "user@realinbox.com",
        "leak_report": report,
    }

@app.post("/api/preferences/approve")
async def approve_preference(req: PreferenceApprovalRequest):
    if req.category not in APPROVED_PREFERENCES:
        APPROVED_PREFERENCES[req.category] = {}
    if isinstance(APPROVED_PREFERENCES[req.category], dict):
        APPROVED_PREFERENCES[req.category][req.key] = req.value
    elif isinstance(APPROVED_PREFERENCES[req.category], list):
        APPROVED_PREFERENCES[req.category].append(req.value)
    return {"status": "saved", "approved_preferences": APPROVED_PREFERENCES}
