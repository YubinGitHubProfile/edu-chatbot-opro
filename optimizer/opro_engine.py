import os
from models.gemini_flash_client import GeminiFlashClient
from models.gemini_pro_client import GeminiProClient
import time

class OproEngine:
    """
    Core OPro optimization pipeline using Gemini Flash for prompt optimization
    and Gemini Pro for evaluation.
    """
    def __init__(self, base_prompt, task_examples, num_iterations=3, candidates_per_iter=4, api_key=None, model_version='gemini-2.5-flash'):
        self.base_prompt = base_prompt
        self.task_examples = task_examples
        self.num_iterations = num_iterations
        self.candidates_per_iter = candidates_per_iter
        self.model_version = model_version
        self.flash_client = GeminiFlashClient(api_key=api_key, model_version=model_version)
        self.pro_client = GeminiProClient(api_key=api_key)

    def generate_candidates(self, prompt):
        """Generate prompt variants using Gemini Flash."""
        candidates = []
        for _ in range(self.candidates_per_iter):
            instruction = (
                "Rewrite the following prompt to make it more effective for the task. "
                "Only return the improved prompt, not any explanation or commentary.\n"
                f"Prompt: {prompt}"
            )
            variant = self.flash_client.generate(instruction)
            candidates.append(variant)
        return candidates

    def score_candidate(self, prompt):
        """Score a prompt using Gemini Pro as evaluator."""
        eval_prompt = f"Evaluate the following prompt for clarity, helpfulness, and task suitability. Give a score from 1 to 10.\nPrompt: {prompt}"
        score_text = self.pro_client.evaluate(eval_prompt)
        # Try to extract a numeric score from the response
        try:
            score = float([s for s in score_text.split() if s.replace('.', '', 1).isdigit()][0])
        except Exception:
            score = 0.0
        return score

    def optimize(self, return_all_scores=False):
        current_prompts = [self.base_prompt]
        for i in range(self.num_iterations):
            print(f"Iteration {i+1}/{self.num_iterations}")
            candidates = []
            for prompt in current_prompts:
                candidates.extend(self.generate_candidates(prompt))
                # time.sleep(1)  # avoid rate limits
            scored = [(p, self.score_candidate(p)) for p in candidates]
            scored.sort(key=lambda x: x[1], reverse=True)
            current_prompts = [p for p, _ in scored[:self.candidates_per_iter]]
            print(f"Top prompt(s) this round: {current_prompts[0][:80]}... Score: {scored[0][1]}")
            if return_all_scores:
                yield (current_prompts[0], scored)
        if return_all_scores:
            return
        return current_prompts[0]

# Example usage:
# base_prompt = "Translate English to French."
# task_examples = [ ... ]
# engine = OproEngine(base_prompt, task_examples)
# best_prompt = engine.optimize()
# print("Best prompt:", best_prompt)
