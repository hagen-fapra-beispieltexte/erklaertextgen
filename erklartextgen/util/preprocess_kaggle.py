from erklartextgen.evaluation.pipeline import process
from sklearn.preprocessing import MinMaxScaler
import sys
import jsonlines
import joblib
import csv
import operator
from readability import Readability
from collections import Counter

READABILITY_FEATURES = [
    "flesch_kincaid",
    "flesch",
    "gunning_fog",
    "coleman_liau",
    "dale_chall",
    "ari",
    "linsear_write",
    "smog",
    "spache",
]

UPOS_TAGS = [
    "ADJ",
    "ADP",
    "ADV",
    "AUX",
    "CCONJ",
    "DET",
    "INTJ",
    "NOUN",
    "NUM",
    "PART",
    "PRON",
    "PROPN",
    "PUNCT",
    "SCONJ",
    "SYM",
    "VERB",
    "X",
]


def build_features(text):
    doc = process(text)
    r = Readability(text)

    readability_features = []
    for f in READABILITY_FEATURES:
        try:
            readability_features.append(operator.methodcaller(f)(r).score)
        except:
            readability_features.append(0)

    pos_counter = Counter(token.pos_ for token in doc)
    pos_frequencies = [pos_counter[tag] / len(doc) for tag in UPOS_TAGS]

    mean_ents_count = len(doc.ents) / len(list(doc.sents))

    total_parse_tree_depth = sum(
        _traverse_parse_tree(sent.root, 0) for sent in doc.sents
    )
    mean_parse_tree_depth = total_parse_tree_depth / len(list(doc.sents))

    return (
        readability_features
        + pos_frequencies
        + [mean_ents_count]
        + [mean_parse_tree_depth]
    )


def _traverse_parse_tree(node, current_depth):
    if node.n_lefts + node.n_rights > 0:
        return max(
            _traverse_parse_tree(child, current_depth + 1) for child in node.children
        )
    else:
        return current_depth


with open(sys.argv[1]) as csvfile:
    reader = csv.reader(csvfile)
    next(reader)

    feature_set = []
    dataset = []

    for row in reader:
        text = row[0]
        label = row[1]

        feature_set.append(build_features(text))
        dataset.append({"text": text, "label": label})

    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(feature_set)
    print(list(scaler.data_max_))
    joblib.dump(scaler, "kaggle_scaler.gz")

    with jsonlines.open("kaggle_preprocessed.jsonl", mode="a") as writer:
        for sf, item in zip(scaled_features, dataset):
            item_write = item.copy()
            item_write["features"] = list(sf)

            writer.write(item_write)
