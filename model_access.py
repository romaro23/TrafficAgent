from google import genai

def send_request_to_model(prompt: str, api_key: str) -> str:
    if not api_key:
        raise ValueError("No API key provided")

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(model='gemini-3.1-flash-lite')

    try:
        response = chat.send_message(prompt).text

        if response:
            return response
        else:
            return "I cannot process this prompt"

    except Exception as e:
        print(f"Error in reaching out to model: {e}")
        return "Error in reaching out to model"

