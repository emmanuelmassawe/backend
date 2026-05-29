from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

app = FastAPI(title="Emmanuel Lelo — Contact API", version="1.0.0")

# ── CORS: allow your portfolio's origin ──────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from dotenv import load_dotenv
load_dotenv()

# ── Config (set these as env vars before running) ───────────────────────────
SMTP_HOST     = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT     = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER     = os.getenv("SMTP_USER", "your_gmail@gmail.com")   # sender account
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_app_password")  # Gmail App Password
OWNER_EMAIL   = os.getenv("OWNER_EMAIL", "leloemmanuel540@email.com")  # where to receive


# ── Request schema ───────────────────────────────────────────────────────────
class ContactForm(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str


# ── In-memory log (replace with a DB if you want persistence) ───────────────
submissions: list[dict] = []


# ── Routes ───────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "Contact API is running 🚀"}


@app.post("/contact", status_code=200)
def send_contact(form: ContactForm):
    """Receive a contact form submission and e-mail it to the portfolio owner."""

    # ── Build e-mail ─────────────────────────────────────────────────────────
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"[Portfolio Contact] {form.subject}"
    msg["From"]    = SMTP_USER
    msg["To"]      = OWNER_EMAIL
    msg["Reply-To"] = form.email

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
    text_body = (
        f"From: {form.name} <{form.email}>\n"
        f"Subject: {form.subject}\n\n{form.message}"
    )

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    # ── Send via SMTP ─────────────────────────────────────────────────────────
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, OWNER_EMAIL, msg.as_string())
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"E-mail delivery failed: {str(exc)}"
        )

    # ── Log submission ────────────────────────────────────────────────────────
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
    """Returns all in-memory submissions (dev/debug use only)."""
    return {"count": len(submissions), "data": submissions}
