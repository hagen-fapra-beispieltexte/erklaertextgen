from collections import Counter

# Linguistic forms that were determined to be likely beyond A2
ADVANCED_FORMS = [
    "advanced_modals",
    "past_perfect",
    "complex_sentences",
    "ing_verb_forms",
    "past_progressive",
    "comparative_long_adv",
    "progressive_aspect",
    "present_progressive",
    "superlative_long_adv",
    "imperative_verbs",
    "real_conditionals",
    "passive_voice",
    "relative_clauses",
    "perfect_aspect",
    "phrasal_verbs",
    "present_perfect",
    "complex_prepositions",
    "comparative_short_adv",
    "unreal_conditionals",
    "comparative_long_adj",
]


def count_linguistic_forms(doc):
    forms_counter = Counter()

    for token in doc:
        if token.tag_ == "TO" and token.head.tag_ == "VB":
            forms_counter["to_infinitives"] += 1
        elif token.pos_ == "ADP" and token.text.lower() in [
            "in",
            "at",
            "on",
            "with",
            "after",
        ]:
            forms_counter["simple_prepositions"] += 1
        elif token.dep_ == "cop":
            forms_counter["copular_verbs"] += 1
        elif token.pos_ == "AUX":
            forms_counter["auxiliary_verbs"] += 1
        elif (
            token.pos_ == "VERB"
            and token.tag_ == "VBD"
            and token.lemma_ not in ["be", "have", "do"]
        ):
            forms_counter["irregular_verbs"] += 1
        elif (
            token.pos_ == "AUX"
            and token.tag_ == "MD"
            and token.text.lower() in ["might", "ought", "able"]
        ):
            forms_counter["advanced_modals"] += 1
        elif token.pos_ == "NOUN" and token.tag_ == "NNS":
            forms_counter["regular_plural_nouns"] += 1
        elif token.pos_ == "ADJ" and token.tag_ == "JJR":
            forms_counter["comparative_short_adj"] += 1
        elif token.pos_ == "ADV" and token.tag_ == "RB":
            forms_counter["positive_adv"] += 1
        elif token.pos_ == "VERB" and token.tag_ == "VBD":
            forms_counter["past_simple"] += 1
        elif token.dep_ == "advmod" and token.head.tag_ in ["VBD", "VBN"]:
            forms_counter["past_time"] += 1
        elif token.text.lower() == "there" and token.dep_ == "expl":
            forms_counter["existential_there"] += 1
        elif (
            token.pos_ == "VERB"
            and token.tag_ == "VBN"
            and token.lemma_ not in ["be", "have", "do"]
        ):
            forms_counter["regular_verbs_past_participle"] += 1
        elif token.pos_ == "ADJ" and token.tag_ == "JJ":
            forms_counter["positive_adj"] += 1
        elif token.pos_ in ["VERB", "AUX"] and token.text.lower() in ["am", "have"]:
            forms_counter["full_verbs"] += 1
        elif token.dep_ == "dobj":
            forms_counter["direct_object"] += 1
        elif token.pos_ == "ADP" and token.text.lower() in ["during", "through"]:
            forms_counter["advanced_prepositions"] += 1
        elif (
            token.text.lower() == "used"
            and token.head.tag_ == "VB"
            and token.head.text == "to"
        ):
            forms_counter["used_to"] += 1
        elif token.pos_ == "VERB" and token.tag_ == "VBZ":
            forms_counter["present_simple"] += 1
        elif token.dep_ in ["advmod", "nsubj", "csubj"] and token.text.lower() in [
            "who",
            "what",
            "when",
            "where",
            "why",
            "how",
        ]:
            forms_counter["wh_questions"] += 1
        elif (
            token.pos_ == "VERB"
            and token.tag_ == "VBN"
            and "VBD" in [child.tag_ for child in token.children]
        ):
            forms_counter["past_perfect"] += 1
        elif token.dep_ == "mark" and token.head.dep_ == "csubj":
            forms_counter["complex_sentences"] += 1
        elif token.dep_ == "advmod" and token.head.tag_ in ["VBZ", "VBP"]:
            forms_counter["present_time"] += 1
        elif token.pos_ == "VERB" and token.tag_ == "VBG":
            forms_counter["ing_verb_forms"] += 1
        elif token.dep_ == "aux" and token.head.dep_ == "ROOT":
            forms_counter["be_questions"] += 1
        elif (
            token.pos_ == "PRON"
            and token.tag_ in ["PRP", "PRP$"]
            and token.text.lower() in ["i", "you"]
        ):
            forms_counter["subjective_pronouns"] += 1
        elif token.dep_ == "csubj":
            forms_counter["subordinate_clauses_reduced"] += 1
        elif token.pos_ == "VERB" and token.tag_ in ["VBD", "VBZ", "VBP"]:
            forms_counter["simple_aspect"] += 1
        elif token.pos_ == "NOUN" and token.tag_ == "NN":
            forms_counter["ing_noun_forms"] += 1
        elif (
            token.pos_ == "VERB"
            and token.tag_ == "VBG"
            and "AUX" in [child.pos_ for child in token.children]
        ):
            forms_counter["past_progressive"] += 1
        elif token.pos_ == "ADV" and token.tag_ == "RBR":
            forms_counter["comparative_long_adv"] += 1
        elif (
            token.pos_ == "VERB"
            and token.tag_ == "VBG"
            and "AUX" in [child.pos_ for child in token.children]
        ):
            forms_counter["progressive_aspect"] += 1
        elif token.dep_ == "advcl":
            forms_counter["adverbial_clauses"] += 1
        elif (
            token.pos_ == "VERB"
            and token.tag_ == "VBG"
            and "AUX" in [child.pos_ for child in token.children]
            and token.head.tag_ in ["VBZ", "VBP"]
        ):
            forms_counter["present_progressive"] += 1
        elif token.pos_ == "ADV" and token.tag_ == "RBS":
            forms_counter["superlative_long_adv"] += 1
        elif token.dep_ == "dep":
            forms_counter["incomplete_sentences"] += 1
        elif token.pos_ == "VERB" and token.tag_ == "VB" and token.dep_ == "ROOT":
            forms_counter["imperative_verbs"] += 1
        elif (
            token.dep_ == "aux"
            and token.head.dep_ == "ROOT"
            and token.text.lower() == "have"
        ):
            forms_counter["have_questions"] += 1
        elif token.dep_ == "mark" and token.head.dep_ == "ccomp":
            forms_counter["real_conditionals"] += 1
        elif token.dep_ == "auxpass" and token.head.dep_ == "ROOT":
            forms_counter["passive_voice"] += 1
        elif (
            token.pos_ == "PRON"
            and token.tag_ in ["PRP", "PRP$"]
            and token.dep_ == "poss"
        ):
            forms_counter["absolute_possessive_pronouns"] += 1
        elif token.dep_ == "relcl":
            forms_counter["relative_clauses"] += 1
        elif (
            token.pos_ == "VERB"
            and token.tag_ in ["VBN", "VBG"]
            and "AUX" in [child.pos_ for child in token.children]
        ):
            forms_counter["perfect_aspect"] += 1
        elif token.dep_ == "prt":
            forms_counter["phrasal_verbs"] += 1
        elif (
            token.pos_ == "VERB"
            and token.tag_ == "VBN"
            and "AUX" in [child.pos_ for child in token.children]
            and token.head.tag_ in ["VBZ", "VBP"]
        ):
            forms_counter["present_perfect"] += 1
        elif token.pos_ == "ADP" and token.text.lower() in ["according", "except"]:
            forms_counter["complex_prepositions"] += 1
        elif (
            token.pos_ == "ADV"
            and token.tag_ == "RBR"
            and token.head.tag_ in ["VBZ", "VBP"]
        ):
            forms_counter["comparative_short_adv"] += 1
        elif token.dep_ == "dobj" and token.head.tag_ in ["VB", "VBP", "VBZ"]:
            forms_counter["indirect_object"] += 1
        elif token.dep_ == "mark" and token.head.dep_ == "xcomp":
            forms_counter["unreal_conditionals"] += 1
        elif (
            token.pos_ == "ADJ"
            and token.tag_ == "JJR"
            and token.head.tag_ in ["VB", "VBP", "VBZ"]
        ):
            forms_counter["comparative_long_adj"] += 1
        elif token.dep_ == "ROOT" and len(list(token.children)) <= 2:
            forms_counter["simple_sentences"] += 1
        elif token.pos_ == "ADJ" and token.tag_ in ["JJR", "JJS"]:
            forms_counter["degrees_of_comparison_adj"] += 1
        elif token.pos_ == "VERB" and token.tag_ in ["VB", "VBD", "VBZ"]:
            forms_counter["tenses"] += 1
        elif token.dep_ == "mark" and token.head.dep_ in ["advcl", "xcomp"]:
            forms_counter["conditionals"] += 1

    return forms_counter


def compute_ratio(doc):
    """
    Computes the ratio of advanced linguistic forms
    """
    form_counts = count_linguistic_forms(doc)
    total_forms = sum(form_counts.values())

    if total_forms == 0:
        return 0.0

    advanced_count = sum(form_counts[form] for form in ADVANCED_FORMS)
    return advanced_count / total_forms
