from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/generate_text", methods=["POST"])
def generate_text():
    data = request.json
    length = data.get("length")
    text_type = data.get("text_type")
    prompt = data.get("prompt")

    # Define prompt text based on user input
    if text_type == "Geschichte":
        prompt_text = f"This is a story about {prompt}:"
    elif text_type == "Erklärtext":
        prompt_text = f"An easy explanation of {prompt} is this:"
    else:
        prompt_text = prompt

    # Determine the maximum length based on user input
    max_length = 50 if length == 1 else 100 if length == 2 else 200

    response = {"generated_text": "dummy text"}
    return jsonify(response)
