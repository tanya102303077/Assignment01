import pandas as pd
import numpy as np

def run_topsis(input_file, weights, impacts, output_file):
    data = pd.read_csv(input_file)

    if data.shape[1] < 3:
        raise Exception("Input file must have at least 3 columns")

    matrix = data.iloc[:, 1:].values

    try:
        matrix = matrix.astype(float)
    except:
        raise Exception("All criteria values must be numeric")

    weights = np.array(list(map(float, weights.split(","))))
    impacts = impacts.split(",")

    if len(weights) != matrix.shape[1]:
        raise Exception("Weights count mismatch")

    norm = matrix / np.sqrt((matrix ** 2).sum(axis=0))
    weighted = norm * weights

    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == "+":
            ideal_best.append(weighted[:, i].max())
            ideal_worst.append(weighted[:, i].min())
        else:
            ideal_best.append(weighted[:, i].min())
            ideal_worst.append(weighted[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = dist_worst / (dist_best + dist_worst)
    rank = score.argsort()[::-1].argsort() + 1

    data["Topsis Score"] = score
    data["Rank"] = rank

    data.to_csv(output_file, index=False)
