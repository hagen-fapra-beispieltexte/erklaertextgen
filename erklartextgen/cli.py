import sys
import jsonlines
import itertools
import json
import csv

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


def run_generate_eval_set():
    """
    Generates an evalation set based on a given wordlist of topics
    """

    wordlist_filename = sys.argv[1]

    config = read_config()
    backend = load_backend(config)

    jobs = []
    current_id = 1
    with open(wordlist_filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row, length in zip(reader, itertools.cycle(["short", "medium", "long"])):
            if row["explanation"] == "true":
                jobs.append(
                    {
                        "topic": row["word"],
                        "length": length,
                        "type": "explanation",
                        "id": current_id,
                    }
                )
                current_id += 1

            if row["story"] == "true":
                jobs.append(
                    {
                        "topic": row["word"],
                        "length": length,
                        "type": "story",
                        "id": current_id,
                    }
                )
                current_id += 1

    outputs = []
    print(f"total jobs {len(jobs)}")
    for job in jobs:
        print(job["id"])
        prompt = generate_prompt(config, job["topic"], job["type"], job["length"])
        backend_output = backend.generate(prompt)

        output = job.copy()
        output["prompt"] = prompt
        output["output"] = backend_output["response"]
        output["backend_duration"] = backend_output["eval_duration"]

        outputs.append(output)

    with open("eval_set.json", "w") as f:
        json.dump(outputs, f)


def run_evaluate_eval_set():
    """
    Runs the evaluation on an evaluation set

    Writes out the evaluation results to a 'eval_output.jsonl'.
    """
    eval_set_path = sys.argv[1]

    config = read_config()
    eval_deps = evaluation.load_deps(config)

    eval_set = None
    with open(eval_set_path) as f:
        eval_set = json.load(f)

    with jsonlines.open("eval_output.jsonl", mode="a") as writer:
        for item in eval_set:
            print(item["id"])

            eval_entry = {}
            eval_entry["id"] = item["id"]
            eval_entry["eval"] = evaluation.evaluate(item["output"], config, eval_deps)

            writer.write(eval_entry)


def main():
    print("todo")


if __name__ == "__main__":
    main()
