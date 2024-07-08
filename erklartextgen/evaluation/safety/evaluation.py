from sklearn.metrics import root_mean_squared_error

from erklartextgen.evaluation.safety import detoxify


def load_dependencies():
    return {"detoxify_model": detoxify.load_model()}


def compute_loss(scores):
    """
    Returns loss values for the safety category

    Target: 0.0 for every feature
    """
    safety_scores = list(scores["detoxify"].values())
    return root_mean_squared_error([0.0] * len(safety_scores), safety_scores)


def compute_scores(text, deps):
    return {"detoxify": detoxify.predict(text, deps)}
