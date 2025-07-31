import os
import requests

class GeminiFlashClient:
    """
    Gemini 2.0 & 2.5 Flash API wrapper for prompt execution.
    """
    def __init__(self, api_key=None, model_version="gemini-2.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_version = model_version
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set in environment or passed to constructor.")

    def generate(self, prompt, **kwargs):
        url = f"{self.base_url}/{self.model_version}:generateContent"
        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        data = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}]
        }
        data.update(kwargs)
        response = requests.post(url, headers=headers, params=params, json=data)
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]

# Example usage:
# client = GeminiFlashClient(model_version="gemini-2.0-flash")
# result = client.generate("What is the capital of France?")
# print(result)