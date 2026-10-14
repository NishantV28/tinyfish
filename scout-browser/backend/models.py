from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class CommandRequest(BaseModel):
    user_id: str
    prompt: str
    current_page_url: Optional[str] = None
    open_tabs: Optional[List[str]] = []
    browser_profile_id: Optional[str] = None

class ApprovalRequest(BaseModel):
    task_id: str
    user_id: str
    approved: bool

class InboundEmailWebhook(BaseModel):
    alias_email: str
    from_email: str
    from_domain: str
    subject: str

class PreferenceApprovalRequest(BaseModel):
    user_id: str
    category: str
    key: str
    value: Any
