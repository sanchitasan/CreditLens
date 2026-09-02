class RAGQueryBuilder:
    def build(
        self,
        foir: float,
        credit_score: float,
        previous_defaults: int,
        default_probability: float,
        risk_level: str,
        lending_decision: str,
    ) -> str:

        foir_guidance = (
            "FOIR below 30% low financial obligation risk"
            if foir < 30
            else "FOIR from 30% to 50% moderate financial obligation risk"
            if foir <= 50
            else "FOIR above 50% high financial obligation risk"
        )

        credit_score_guidance = (
            "strong credit quality and credit score guidelines"
            if credit_score >= 750
            else "credit score guidelines and weaker credit quality"
        )

        default_guidance = (
            "previous default guidelines for applicants with no previous defaults"
            if previous_defaults == 0
            else "previous default guidelines and increased risk from previous defaults"
        )

        ml_guidance = (
            "ML default probability guidelines and low predicted default risk"
            if default_probability < 0.30
            else "ML default probability guidelines and elevated predicted default risk"
        )

        decision_guidance = (
            "APPROVE lending decision guidelines"
            if lending_decision == "APPROVE"
            else "MANUAL_REVIEW lending decision guidelines"
            if lending_decision == "MANUAL_REVIEW"
            else "REJECT lending decision guidelines"
        )

        return (
            "CreditLens credit policy retrieval. "
            f"Applicant has FOIR {foir:.2f}%. "
            f"Relevant FOIR policy: {foir_guidance}. "
            f"Applicant credit score is {credit_score:.0f}. "
            f"Relevant credit score policy: {credit_score_guidance}. "
            f"Applicant has {previous_defaults} previous defaults. "
            f"Relevant default policy: {default_guidance}. "
            f"ML default probability is {default_probability:.4f}. "
            f"Relevant ML policy: {ml_guidance}. "
            f"Applicant risk level is {risk_level}. "
            f"Relevant lending policy: {decision_guidance}. "
            "Retrieve the policy sections that explain these risk factors, "
            "their thresholds, and the applicable lending decision."
        )