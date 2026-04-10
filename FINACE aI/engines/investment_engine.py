"""
Investment Recommendation Engine
Suggests investment options based on available capital and risk profile
"""


class InvestmentEngine:

    INVESTMENT_OPTIONS = {
        "emergency_fund": {
            "name": "Emergency Fund (Liquid Fund / FD)",
            "risk": "Very Low",
            "expected_return": "5-7%",
            "liquidity": "High",
            "horizon": "Anytime",
            "description": "Keep 6 months of expenses in a high-yield savings account or liquid mutual fund."
        },
        "ppf": {
            "name": "Public Provident Fund (PPF)",
            "risk": "None (Government Backed)",
            "expected_return": "7-7.5%",
            "liquidity": "Low (15 year lock-in)",
            "horizon": "Long-term (15 years)",
            "description": "Tax-free returns, Section 80C benefit. Max ₹1.5L/year."
        },
        "elss": {
            "name": "ELSS Mutual Funds",
            "risk": "Moderate-High",
            "expected_return": "10-14%",
            "liquidity": "Moderate (3 year lock-in)",
            "horizon": "3+ years",
            "description": "Tax saving + equity growth. Best for long-term wealth + 80C deduction."
        },
        "index_fund": {
            "name": "Nifty 50 / Sensex Index Fund (SIP)",
            "risk": "Moderate",
            "expected_return": "10-12% CAGR",
            "liquidity": "High",
            "horizon": "5+ years",
            "description": "Low-cost, diversified equity. Start SIP with as little as ₹500/month."
        },
        "fd": {
            "name": "Fixed Deposit (Bank FD)",
            "risk": "Very Low",
            "expected_return": "6.5-7.5%",
            "liquidity": "Moderate",
            "horizon": "1-5 years",
            "description": "Safe, predictable returns. Good for short-medium term goals."
        },
        "nps": {
            "name": "National Pension System (NPS)",
            "risk": "Low-Moderate",
            "expected_return": "8-10%",
            "liquidity": "Very Low (retirement)",
            "horizon": "Until retirement",
            "description": "Additional 80CCD(1B) deduction of ₹50,000. Great for retirement planning."
        },
        "gold": {
            "name": "Sovereign Gold Bonds (SGB)",
            "risk": "Low-Moderate",
            "expected_return": "7-9% + gold appreciation",
            "liquidity": "Low (5-8 years)",
            "horizon": "5-8 years",
            "description": "Hedge against inflation. Interest + capital gains, no storage risk."
        }
    }

    def recommend(self, available_amount: float = 0, income: float = 0, risk_appetite: str = "moderate") -> dict:
        recommendations = []
        allocation = {}

        if income > 0 and available_amount == 0:
            available_amount = income * 0.20  # Assume 20% of income if not specified

        # Always recommend emergency fund first
        if available_amount > 0:
            recommendations.append({
                "priority": 1,
                "option": self.INVESTMENT_OPTIONS["emergency_fund"],
                "suggested_amount": min(available_amount * 0.3, income * 6 if income else available_amount * 0.3),
                "reason": "Foundation of financial security — do this first"
            })

        # Tax saving (if income exists)
        if income > 0:
            recommendations.append({
                "priority": 2,
                "option": self.INVESTMENT_OPTIONS["ppf"],
                "suggested_amount": min(12500, available_amount * 0.2),  # ₹1.5L/year = ₹12,500/month
                "reason": "Tax-free, government-backed, Section 80C benefit"
            })

        # Long-term wealth
        recommendations.append({
            "priority": 3,
            "option": self.INVESTMENT_OPTIONS["index_fund"],
            "suggested_amount": available_amount * 0.3,
            "reason": "Best long-term wealth builder with low cost"
        })

        # Stable portion
        recommendations.append({
            "priority": 4,
            "option": self.INVESTMENT_OPTIONS["fd"],
            "suggested_amount": available_amount * 0.2,
            "reason": "Capital protection for medium-term goals"
        })

        # Allocation summary
        allocation = {
            "Emergency / Liquid": "30%",
            "Index Fund SIP": "30%",
            "PPF / Tax Saving": "20%",
            "Fixed Deposit": "20%"
        }

        return {
            "available_to_invest": round(available_amount, 2),
            "monthly_income": income,
            "recommended_monthly_sip": round(available_amount * 0.3, 2),
            "allocation_strategy": allocation,
            "recommendations": recommendations,
            "all_options": list(self.INVESTMENT_OPTIONS.values()),
            "disclaimer": "⚠️ Past returns are not guaranteed. Consult a SEBI-registered advisor before investing."
        }
