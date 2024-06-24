from flask import Flask, request, jsonify
from flask_cors import CORS
from .config import read_config
from .prompting import *
from .backend import load_backend

app = Flask(__name__)
CORS(app)

config = read_config()


@app.route("/generate_text", methods=["POST"])
def generate_text():
    data = request.json
    length = data.get("length")
    text_type = data.get("text_type")
    topic = data.get("prompt")

    if text_type == "Geschichte":
        text_type = "story"
    elif text_type == "Erklärtext":
        text_type = "explanation"

    text_length_str = "short"
    if length == 1:
        text_length = "medium"
    elif length == 2:
        text_length = "long"

    prompt = generate_prompt(config, topic, text_type, text_length_str)
    backend = load_backend(config)
    text = backend.generate(prompt)

    response = {"generated_text": text}
    return jsonify(response)
