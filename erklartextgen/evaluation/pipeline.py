import spacy

nlp = spacy.load("en_core_web_sm")


def process(text):
    return nlp(text)
