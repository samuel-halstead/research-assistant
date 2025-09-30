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

    Returns:
        A DocumentsResponse instance with all documents.
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

    Returns:
        A Document instance with the specified UUID.
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

    Returns:
        A Document instance with the created document.
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

    Returns:
        None
    """
    return manager.delete_document(document_uuid, request)
