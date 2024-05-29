from . import pipeline
from .linguistic import indicators as linguistic_indicators
from .cefr import efllex as efllex
from . import safety
from . import readability


def evaluate(text):
    doc = pipeline.process(text)

    indicators_structural_complexity = (
        linguistic_indicators.compute_structural_complexity_indicators(doc)
    )
    indicators_ambiguity = linguistic_indicators.compute_ambiguity_indicators(doc)

    out = {
        "indicators_structural_complexty": indicators_structural_complexity,
        "indicators_ambiguity": indicators_ambiguity,
        "cefr_efflex_values": efllex.analyze_first_observation(doc),
        "safety": safety.analyze(text),
        "flesch": readability.score_flesch_reading_ease(doc),
        "flesch_kincaid": readability.score_flesch_kincaid_level(doc),
    }

    return out
