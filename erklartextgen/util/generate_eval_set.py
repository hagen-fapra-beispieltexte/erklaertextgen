import sys
import itertools
import json
import csv

from .config import read_config
from .prompting import generate_prompt
from .backend import load_backend

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
    print(backend_output)

    output = job.copy()
    output["prompt"] = prompt
    output["output"] = backend_output["response"]
    output["backend_duration"] = backend_output["eval_duration"]

    print(output)
    outputs.append(output)

with open("eval_set.json", "w") as f:
    json.dump(outputs, f)
