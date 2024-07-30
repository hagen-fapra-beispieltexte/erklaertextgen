"""
Implements text generation functionality
"""

import re

from . import evaluation
from . import prompting


def generate(config, deps, backend, topic, text_type, text_length):
    """
    Generates a text and samples the one that is closest to the target text length
    """
    sample_count = 1

    if config["oversampling"]["enabled"]:
        sample_count = config["oversampling"]["count"]

    prompt = prompting.generate_prompt(config, topic, text_type, text_length)
    texts = [backend.generate(prompt) for _ in range(0, sample_count)]

    text_evals = [evaluation.evaluate(t, config, deps, text_length) for t in texts]

    min_len_diff = 100000
    min_idx = None
    for idx, eval_res in text_evals:
        if eval_res["text_length"] < min_len_diff:
            min_len_diff = eval_res["text_length"]
            min_idx = idx

    selected_text = texts[min_idx]

    if config["postprocessing"]["enabled"]:
        selected_text = _shorten_to_nearest_sentence(selected_text, text_length)
        selected_text = _clean_text(selected_text)
        return selected_text
    else:
        return selected_text


def _shorten_to_nearest_sentence(text, max_length):
    words = text.split()
    if len(words) <= max_length:
        return text
    truncated_text = " ".join(words[:max_length])
    sentences = re.split(r"(?<=[.!?])\s+", truncated_text)
    shortened_text = ""
    for sentence in sentences:
        if len(shortened_text.split()) + len(sentence.split()) <= max_length:
            shortened_text += sentence
        else:
            break

    last_sentence_end = truncated_text.rfind(".")
    if last_sentence_end != -1 and len(shortened_text.split()) < max_length:
        shortened_text = truncated_text[: last_sentence_end + 1]

    return shortened_text.strip()


def _clean_text(text):
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"(Title:|Characters:|Story:)\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*\(boy\)|\s*\(girl\)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*\(.*?\)", "", text)
    text = re.sub(r"^-.*?$", "", text, flags=re.MULTILINE)

    return text
