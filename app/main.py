from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.core.config import settings
from app.core.logging import init_logging, get_logger
from app.api.v1.api import api_router
from app.core.exceptions import logic_exception
from app.core.exception_handlers import validation_exception_handler, logic_exception_handler

# Initialize logging before app creation
init_logging()
logger = get_logger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)


app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(logic_exception, logic_exception_handler)
logger.info(f"Application starting up")
app.include_router(api_router, prefix=settings.API_V1_STR)

logger.info(f"Application started")