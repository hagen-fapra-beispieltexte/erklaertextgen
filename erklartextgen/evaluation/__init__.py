from . import pipeline
from .linguistic import indicators as linguistic_indicators
from .linguistic import forms as forms
from .cefr import efllex as efllex
from .cefr import cefr_j as cefr_j
from . import safety
from . import readability
from . import stylistic


def evaluate(text, config):
    doc = pipeline.process(text)

    stylistic_evaluator = stylistic.GPT4StyleEvaluator(
        config["evaluation"]["openai_api_key"]
    )
    indicators_structural_complexity = (
        linguistic_indicators.compute_structural_complexity_indicators(doc)
    )
    indicators_ambiguity = linguistic_indicators.compute_ambiguity_indicators(doc)

    out = {
        "linguistic": {
            "indicators_structural_complexty": indicators_structural_complexity,
            "indicators_ambiguity": indicators_ambiguity,
            "advanced_ratio": forms.compute_ratio(doc),
        },
        "cefr": {
            "cefr_j": cefr_j.predict(doc),
            "efflex": efllex.analyze_first_observation(doc),
        },
        "safety": {
            "detoxify": safety.analyze(text),
        },
        "readability": {
            "flesch": readability.compute_flesch_reading_ease(doc),
            "flesch_kincaid": readability.compute_flesch_kincaid_level(doc),
            "smog_index": readability.compute_smog_index(doc),
            "gunning_fog": readability.compute_gunning_fog_index(doc),
            "ari": readability.compute_ari(doc),
            "coleman_liau": readability.compute_coleman_liau(doc),
        },
        "stylistic": stylistic_evaluator.evaluate(text),
    }

    return out
