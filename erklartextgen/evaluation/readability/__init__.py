def _count_syllables(word):
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


def compute_flesch_reading_ease(doc):
    """
    Flesch Reading Ease Score
    """
    words = [token.text for token in doc if token.is_alpha]
    sentences = list(doc.sents)
    syllables = sum(_count_syllables(word) for word in words)

    num_sentences = max(len(sentences), 1)
    num_words = len(words)
    num_syllables = syllables

    score = (
        206.835
        - 1.015 * (num_words / num_sentences)
        - 84.6 * (num_syllables / num_words)
    )
    return score


def compute_flesch_kincaid_level(doc):
    """
    Flesch-Kincaid readability formula
    """
    words = [token.text for token in doc if token.is_alpha]
    sentences = list(doc.sents)
    syllables = sum(_count_syllables(word) for word in words)

    num_sentences = max(len(sentences), 1)
    num_words = len(words)
    num_syllables = syllables

    score = 0.4 * (num_words / num_sentences) + 12 * (num_syllables / num_words) - 15
    return score


def compute_smog_index(doc):
    """
    Smog index
    """
    sentences = list(doc.sents)
    words = [word.text for word in doc if word.is_alpha]

    sentence_count = max(len(sentences), 1)
    polysyllable_count = sum(1 for word in words if _count_syllables(word) > 2)

    smog_score = 1.043 * (30 * polysyllable_count / sentence_count) ** 0.5 + 3.1291
    return smog_score


def compute_gunning_fog_index(doc):
    """
    Gunning FOG index
    """
    sentences = list(doc.sents)
    words = [word.text for word in doc if word.is_alpha]

    sentence_count = max(len(sentences), 1)
    word_count = len(words)
    complex_word_count = sum(1 for word in words if _count_syllables(word) >= 3)

    gunning_fog_index = 0.4 * (
        (word_count / sentence_count) + (100 * (complex_word_count / word_count))
    )

    return gunning_fog_index


def compute_ari(doc):
    """
    Automated Readability Index (ARI)
    """

    sentences = list(doc.sents)
    words = [word.text for word in doc if word.is_alpha]

    sentence_count = max(len(sentences), 1)
    word_count = len(words)
    char_count = sum(len(word) for word in words)

    ari_score = (
        4.71 * (char_count / word_count) + 0.5 * (word_count / sentence_count) - 21.43
    )
    return round(ari_score)


def compute_coleman_liau(doc):
    """
    Coleman-Liau index
    """

    sentences = list(doc.sents)
    words = [word.text for word in doc if word.is_alpha]

    sentence_count = max(len(sentences), 1)
    word_count = len(words)
    char_count = sum(len(word) for word in words)

    lr = (char_count / word_count) * 100
    sr = (sentence_count / word_count) * 100
    coleman_liau_score = 0.0588 * lr - 0.296 * sr - 15.8
    return coleman_liau_score
