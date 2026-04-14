"""
Financial Analyzer Engine
Calculates DTI, savings rate, financial health score, and overall analysis
"""


class FinancialAnalyzer:

    def full_analysis(
        self,
        monthly_income: float,
        monthly_expenses: float,
        total_emis: float,
        savings: float,
        loan_amount: float = 0
    ) -> dict:
        if monthly_income <= 0:
            return {"error": "Monthly income must be greater than 0"}

        # Key ratios
        dti = self._debt_to_income(total_emis, monthly_income)
        savings_rate = self._savings_rate(savings, monthly_income)
        expense_ratio = (monthly_expenses / monthly_income) * 100
        disposable = monthly_income - monthly_expenses - total_emis

        # Health score (0-100)
        health_score = self._health_score(dti, savings_rate, disposable, monthly_income)
        health_label = self._health_label(health_score)

        # Emergency fund status (should be 6 months of expenses)
        emergency_fund_target = monthly_expenses * 6
        emergency_fund_months = savings / monthly_expenses if monthly_expenses > 0 else 0

        result = {
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
            "total_emis": total_emis,
            "total_savings": savings,
            "disposable_income": round(disposable, 2),
            "debt_to_income_ratio": round(dti, 2),
            "savings_rate_percent": round(savings_rate, 2),
            "expense_ratio_percent": round(expense_ratio, 2),
            "financial_health_score": round(health_score, 1),
            "health_label": health_label,
            "emergency_fund_months": round(emergency_fund_months, 1),
            "emergency_fund_target": emergency_fund_target,
            "warnings": self._generate_warnings(dti, savings_rate, disposable, emergency_fund_months),
            "recommendations": self._generate_recommendations(dti, savings_rate, disposable, monthly_income)
        }

        return result

    def _debt_to_income(self, emis: float, income: float) -> float:
        return (emis / income) * 100 if income > 0 else 0

    def _savings_rate(self, savings: float, income: float) -> float:
        return (savings / income) * 100 if income > 0 else 0

    def _health_score(self, dti: float, savings_rate: float, disposable: float, income: float) -> float:
        score = 100

        # Penalize high DTI (ideal < 30%)
        if dti > 50:
            score -= 40
        elif dti > 40:
            score -= 25
        elif dti > 30:
            score -= 10

        # Penalize low savings rate (ideal > 20%)
        if savings_rate < 5:
            score -= 30
        elif savings_rate < 10:
            score -= 15
        elif savings_rate < 20:
            score -= 5

        # Penalize negative disposable income
        if disposable < 0:
            score -= 30
        elif disposable < income * 0.1:
            score -= 10

        return max(0, min(100, score))

    def _health_label(self, score: float) -> str:
        if score >= 80:
            return "Excellent 🟢"
        elif score >= 60:
            return "Good 🟡"
        elif score >= 40:
            return "Fair 🟠"
        else:
            return "Critical 🔴"

    def _generate_warnings(self, dti, savings_rate, disposable, emergency_months) -> list:
        warnings = []
        if dti > 50:
            warnings.append("🚨 CRITICAL: Debt-to-income ratio exceeds 50%. High risk of debt trap.")
        elif dti > 40:
            warnings.append("⚠️ HIGH RISK: Debt obligations are consuming too much of your income.")
        elif dti > 30:
            warnings.append("⚠️ WARNING: DTI above 30%. Consider paying down debt before new loans.")

        if savings_rate < 5:
            warnings.append("🚨 Very low savings rate. You are financially vulnerable.")
        elif savings_rate < 10:
            warnings.append("⚠️ Savings rate below recommended 10-20%. Try to cut discretionary expenses.")

        if disposable < 0:
            warnings.append("🚨 CRITICAL: You are spending more than you earn. Immediate action required.")

        if emergency_months < 3:
            warnings.append("⚠️ Emergency fund insufficient. Target at least 6 months of expenses.")

        return warnings

    def _generate_recommendations(self, dti, savings_rate, disposable, income) -> list:
        recs = []
        if dti > 40:
            recs.append("Prioritize paying off high-interest debt (credit cards first).")
        if savings_rate < 20:
            recs.append(f"Try to save at least ₹{income * 0.20:,.0f}/month (20% of income).")
        if disposable > income * 0.3:
            recs.append("You have good surplus income — consider SIP investments in mutual funds.")
        recs.append("Maintain an emergency fund covering 6 months of expenses.")
        return recs
