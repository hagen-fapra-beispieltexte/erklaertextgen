import torch
import torch.nn as nn
import spacy
from transformers import AutoTokenizer, AutoModel
import sys
import jsonlines
import operator
from readability import Readability
from collections import Counter

NLP_MODEL = spacy.load("en_core_web_sm")
TOKENIZER_MAX_LENGTH = 512
CLASSIFIER_NUM_CEFR_LEVELS = 6
DEVICE = "cuda"

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
    doc = NLP_MODEL(text)
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


class CEFRClassifier(nn.Module):
    def __init__(self, num_cefr_levels):
        super(CEFRClassifier, self).__init__()

        self.bert = AutoModel.from_pretrained("distilbert/distilbert-base-uncased")

        # Freeze distilBERT params
        for param in self.bert.parameters():
            param.requires_grad = False

        self.fc1 = nn.Linear(768, 768)
        self.fc2 = nn.Linear(768, 128)
        self.fc3 = nn.Linear(28, 28)
        self.output = nn.Linear(128 + 28, num_cefr_levels)

        self.dropout = nn.Dropout(0.5)
        self.relu = nn.ReLU()

    def forward(self, input_ids, attention_mask, aux_features):
        bert_output = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        sequence_output = bert_output.last_hidden_state
        pooled_output = sequence_output[:, 0].squeeze()

        x = self.fc1(pooled_output)
        x = self.dropout(x)
        x = self.relu(x)

        x = self.fc2(x)
        x = self.dropout(x)
        x = self.relu(x)

        y = self.fc3(aux_features)
        y = self.relu(y)
        y = self.dropout(y)

        return self.output(torch.cat((x, y), -1))


def classify(text, classifier, tokenizer):
    tokenized = tokenizer(
        text,
        return_tensors="pt",
        padding="max_length",
        max_length=TOKENIZER_MAX_LENGTH,
        truncation=True,
    )

    features = torch.tensor(build_features(text)).to(DEVICE)
    logits = classifier.forward(
        tokenized["input_ids"].squeeze().to(DEVICE),
        tokenized["attention_mask"].squeeze().to(DEVICE),
        features,
    )
    return torch.argmax(torch.nn.functional.softmax(logits, dim=-1)).item()


load_path = "assets/dataset_model_20240712_092923_9"
load_path_dataset = "simplewiki_transformed.jsonl"
classifier = CEFRClassifier(CLASSIFIER_NUM_CEFR_LEVELS)
classifier.load_state_dict(torch.load(load_path, map_location=torch.device(DEVICE)))
classifier.to(DEVICE)
classifier.eval()

tokenizer = AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased")

n_total = 253830

with jsonlines.open(sys.argv[1]) as reader:
    for idx, obj in enumerate(reader):
        text = None
        if obj["opening_text"]:
            text = obj["opening_text"]
        else:
            text = obj["text"]

        print(f"{idx} / {n_total}")
        with jsonlines.open("simplewiki_classified.jsonl", mode="a") as writer:
            label = classify(text, classifier, tokenizer)
            title = obj["title"]
            page_id = obj["page_id"]

            writer.write(
                {"page_id": page_id, "title": title, "text": text, "label": label}
            )
