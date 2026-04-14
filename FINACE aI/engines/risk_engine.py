"""
Financial Risk Detection Engine
Identifies financial crisis signals and debt trap indicators
"""


class RiskEngine:

    def assess(
        self,
        income: float,
        emis: float = 0,
        savings: float = 0,
        expenses: float = 0,
        credit_card_debt: float = 0
    ) -> dict:

        risks = []
        risk_score = 0  # 0 = safe, 100 = critical

        if income <= 0:
            return {"error": "Income required for risk assessment"}

        dti = (emis / income) * 100
        savings_rate = (savings / income) * 100
        expense_ratio = (expenses / income) * 100 if expenses > 0 else 0

        # --- Risk Checks ---

        # 1. Debt Trap Risk
        if dti > 60:
            risks.append({
                "type": "DEBT TRAP",
                "severity": "CRITICAL 🔴",
                "detail": f"EMIs consume {dti:.1f}% of income. You are in a debt trap.",
                "action": "Stop all new borrowing immediately. Seek debt consolidation."
            })
            risk_score += 40
        elif dti > 50:
            risks.append({
                "type": "HIGH DEBT BURDEN",
                "severity": "HIGH 🟠",
                "detail": f"DTI of {dti:.1f}% is dangerously high.",
                "action": "Avoid new loans. Focus on prepaying highest interest debt."
            })
            risk_score += 25
        elif dti > 40:
            risks.append({
                "type": "ELEVATED DEBT",
                "severity": "MODERATE 🟡",
                "detail": f"DTI of {dti:.1f}% is above safe threshold (30-40%).",
                "action": "Limit discretionary spending. Don't take new loans."
            })
            risk_score += 15

        # 2. Zero/Negative Savings
        if savings_rate < 0:
            risks.append({
                "type": "DISSAVING",
                "severity": "CRITICAL 🔴",
                "detail": "You are spending more than you earn.",
                "action": "Create an emergency budget. Cut non-essential expenses immediately."
            })
            risk_score += 35
        elif savings_rate < 5:
            risks.append({
                "type": "INSUFFICIENT SAVINGS",
                "severity": "HIGH 🟠",
                "detail": "Savings rate below 5% leaves you exposed to emergencies.",
                "action": "Target saving at least 10% of income, starting this month."
            })
            risk_score += 20

        # 3. Overspending
        if expense_ratio > 80 and expense_ratio > 0:
            risks.append({
                "type": "OVERSPENDING",
                "severity": "HIGH 🟠",
                "detail": f"{expense_ratio:.1f}% of income goes to expenses, leaving no room.",
                "action": "Review and cut at least 3 discretionary categories."
            })
            risk_score += 15

        # 4. Credit Card Debt
        if credit_card_debt > income * 3:
            risks.append({
                "type": "CREDIT CARD DEBT SPIRAL",
                "severity": "CRITICAL 🔴",
                "detail": "Credit card debt exceeds 3x monthly income at ~36-40% interest.",
                "action": "Pay minimum + extra every month. Stop using card until cleared."
            })
            risk_score += 30

        # 5. Overall stability check
        combined_outflow = emis + (expenses if expenses > 0 else income * 0.5)
        if combined_outflow > income:
            risks.append({
                "type": "NEGATIVE CASH FLOW",
                "severity": "CRITICAL 🔴",
                "detail": "Total outflows exceed income. You are accumulating debt every month.",
                "action": "Immediate financial restructuring required."
            })
            risk_score += 30

        # Clamp and label
        risk_score = min(100, risk_score)
        overall = self._overall_label(risk_score)

        return {
            "risk_score": risk_score,
            "overall_risk": overall,
            "risks_detected": risks,
            "risk_count": len(risks),
            "summary": {
                "dti_percent": round(dti, 1),
                "savings_rate_percent": round(savings_rate, 1),
                "monthly_income": income,
                "total_emis": emis
            },
            "immediate_actions": self._priority_actions(risks),
            "safe_signals": self._safe_signals(dti, savings_rate, income)
        }

    def _overall_label(self, score: int) -> str:
        if score == 0:
            return "Financially Stable 🟢"
        elif score < 20:
            return "Minor Risks Detected 🟡"
        elif score < 50:
            return "Significant Risk 🟠"
        elif score < 75:
            return "High Risk — Act Now 🔴"
        else:
            return "Financial Crisis Warning ⛔"

    def _priority_actions(self, risks: list) -> list:
        critical = [r["action"] for r in risks if "CRITICAL" in r["severity"]]
        high = [r["action"] for r in risks if "HIGH" in r["severity"]]
        return (critical + high)[:3]

    def _safe_signals(self, dti: float, savings_rate: float, income: float) -> list:
        signals = []
        if dti < 30:
            signals.append("✅ Debt-to-income ratio is within safe limits")
        if savings_rate > 20:
            signals.append("✅ Strong savings habit — above 20%")
        if income > 50000:
            signals.append("✅ Income level provides reasonable financial flexibility")
        return signals
