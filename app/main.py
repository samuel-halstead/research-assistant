from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import documents, healthcheck, research
from app.core.config import logger, settings
from app.managers.embedding import EmbeddingManager
from app.managers.language import LanguageManager
from app.managers.vector_store import VectorStoreManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan function to load models and initialize managers on startup.
    """
    # Load models and initialize managers on startup
    logger.info("Loading models and initializing managers...")

    # Initialize language manager (loads FastText model)
    language_manager = LanguageManager()
    app.state.language_manager = language_manager

    # Initialize correlation filter manager (initializes OpenAI client)
    embedding_manager = EmbeddingManager()
    embedding_model = embedding_manager.get_embedding_model()

    # Vector store manager
    vector_store_manager = VectorStoreManager(embedding_model)
    app.state.vector_store_manager = vector_store_manager

    logger.info("Models loaded successfully!")

    yield

    # Cleanup on shutdown (if needed)
    logger.info("Shutting down...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

app.include_router(healthcheck.router, prefix=settings.API_V1_STR)
app.include_router(documents.router, prefix=settings.API_V1_STR)
app.include_router(research.router, prefix=settings.API_V1_STR)
