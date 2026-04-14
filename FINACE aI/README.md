# 💰 FinanceAI — Local AI Personal Finance Assistant

A fully offline AI-powered personal finance advisor using a local LLM (Ollama).

## 🏗 Architecture
```
User → Chat UI (HTML/JS) → Flask Backend → Ollama (Llama3) → Financial Engines → SQLite Memory → Response
```

## 📁 Project Structure
```
finance-ai/
├── app.py                    # Main Flask application
├── requirements.txt
├── backend/
│   ├── llm_client.py         # Ollama LLM connector
│   └── tool_router.py        # Intent detection & engine routing
├── engines/
│   ├── financial_analyzer.py # DTI, health score, full analysis
│   ├── loan_engine.py        # Loan eligibility & EMI calculation
│   ├── credit_engine.py      # Credit score estimation
│   ├── investment_engine.py  # Investment recommendations
│   └── risk_engine.py        # Financial crisis detection
├── memory/
│   └── memory_manager.py     # SQLite conversation storage
└── templates/
    └── index.html            # Chat UI
```

## 🚀 Setup & Run

### 1. Install Ollama
```bash
# Mac/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: Download from https://ollama.ai
```

### 2. Download a Model
```bash
ollama pull llama3        # Recommended (4.7GB)
# OR
ollama pull mistral       # Lighter alternative (4.1GB)
```

### 3. Start Ollama
```bash
ollama serve
```

### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the App
```bash
python app.py
```

### 6. Open in Browser
```
http://localhost:5000
```

## 🔧 Configuration

### Change Model
In `backend/llm_client.py`, update:
```python
def __init__(self, model: str = "llama3", ...):
```
Options: `llama3`, `mistral`, `llama3:8b`, `phi3`

### Switch to MySQL Memory
In `memory/memory_manager.py`, replace SQLite with:
```python
import mysql.connector
conn = mysql.connector.connect(host="localhost", user="root", password="", database="financeai")
```

## 💡 Example Queries

- *"Can I get a home loan of ₹30 lakh with salary ₹70,000?"*
- *"Estimate my credit score — income ₹60,000, EMI ₹18,000, no missed payments"*
- *"Where should I invest ₹15,000 per month?"*
- *"Am I in a debt trap? Income ₹45,000, EMI ₹28,000"*
- *"How do I improve my CIBIL score?"*

## 🔮 Future Extensions

- [ ] Vector DB memory (ChromaDB) for long-term context
- [ ] RAG web search for live financial news
- [ ] PDF export of financial reports
- [ ] Multi-user support with JWT auth
- [ ] Mobile app (React Native / Flutter)

## ⚠️ Disclaimer
This tool provides general financial information, not personalized financial advice.
Always consult a SEBI-registered financial advisor for major investment decisions.
