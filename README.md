# 📬 Portfolio Contact API

A simple FastAPI backend that powers the contact form on **Emmanuel John Lelo's** portfolio website. When a visitor submits the form, this API sends an email directly to the portfolio owner.

---

## 🚀 Features

- Receives contact form submissions via REST API
- Sends a formatted HTML email to the owner via Gmail SMTP
- Input validation using Pydantic
- CORS enabled — works with any frontend
- In-memory submission log for debugging
- Clean and minimal — single `main.py` file

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| FastAPI | Web framework |
| Uvicorn | ASGI server |
| Pydantic | Data validation |
| smtplib | Sending emails |
| python-dotenv | Managing credentials |

---

## 📁 Project Structure

```
backend/
├── main.py          # Main FastAPI application
├── .env             # Credentials (NOT pushed to GitHub)
├── .gitignore       # Protects .env from GitHub
├── requirements.txt # Dependencies
└── README.md        # This file
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/emmanuelmassawe/backend.git
cd backend
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv myenv
myenv\Scripts\activate

# Mac/Linux
python -m venv myenv
source myenv/bin/activate
```

### 3. Install Dependencies

```bash
pip install fastapi uvicorn pydantic[email] python-dotenv
```

Or using requirements.txt:

```bash
pip install -r requirements.txt
```

### 4. Create `.env` File

Create a file named `.env` in the project folder:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_gmail@gmail.com
SMTP_PASSWORD=your_app_password_here
OWNER_EMAIL=your_email@gmail.com
```

> ⚠️ **Never push `.env` to GitHub!** It is already protected by `.gitignore`.

### 5. Get Gmail App Password

1. Go to: **myaccount.google.com/apppasswords**
2. Type any name (e.g. `portfolio`)
3. Click **Create**
4. Copy the 16-character password
5. Paste it into `.env` as `SMTP_PASSWORD`

> 💡 Make sure **2-Step Verification** is enabled on your Google account first.

### 6. Run the Server

```bash
uvicorn main:app --reload
```

Server will start at:
```
http://localhost:8000
```

---

## 📡 API Endpoints

### `GET /`
Health check — confirms the API is running.

**Response:**
```json
{
  "status": "Contact API is running 🚀"
}
```

---

### `POST /contact`
Receives a contact form submission and sends an email.

**Request Body:**
```json
{
  "name": "Jane Smith",
  "email": "jane@company.com",
  "subject": "Remote ML Engineer opportunity",
  "message": "Hi Emmanuel, I would love to discuss..."
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "Your message was sent successfully!"
}
```

**Error Response:**
```json
{
  "detail": "E-mail delivery failed: ..."
}
```

---

### `GET /submissions`
Returns all submissions received since server started (for debugging only).

**Response:**
```json
{
  "count": 2,
  "data": [
    {
      "name": "Jane Smith",
      "email": "jane@company.com",
      "subject": "Job opportunity",
      "message": "Hello...",
      "timestamp": "2026-05-30T10:22:00"
    }
  ]
}
```

---

## 🔒 Security Notes

- ✅ Credentials stored in `.env` — not in code
- ✅ `.env` is listed in `.gitignore` — never pushed to GitHub
- ✅ Gmail App Password used — not your real Gmail password
- ✅ CORS configured — restrict `allow_origins` to your domain in production

---

## 🌍 Connecting to Portfolio Frontend

In `portfolio.html`, update this line with your server URL:

```javascript
const API_URL = 'http://localhost:8000'; // development

// Change to your live server in production, e.g:
const API_URL = 'https://your-server.com';
```

---

## 📦 requirements.txt

```
fastapi
uvicorn
pydantic[email]
python-dotenv
```

Generate automatically with:
```bash
pip freeze > requirements.txt
```

---

## 👤 Author

**Emmanuel John Lelo**
Full-Stack Data Scientist & MLOps Engineer
📧 leloemmanuel540@email.com
💼 [LinkedIn](https://linkedin.com/in/emmanuel-john-61b343334)
🐙 [GitHub](https://github.com/emmanuelmassawe)
🌍 Open to Remote — Europe & Worldwide

---

## 📄 License

MIT License — free to use and modify.
