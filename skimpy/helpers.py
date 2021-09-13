import pandas as pd
import numpy as np
from typing import List, Optional, Tuple
from collections import Counter

# from pyspark.sql import DataFrame

TYPES = {
    "numeric": [
        "int8",
        "int16",
        "int32",
        "int64",
        "uint8",
        "uint16",
        "uint32",
        "uint64",
        "float16",
        "float32",
        "float64",
        "float128"
        ],
    "object": [
        "object"
        ],
    "category": [
        "category"
    ]
}


def columns_with_type(
    data: pd.DataFrame,
    dtype: str
) -> pd.DataFrame:
    """
    Select all columns with the specified type.

    Args:
    -----
    - data:
    - dtype: string can be "numeric", "object", "category" or "date"

    Return:
    -------
    A pandas DataFrame
    """
    def is_type_in(_dtype: str) -> bool:
        return _dtype in TYPES[dtype]
    alltypes = [str(dtype) for dtype in data.dtypes.unique()]
    filtered_type = list(filter(is_type_in, alltypes))
    try:
        return data.select_dtypes(include=filtered_type)
    except ValueError:
        return pd.DataFrame()


def list_columns(
    data: pd.DataFrame
) -> List:
    """
    Function defined to select all columns with a specified type.

    Args:
    -----
    - data:

    Return:
    -------

    """
    return list(data)


def calculate_quantiles(
    data: pd.DataFrame
) -> Tuple[List[str], ...]:
    """
    Calculate quantiles of a Pandas Series

    Args:
    -----
    - data: a pandas DataFrame

    Return:
    -------
    A tuple(list(str...))
    """
    q0, q25, q50, q75, q100 = data.quantile([.0, .25, .50, .75, 1.0]).values
    q0 = [str(value) for value in q0]
    q25 = [str(value) for value in q25]
    q50 = [str(value) for value in q50]
    q75 = [str(value) for value in q75]
    q100 = [str(value) for value in q100]
    return (q0, q25, q50, q75, q100)


def calculate_means(
    data: pd.DataFrame,
    columns: List[str]
) -> List[str]:
    """
    Calculate the mean of all Pandas Dataframe columns

    Args:
    -----
    - data: a pandas DataFrame
    - columns: a list of string with columns names

    Return:
    -------
    A list of string for formating purpose with rich
    """
    return [str(round(data[column].mean(), 3)) for column in columns]


def calculate_sd(
    data: pd.DataFrame,
    columns: List[str]
) -> List[str]:
    """
    Calculate the standard deviation of all Pandas Dataframe columns

    Args:
    -----
    - data: a pandas DataFrame
    - columns: a list of string with columns names

    Return:
    -------
    A list of string for formating purpose with rich
    """
    return [str(round(data[column].std(), 3)) for column in columns]


def calculate_skew(
    data: pd.DataFrame,
    columns: List[str],
    skipna: Optional[bool] = None
) -> List[str]:
    """
    Calculate the skew factors of all Pandas Dataframe columns

    Args:
    -----
    - data: a pandas DataFrame
    - columns: a list of string with columns names
    - skipna: a boolean, to take into account np.na values

    Return:
    -------
    A list of string for formating purpose with rich
    """
    return [str(round(data[column].skew(skipna=skipna), 3)) for column in columns]


def calculate_kurosis(
        data: pd.DataFrame,
        columns: List[str],
        skipna: Optional[bool] = None
) -> List[str]:
    """
    Calculate the kurtosis of all Pandas Dataframe columns

    Args:
    -----
    - data: a pandas DataFrame
    - columns: a list of string with columns names
    - skipna: a boolean, to take into account np.na values

    Return:
    -------
    A list of string for formating purpose with rich
    """
    return [str(round(data[column].kurtosis(skipna=skipna), 3))
            for column in columns]


def spark_bar(
    data: pd.Series,
    bins: int = 10
) -> str:
    """
    Draw histogram from an array of data points

    Args:
    -----
    - data: a pandas Series
    - bins: an int that defines the number of bins (10 by default)

    Return:
    -------
    A string of rectangle unicode
    """
    bars = u" ▁▂▃▄▅▆▇█"
    _data = data[~data.isna()]
    n, _ = np.histogram(_data, bins=bins)
    temp = n * (len(bars) - 1) // (max(n))
    hist = u"".join(bars[i] for i in temp)
    return hist


def draw_distribitions(
    data: pd.DataFrame,
    columns: List[str]
) -> List[str]:
    return [spark_bar(data[column]) for column in columns]


def count_types_freq(
    data: pd.DataFrame
) -> Counter:
    """
    TODO
    """
    types: List[str] = [str(dtype) for dtype in data.dtypes]
    return Counter(types)


def count_columns_values(
    data: pd.DataFrame,
    columns: List[str]
) -> List[str]:
    """
    TODO
    """
    return [str(data[column].count()) for column in columns]


def count_missing_values(
    data: pd.DataFrame,
    columns: List[str]
) -> List[str]:
    """
    TODO
    """
    return [str(data[column].isnull().sum()) for column in columns]


def columns_min_max(
    data: pd.DataFrame,
    columns: List[str]
) -> Tuple[List[str], ...]:
    """
    TODO
    """
    _min = [str(int(data[column].loc[~data[column].isna()].min())) for column in columns]
    _max = [str(int(data[column].loc[~data[column].isna()].max())) for column in columns]
    return (_min, _max)


def columns_lenmin_lenmax(
    data: pd.DataFrame,
    columns: List[str]
) -> Tuple[List[str], ...]:
    """
    TODO
    """
    length_df = data.copy()
    for column in columns:
        length_df[column] = length_df[column].str.len()
    return columns_min_max(length_df, columns)


def count_empty_strings(
    data: pd.DataFrame,
    columns: List[str]
) -> List[str]:
    """
    TODO
    """
    return [str((data[column] == "").sum()) for column in columns]


def count_distinct(
    data: pd.DataFrame,
    columns: List[str]
) -> List[str]:
    """
    TODO
    """
    return [str(data[column].unique().size) for column in columns]

