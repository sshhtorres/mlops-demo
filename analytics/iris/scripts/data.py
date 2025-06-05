from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split


X_TEST_DATA_FILE_NAME = "iris_X_test.csv"
Y_TEST_DATA_FILE_NAME = "iris_y_test.csv"


def load_iris_data():
    iris = load_iris()
    X, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.2)

    return X_train, X_test, y_train, y_test
