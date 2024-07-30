import sys
import jsonlines
import json

from . import evaluation
from .config import read_config

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
