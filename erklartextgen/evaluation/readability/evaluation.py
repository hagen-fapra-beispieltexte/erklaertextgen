from sklearn.metrics import root_mean_squared_error

from erklartextgen.evaluation.readability import metrics


def compute_loss(scores):
    """
    Returns loss values for the readability category

    Targets (approx. fifth grade):
    - Flesch-Kincaid: 5
    - ARI: 6
    - SMOG: 5
    - Coleman-Liau: 5

    The Flesch score is dropped to provide an interpretable overall RSME loss.
    """
    transformed_scores = []
    for key in ["flesch_kincaid", "coleman_liau", "gunning_fog", "smog_index"]:
        transformed_scores.append(scores[key])
    transformed_scores.append(scores["ari"] - 1.0)

    return root_mean_squared_error([5.0] * len(transformed_scores), transformed_scores)


def compute_scores(doc):
    return {
        "flesch": metrics.compute_flesch_reading_ease(doc),
        "flesch_kincaid": metrics.compute_flesch_kincaid_level(doc),
        "smog_index": metrics.compute_smog_index(doc),
        "gunning_fog": metrics.compute_gunning_fog_index(doc),
        "ari": metrics.compute_ari(doc),
        "coleman_liau": metrics.compute_coleman_liau(doc),
    }
