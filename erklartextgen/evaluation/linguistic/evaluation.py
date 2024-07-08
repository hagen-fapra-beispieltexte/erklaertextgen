from sklearn.metrics import root_mean_squared_error

from erklartextgen.evaluation.linguistic import indicators
from erklartextgen.evaluation.linguistic import forms


def compute_scores(doc):
    return {
        "indicators_structural_complexity": indicators.compute_structural_complexity_indicators(
            doc
        ),
        "indicators_ambiguity": indicators.compute_ambiguity_indicators(doc),
        "advanced_ratio": forms.compute_ratio(doc),
    }


def compute_loss(scores):
    """
    Returns loss values for the linguistic category

    Target: 0.0, for every feature
    """
    structural_complexity_scores = list(
        scores["indicators_structural_complexity"].values()
    )
    ambiguity_scores = list(scores["indicators_structural_complexity"].values())
    advanced_ratio_scores = [scores["advanced_ratio"]]

    combined_scores = (
        structural_complexity_scores + ambiguity_scores + advanced_ratio_scores
    )
    return root_mean_squared_error([0.0] * len(combined_scores), combined_scores)
