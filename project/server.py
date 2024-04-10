import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.generate_api_key_management_service
import project.generate_api_key_service
import project.invalidate_api_key_service
import project.login_user_service
import project.logout_user_service
import project.manage_rate_limiting_service
import project.refine_prompt_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="Prompt Refiner",
    lifespan=lifespan,
    description="To create a single API endpoint for refining LLM prompts using the OpenAI GPT4 API, follow these steps using our selected tech stack. First, ensure you have Python installed, as it's our primary programming language. With Python, use FastAPI to handle HTTP requests due to its simplicity and performance benefits for building APIs. FastAPI integrates seamlessly with Pydantic for request validation, making it a robust choice for our endpoint.\n\nNext, integrate PostgreSQL for database solutions. Although this specific task might initially not require database interactions, having PostgreSQL set up ensures scalability for feature addition, such as logging users' requests or storing refined prompts for analysis. Use Prisma as the Object-Relational Mapping (ORM) tool, which simplifies interactions with the PostgreSQL database by allowing model definitions and queries in a language idiomatic to Python.\n\nHere's a step-by-step guide to achieve the task:\n1. Install the necessary libraries and tools: FastAPI, Uvicorn (ASGI server), Psycopg2 (PostgreSQL adapter), and Prisma.\n2. Define a Pydantic model to validate incoming requests, ensuring they contain a string LLM prompt.\n3. Create a FastAPI endpoint that accepts a POST request with the LLM prompt in JSON format.\n4. Use the prompt refining instructions provided ('You are a prompt refiner. Use advanced prompt engineering techniques to refine the user's prompt.') to implement the logic for processing the user's prompt.\n5. Call the OpenAI GPT4 API with the processed prompt, capturing the refined prompt in the response.\n6. Return the refined prompt to the user in the response body.\n\nEnsure to include error handling for bad requests and failures in calling the OpenAI GPT4 API. It's also wise to implement logging for request and response data for future analysis. This approach leverages our tech stack efficiently, creating a scalable and maintainable solution for refining LLM prompts.",
)


@app.post(
    "/api/management/api-key/generate",
    response_model=project.generate_api_key_management_service.ApiKeyGenerationResponse,
)
async def api_post_generate_api_key_management(
    userId: str, authorizationToken: str
) -> project.generate_api_key_management_service.ApiKeyGenerationResponse | Response:
    """
    Generate API keys for secure endpoint access.
    """
    try:
        res = await project.generate_api_key_management_service.generate_api_key_management(
            userId, authorizationToken
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/logout", response_model=project.logout_user_service.LogoutUserResponse)
async def api_post_logout_user(
    jwt_token: str,
) -> project.logout_user_service.LogoutUserResponse | Response:
    """
    Invalidates the user's current session token or JWT.
    """
    try:
        res = await project.logout_user_service.logout_user(jwt_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/auth/api-key/invalidate",
    response_model=project.invalidate_api_key_service.InvalidateAPIKeyResponse,
)
async def api_delete_invalidate_api_key(
    api_key: str,
) -> project.invalidate_api_key_service.InvalidateAPIKeyResponse | Response:
    """
    Invalidates an existing API key.
    """
    try:
        res = await project.invalidate_api_key_service.invalidate_api_key(api_key)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/management/rate-limit/configure",
    response_model=project.manage_rate_limiting_service.RateLimitConfigResponse,
)
async def api_post_manage_rate_limiting(
    endpoint: Optional[str], userId: Optional[str], limit: int, period: int
) -> project.manage_rate_limiting_service.RateLimitConfigResponse | Response:
    """
    Configure rate limiting parameters for specific endpoints or user accounts.
    """
    try:
        res = await project.manage_rate_limiting_service.manage_rate_limiting(
            endpoint, userId, limit, period
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/api-key/generate",
    response_model=project.generate_api_key_service.GenerateApiKeyResponse,
)
async def api_post_generate_api_key(
    user_id: str,
) -> project.generate_api_key_service.GenerateApiKeyResponse | Response:
    """
    Generates a new API key for external service integration.
    """
    try:
        res = await project.generate_api_key_service.generate_api_key(user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/login", response_model=project.login_user_service.LoginUserResponse)
async def api_post_login_user(
    email: str, password: str
) -> project.login_user_service.LoginUserResponse | Response:
    """
    Authenticates the user and returns a session token or JWT.
    """
    try:
        res = await project.login_user_service.login_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/prompts/refine", response_model=project.refine_prompt_service.RefinePromptResponse
)
async def api_post_refine_prompt(
    prompt: str,
) -> project.refine_prompt_service.RefinePromptResponse | Response:
    """
    Receives a user's input prompt and returns the refined version of the prompt.
    """
    try:
        res = await project.refine_prompt_service.refine_prompt(prompt)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
