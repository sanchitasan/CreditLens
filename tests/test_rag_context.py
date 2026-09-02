from app.rag.context import RAGContextBuilder


class FakeResult:

    def __init__(self, content):

        self.payload = {
            "content": content
        }


def test_context_builder_creates_policy_context():

    results = [
        FakeResult(
            "## 2. FOIR Guidelines\nFOIR above 50% is high risk."
        ),
        FakeResult(
            "## 3. Credit Score Guidelines\nScores above 750 indicate strong credit quality."
        ),
    ]

    builder = RAGContextBuilder()

    context = builder.build(results)

    assert "[Policy Context 1]" in context
    assert "[Policy Context 2]" in context

    assert "FOIR above 50% is high risk." in context
    assert "Scores above 750 indicate strong credit quality." in context

def test_context_builder_returns_empty_string_for_no_results():

    builder = RAGContextBuilder()

    context = builder.build([])

    assert context == ""

def test_context_builder_includes_source_and_retrieval_score():

    class FakeResult:

        score = 0.7423717930188408

        payload = {
            "source": "credit_policy.md",
            "content": "FOIR above 50% is high risk.",
        }

    builder = RAGContextBuilder()

    context = builder.build([FakeResult()])

    assert "Source: credit_policy.md" in context
    assert "Retrieval Score: 0.7424" in context
    assert "FOIR above 50% is high risk." in context

def test_context_builder_handles_missing_score():

    class FakeResult:

        payload = {
            "source": "credit_policy.md",
            "content": "Credit score policy.",
        }

    builder = RAGContextBuilder()

    context = builder.build([FakeResult()])

    assert "Source: credit_policy.md" in context
    assert "Retrieval Score: N/A" in context
    assert "Credit score policy." in context