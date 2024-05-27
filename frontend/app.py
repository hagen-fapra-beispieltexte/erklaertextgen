from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Load GPT-2 model and tokenizer
model_name = "gpt2"  # You can use "gpt2-medium", "gpt2-large", etc. for larger models
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

@app.route('/generate_text', methods=['POST'])
def generate_text():
    data = request.json
    length = data.get('length')
    text_type = data.get('text_type')
    prompt = data.get('prompt')

    # Define prompt text based on user input
    if text_type == 'Geschichte':
        prompt_text = f"This is a story about {prompt}:"
    elif text_type == 'Erklärtext':
        prompt_text = f"An easy explanation of {prompt} is this:"
    else:
        prompt_text = prompt

    # Determine the maximum length based on user input
    max_length = 50 if length == 1 else 100 if length == 2 else 200

    # Encode the prompt text and generate the text
    inputs = tokenizer.encode(prompt_text, return_tensors='pt')
    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2, early_stopping=True)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    response = {
        'generated_text': generated_text
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
