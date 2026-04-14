"""
Tool Router - Detects financial intent and routes to appropriate engine
Uses keyword/pattern matching (no external NLP API needed)
"""

import re
from engines.financial_analyzer import FinancialAnalyzer
from engines.loan_engine import LoanEngine
from engines.credit_engine import CreditEngine
from engines.investment_engine import InvestmentEngine
from engines.risk_engine import RiskEngine


class ToolRouter:
    def __init__(self):
        self.analyzer = FinancialAnalyzer()
        self.loan_engine = LoanEngine()
        self.credit_engine = CreditEngine()
        self.investment_engine = InvestmentEngine()
        self.risk_engine = RiskEngine()

        # Intent patterns
        self.patterns = {
            "loan": [
                r"loan", r"borrow", r"emi", r"mortgage", r"credit limit",
                r"eligible.*loan", r"can i (get|take|afford) a loan", r"home loan", r"car loan"
            ],
            "credit": [
                r"credit score", r"cibil", r"credit rating", r"credit report",
                r"improve.*credit", r"credit history"
            ],
            "investment": [
                r"invest", r"mutual fund", r"sip", r"stock", r"portfolio",
                r"where.*put.*money", r"grow.*money", r"returns", r"fd", r"fixed deposit"
            ],
            "risk": [
                r"risk", r"danger", r"crisis", r"warn", r"debt trap",
                r"overspend", r"bankrupt", r"financial health"
            ],
            "analysis": [
                r"analyze", r"summary", r"overview", r"financial status",
                r"how am i doing", r"budget", r"savings rate", r"income.*expense"
            ]
        }

    def detect_intent(self, message: str) -> str:
        message_lower = message.lower()
        scores = {intent: 0 for intent in self.patterns}

        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    scores[intent] += 1

        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "general"

    def extract_numbers(self, message: str) -> dict:
        """Extract financial figures mentioned in the message"""
        numbers = {}
        
        # Income patterns
        income_match = re.search(
            r"(?:income|salary|earn(?:ing)?s?)[^\d]*?(\d[\d,]*)", message, re.I
        )
        if income_match:
            numbers["income"] = float(income_match.group(1).replace(",", ""))

        # EMI patterns
        emi_match = re.search(
            r"(?:emi|monthly payment)[^\d]*?(\d[\d,]*)", message, re.I
        )
        if emi_match:
            numbers["emi"] = float(emi_match.group(1).replace(",", ""))

        # Loan amount patterns
        loan_match = re.search(
            r"(?:loan|borrow)[^\d]*?(\d[\d,]*(?:\s*(?:lakh|lac|k|thousand|crore))?)", message, re.I
        )
        if loan_match:
            raw = loan_match.group(1).lower().replace(",", "")
            numbers["loan_amount"] = self._parse_amount(raw)

        # Savings patterns
        savings_match = re.search(
            r"(?:sav(?:ing|e)s?)[^\d]*?(\d[\d,]*)", message, re.I
        )
        if savings_match:
            numbers["savings"] = float(savings_match.group(1).replace(",", ""))

        return numbers

    def _parse_amount(self, raw: str) -> float:
        num = re.search(r"[\d.]+", raw)
        if not num:
            return 0
        value = float(num.group())
        if "lakh" in raw or "lac" in raw:
            value *= 100000
        elif "crore" in raw:
            value *= 10000000
        elif "k" in raw or "thousand" in raw:
            value *= 1000
        return value

    def route(self, message: str) -> dict:
        intent = self.detect_intent(message)
        numbers = self.extract_numbers(message)

        result = {"tool": intent, "data": {}, "numbers": numbers}

        try:
            if intent == "loan" and numbers.get("income"):
                result["data"] = self.loan_engine.evaluate(
                    monthly_income=numbers.get("income", 0),
                    existing_emis=numbers.get("emi", 0),
                    requested_loan=numbers.get("loan_amount", 0)
                )

            elif intent == "credit":
                result["data"] = self.credit_engine.estimate(
                    income=numbers.get("income", 0),
                    emis=numbers.get("emi", 0),
                    savings=numbers.get("savings", 0)
                )

            elif intent == "investment":
                result["data"] = self.investment_engine.recommend(
                    available_amount=numbers.get("savings", 0),
                    income=numbers.get("income", 0)
                )

            elif intent == "risk":
                result["data"] = self.risk_engine.assess(
                    income=numbers.get("income", 0),
                    emis=numbers.get("emi", 0),
                    savings=numbers.get("savings", 0)
                )

        except Exception as e:
            result["data"] = {"error": str(e)}

        return result
