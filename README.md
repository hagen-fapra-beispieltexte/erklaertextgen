# erklärtextgen

This repository contains the code and associated artifacts of the project "Beispieltexte", which was carried out as part of the *Fachpraktikum Sprachtechnologie* in the summer semester 2024 at the University of Hagen.

The goal of this application is to enable both students and teachers to generate child-suitable and readable texts that approximately conform to the CEFR level A2. Two types of texts can be requested: Explanation texts or stories.

Below you can find the instructions for setting up and running the project. For more information please see the wiki of this repository.

## Installation

Make sure you have [poetry](https://python-poetry.org/) and [yarn](https://classic.yarnpkg.com/en/) installed. You can obtain them via the package manager of your system. Clone this repository and install the project dependencies:

```
git clone [github-url]
cd erklartextgen
poetry install
```

Execute the following to download the dependencies used for NLP processing:

```
poetry run python -m spacy download en_core_web_sm
poetry run python -m wn download oewn:2023
```

Obtain trained model files and auxiliary assets [here](https://drive.google.com/file/d/15KZWG-nOZ8F2VSKxWS4ESaIBow3lQliB/view?usp=sharing). Untar the archive and make sure that the folder `assets` is placed in your project directory.

```
tar -xvf assets.tar.gz
```

Install the frontend dependencies:

```
cd frontend
yarn install
```

Finally, copy the file `config/config.toml.example` to `config/config.toml` and configure all values. You are now ready to start using the application!

## Usage

First, start the backend:

```
poetry run flask --app erklartextgen.server run
```

Then, in a separate shell session, start the frontend:

```
cd frontend
yarn run dev
```

You can open the student view in your browser at http://localhost:5173 and the teacher view at http://localhost:5173/teacher.

## Development

Please see the further documentation in the wiki. While this project is not actively maintained, you might want to lint and format any changes you make using [ruff](https://docs.astral.sh/ruff/):

Please lint and format your code:
```
poetry run ruff lint
poetry run ruff format
```

Furthermore, two CLI utilities are provided for generating texts or printing raw evaluation scores, which might be useful for development:

```
# Generates a medium-length explanation text about 'cars'
poetry run generate "cars" 

# Prints the raw evaluation output for the given sentence
poetry run eval "This is a complex test text" 
```
