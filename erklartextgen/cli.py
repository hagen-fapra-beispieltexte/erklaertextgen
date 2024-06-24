import sys

from . import evaluation
from .config import read_config
from .prompting import *
from .backend import load_backend


def run_eval():
    config = read_config()
    print(evaluation.evaluate(sys.argv[1], config))


def run_generate():
    topic = sys.argv[2]
    config = read_config()
    prompt = generate_prompt(config, topic, sys.argv[1], "medium")
    backend = load_backend(config)


def main():
    print("todo")


if __name__ == "__main__":
    main()
