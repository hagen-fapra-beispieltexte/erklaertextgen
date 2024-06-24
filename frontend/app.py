from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Setzen Sie Ihren OpenAI API-Schlüssel hier
api_key = "sk-proj-sqmsSNvYP63aqQswDH2RT3BlbkFJOD91UfpSYbkILJzjOE0W"


@app.route("/generate_text", methods=["POST"])
def generate_text():
    data = request.json
    prompt = data.get("prompt")  # wichtig
    length = data.get("length")  # wichtig
    text_type = data.get("text_type")  # wichtig

    # Define prompt text based on user input
    if text_type == "Geschichte":
        prompt_text = f"Write an exciting or funny story about this German word and/or words: {prompt}. Make the story fun to read and engaging."
    elif text_type == "Erklärtext":
        prompt_text = f"Write an easy to understand explanation in very simple English, about what {prompt} is and/or how it works."
    else:
        prompt_text = prompt

    # Dynamische Anpassung von max_tokens basierend auf length
    if length == 1:
        max_tokens = 50
    elif length == 2:
        max_tokens = 200
    else:
        max_tokens = 400

    # Create OpenAI client
    client = openai.OpenAI(api_key=api_key)

    # Anfrage an die OpenAI API, um den Text in einfachem Englisch zu generieren
    response = client.chat.completions.create(
        model="gpt-4o",  # oder "gpt-3.5-turbo" je nach Verfügbarkeit
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that writes an engaging and fun to read text in simple English. Your text is suitable for children. The sentences in your output are rather short. Your prompt is in german or english. Answer in English, without going into detail, that the word was in German.",
            },
            {"role": "user", "content": prompt_text},
        ],
        max_tokens=max_tokens,  # Dynamische Länge
        temperature=0.7,  # Sie können die Temperatur anpassen
    )

    generated_text = response.choices[0].message.content.strip()

    response = {"generated_text": generated_text}
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
