# Architecture

This project has three main components:

## Backend

The backend provides an API with a single HTTP endpoint `/generate_text` and is called by our frontend with parameters such as the desired text length, text type, and topic.

## Frontend

The frontend is a web application that can be accessed within the browser. For more information see the README of this project or the wiki page 'Project structure'.

## Evaluation

We implemented a list of evaluation metrics to judge the quality of generated texts. They are implemented within the directory `erklartextgen/evaluation`. Below you can find a list of the categories and metrics that we have implemented (every metric is `prefixed` by the name of the submodule in which it is implemented):

- **CEFR**
  - `cefr_j`: CEFR-J level classifier
  - `bert_efcamdat`: distilBERT classifier trained on the EFCAMDAT dataset
  - `efflex`: CEFR level analyzer using the EFLLex vocabulary dataset
- **Readability**
  - `metrics`: Flesch Reading Ease Score
  - `metrics`: Flesch-Kincaid readability formula
  - `metrics`: SMOG index
  - `metrics`: Gunning Fog index
  - `metrics`: Automated Readability Index (ARI)
  - `metrics`: Coleman-Liau index
- **Linguistic**
  - `forms`: Measures advanced linguistic forms
  - `indicators`: Structural complexity indicators
  - `indicators`: Ambiguity indicators
- **Safety**
  - `detoxify`: Toxicity analysis using the detoxify model/package
- **Stylistic**
  - `gpt4`: Stylistic analysis using a GPT4o "discriminator"
- **Text length**
  - `evaluation`: Simple measure of the text length 
  
Note that this repository contains a `bibliography.bib` file that provides references to nearly all implemented evaluation metrics. Within the source code you can find BibTeX keys for the associated papers if you wish to look into them closer

Every evaluation metric implementation contains a function `compute_scores` that returns the raw scores and a function `compute_loss` that returns an error value to the targets that have been set for this project (documented within the code).
