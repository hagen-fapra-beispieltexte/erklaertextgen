"""
Implements functionality for prompting and prompt templating
"""

from sentence_transformers import SentenceTransformer, util
import numpy as np

GENRE_DESCRIPTIONS = {
    "Abenteuer": "Ein Abenteuer mit einer Reise, neuen Orten und Herausforderungen.",
    "Märchen": "Ein modernes Märchen mit magischen Kreaturen, Problemlösung und einer Lektion.",
    "Geheimnis": "Ein Geheimnis mit einer Rätsellösung durch Hinweise.",
    "Freundschaft": "Eine Geschichte über Freundschaft und neue Freunde.",
    "Natur": "Eine Geschichte in der Natur, die deren Schönheit zeigt.",
    "Tiere": "Eine Geschichte mit Tieren als Hauptfiguren und ihren Abenteuern.",
    "Magie": "Eine Geschichte mit magischen Elementen und einer zauberhaften Welt.",
    "Reisen": "Eine Geschichte über eine Reise zu neuen Orten und Kulturen.",
}


def suggest_genre(model_identifier, topic):
    model = SentenceTransformer(model_identifier)

    genres, genre_descriptions = [list(x) for x in zip(*GENRE_DESCRIPTIONS.items())]
    genre_embeddings = model.encode(genre_descriptions)
    topic_embedding = model.encode(topic)
    similarities = util.pytorch_cos_sim(topic_embedding, genre_embeddings)
    best_genre_idx = np.argmax(similarities)

    return genres[best_genre_idx]


def generate_prompt(config, topic, text_type, text_wordlen):
    params = {"topic": topic, "length": text_wordlen}

    if text_type == "explanation":
        return config["prompting"]["explanation_prompt"].format(**params)
    elif text_type == "story":
        genre = suggest_genre(config["prompting"]["genre_embedding_model"], topic)
        params["genre"] = genre
        return config["prompting"]["story_prompt"].format(**params)
