"""
Loan Eligibility Engine
Calculates max loan eligibility, EMI affordability, and risk level
"""


class LoanEngine:

    INTEREST_RATES = {
        "home_loan": 8.5,
        "personal_loan": 14.0,
        "car_loan": 9.5,
        "education_loan": 9.0,
        "default": 12.0
    }

    def evaluate(
        self,
        monthly_income: float,
        existing_emis: float = 0,
        requested_loan: float = 0,
        tenure_months: int = 60,
        loan_type: str = "default"
    ) -> dict:

        # Standard: EMIs should not exceed 40-50% of income
        max_emi_allowed = monthly_income * 0.40
        available_emi = max_emi_allowed - existing_emis

        interest_rate = self.INTEREST_RATES.get(loan_type, 12.0)
        monthly_rate = interest_rate / 12 / 100

        # Max eligible loan based on available EMI
        if monthly_rate > 0 and available_emi > 0:
            max_eligible_loan = available_emi * (
                ((1 + monthly_rate) ** tenure_months - 1) /
                (monthly_rate * (1 + monthly_rate) ** tenure_months)
            )
        else:
            max_eligible_loan = 0

        # EMI for requested loan
        requested_emi = 0
        if requested_loan > 0 and monthly_rate > 0:
            requested_emi = requested_loan * (
                monthly_rate * (1 + monthly_rate) ** tenure_months /
                ((1 + monthly_rate) ** tenure_months - 1)
            )

        total_emi_after = existing_emis + requested_emi
        new_dti = (total_emi_after / monthly_income) * 100 if monthly_income > 0 else 0

        # Eligibility decision
        eligible = available_emi > 0 and (requested_loan <= max_eligible_loan or requested_loan == 0)

        risk_level = "Low"
        if new_dti > 50:
            risk_level = "Very High 🔴"
        elif new_dti > 40:
            risk_level = "High 🟠"
        elif new_dti > 30:
            risk_level = "Moderate 🟡"
        else:
            risk_level = "Low 🟢"

        return {
            "eligible": eligible,
            "monthly_income": monthly_income,
            "existing_emis": existing_emis,
            "available_emi_capacity": round(available_emi, 2),
            "max_eligible_loan": round(max_eligible_loan, 2),
            "requested_loan": requested_loan,
            "required_emi_for_requested": round(requested_emi, 2),
            "interest_rate_percent": interest_rate,
            "tenure_months": tenure_months,
            "total_emi_after_loan": round(total_emi_after, 2),
            "new_dti_percent": round(new_dti, 2),
            "risk_level": risk_level,
            "recommendation": self._recommend(eligible, new_dti, available_emi, max_eligible_loan)
        }

    def _recommend(self, eligible, dti, available_emi, max_loan) -> str:
        if not eligible:
            return (
                f"❌ Loan not recommended. Your current EMI obligations are too high. "
                f"Reduce existing debt before applying. Max eligible: ₹{max_loan:,.0f}"
            )
        if dti > 40:
            return "⚠️ Eligible but risky. Consider a smaller loan amount or longer tenure."
        return f"✅ You appear eligible. Proceed cautiously. Always compare rates across lenders."
