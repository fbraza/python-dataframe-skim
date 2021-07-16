import pandas as pd
import pytest
from skimpy.helpers import columns_with_type, list_columns


@pytest.fixture
def iris_csv():
    return pd.read_csv("tests/data/iris.csv")


def test_list_columns_should_return_a_list_of_columns_name(iris_csv):
    exp_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    res_cols = list_columns(iris_csv)
    assert exp_cols == res_cols


def test_columns_with_type_dtype_numeric_should_return_numeric_cols(iris_csv):
    exp_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    res_cols = columns_with_type(iris_csv, "numeric")
    assert exp_cols == list_columns(res_cols)


def test_columns_with_type_dtype_object_should_return_object_cols(iris_csv):
    exp_cols = ['species']
    res_cols = columns_with_type(iris_csv, "object")
    assert exp_cols == list_columns(res_cols)


def test_columns_with_type_dtype_category_should_return_no_cols(iris_csv):
    exp_cols = []
    res_cols = columns_with_type(iris_csv, "category")
    assert exp_cols == list_columns(res_cols)
