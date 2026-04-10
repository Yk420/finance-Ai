"""
Personal Finance AI Assistant - Main Flask App
Local LLM (Ollama) powered, no external APIs
"""

from flask import Flask, request, jsonify, render_template, session
import uuid
from backend.llm_client import LLMClient
from backend.tool_router import ToolRouter
from memory.memory_manager import MemoryManager
from flask import redirect

app = Flask(__name__)
app.secret_key = "finance-ai-secret-key-change-in-production"

llm = LLMClient()
router = ToolRouter()
memory = MemoryManager()

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/")
def index():
    return redirect("/login")

@app.route("/home")
def home():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return render_template("home.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()
    session_id = session.get("session_id", str(uuid.uuid4()))

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Save user message to memory
    memory.save_message(session_id, "user", user_message)

    # Get conversation history for context
    history = memory.get_history(session_id, limit=10)

    # Route message to appropriate financial engine
    tool_result = router.route(user_message)

    # Build system prompt with financial context
    system_prompt = build_system_prompt(tool_result)

    # Get LLM response
    response = llm.chat(user_message, history, system_prompt)

    # Save assistant response
    memory.save_message(session_id, "assistant", response)

    return jsonify({
        "response": response,
        "tool_used": tool_result.get("tool"),
        "data": tool_result.get("data", {})
    })


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """Deep financial analysis endpoint"""
    data = request.json
    income = float(data.get("monthly_income", 0))
    expenses = float(data.get("monthly_expenses", 0))
    emis = float(data.get("total_emis", 0))
    savings = float(data.get("savings", 0))
    loan_amount = float(data.get("loan_amount", 0))

    from engines.financial_analyzer import FinancialAnalyzer
    analyzer = FinancialAnalyzer()
    result = analyzer.full_analysis(income, expenses, emis, savings, loan_amount)
    return jsonify(result)


@app.route("/api/clear", methods=["POST"])
def clear():
    session_id = session.get("session_id")
    if session_id:
        memory.clear_session(session_id)
    return jsonify({"status": "cleared"})


def build_system_prompt(tool_result: dict) -> str:
    base = """You are FinanceAI, a professional and empathetic personal finance advisor.
You provide honest, responsible financial guidance. You ALWAYS:
- Warn users about high financial risks clearly
- Suggest safe, diversified investments
- Avoid giving guaranteed return promises
- Recommend consulting a certified financial advisor for major decisions
- Use simple language with numbers and percentages

"""
    if tool_result.get("data"):
        base += f"\n[FINANCIAL ANALYSIS DATA]\n{tool_result['data']}\n"
        base += "Use the above calculated data to provide accurate, specific advice.\n"
    return base


if __name__ == "__main__":
    print("🚀 Finance AI Assistant starting on http://localhost:5000")
    print("📦 Make sure Ollama is running: ollama serve")
    app.run(debug=True, port=5000)
