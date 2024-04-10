import bcrypt
import prisma
import prisma.models
from jose import jwt
from pydantic import BaseModel


class LoginUserResponse(BaseModel):
    """
    This model represents the response body for a successful user login, containing the session token or JWT.
    """

    token: str


async def login_user(email: str, password: str) -> LoginUserResponse:
    """
    Authenticates the user and returns a session token or JWT.

    The function first retrieves the user by email. If the user exists, it checks if the password matches the one
    stored in the database. If the authentication is successful, it generates a JWT token for the user session.

    Args:
        email (str): The email address of the user trying to log in.
        password (str): The password of the user trying to log in.

    Returns:
        LoginUserResponse: This model represents the response body for a successful user login, containing
                           the session token or JWT.

    Raises:
        Exception: If authentication fails.

    Example:
        login_user('user@example.com', 'password123')
        > LoginUserResponse(token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...')
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        secret = "your-256-bit-secret"
        algorithm = "HS256"
        subject_id = str(user.id)
        token_payload = {
            "sub": subject_id,
            "email": email,
            "iat": 1633492022,
            "exp": 1938816022,
        }
        token = jwt.encode(token_payload, secret, algorithm=algorithm)
        return LoginUserResponse(token=token)
    raise Exception("Authentication failed")
