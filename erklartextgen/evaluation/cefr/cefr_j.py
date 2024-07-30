"""
Computes the CEFR-J level of a given text

Bibliography key: uchida2018assigning
"""

import csv

from erklartextgen.evaluation.readability.metrics import compute_ari

CEFRJ_DIFFICULTY_MAPPING = {"A1": 1, "A2": 2, "B1": 3, "B2": 4}

# Thresholds for mapping scores to CEFR-J levels
CEFRJ_LEVEL_CRITERIA = {
    0.50: "pre-A1",
    0.84: "A1.1",
    1.17: "A1.2",
    1.50: "A1.3",
    2.00: "A2.1",
    2.50: "A2.2",
    3.00: "B1.1",
    3.50: "B1.2",
    4.00: "B2.1",
    4.50: "B2.2",
    5.00: "C1",
    6.00: "C2",
}

# Slopes and y-intercepts of the linear regression models per feature
READING_LM_COEFFS = {
    "ari": (0.4298, -1.27085),
    "vpersent": (2.1075, -2.01),
    "avrdiff": (7.2961, -8.4442),
    "bpera": (16.3043, -0.1087),
}


def load_wordlist(load_path):
    cefr_dictionary = {}

    with open(load_path, mode="r", encoding="utf-8") as csvfile:
        csv_reader = csv.DictReader(csvfile)

        for row in csv_reader:
            cefr_dictionary[row["headword"]] = row["CEFR"]

    return cefr_dictionary


def compute_vpersent(doc):
    """
    Computes the sentence feature VperSent
    """

    total_verbs = 0
    total_sentences = 0

    for sentence in doc.sents:
        total_sentences += 1
        total_verbs += sum(token.pos_ == "VERB" for token in sentence)

    return total_verbs / total_sentences if total_sentences > 0 else 0


def compute_avrdiff(doc, wordlist, cefr_levels):
    """
    Computes vocabulary feature AvrDiff
    """

    difficulty_sum = 0
    content_words = 0

    for token in doc:
        if token.is_alpha and token.text.lower() in wordlist:
            difficulty_sum += cefr_levels[wordlist[token.text.lower()]]
            content_words += 1

    return difficulty_sum / content_words if content_words > 0 else 0


def compute_bpera(doc, wordlist):
    """
    Computes vocabulary feature BperA
    """

    a_level_words = 0
    b_level_words = 0

    for token in doc:
        if token.is_alpha and token.text.lower() in wordlist:
            if wordlist[token.text.lower()] in ["A1", "A2"]:
                a_level_words += 1
            elif wordlist[token.text.lower()] in ["B1", "B2"]:
                b_level_words += 1

    return b_level_words / a_level_words if a_level_words > 0 else 0


def predict(doc, deps):
    wordlist = deps["cefrj_wordlist"]

    raw_features = {
        "ari": compute_ari(doc),
        "vpersent": compute_vpersent(doc),
        "avrdiff": compute_avrdiff(doc, wordlist, CEFRJ_DIFFICULTY_MAPPING),
        "bpera": compute_bpera(doc, wordlist),
    }

    predicted_scores = {
        k: READING_LM_COEFFS[k][0] * v + READING_LM_COEFFS[k][1]
        for k, v in raw_features.items()
    }
    average_score = sum(predicted_scores.values()) / len(predicted_scores)

    return average_score
