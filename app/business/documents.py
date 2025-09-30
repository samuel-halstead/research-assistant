from fastapi import Request

from app.schemas.documents import Document, DocumentsResponse


class DocumentsManager:

    """
    A manager to handle the business logic related with research.
    """

    @staticmethod
    def get_documents(request: Request) -> DocumentsResponse:
        """
        Get the documents from the database.

        Returns:
            A valid DocumentsResponse instance with all the documents.
        """
        vector_store_manager = request.app.state.vector_store_manager
        documents = vector_store_manager.get_documents()

        return DocumentsResponse(
            documents=documents,
        )

    @staticmethod
    def get_document_by_uuid(document_uuid: str, request: Request) -> Document:
        """
        Get the document from the database by id.

        Returns:
            A valid Document instance with the document.
        """

        vector_store_manager = request.app.state.vector_store_manager
        document = vector_store_manager.get_document_by_uuid(document_uuid)

        return document

    @staticmethod
    def create_document(document: Document, request: Request) -> Document:
        """
        Create a new document.

        Returns:
            A valid Document instance with the created document.
        """
        vector_store_manager = request.app.state.vector_store_manager
        vector_store_manager.add_documents([document])

        return document

    @staticmethod
    def delete_document(document_uuid: str, request: Request) -> None:
        """
        Delete a document.

        Returns:
            None
        """
        vector_store_manager = request.app.state.vector_store_manager
        vector_store_manager.delete_documents([document_uuid])

        return None
