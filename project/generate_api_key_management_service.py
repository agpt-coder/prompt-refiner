from datetime import datetime, timedelta

import prisma
import prisma.models
from pydantic import BaseModel


class ApiKeyGenerationResponse(BaseModel):
    """
    The response model for the API key generation request. It provides the generated API key and associated details like the valid until date.
    """

    apiKey: str
    validUntil: datetime
    message: str


async def generate_api_key_management(
    userId: str, authorizationToken: str
) -> ApiKeyGenerationResponse:
    """
    Generate API keys for secure endpoint access.

    Args:
    userId (str): The unique identifier of the user requesting the API key.
    authorizationToken (str): The authorization token to validate the requestor's permission to generate an API key.

    Returns:
    ApiKeyGenerationResponse: The response model for the API key generation request. It provides the generated API key and associated details like the valid until date.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if user is None:
        return ApiKeyGenerationResponse(
            apiKey="", validUntil=datetime.now(), message="User not found."
        )
    if user.accessToken != authorizationToken:
        return ApiKeyGenerationResponse(
            apiKey="", validUntil=datetime.now(), message="Invalid authorization token."
        )
    new_api_key = "SOME_GENERATED_API_KEY"
    valid_until_date = datetime.now() + timedelta(days=30)
    await prisma.models.APIKey.prisma().create(
        data={"key": new_api_key, "validUntil": valid_until_date, "userId": userId}
    )
    return ApiKeyGenerationResponse(
        apiKey=new_api_key,
        validUntil=valid_until_date,
        message="API key generated successfully.",
    )
