# erklärtextgen

## Installation

Make sure you have `poetry` and `yarn` installed, then install the project dependencies:

```
poetry install
```

Download the spacy model and the Open English WordNet.

```
poetry run python -m spacy download en_core_web_sm
poetry run python -m wn download oewn:2023
```

Install frontend dependencies:
```
cd frontend
yarn install
```

Obtain the assets data and place them in the folder `assets`.

Finally, copy the `config/config.toml.example` to `config/config.toml` and configure all values.

## Development

Start the backend:

```
poetry run flask --app erklartextgen.server run
```

Start the frontend:

```
yarn run dev
```

You can get the raw evaluation metrics for a single sentence like this:
```
poetry run eval "This is a test sentence"
```

Please lint and format your code:
```
poetry run ruff lint
poetry run ruff format
```

## Usage
**Text Generation**

To generate text, use the `generate` function from the `generation.py` script. This function uses a specified backend and configuration to produce text based on a given topic.

**Example:**
```python
from generation import generate

config = read_config()  # Load your configuration
text = generate(config, deps, backend, "Technology", "explanation", 150)
print(text)
```
**Genre Suggestion**

The `suggest_genre` function suggests a genre based on the provided topic using the `SentenceTransformer` model.

**Example:**
```python
from prompts import suggest_genre

genre = suggest_genre("distiluse-base-multilingual-cased-v1", "Space Exploration")
print(genre)  # Output: "Abenteuer"
```

**Prompt Generation**

Generate prompts for different text types using the `generate_prompt` function. This function formats a prompt template with provided parameters such as topic, text type, and length.

**Example:**
```python
from prompts import generate_prompt

prompt = generate_prompt(config, "Space Exploration", "story", 200)
print(prompt)
```

**Postprocessing**

To shorten a text to the nearest sentence within a word limit, use: `shorten_to_nearest_sentence(text, max_length)`. The function will return the shortened text without cutting off mid-sentence.

**Example:**
```python
text = "This is a complete sentence. This is another one."
max_length = 6
shortened_text = shorten_to_nearest_sentence(text, max_length)
print(shortened_text)  # Output: "This is a complete sentence." 
```

**Configuration**

Ensure your `config.toml` file is set up correctly. Key sections include:

- `[backend]`: Defines the backend to use for text generation.
- `[prompting]`: Contains prompt templates for different text types.
- `[lengths]`: Predefined lengths for generated texts.
- `[evaluation]`: API keys and settings for evaluating generated content.

Make sure to configure your `config.toml` file with the appropriate settings for your environment and use case.


