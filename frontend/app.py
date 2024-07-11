from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import requests

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Setzen Sie Ihren OpenAI API-Schlüssel hier
api_key = "sk-proj-sqmsSNvYP63aqQswDH2RT3BlbkFJOD91UfpSYbkILJzjOE0W"

@app.route('/generate_text', methods=['POST'])
def generate_text():
    data = request.json
    prompt = data.get('prompt')
    max_tokens = data.get('length')
    text_type = data.get('text_type')

    if text_type == 'Geschichte':
        prompt_text = f"Write an exciting or funny story about this German word and/or words: {prompt}. Make the story fun to read and engaging."
    elif text_type == 'Erklärtext':
        prompt_text = f"Write an easy to understand explanation in very simple English, about what {prompt} is and/or how it works."
    else:
        prompt_text = prompt

    client = openai.OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes an engaging and fun to read text in simple English. Your text is suitable for children. The sentences in your output are rather short. Your prompt is in german or english. Answer in English, without going into detail, that the word was in German."},
            {"role": "user", "content": prompt_text}
        ],
        max_tokens=max_tokens,
        temperature=0.7
    )

    generated_text = response.choices[0].message.content.strip()

    return jsonify({'generated_text': generated_text})

@app.route('/get_synonyms', methods=['GET'])
def get_synonyms():
    word = request.args.get('word')
    if not word:
        return jsonify({'error': 'No word provided'}), 400

    response = requests.get(f'https://api.datamuse.com/words?rel_trg={word}&v=de')
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch translations'}), 500

    translations = [item['word'] for item in response.json()[:3]]

    return jsonify({'synonyms': translations})

@app.route('/translate_text', methods=['POST'])
def translate_text():
    data = request.json
    text = data.get('text')

    client = openai.OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates text to German."},
            {"role": "user", "content": text}
        ],
        max_tokens=500,
        temperature=0.7
    )

    translated_text = response.choices[0].message.content.strip()

    return jsonify({'translated_text': translated_text})

if __name__ == '__main__':
    app.run(debug=True)