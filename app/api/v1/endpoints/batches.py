from fastapi import APIRouter, Depends
from typing import Any
from app.services.batch_service import BatchService

router = APIRouter()

@router.post("/")
async def create_batch(
    *,
    batch_in: dict,
    # current_user: dict = Depends(get_current_user_stub) # From shared lib
) -> Any:
    """
    Create new batch.
    """
    service = BatchService()
    return await service.create_new_batch("user_id", "school_id", batch_in)
