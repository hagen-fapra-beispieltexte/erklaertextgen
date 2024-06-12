from . import ollama


def load_backend(config):
    if config["backend"]["active"] == "ollama":
        return ollama.Ollama(config["backend"]["ollama"])
