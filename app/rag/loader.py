from pathlib import Path


class DocumentLoader:
    """
    Load text documents from the CreditLens knowledge base.
    """

    def __init__(self, knowledge_directory: Path):
        self.knowledge_directory = knowledge_directory

    def load_documents(self) -> list[dict]:
        """
        Load all Markdown documents from the knowledge base.
        """

        documents = []

        for file_path in sorted(
            self.knowledge_directory.glob("*.md")
        ):
            documents.append(
                {
                    "source": file_path.name,
                    "content": file_path.read_text(
                        encoding="utf-8"
                    ),
                }
            )

        return documents