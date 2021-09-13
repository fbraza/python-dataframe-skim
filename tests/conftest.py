import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def iris_csv():
    return pd.read_csv("tests/data/iris.csv")


@pytest.fixture
def iris_sepal_length():
    data = pd.read_csv("tests/data/iris.csv")
    return data.sepal_length


@pytest.fixture
def iris_numeric():
    data = pd.read_csv("tests/data/iris.csv")
    return data.select_dtypes(include=np.number)


@pytest.fixture
def fake_data():
    values = [[4, 5, 6], [7, 8, 9], [1, 3, 0]]
    columns = ["column_1", "column_2", "column_3"]
    return pd.DataFrame(columns=columns, data=values)
