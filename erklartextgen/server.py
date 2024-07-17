from flask import Flask, request, jsonify
from flask_cors import CORS
from .config import read_config
from .backend import load_backend
from .evaluation import load_deps
from . import generation

app = Flask(__name__)
CORS(app)

config = read_config()
deps = load_deps(config)
backend = load_backend(config)

CONFIG_LENGTH_LOOKUP = {1: "short", 2: "medium", 3: "long"}


@app.route("/generate_text", methods=["POST"])
def generate_text():
    data = request.json
    length = data.get("length")
    text_type = data.get("textType")
    topic = data.get("prompt")
    is_teacher_request = data.get("isTeacherRequest")

    if text_type == "Geschichte":
        text_type = "story"
    elif text_type == "Erklärtext":
        text_type = "explanation"

    text_length = 100
    if is_teacher_request:
        text_length = length
    else:
        text_length = config["lengths"][CONFIG_LENGTH_LOOKUP[length]]

    text = generation.generate(config, deps, backend, topic, text_type, text_length)
    response = {"generated_text": text}

    return jsonify(response)
