"""
Implements a CLI for the project
"""
import sys

from . import evaluation
from . import generation
from .config import read_config
from .backend import load_backend

def run_eval():
    config = read_config()
    deps = evaluation.load_deps(config)

    print(evaluation.compute_scores(sys.argv[1], config, deps))


def run_generate():
    config = read_config()
    deps = evaluation.load_deps(config)
    backend = load_backend(config)

    print(generation.generate(config, deps, backend, sys.argv[1], "explanation", 200))


def main():
    print("Please use either the 'generate' or 'eval' subcommand.")
    print("Consult the README.md of this project for more information.")


if __name__ == "__main__":
    main()
