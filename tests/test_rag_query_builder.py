from app.rag.factor_queries import RAGFactorQueryBuilder


def test_factor_query_builder_returns_five_queries():

    builder = RAGFactorQueryBuilder()

    queries = builder.build(
        foir=25.0,
        credit_score=780,
        previous_defaults=0,
        default_probability=0.10,
        lending_decision="APPROVE",
    )

    assert len(queries) == 5


def test_factor_query_builder_contains_relevant_policy_factors():

    builder = RAGFactorQueryBuilder()

    queries = builder.build(
        foir=58.0,
        credit_score=680,
        previous_defaults=2,
        default_probability=0.72,
        lending_decision="REJECT",
    )

    combined_query = " ".join(queries)

    assert "FOIR" in combined_query
    assert "credit score" in combined_query
    assert "Previous default" in combined_query
    assert "ML default probability" in combined_query
    assert "REJECT" in combined_query


def test_factor_query_builder_includes_foir_range():

    builder = RAGFactorQueryBuilder()

    queries = builder.build(
        foir=58.0,
        credit_score=680,
        previous_defaults=2,
        default_probability=0.72,
        lending_decision="REJECT",
    )

    combined_query = " ".join(queries)

    assert "FOIR above 50%" in combined_query


def test_factor_query_builder_does_not_invent_policy_thresholds():

    builder = RAGFactorQueryBuilder()

    queries = builder.build(
        foir=58.0,
        credit_score=680,
        previous_defaults=2,
        default_probability=0.72,
        lending_decision="REJECT",
    )

    combined_query = " ".join(queries)

    assert "weaker credit quality" not in combined_query
    assert "elevated predicted default risk" not in combined_query