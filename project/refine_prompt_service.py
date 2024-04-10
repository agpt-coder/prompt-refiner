import httpx
from pydantic import BaseModel


class RefinePromptResponse(BaseModel):
    """
    This model represents the structured response returned after the refinement process. It contains the original prompt and the refined prompt.
    """

    original_prompt: str
    refined_prompt: str


async def refine_prompt(prompt: str) -> RefinePromptResponse:
    """
    Receives a user's input prompt and returns the refined version of the prompt.

    This function acts as an interface with the OpenAI GPT-4 API to refine the
    original prompt given by the user by applying advanced prompt engineering
    techniques. It then returns both the original and refined prompts as part of
    a structured response.

    Args:
        prompt (str): The LLM prompt submitted by the user for refinement.

    Returns:
        RefinePromptResponse: This model represents the structured response returned
        after the refinement process. It contains the original prompt and the
        refined prompt.

    Raises:
        ValueError: If the OpenAI API returns an empty response or an error occurs.
    """
    openai_api_key = "your_openai_api_key_here"
    refining_instructions = (
        "You are a prompt refiner. Use advanced prompt engineering techniques to refine the user's prompt:\n"
        + prompt
    )
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": "text-davinci-003",
        "prompt": refining_instructions,
        "temperature": 0.5,
        "max_tokens": 100,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/completions", json=body, headers=headers
        )
    if response.status_code == 200:
        result = response.json()
        refined_text = (
            result["choices"][0]["text"].strip() if result.get("choices") else ""
        )
        if not refined_text:
            raise ValueError(
                "The OpenAI API returned an empty response for the refinement process."
            )
        return RefinePromptResponse(original_prompt=prompt, refined_prompt=refined_text)
    else:
        raise ValueError(
            f"Failed to refine prompt. OpenAI API status code: {response.status_code}, response: {response.text}"
        )
