# erklarmistral

For this project we have fine-tuned a Mistral LLM model which can be downloaded [here](https://drive.google.com/file/d/1X1otk-6zchtARjbn5FpjChYuoTiILgav/view?usp=sharing) in the GGUF format. The model was trained using a subset of the Simple English Wikipedia, that has been classified as approximately conforming to the CEFR level A2. We trained the initial classifier [on this dataset](https://www.kaggle.com/datasets/amontgomerie/cefr-levelled-english-texts/code). For more information on the methodology please consult the file `notebooks/cefr_classifier.ipynb` and the file `erklartextgen/util/preprocess_dataset.py`.

Our fine-tuned model performed significantly worse (w.r.t. the evaluation metrics implemented within this project) than a pre-trained Mistral model. Nevertheless, if you want to play around with it, you can import the GGUF model file into ollama by using the following `Modelfile`:

```
FROM ./unsloth.Q4_K_M.gguf

TEMPLATE """
Below are some instructions that describe a task. Write responses that appropriately complete each request.

### Input:
{{ .Prompt }}

### Response:"""

PARAMETER stop <s>
PARAMETER stop </s>
```

and importing the model using `ollama create erklarmistral -f Modelfile`. Please consult the ollama documentation for more detailed [information on importing models](https://github.com/ollama/ollama/blob/main/docs/import.md). You can then adjust then `config.toml` of erklartextgen to make use of the newly imported model.
