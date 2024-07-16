from scipy.stats import wasserstein_distance
from sklearn.metrics import root_mean_squared_error

from erklartextgen.evaluation.cefr import cefr_j, efllex, bert_efcamdat

BERT_EFCAMDAT_MODEL_PATH = "assets/efcamdat_model_20240620_204416_2"
EFLLEX_DATASET_PATH = "assets/EFLLex_NLP4J.tsv"
CEFRJ_DATASET_PATH = "assets/cefrj-vocabulary-profile-1.5.csv"


def load_dependencies():
    return {
        "bert_efcamdat": bert_efcamdat.load(BERT_EFCAMDAT_MODEL_PATH),
        "cefrj_wordlist": cefr_j.load_wordlist(CEFRJ_DATASET_PATH),
        "efllex_dataset": efllex.load_dataset(EFLLEX_DATASET_PATH),
    }


def compute_loss(scores):
    """
    Returns loss values for the CEFR category

    Targets:
    - CEFR-J: 2.0 (corresponding to A2.1)
    - EFLLEX: [0.0, 1.0, 0.0, 0.0, 0.0] (corresponding to all words being "in A2")
              computes the Wasserstein distance between both distributions
    - DistilBert EFCAMDAT classifier: 2 (corresponding to A2)
    """
    efllex_levels = ["a1", "a2", "b1", "b2", "c1"]
    efllex_scores = [scores["efllex"][level] for level in efllex_levels]
    efflex_target = [0.0, 1.0, 0.0, 0.0, 0.0]

    return {
        "efllex": wasserstein_distance(efllex_scores, efflex_target),
        "cefr_j": root_mean_squared_error([2.0], [scores["cefr_j"]]),
        "bert_efcamdat": root_mean_squared_error([2.0], [scores["bert_efcamdat"]]),
    }


def compute_scores(doc, text, deps):
    return {
        "cefr_j": cefr_j.predict(doc, deps),
        "efllex": efllex.analyze_first_observation(doc, deps),
        "bert_efcamdat": bert_efcamdat.classify(text, deps["bert_efcamdat"]),
    }
