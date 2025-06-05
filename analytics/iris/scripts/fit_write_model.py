import pathlib
import os

from sklearn.linear_model import LogisticRegression

from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

from .cli import parse_dir_and_name
from .data import load_iris_data


def fit_onnx_model():
    X_train, _, y_train, _ = load_iris_data()

    clr = LogisticRegression()
    clr.fit(X_train, y_train)

    initial_type = [('float_input', FloatTensorType([None, 4]))]
    onx = convert_sklearn(clr, initial_types=initial_type)
    
    return onx


def write_onnx_model(filepath, onnx_model):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "wb") as f:
        f.write(onnx_model.SerializeToString())


if __name__ == "__main__":
    filepath = parse_dir_and_name()
    onnx_model = fit_onnx_model()
    write_onnx_model(filepath, onnx_model)
    print(f'Model saved to "{filepath}"')
