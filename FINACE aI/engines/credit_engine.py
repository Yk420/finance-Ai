"""
Credit Score Estimation Engine
Estimates credit score range based on financial behavior
Note: This is an ESTIMATION — actual CIBIL score requires bureau data
"""


class CreditEngine:

    def estimate(
        self,
        income: float = 0,
        emis: float = 0,
        savings: float = 0,
        missed_payments: int = 0,
        credit_utilization: float = 0,   # % of credit card limit used
        years_of_credit: int = 0
    ) -> dict:

        score = 650  # Base score

        # 1. DTI impact (35% weight)
        if income > 0:
            dti = (emis / income) * 100
            if dti < 20:
                score += 80
            elif dti < 30:
                score += 50
            elif dti < 40:
                score += 20
            elif dti < 50:
                score -= 30
            else:
                score -= 80

        # 2. Savings behavior (20% weight)
        if income > 0:
            savings_rate = (savings / income) * 100
            if savings_rate > 30:
                score += 50
            elif savings_rate > 20:
                score += 30
            elif savings_rate > 10:
                score += 10
            elif savings_rate < 5:
                score -= 30

        # 3. Payment history (35% weight — most important)
        if missed_payments == 0:
            score += 70
        elif missed_payments <= 2:
            score -= 40
        elif missed_payments <= 5:
            score -= 100
        else:
            score -= 150

        # 4. Credit utilization (10% weight)
        if credit_utilization > 0:
            if credit_utilization < 30:
                score += 40
            elif credit_utilization < 50:
                score += 10
            elif credit_utilization < 75:
                score -= 30
            else:
                score -= 70

        # 5. Credit history length (bonus)
        if years_of_credit > 5:
            score += 30
        elif years_of_credit > 2:
            score += 10

        # Clamp to 300-900 range (CIBIL scale)
        score = max(300, min(900, score))

        return {
            "estimated_score": score,
            "score_range": self._score_label(score),
            "loan_approval_likelihood": self._loan_likelihood(score),
            "breakdown": {
                "dti_ratio": round((emis / income * 100) if income > 0 else 0, 1),
                "savings_rate": round((savings / income * 100) if income > 0 else 0, 1),
                "missed_payments": missed_payments,
                "credit_utilization": credit_utilization
            },
            "improvement_tips": self._improvement_tips(score, emis, income, missed_payments, credit_utilization),
            "disclaimer": "⚠️ This is an AI estimation only. Get your actual CIBIL score from cibil.com"
        }

    def _score_label(self, score: int) -> str:
        if score >= 800:
            return "Excellent (800-900) 🟢"
        elif score >= 700:
            return "Good (700-799) 🟡"
        elif score >= 600:
            return "Fair (600-699) 🟠"
        elif score >= 500:
            return "Poor (500-599) 🔴"
        else:
            return "Very Poor (<500) ⛔"

    def _loan_likelihood(self, score: int) -> str:
        if score >= 750:
            return "High — Most banks will approve at good rates"
        elif score >= 700:
            return "Moderate — Likely approved, may get higher interest"
        elif score >= 650:
            return "Low — Approval not guaranteed, may need collateral"
        else:
            return "Very Low — Work on credit improvement before applying"

    def _improvement_tips(self, score, emis, income, missed, utilization) -> list:
        tips = []
        if missed > 0:
            tips.append("🔑 Never miss EMI/credit card payments — set auto-pay")
        if income > 0 and (emis / income) > 0.35:
            tips.append("💳 Pay down existing EMIs to reduce debt burden")
        if utilization > 30:
            tips.append("📉 Keep credit card usage below 30% of your limit")
        if score < 700:
            tips.append("📅 Maintain consistent on-time payments for 6-12 months")
            tips.append("🏦 Consider a secured credit card to build credit history")
        return tips
