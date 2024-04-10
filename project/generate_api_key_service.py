import secrets
from datetime import datetime, timedelta

import prisma
import prisma.models
from pydantic import BaseModel


class GenerateApiKeyResponse(BaseModel):
    """
    The response model for generating a new API key, including the key itself and related metadata such as creation date and validity period.
    """

    api_key: str
    valid_until: datetime
    issued_at: datetime


async def generate_api_key(user_id: str) -> GenerateApiKeyResponse:
    """
    Generates a new API key for external service integration.

    This function generates an API key, stores it in the database associated with the user,
    and returns the key along with its validity metadata.

    Args:
        user_id (str): The ID of the user requesting a new API key.

    Returns:
        GenerateApiKeyResponse: The response model for generating a new API key, including the key itself
                                and related metadata such as creation date and validity period.
    """
    new_api_key = secrets.token_urlsafe(32)
    validity_period = timedelta(days=365)
    valid_until = datetime.utcnow() + validity_period
    await prisma.models.APIKey.prisma().create(
        data={"key": new_api_key, "validUntil": valid_until, "userId": user_id}
    )
    response = GenerateApiKeyResponse(
        api_key=new_api_key, valid_until=valid_until, issued_at=datetime.utcnow()
    )
    return response
