from models.gemini_pro_client import GeminiProClient

class Scorer:
    """
    Uses Gemini 2.5 Pro as evaluator/reward model for prompt optimization.
    """
    def __init__(self, api_key=None):
        self.pro_client = GeminiProClient(api_key=api_key)

    def score(self, prompt, response=None, criteria=None):
        """
        Score a prompt (and optionally a response) using Gemini 2.5 Pro.
        Optionally, custom criteria can be provided.
        """
        if criteria is None:
            criteria = "clarity, helpfulness, and task suitability"
        if response:
            eval_prompt = (
                f"Evaluate the following prompt and response for {criteria}. "
                f"Give a score from 1 to 10.\nPrompt: {prompt}\nResponse: {response}"
            )
        else:
            eval_prompt = (
                f"Evaluate the following prompt for {criteria}. "
                f"Give a score from 1 to 10.\nPrompt: {prompt}"
            )
        score_text = self.pro_client.evaluate(eval_prompt)
        # Try to extract a numeric score from the response
        try:
            score = float([s for s in score_text.split() if s.replace('.', '', 1).isdigit()][0])
        except Exception:
            score = 0.0
        return score

# Example usage:
# scorer = Scorer()
# score = scorer.score("Translate English to French.", response="Bonjour.")
# print("Score:", score)
