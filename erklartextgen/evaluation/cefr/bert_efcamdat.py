import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel

TOKENIZER_MAX_LENGTH = 450
CLASSIFIER_NUM_CEFR_LEVELS = 5


def load(load_path):
    classifier = CEFRClassifier(CLASSIFIER_NUM_CEFR_LEVELS)
    classifier.load_state_dict(torch.load(load_path, map_location=torch.device("cpu")))
    classifier.eval()

    tokenizer = AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased")

    return {"tokenizer": tokenizer, "model": classifier}


def classify(text, deps):
    classifier = deps["model"]
    tokenizer = deps["tokenizer"]

    tokenized = tokenizer(
        text,
        return_tensors="pt",
        padding="max_length",
        max_length=TOKENIZER_MAX_LENGTH,
        truncation=True,
    )

    logits = classifier.forward(tokenized["input_ids"], tokenized["attention_mask"])
    cefr_numeric = torch.argmax(torch.nn.functional.softmax(logits, dim=1)).item() + 1

    return cefr_numeric


class CEFRClassifier(nn.Module):
    def __init__(self, num_cefr_levels):
        super(CEFRClassifier, self).__init__()

        self.bert = AutoModel.from_pretrained("distilbert/distilbert-base-uncased")

        # Freeze distilBERT params
        for param in self.bert.parameters():
            param.requires_grad = False

        # Classifier layers
        self.pre_classifier = nn.Linear(768, 768)
        self.fc2 = nn.Linear(768, 128)
        self.output = nn.Linear(128, num_cefr_levels)

        self.dropout = nn.Dropout(0.2)
        self.relu = nn.ReLU()

    def forward(self, input_ids, attention_mask):
        output = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        sequence_output = output.last_hidden_state
        pooled_output = sequence_output[:, 0]

        x = self.pre_classifier(pooled_output)
        x = self.dropout(x)
        x = self.relu(x)

        x = self.fc2(x)
        x = self.dropout(x)
        x = self.relu(x)

        logits = self.output(x)
        return logits
