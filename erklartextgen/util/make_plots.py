import jsonlines
import csv
import pandas as pd
import matplotlib.pyplot as plt


def read_qualitative_dataset(path):
    with open(path) as csvfile:
        reader = csv.reader(csvfile)

        quality_rating = []
        a2_rating = []
        for row in reader:
            quality_rating.append(int(row[2]))
            a2_rating.append(row[3] == "A2")

        return pd.DataFrame({"quality": quality_rating, "quality_a2": a2_rating})


# Function to read a JSONLines file into a Pandas DataFrame
def read_jsonlines(file_path):
    data = []
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            obj = obj["eval"]
            data_obj = {
                "cefr_efllex": obj["cefr"]["efllex"],
                "cefr_j": obj["cefr"]["cefr_j"],
                "cefr_efcamdat": obj["cefr"]["bert_efcamdat"],
                "readability": obj["readability"],
                "safety": obj["safety"],
                "stylistic": obj["stylistic"],
                "text_length": obj["text_length"],
            }

            data.append(data_obj)
    return pd.DataFrame(data)


df = read_jsonlines("datasets/eval_output_mistral_w_len.jsonl")
df2 = read_jsonlines("datasets/eval_output_erklarmistral_w_len.jsonl")

qf1 = read_qualitative_dataset("datasets/qualitative_eval_mistral.csv")
qf2 = read_qualitative_dataset("datasets/qualitative_eval_finetune.csv")

# num_columns = len(df.columns)
# num_plots = sum(pd.api.types.is_numeric_dtype(df[col]) for col in df.columns)
# cols = 3
# rows = (num_plots // cols) + (num_plots % cols > 0)

fig, axes = plt.subplots(3, 3, figsize=(15, 15))
axes = axes.flatten()

labels = [
    "cefr_efllex loss (Wasserstein distance)",
    "cefr_j loss (RMSE)",
    "cefr_efcamdat loss (RMSE)",
    "readability loss (RMSE)",
    "safety loss (RMSE)",
    "stylistic loss (RMSE)",
    "text_length loss (RMSE)",
]

idx = 0
for column in df.columns:
    if pd.api.types.is_numeric_dtype(df[column]):
        axes[idx].hist(df[column], alpha=0.5, label="x")
        axes[idx].hist(df2[column], alpha=0.5, label="y")
        axes[idx].set_xlabel(labels[idx])
        axes[idx].set_ylabel("Frequency")
        idx += 1


ratings_hist1 = qf1["quality"].value_counts().sort_index()
axes[idx].bar([0, 1, 2, 3, 4, 5], ratings_hist1, alpha=0.5)
ratings_hist2 = qf2["quality"].value_counts().sort_index()
axes[idx].bar([0, 1, 2, 3, 4], ratings_hist2, alpha=0.5)
axes[idx].set_xlabel("Subjective rating (qualitative eval)")
axes[idx].set_ylabel("Frequency")
idx += 1

a2_ratings_hist1 = qf1["quality_a2"].value_counts().sort_index()
axes[idx].bar(["False", "True"], a2_ratings_hist1, alpha=0.5)
a2_ratings_hist2 = qf2["quality_a2"].value_counts().sort_index()
axes[idx].bar(["False", "True"], a2_ratings_hist2, alpha=0.5)
axes[idx].set_xlabel("Is CEFR A2? (qualitative eval)")
axes[idx].set_ylabel("Frequency")

# Hide any unused subplots
# for i in range(idx, len(axes)):
#     axes[i].set_visible(False)

plt.tight_layout()
plt.savefig("foo.png")

# print(df.describe())
# print(df2.describe())

# plot_histograms_subplots(df, df2)
