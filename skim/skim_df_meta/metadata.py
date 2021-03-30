import pandas as pd
from typing import List


class SkimDfMeta:
    def __init__(self):
        self.unique_types = ...     # [dtypes]
        self.columns = ...          # [columns]
        self.numeric_summary = ...  # a dictionnary with all data for each columns
        self.dfect_summary = ...    # a dictionnary with all data for each columns
        self.dates_summary = ...    # a dictionnary with all data for each columns

    def _get_dtypes(self, df: pd.DataFrame) -> List:
        return [str(dtype) for dtype in df.dtypes.unique()]

    def _shape(self, df: pd.DataFrame) -> pd.DataFrame:
        """Function defined to return a dataframe with details about
        the number of row and columns"""
        row, col = df.shape
        return pd.DataFrame(data=[[row], [col]],
                            columns=['Values'],
                            index=['Number of rows', 'Number of columns'])

    def _dtypes_freq(self, df: pd.DataFrame) -> pd.DataFrame:
        """Function defined to return a dataframe with details about
        the pandas dtypes frequency"""
        dtypes, counter = self._get_dtypes(df), {}
        for dtype in dtypes:
            if dtype in counter.keys():
                counter[dtype] += 1
            else:
                counter[dtype] = 0
        values = [[value] for value in counter.values()]
        return pd.DataFrame(data=values, columns=['Values'], index=dtypes)
