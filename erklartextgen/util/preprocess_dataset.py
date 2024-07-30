from erklartextgen.evaluation.pipeline import process
import sys
import jsonlines
import joblib
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


def build_features(text, doc):
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

    return len(doc), readability_features + pos_frequencies + [mean_ents_count] + [
        mean_parse_tree_depth
    ]


def _traverse_parse_tree(node, current_depth):
    if node.n_lefts + node.n_rights > 0:
        return max(
            _traverse_parse_tree(child, current_depth + 1) for child in node.children
        )
    else:
        return current_depth


def remove_last_part(text, start_phrase):
    start_index = text.find(start_phrase)

    if start_index != -1:
        return text[:start_index].strip()
    else:
        return text


scaler = joblib.load("kaggle_scaler.gz")

with jsonlines.open(sys.argv[1]) as reader:
    total_len = 253830

    for idx, obj in enumerate(reader):
        text = None
        if obj["opening_text"]:
            text = obj["opening_text"]
        else:
            text = obj["text"]

        doc = process(text)

        # Removes stub texts
        text = remove_last_part(text, "This short article")

        # Skips texts that are only one sentence long
        if len(list(doc.sents)) <= 1:
            continue

        print(f"{idx} / {total_len}")
        try:
            text_len, features = build_features(text, doc)
            transformed_features = list(scaler.transform([features])[0])

            with jsonlines.open("simplewiki_preprocessed.jsonl", mode="a") as writer:
                writer.write(
                    {
                        "page_id": obj["page_id"],
                        "title": obj["title"],
                        "text": text,
                        "text_length": text_len,
                        "features": transformed_features,
                    }
                )
        except Exception as e:
            print(e)
