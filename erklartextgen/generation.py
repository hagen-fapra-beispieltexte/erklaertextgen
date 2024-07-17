from . import evaluation
from . import prompting


def generate(config, deps, backend, topic, text_type, text_length):
    sample_count = 1

    if config["oversampling"]["enabled"]:
        sample_count = config["oversampling"]["count"]

    print(text_length)
    prompt = prompting.generate_prompt(config, topic, text_type, text_length)
    return backend.generate(prompt)
