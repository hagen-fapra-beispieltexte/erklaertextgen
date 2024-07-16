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

TODO
