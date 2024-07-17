from sklearn.metrics import root_mean_squared_error


def compute_loss(score, target_len):
    return root_mean_squared_error([target_len], [score])


def compute_scores(doc):
    return len(doc)
