# 🧵 TailorTalk - AI Calendar Assistant

TailorTalk is an intelligent meeting scheduling assistant that helps users book, manage, and query appointments using natural language. It integrates with Google Calendar and is powered by OpenRouter (via LangChain) to understand conversational inputs like "schedule something for tomorrow afternoon" or "book a call next Friday between 3-5 PM".

---

## 🌐 Live Demo

👉 [Try TailorTalk on Streamlit](https://tailor-talk-imkppawqbqgzb4ftjrqjf7.streamlit.app/)

---

## 🚀 Project Features

* 🤖 **Conversational AI Chatbot** powered by OpenRouter (using models like LLaMA3/Mixtral)
* 🧠 **Natural Language Understanding** for vague or human-friendly phrases ("tomorrow", "next Friday", etc.)
* 📅 **Google Calendar Integration** for booking and viewing events
* 🔁 **Real-time availability checks** to prevent double-booking
* 📆 **Time range handling** (e.g., "between 3–5 PM")
* 🤔 **Smart fallback suggestions** when the model is uncertain
* 🌐 **Streamlit frontend** with interactive chat UI

---

## 🧠 Technologies Used

| Layer      | Tech Stack                                       |
| ---------- | ------------------------------------------------ |
| Frontend   | Streamlit                                        |
| Backend    | FastAPI                                          |
| AI Models  | OpenRouter (LLaMA3, Mixtral, etc.) via LangChain |
| Calendar   | Google Calendar API                              |
| NLP Tools  | parsedatetime, dateparser                        |
| Deployment | Render (Backend) + Streamlit Cloud (Frontend)    |

---

## 📁 Folder Structure

```
tailor-talk/
├── app.py                 # Streamlit frontend
├── main.py                # FastAPI backend entry
├── chatbot/
│   └── agent.py           # Core logic for AI and scheduling
├── gcal/
│   ├── calendar_auth.py   # Google Calendar auth setup
│   └── calendar_utils.py  # Availability + booking logic
├── .env                   # OpenRouter API Key (not committed)
├── credentials.json       # Google OAuth client file
├── token.pkl              # Generated Google token (auto)
└── requirements.txt       # Python dependencies
```

---

## 💻 Run Locally

> Make sure you have Python 3.10+ and `pip` installed.

### 1. Clone the repository

```bash
git clone https://github.com/your-username/tailor-talk.git
cd tailor-talk
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add `.env` file

Create a file named `.env` with your OpenRouter key:

```env
OPENROUTER_API_KEY=sk-or-your-openrouter-key
```

### 4. Add Google Calendar credentials

Download your `credentials.json` from Google Cloud Console and place it in the root folder.
It will generate a `token.pkl` automatically on first run.

### 5. Run backend (FastAPI)

```bash
uvicorn main:app --reload
```

It will start on: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 6. Run frontend (Streamlit)

In a new terminal:

```bash
streamlit run app.py
```

It will open on: [http://localhost:8501](http://localhost:8501)

---

## 🔐 Google Calendar Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the **Google Calendar API**
3. Create **OAuth 2.0 Client ID** (Desktop app)
4. Download `credentials.json`
5. Place it in your project root
6. When prompted, login and allow calendar permissions

---

## 🧪 Example Prompts

* "Book me an appointment for June 30 at 4 PM"
* "Schedule a call tomorrow at 11 AM"
* "Do I have free time next Friday between 3 and 5 PM?"
* "Can you book something on Monday morning?"

---

## ✅ Submission Checklist

* [x] Booking via OpenRouter works ✅
* [x] Free time checking logic implemented ✅
* [x] Duplicate booking prevention ✅
* [x] Streamlit frontend deployed ✅
* [x] Calendar API authentication ✅

---

## 🙌 Author

Built by SamuelBaiju

🔗 Live Link: [https://tailor-talk-93qz.streamlit.app](https://tailor-talk-imkppawqbqgzb4ftjrqjf7.streamlit.app/)

📬 For feedback or support, contact: \[[your.email@example.com](mailto:baijusamuel10@gmail.com)]
