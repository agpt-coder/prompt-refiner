from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class InvalidateAPIKeyResponse(BaseModel):
    """
    Provides feedback on the outcome of the invalidate API key request.
    """

    success: bool
    message: str


async def invalidate_api_key(api_key: str) -> InvalidateAPIKeyResponse:
    """
    Invalidates an existing API key.

    This function attempts to find an API key in the database and invalidate it by setting its validUntil attribute
    to the current datetime. If the key is already invalidated or does not exist, it informs the caller accordingly.

    Args:
        api_key (str): The API key that needs to be invalidated.

    Returns:
        InvalidateAPIKeyResponse: Object with success status and a message describing the result.

    Example:
        await invalidate_api_key("some_api_key_string")
        > InvalidateAPIKeyResponse(success=True, message="API key has been successfully invalidated.")
    """
    api_key_record = await prisma.models.APIKey.prisma().find_unique(
        where={"key": api_key}
    )
    if api_key_record and api_key_record.validUntil > datetime.now():
        await prisma.models.APIKey.prisma().update(
            where={"key": api_key}, data={"validUntil": datetime.now()}
        )
        response = InvalidateAPIKeyResponse(
            success=True, message="API key has been successfully invalidated."
        )
    else:
        response = InvalidateAPIKeyResponse(
            success=False,
            message="API key does not exist or has already been invalidated.",
        )
    return response
