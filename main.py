from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import httpx
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

if not RESEND_API_KEY:
    raise RuntimeError("RESEND_API_KEY not found")

app = FastAPI(title="Emmanuel Lelo — Contact API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
OWNER_EMAIL    = os.getenv("OWNER_EMAIL", "leloemmanuel540@gmail.com")

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

submissions: list[dict] = []

@app.get("/")
def root():
    return {"status": "Contact API is running 🚀"}

@app.get("/ping")
def ping():
    return {"status": "alive"}

@app.post("/contact", status_code=200)
async def send_contact(form: ContactForm):

    html_body = f"""
    <html><body style="font-family:sans-serif;color:#1e293b;max-width:600px;margin:auto">
      <div style="background:#0f172a;padding:24px 32px;border-radius:12px 12px 0 0">
        <h2 style="color:#14b8a6;margin:0">New Portfolio Message 📬</h2>
      </div>
      <div style="background:#f8fafc;padding:24px 32px;border:1px solid #e2e8f0;border-radius:0 0 12px 12px">
        <p><strong>From:</strong> {form.name} &lt;{form.email}&gt;</p>
        <p><strong>Subject:</strong> {form.subject}</p>
        <p><strong>Received:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</p>
        <hr style="border:none;border-top:1px solid #e2e8f0;margin:18px 0">
        <p style="white-space:pre-wrap">{form.message}</p>
      </div>
    </body></html>
    """

    payload = {
        "from": "Portfolio Contact <onboarding@resend.dev>",
        "to": [OWNER_EMAIL],
        "reply_to": form.email,
        "subject": f"[Portfolio] {form.subject}",
        "html": html_body,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"Email failed: {response.text}"
        )

    submissions.append({
        "name":      form.name,
        "email":     form.email,
        "subject":   form.subject,
        "message":   form.message,
        "timestamp": datetime.utcnow().isoformat(),
    })

    return {"success": True, "message": "Your message was sent successfully!"}

@app.get("/submissions")
def list_submissions():
    return {"count": len(submissions), "data": submissions}
