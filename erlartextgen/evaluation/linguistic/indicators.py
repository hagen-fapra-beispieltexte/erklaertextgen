from collections import Counter
import wn

STRUCTURAL_COMPLEXITY_POS = [
    "NOUN",
    "ADJ",
    "DET",
    "ADV",
    "VERB",
    "CCONJ",
    "SCONJ",
    "ADP",  # proxy for prepositions
]

POS_WN_MAP = {
    "NOUN": "n",
    "VERB": "v",
    "ADJ": "a",
    "ADV": "r",
    "CCONJ": "c",
    "SCONJ": "c",
    "X": "x",
}


def compute_structural_complexity_indicators(doc):
    """
    Returns a map of frequencies of structural complexity indicators

    - Nouns (noun)
    - Adjectives (adj)
    - Determiners (det)
    - Adverbs (adv)
    - Verbs (verb)
    - Infinitive markers (inf)
    - Coordinating conjunctions (cconj)
    - Subordinating conjunctions (sconj)
    - Adpositions (adp), used as proxy indicator for prepositions
    """

    counter = Counter([token.pos_ for token in doc])
    token_count = len(doc)
    out = {
        pos.lower(): _normalize(count, token_count)
        for pos, count in counter.items()
        if pos in STRUCTURAL_COMPLEXITY_POS
    }

    # Additionally counts infinitive markers
    out["inf"] = _normalize([token.tag_ for token in doc].count("TO"), token_count)
    return out


def compute_ambiguity_indicators(doc):
    """
    Returns a map of frequencies of ambiguity indicators

    - Pronouns (pron)
    - Definite descriptions (def_np)
    - Word senses (word_senses)
    """

    token_count = len(doc)
    pron = [token.tag_ for token in doc].count("PRP")
    def_np = len(
        [
            c
            for c in doc.noun_chunks
            if c.text.startswith("the") or c.text.startswith("The")
        ]
    )

    word_senses = sum(
        len(wn.senses(token.lemma_, pos=POS_WN_MAP[token.pos_]))
        for token in doc
        if token.pos_ in POS_WN_MAP.keys()
    )

    return {
        "pron": _normalize(pron, token_count),
        "def_np": _normalize(def_np, token_count),
        "word_senses": _normalize(word_senses, token_count),
    }


def _normalize(feature_count, total_count):
    return feature_count / total_count
