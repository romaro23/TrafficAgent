from google import genai
import logging

logger = logging.getLogger(__name__)

async def send_request_to_model(prompt: str, api_key: str) -> str | None:
    if not api_key:
        raise ValueError("No API key provided")

    client = genai.Client(api_key=api_key)
    chat = client.aio.chats.create(model='gemini-3.1-flash-lite')

    try:
        response = await chat.send_message(prompt)

        if response and response.text:
            return response.text
        else:
            logger.warning("Model returned an empty response.")
            return "I cannot process this prompt"

    except Exception as e:
        logger.error(f"Error in reaching out to model: {e}")
        return "Error in reaching out to model"

