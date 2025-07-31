import numpy as np

class Metrics:
    """
    Provides standard metrics for evaluating chatbot responses.
    """
    @staticmethod
    def accuracy(predictions, targets):
        """Compute exact match accuracy."""
        correct = sum([p.strip() == t.strip() for p, t in zip(predictions, targets)])
        return correct / len(predictions) if predictions else 0.0

    @staticmethod
    def average_score(scores):
        """Compute the average of numeric scores."""
        return float(np.mean(scores)) if scores else 0.0

    @staticmethod
    def helpfulness_score(scores):
        """Alias for average_score, for clarity."""
        return Metrics.average_score(scores)

    @staticmethod
    def coherence_score(scores):
        """Alias for average_score, for clarity."""
        return Metrics.average_score(scores)

    @staticmethod
    def custom_metric(func, *args, **kwargs):
        """Allow user to pass a custom metric function."""
        return func(*args, **kwargs)

# Example usage:
# preds = ["Bonjour!", "Salut!"]
# targets = ["Bonjour!", "Salut!"]
# print("Accuracy:", Metrics.accuracy(preds, targets))
# print("Average score:", Metrics.average_score([8.5, 9.0, 7.5]))
