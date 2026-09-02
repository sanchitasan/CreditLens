class RAGFactorQueryBuilder:
    def build(
        self,
        foir: float,
        credit_score: float,
        previous_defaults: int,
        default_probability: float,
        lending_decision: str,
    ) -> list[str]:

        queries = []

        # 1. FOIR policy
        if foir < 30:
            foir_context = "FOIR below 30%"
        elif foir <= 50:
            foir_context = "FOIR from 30% to 50%"
        else:
            foir_context = "FOIR above 50%"

        queries.append(
            f"FOIR policy guidelines, thresholds, and risk classification. "
            f"Applicant FOIR is {foir:.2f}%. "
            f"Retrieve the applicable policy for {foir_context}."
        )

        # 2. Credit score policy
        queries.append(
            f"Credit score policy guidelines and risk classification. "
            f"Applicant credit score is {credit_score:.0f}. "
            f"Retrieve the applicable credit score policy and risk profile."
        )

        # 3. Previous defaults policy
        queries.append(
            f"Previous default policy and impact on credit risk. "
            f"Applicant has {previous_defaults} previous defaults. "
            f"Retrieve the applicable policy for previous defaults."
        )

        # 4. ML default probability policy
        queries.append(
            f"ML default probability policy and interpretation. "
            f"Applicant default probability is {default_probability:.4f}. "
            f"Retrieve the applicable policy explaining how ML default "
            f"probability should be used in credit assessment."
        )

        # 5. Lending decision policy
        queries.append(
            f"Lending decision policy and criteria for {lending_decision}. "
            f"Retrieve the policy explaining when this lending outcome "
            f"is applicable."
        )

        return queries