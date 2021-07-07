from typing import Dict, List, Optional
import pytest
import pandas as pd
from po.skim import skim, Skimer


@pytest.fixture
def dummy_types():
    data = {
        "a_dict": {1: ['a', 'e', 'i', 'o', 'u'], 2: ['b', 'c', 'd', 'f', 'g']},
        "a_list": [1, 2, 3],
        "a_str": "string",
        "a_serie": pd.Series([1, 2, 3]),
    }
    return data


@pytest.fixture
def iris_csv():
    return pd.read_csv("tests/data/iris.csv")


def test_skim_should_raise_error_if_incorrect_type_is_passed(dummy_types):
    types = ["a_dict", "a_list", "a_str", "a_serie"]
    for type in types:
        with pytest.raises(TypeError):
            skim(dummy_types[type])


def test_dataframe_summary_on_iris_dataset(iris_csv):
    sk_summary = Skimer(data=iris_csv, name="Iris").summary
    expected_summary = [
        ("Number of rows", "150"),
        ("Number of columns", "5"),
        ("The frequency of float64", "4"),
        ("The frequency of object", "1")
        ]
    assert sk_summary == expected_summary


def test_numeric_summary_returns_on_iris_dataset(iris_csv):
    sk_numeric: Optional[Dict[str, List]] = Skimer(data=iris_csv, name="Iris").numeric
    assert sk_numeric["variable"] == ["sepal_length", "sepal_width",
                                      "petal_length", "petal_width"]
    assert sk_numeric["missing"] == ["0", "0", "0", "0"]
    assert sk_numeric["min"] == ["4.3", "2.0", "1.0", "0.1"]
    assert sk_numeric["max"] == ["7.9", "4.4", "6.9", "2.5"]
    assert sk_numeric["mean"] == ["5.843", "3.054", "3.759", "1.199"]
    assert sk_numeric["sd"] == ["0.828", "0.434", "1.764", "0.763"]
    assert sk_numeric["q0"] == ["4.3", "2.0", "1.0", "0.1"]
    assert sk_numeric["q25"] == ["5.1", "2.8", "1.6", "0.3"]
    assert sk_numeric["q50"] == ["5.8", "3.0", "4.35", "1.3"]
    assert sk_numeric["q75"] == ["6.4", "3.3", "5.1", "1.8"]
    assert sk_numeric["q100"] == ["7.9", "4.4", "6.9", "2.5"]
