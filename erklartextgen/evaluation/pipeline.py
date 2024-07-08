import spacy

NLP_MODEL = spacy.load("en_core_web_sm")


def process(text):
    return NLP_MODEL(text)
