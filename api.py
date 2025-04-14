from ollama import Client

OLLAMA_HOST = "<YOUR_OLLAMA_SERVER_HERE>"  # e.g., "http://localhost:11434"

client = Client(host=OLLAMA_HOST)


def get_ollama_models():
    models_info = client.list()

    models = [model.model for model in models_info.models]
    return models


# Example usage
ollama_models = get_ollama_models()
SUPPORTED_MODELS = ollama_models


def chat_with_model(model_name, messages, options=None):
    """
    Generic wrapper for chatting with an Ollama model.

    Args:
        model_name (str): One of the supported models.
        messages (list): List of dicts, each with "role" and "content" keys.
                         Example: [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
        options (dict, optional): Inference options such as:
            - temperature (float): Sampling temperature (e.g., 0.7)
            - top_p (float): Nucleus sampling parameter (e.g., 0.9)
            - presence_penalty, frequency_penalty, stop, mirostat, etc.
            Full list here: https://github.com/ollama/ollama/blob/main/docs/api.md#generate-request-with-options

    Returns:
        dict: Full response object with the following keys:

            {
                'model': str,                # Model used (e.g., "phi4-mini")
                'created_at': str,           # ISO timestamp
                'done': bool,                # Whether generation is complete
                'done_reason': str,          # e.g. "stop"
                'total_duration': int,       # Total response time in nanoseconds
                'load_duration': int,        # Time to load the model (ns)
                'prompt_eval_count': int,    # Number of prompt tokens
                'prompt_eval_duration': int, # Time taken to evaluate prompt
                'eval_count': int,           # Number of tokens generated
                'eval_duration': int,        # Time spent generating tokens
                'message': {
                    'role': str,             # "assistant"
                    'content': str           # Model response content (what you care about)
                }
            }

    Example usage:
        content = chat_with_model("phi4", messages)["message"]["content"]
    """

    if model_name not in SUPPORTED_MODELS:
        raise ValueError(
            f"Model '{model_name}' is not supported. Choose from: {SUPPORTED_MODELS}")

    response = client.chat(
        model=model_name,
        messages=messages,
        options=options or {}
    )

    return response
