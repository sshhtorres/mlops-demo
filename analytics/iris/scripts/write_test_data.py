import pathlib
import os

import numpy as np

from .cli import parse_dir
from .data import load_iris_data, X_TEST_DATA_FILE_NAME, Y_TEST_DATA_FILE_NAME


def write_iris_test_data(dir_dest: pathlib.Path):
    _, X_test, _, y_test = load_iris_data()

    os.makedirs(dir_dest, exist_ok=True)

    with open(dir_dest / X_TEST_DATA_FILE_NAME, "w") as f:
        for features in X_test:
            features_str = ",".join(map(str, features))
            f.write(f"{features_str}\n")

    with open(dir_dest / Y_TEST_DATA_FILE_NAME, "w") as f:
        for label in y_test:
            f.write(f"{label}\n")


if __name__ == "__main__":
    dir_dest = parse_dir()
    write_iris_test_data(dir_dest)
    print(f"Wrote test data to \"{dir_dest}\"")
