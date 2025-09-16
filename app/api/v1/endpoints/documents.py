from fastapi import APIRouter, Depends, status

from app.api.dependencies import ManagerFactory
from app.business.documents import DocumentsManager
from app.schemas.documents import Document, DocumentsResponse

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get(
    "",
    response_model=DocumentsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_documents(
    manager: DocumentsManager = Depends(ManagerFactory.for_documents),
) -> DocumentsResponse:
    """
    Get the documents from the database.

    Args:
        manager(DocumentsManager): The manager (domain) with the business logic.

    Returns:
        (json): Documents
    """

    return manager.get_documents()


@router.get(
    "/{document_id}",
    response_model=Document,
    status_code=status.HTTP_200_OK,
)
async def get_document_by_id(
    document_id: int,
    manager: DocumentsManager = Depends(ManagerFactory.for_documents),
) -> Document:
    """
    Get the document from the database by id.

    Args:
        document_id(int): The id of the document.
        manager(DocumentsManager): The manager (domain) with the business logic.

    Returns:
        (json): Document
    """
    return manager.get_document_by_id(document_id)


@router.post(
    "",
    response_model=Document,
    status_code=status.HTTP_200_OK,
)
async def create_document(
    document: Document,
    manager: DocumentsManager = Depends(ManagerFactory.for_documents),
) -> Document:
    """
    Create a new document.

    Args:
        document(Document): The document to create.
        manager(DocumentsManager): The manager (domain) with the business logic.

    Returns:
        (json): Document
    """
    return manager.create_document(document)


@router.delete(
    "/{document_id}",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_document(
    document_id: int,
    manager: DocumentsManager = Depends(ManagerFactory.for_documents),
) -> None:
    """
    Delete a document.

    Args:
        document_id(int): The id of the document.
        manager(DocumentsManager): The manager (domain) with the business logic.

    Returns:
        (json): None
    """
    return manager.delete_document(document_id)
