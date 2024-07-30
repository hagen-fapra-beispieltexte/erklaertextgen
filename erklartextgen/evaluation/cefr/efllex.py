"""
Computes the CEFR level using the EFLLex dataset

This implementation uses the same metholodogy as implemented
on https://cental.uclouvain.be/cefrlex/efllex/analyse/.

Bibliography key: durlich2018efllex
"""

import csv
from collections import Counter

# Below you can find all NLP4J POS tags that appear in the EFLLex lexicon:
# {
#     'NN': 9243, 'JJ': 2630, 'VB': 2230, 'RB': 754, 'CD': 121, 'IN': 85, 'UH': 64,
#     'PRP': 29, 'DT': 20, 'RP': 17, 'MD': 14, 'CC': 13, 'PR': 13, 'PRP$': 9, 'WP': 8,
#     'WRB': 8, 'PDT': 6, 'WDT': 5, 'TO': 4, 'EX': 3, 'RH': 1, ' NN': 1, 'XX': 1, 'FW': 1, 'WP$': 1
# }

LEVELS = ["a1", "a2", "b1", "b2", "c1"]

POS_NLP4J_MAP = {
    "ADJ": "JJ",
    "ADP": "IN",
    "ADV": "RB",
    "CCONJ": "CC",
    "DET": "DT",
    "INTJ": "UH",  # hah!
    "NOUN": "NN",
    "PART": "RP",
    "PRON": "PRP",
    "PROPN": "NNP",
    "PUNCT": ".",
    "SCONJ": "IN",
    "SYM": "SYM",
    "VERB": "VB",
    "X": "XX",
}


def load_dataset(load_path):
    dataset = {}
    with open(load_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter="\t")
        for row in reader:
            dataset[(row["word"], row["tag"])] = {
                level: float(row[f"level_freq@{level}"]) for level in LEVELS
            }

    return dataset


def analyze_first_observation(doc, deps):
    efllex = deps["efllex_dataset"]

    first_observations = []
    for token in doc:
        word_freqs = efllex.get((token.lemma_, POS_NLP4J_MAP.get(token.pos_)))

        if word_freqs:
            first_observations.append(
                next(level for level in LEVELS if word_freqs.get(level, 0.0) != 0.0)
            )

    token_count = len(doc)
    first_observation_counts = Counter(first_observations)
    return {
        level: first_observation_counts.get(level, 0) / token_count for level in LEVELS
    }
