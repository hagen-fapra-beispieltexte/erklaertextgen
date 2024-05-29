import sys

from . import evaluation
from . import server


def run_eval():
    print(evaluation.evaluate(sys.argv[1]))


def main():
    print("todo")


if __name__ == "__main__":
    main()
