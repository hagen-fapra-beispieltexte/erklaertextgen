def shorten_to_nearest_sentence(text, max_length):
    """
    Kürzt den Text auf die maximale Länge, ohne mitten im Satz zu schneiden.

    Parameters:
    text (str): Der zu kürzende Text.
    max_length (int): Die maximale Anzahl von Wörtern.

    Returns:
    str: Der gekürzte Text.
    """
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
    # Füge den letzten vollständigen Satz hinzu, falls vorhanden
    last_sentence_end = truncated_text.rfind(".")
    if last_sentence_end != -1 and len(shortened_text.split()) < max_length:
        shortened_text = truncated_text[: last_sentence_end + 1]
    return shortened_text.strip()
