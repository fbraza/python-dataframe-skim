import pandas as pd
from typing import Any, List, Union
from collections import Counter


def skim_df(
    obj: Union[pd.DataFrame, pd.Series],
    column: str = None,
    columns: List[str] = None
) -> List:
    """Summarize data present in dataframe

    Raise
    -----
    An AttributeError if an object other than Series / DataFrame is passed
    as a parameter
    """
    pass


def is_dataframe(obj: Any) -> bool:
    """Check if passed object is a pandas Dataframe"""
    return True if isinstance(obj, pd.DataFrame) else False


def data_summary(obj: pd.DataFrame) -> pd.DataFrame:
    """Function defined to return a concatenated dataframe containing
    details about the number of row and columns and the column dtype
    frequency of the passed dataframe or series object"""
    def __shape(obj: pd.DataFrame) -> pd.DataFrame:
        """Function defined to return a dataframe with details about
        the number of row and columns"""
        row, col = obj.shape
        return pd.DataFrame(data=[[row], [col]],
                            columns=['Values'],
                            index=['Number of rows', 'Number of columns'])

    def __dtype_freq(obj: pd.DataFrame) -> pd.DataFrame:
        """Function defined to return a dataframe with details about
        the pandas dtypes frequency"""
        types = [str(key) for key in Counter(obj.dtypes).keys()]
        values = [[value] for value in Counter(obj.dtypes).values()]
        return pd.DataFrame(data=values, columns=['Values'], index=types)
    return pd.concat([__shape(obj), __dtype_freq(obj)])


def summary_by_type(obj: pd.DataFrame) -> None:
    types = [str(key) for key in Counter(obj.dtypes).keys()]


def numeric_summary(obj: pd.DataFrame):
    columns = obj.columns

