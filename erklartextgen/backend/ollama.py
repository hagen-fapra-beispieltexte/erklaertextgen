from ollama import Client


class Ollama:
    def __init__(self, config):
        self.client = Client(host=config["base_url"])
        self.model = config["model"]

    def generate(self, prompt):
        return self.client.generate(model=self.model, prompt=prompt)
