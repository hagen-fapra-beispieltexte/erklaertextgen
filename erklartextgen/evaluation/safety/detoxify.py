"""
Analyzes the text for toxicity

Bibliography key: bhandari2023trustworthiness
"""

from detoxify import Detoxify


def load_model():
    return Detoxify("original")


def predict(text, deps):
    return deps["detoxify_model"].predict(text)
