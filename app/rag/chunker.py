import re


class DocumentChunker:
    """
    Split loaded Markdown documents into
    meaningful section-level chunks.
    """

    def chunk_documents(
        self,
        documents: list[dict],
    ) -> list[dict]:
        """
        Split documents by Markdown headings.
        """

        chunks = []

        for document in documents:

            sections = re.split(
                r"(?=^## )",
                document["content"],
                flags=re.MULTILINE,
            )

            for index, section in enumerate(sections):

                section = section.strip()

                if not section:
                    continue

                chunks.append(
                    {
                        "source": document["source"],
                        "chunk_id": index,
                        "content": section,
                    }
                )

        return chunks