import os
import json
from models.gemini_flash_client import GeminiFlashClient
from optimizer.scorer import Scorer

class RunEval:
    """
    Run prompt-based chatbot and evaluate responses using Gemini Flash and Gemini Pro.
    """
    def __init__(self, prompt, test_examples, api_key=None):
        self.prompt = prompt
        self.test_examples = test_examples  # List of dicts: {input: ..., target: ...}
        self.flash_client = GeminiFlashClient(api_key=api_key)
        self.scorer = Scorer(api_key=api_key)

    def run(self):
        results = []
        for ex in self.test_examples:
            user_input = ex["input"]
            target = ex.get("target")
            full_prompt = f"{self.prompt}\nUser: {user_input}"
            response = self.flash_client.generate(full_prompt)
            score = self.scorer.score(self.prompt, response=response)
            results.append({
                "input": user_input,
                "target": target,
                "response": response,
                "score": score
            })
            print(f"Input: {user_input}\nResponse: {response}\nScore: {score}\n---")
        return results

if __name__ == "__main__":
    # Example usage: load prompt and test examples from files or define inline
    prompt = "Translate English to French."
    test_examples = [
        {"input": "Hello!", "target": "Bonjour!"},
        {"input": "How are you?", "target": "Comment ça va?"}
    ]
    api_key = os.getenv("GEMINI_API_KEY")
    runner = RunEval(prompt, test_examples, api_key=api_key)
    results = runner.run()
    # Optionally save results
    with open("results/eval_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
