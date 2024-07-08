from sklearn.metrics import root_mean_squared_error

from erklartextgen.evaluation.stylistic.gpt4 import GPT4StyleEvaluator


def load_dependencies(config):
    return {
        "gpt4_evaluator": GPT4StyleEvaluator(config["evaluation"]["openai_api_key"])
    }


def compute_loss(scores):
    """
    Returns loss values for the stylistic category

    Target: 5/5, for every feature
    """
    all_scores = list(scores["gpt4"].values())
    return root_mean_squared_error([5.0] * len(all_scores), all_scores)


def compute_scores(text, deps):
    return {"gpt4": deps["gpt4_evaluator"].evaluate(text)}
