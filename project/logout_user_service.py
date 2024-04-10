from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class LogoutUserResponse(BaseModel):
    """
    Response model for the logout_user endpoint, indicating whether the logout was successful or not.
    """

    success: bool
    message: Optional[str] = None


async def logout_user(jwt_token: str) -> LogoutUserResponse:
    """
    Invalidates the user's current session token or JWT by clearing the accessToken and refreshToken fields in the database.

    Args:
        jwt_token (str): The JWT token used for session management, to be invalidated on logout.

    Returns:
        LogoutUserResponse: Response model for the logout_user endpoint, indicating whether the logout was successful or not.
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"accessToken": jwt_token}
    )
    if user is None:
        return LogoutUserResponse(
            success=False, message="No active session found for the given token."
        )
    await prisma.models.User.prisma().update(
        data={"accessToken": None, "refreshToken": None}, where={"id": user.id}
    )
    return LogoutUserResponse(success=True, message="Logout successful.")
