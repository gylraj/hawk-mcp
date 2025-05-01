# 🧠 Hawk.io – MCP Integration Project

This project demonstrates a modular command protocol (MCP) system designed to support agentic workflows, such as account research and engagement opportunity identification. It includes:

- ✅ A web scraper MCP server (FastAPI + BeautifulSoup)
- ✅ A Google Drive MCP server (FastAPI + Google Drive API)
- ✅ An agent workflow script powered by OpenAI

---

## 📁 Project Structure

```
hawk-mcp/
├── agent/
│   └── workflow.py
├── google_drive_tool/
│   ├── auth.py
│   ├── credentials.json
│   ├── main.py
│   └── token.json  ← generated after auth
├── web_scraper/
│   └── main.py
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate          # On Windows: venv\Scripts\activate
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Generate `token.json` for Google Drive

- Get your `credentials.json` from Google Cloud Console (OAuth Client ID)
- Then run:

```bash
cd google_drive_tool
python auth.py
```

---

### 4. Create `.env` file for OpenAI

In the project root, create `.env`:

```env
OPENAI_API_KEY=sk-your-key-here
```

---

## 🚀 Run Instructions

### ✅ Start MCP Servers (in separate terminals)

#### Terminal 1: Web Scraper

```bash
cd web_scraper
uvicorn main:app --reload --port 8001
```

#### Terminal 2: Google Drive Tool

```bash
cd google_drive_tool
uvicorn main:app --reload --port 8002
```

---

### 🧠 Run Agent Workflow

In another terminal:

```bash
cd agent
python workflow.py
```

It will print a summarized result for the target company.
