# Project structure

To give you an overview over this project you can find a list of relevant folders below:

```
.
├── bibliography.bib - contains citations of prior art
├── config - contains an example configuration file for the project
├── docs - contains the documentation that you are currently reading
├── erklartextgen - contains the main code of this project
├── frontend - contains the code for the frontend
├── notebooks - contains Jupyter notebooks that have been used for model training and experiments
├── pyproject.toml - contains a specification of all project dependencies
├── README.md
```

## Frontend

Within the `frontend` directory, the `src` directory contains the implementation of our frontend. It was built using the web framework [Vue.js](https://vuejs.org/).

## Main code

The folder `erklartextgen` is the Python package that contains the main code of this project. Below are the relevant files/folders:

```
.
├── backend - contains text generation backends, currently only ollama is implemented
│   ├── __init__.py
│   ├── ollama.py
├── cli.py - contains a CLI that provides the 'generate' and 'eval' commands (see README)
├── config.py - contains utilities for parsing the configuration file
├── evaluation - contains implementations of text evaluation methods, structured by category
│   ├── cefr 
│   ├── __init__.py
│   ├── linguistic
│   ├── pipeline.py
│   ├── readability
│   ├── safety
│   ├── stylistic
│   └── text_length
├── generation.py - contains text generation functionality (e.g. oversampling, postprocessing)
├── prompting.py - contains the generation/templating of prompts
├── server.py - contains the backend code
└── util - contains various utility scripts that have been used for experiments/dataset transformations
```
