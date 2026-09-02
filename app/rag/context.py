class RAGContextBuilder:

    def build(self, results) -> str:

        if not results:
            return ""

        context_parts = []

        for index, result in enumerate(results, start=1):

            payload = result.payload or {}

            source = payload.get("source", "unknown")
            content = payload.get("content", "")
            score = getattr(result, "score", None)

            if score is not None:
                score_text = f"{score:.4f}"
            else:
                score_text = "N/A"

            context_parts.append(
                f"[Policy Context {index}]\n"
                f"Source: {source}\n"
                f"Retrieval Score: {score_text}\n\n"
                f"{content}"
            )

        return "\n\n".join(context_parts)