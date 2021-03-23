import pandas as pd
from typing import Any, List, Tuple, Union
from pandas.core.frame import DataFrame
from pandas.core.series import Series


def skim(
    obj: Union[pd.DataFrame, pd.Series],
    column: str = None,
    groupby: str = None,
    columns: List[str] = None
) -> List:
    """Summarize data present in dataframe"""
    if not is_dataframe(obj) or not is_series(obj):
        raise AttributeError('Error: {} passed: please pass a Pandas DataFrame or Series as argument.')

def is_dataframe(obj: Any) -> bool:
    """Check if passed object is a pandas Dataframe"""
    return True if isinstance(obj, pd.DataFrame) else False


def is_series(obj: Any) -> bool:
    """Check if passed object is a pandas Series"""
    return True if isinstance(obj, pd.Series) else False

def __shape(obj: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
    row, col = obj.shape
    return pd.DataFrame(data=[[row], [col]], columns=['Values'], index=['Number of rows', 'Number of columns'])

def __dtype_freq(obj: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
    pass