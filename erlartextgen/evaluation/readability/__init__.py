def count_syllables(word):
    count = 0
    vowels = "aeiouy"
    word = word.lower()
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if word.endswith("le"):
        count += 1
    if count == 0:
        count += 1
    return count


# Flesch Reading Ease Score
def score_flesch_reading_ease(doc):
    words = [token.text for token in doc if token.is_alpha]
    sentences = list(doc.sents)
    syllables = sum(count_syllables(word) for word in words)

    num_sentences = max(len(sentences), 1)
    num_words = len(words)
    num_syllables = syllables

    score = (
        206.835
        - 1.015 * (num_words / num_sentences)
        - 84.6 * (num_syllables / num_words)
    )
    return score


# Flesch-Kincaid readability formula
def score_flesch_kincaid_level(doc):
    words = [token.text for token in doc if token.is_alpha]
    sentences = list(doc.sents)
    syllables = sum(count_syllables(word) for word in words)

    num_sentences = max(len(sentences), 1)
    num_words = len(words)
    num_syllables = syllables

    score = 0.4 * (num_words / num_sentences) + 12 * (num_syllables / num_words) - 15
    return score
