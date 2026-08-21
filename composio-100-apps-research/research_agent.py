import json
import os
from pydantic import BaseModel, Field
from openai import OpenAI

class AppAudit(BaseModel):
    app_name: str
    category: str
    summary: str
    auth_method: str = Field(description="OAuth2, API Key, Basic, Token, or CLI")
    access_model: str = Field(description="Self-Serve, Gated, or Enterprise")
    api_surface: str
    buildability: str = Field(description="Ready, Friction, or Blocked")
    blocker_reason: str
    evidence_url: str

def audit_app(app_name: str, hint_url: str) -> AppAudit:
    client = OpenAI()
    prompt = f"Research developer API specs for {app_name} ({hint_url}). Classify auth, access, and buildability."
    
    res = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format=AppAudit,
    )
    return res.choices[0].message.parsed