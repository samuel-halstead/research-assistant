from app.schemas.documents import Document, DocumentsResponse


class DocumentsManager:

    """
    A manager to handle the business logic related with research.
    """

    @staticmethod
    def get_documents() -> DocumentsResponse:
        """
        Get the documents from the database.

        Returns:
            A valid DocumentsResponse instance with all the documents.
        """
        return DocumentsResponse(
            documents=[],
        )

    @staticmethod
    def get_document_by_id(document_id: int) -> Document:
        """
        Get the document from the database by id.

        Args:
            document_id(int): The id of the document.

        Returns:
            A valid Document instance with the document.
        """

        return Document(
            id=document_id,
            title="",
            abstract="",
            authors=[],
        )

    @staticmethod
    def create_document(document: Document) -> Document:
        """
        Create a new document.

        Args:
            document(Document): The document to create.

        Returns:
            A valid Document instance with the created document.
        """
        return Document(
            id=document.id,
            title=document.title,
            abstract=document.abstract,
            authors=document.authors,
        )

    @staticmethod
    def delete_document(document_id: int) -> None:
        """
        Delete a document.

        Args:
            document_id(int): The id of the document.

        Returns:
            None
        """
        return None
