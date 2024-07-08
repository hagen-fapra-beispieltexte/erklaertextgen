from . import pipeline

import erklartextgen.evaluation.cefr.evaluation as cefr
import erklartextgen.evaluation.linguistic.evaluation as linguistic
import erklartextgen.evaluation.readability.evaluation as readability
import erklartextgen.evaluation.safety.evaluation as safety
import erklartextgen.evaluation.stylistic.evaluation as stylistic


def load_deps(config):
    return {
        **cefr.load_dependencies(),
        **safety.load_dependencies(),
        **stylistic.load_dependencies(config),
    }


def evaluate(text, config, deps):
    """
    Evaluates the text and returns loss values for all categories

    TODO: document loss values
    """

    scores = compute_scores(text, config, deps)

    return {
        "cefr": cefr.compute_loss(scores["cefr"]),
        "linguistic": linguistic.compute_loss(scores["linguistic"]),
        "readability": readability.compute_loss(scores["readability"]),
        "safety": safety.compute_loss(scores["safety"]),
        "stylistic": stylistic.compute_loss(scores["stylistic"]),
    }


def compute_scores(text, config, deps):
    """
    Returns scores in all categories for the text
    """

    doc = pipeline.process(text)

    return {
        "cefr": cefr.compute_scores(doc, text, deps),
        "linguistic": linguistic.compute_scores(doc),
        "readability": readability.compute_scores(doc),
        "safety": safety.compute_scores(text, deps),
        "stylistic": stylistic.compute_scores(text, deps),
    }
