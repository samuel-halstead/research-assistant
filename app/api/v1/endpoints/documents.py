from fastapi import APIRouter, Depends, Request, status

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
    request: Request,
    manager: DocumentsManager = Depends(ManagerFactory.for_documents),
) -> DocumentsResponse:
    """
    Get the documents from the database.

    Args:
        manager(DocumentsManager): The manager (domain) with the business logic.

    Returns:
        (json): Documents
    """

    return manager.get_documents(request)


@router.get(
    "/{document_id}",
    response_model=Document,
    status_code=status.HTTP_200_OK,
)
async def get_document_by_uuid(
    document_uuid: str,
    request: Request,
    manager: DocumentsManager = Depends(ManagerFactory.for_documents),
) -> Document:
    """
    Get the document from the database by id.

    Args:
        document_uuid(str): The uuid of the document.
        manager(DocumentsManager): The manager (domain) with the business logic.

    Returns:
        (json): Document
    """
    return manager.get_document_by_uuid(document_uuid, request)


@router.post(
    "",
    response_model=Document,
    status_code=status.HTTP_200_OK,
)
async def create_document(
    payload: Document,
    request: Request,
    manager: DocumentsManager = Depends(ManagerFactory.for_documents),
) -> Document:
    """
    Create a new document.

    Args:
        payload(Document): The document to create.
        manager(DocumentsManager): The manager (domain) with the business logic.

    Returns:
        (json): Document
    """
    return manager.create_document(payload, request)


@router.delete(
    "/{document_id}",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_document(
    document_uuid: str,
    request: Request,
    manager: DocumentsManager = Depends(ManagerFactory.for_documents),
) -> None:
    """
    Delete a document.

    Args:
        document_uuid(str): The uuid of the document.
        manager(DocumentsManager): The manager (domain) with the business logic.

    Returns:
        (json): None
    """
    return manager.delete_document(document_uuid, request)
