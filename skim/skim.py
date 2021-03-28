import pandas as pd
from typing import Any, List, Union
from collections import Counter


def skim(
    obj: Union[pd.DataFrame, pd.Series],
    column: str = None,
    groupby: str = None,
    columns: List[str] = None
) -> List:
    """Summarize data present in dataframe

    Raise
    -----
    An AttributeError if an object other than Series / DataFrame is passed
    as a parameter
    """
    check_types(obj)


def check_types(obj: Any) -> None:
    if not is_dataframe(obj) or not is_series(obj):
        raise AttributeError('''Error: {} passed: please pass a Pandas DataFrame
            or Series as argument.''')


def is_dataframe(obj: Any) -> bool:
    """Check if passed object is a pandas Dataframe"""
    return True if isinstance(obj, pd.DataFrame) else False


def is_series(obj: Any) -> bool:
    """Check if passed object is a pandas Series"""
    return True if isinstance(obj, pd.Series) else False


def data_summary(obj: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
    """Function defined to return a concatenated dataframe containing
    details about the number of row and columns and the column dtype
    frequency of the passed dataframe or series object"""
    def __shape(obj: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
        """Function defined to return a dataframe with details about
        the number of row and columns"""
        row, col = obj.shape
        return pd.DataFrame(data=[[row], [col]],
                            columns=['Values'],
                            index=['Number of rows', 'Number of columns'])

    def __dtype_freq(obj: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
        """Function defined to return a dataframe with details about
        the pandas dtypes frequency"""
        types = [str(key) for key in Counter(obj.dtypes).keys()]
        values = [[value] for value in Counter(obj.dtypes).values()]
        return pd.DataFrame(data=values, columns=['Values'], index=types)
    return pd.concat([__shape(obj), __dtype_freq(obj)])


def summary_by_type(obj: Union[pd.DataFrame, pd.Series]) -> None:
    types = [str(key) for key in Counter(obj.dtypes).keys()]