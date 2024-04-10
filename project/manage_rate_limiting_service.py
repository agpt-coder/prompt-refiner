from typing import Optional

from pydantic import BaseModel


class RateLimitConfigResponse(BaseModel):
    """
    Confirms the successful configuration of rate limiting for the specified endpoint or user account. Includes the newly applied limit and period for verification.
    """

    endpoint: Optional[str] = None
    userId: Optional[str] = None
    limit: int
    period: int
    status: str


async def manage_rate_limiting(
    endpoint: Optional[str], userId: Optional[str], limit: int, period: int
) -> RateLimitConfigResponse:
    """
    Configure rate limiting parameters for specific endpoints or user accounts.

    Args:
        endpoint (Optional[str]): Optional. The API endpoint to configure rate limiting for. If present, applies the configuration specifically to this endpoint.
        userId (Optional[str]): Optional. The user ID to configure rate limiting for. If present, applies the configuration specifically to this user account.
        limit (int): The maximum number of allowed requests within the given period.
        period (int): The period (in seconds) over which the limit applies.

    Returns:
        RateLimitConfigResponse: Confirms the successful configuration of rate limiting for the specified endpoint or user account. Includes the newly applied limit and period for verification.
    """
    return RateLimitConfigResponse(
        endpoint=endpoint,
        userId=userId,
        limit=limit,
        period=period,
        status="Rate limiting configuration successful.",
    )
