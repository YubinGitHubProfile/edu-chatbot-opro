import os
import requests

class GeminiProClient:
    """
    Gemini 2.5 Pro API wrapper for evaluation/reward modeling.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_version = "gemini-2.5-pro"
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set in environment or passed to constructor.")

    def evaluate(self, prompt, **kwargs):
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
# client = GeminiProClient()
# score = client.evaluate("Evaluate the helpfulness of this response: ...")
# print(score)
