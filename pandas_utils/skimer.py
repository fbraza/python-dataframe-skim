import pandas as pd
import numpy as np
from typing import List, Union


class Skimer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric = self.numeric_summary()

    def numeric_summary(self, bins: int = 10) -> Union[dict, None]:
        # check if dataframe has numeric values
        df = self._select_numeric(self.df)
        if df.columns.size == 0:
            return None
        # initialize the calculations and record in a dictionnary
        cols = self._get_columns(df)
        q0, q25, q50, q75, q100 = self._get_quantiles(df)
        summary_record = {
            "variable": [str(col) for col in cols],
            "missing": [str(df[col].isnull().sum()) for col in cols],
            "min": [str(df[col].min()) for col in cols],
            "max": [str(df[col].max()) for col in cols],
            "mean": [str(round(df[col].mean(), 3)) for col in cols],
            "sd": [str(round(df[col].std(), 3)) for col in cols],
            "q0": [str(value) for value in q0],
            "q25": [str(value) for value in q25],
            "q50": [str(value) for value in q50],
            "q75": [str(value) for value in q75],
            "q100": [str(value) for value in q100],
            "dist": [self._hist(df[col], bins=bins) for col in cols]
        }
        return summary_record

    @staticmethod
    def _select_numeric(df: pd.DataFrame) -> pd.DataFrame:
        """
        Function defined to select all DataFrame columns with a numeric dtype
        """
        def _is_numeric(dtype: str) -> bool:
            """
            Function defined to determine if a column's dtype is numeric
            """
            types = ['int8', 'int16', 'int32', 'int64',
                     'uint8', 'uint16', 'uint32', 'uint64',
                     'float16', 'float32', 'float64', 'float128']
            return dtype in types
        alltypes = [str(dtype) for dtype in df.dtypes.unique()]
        numtypes = list(filter(_is_numeric, alltypes))
        return df.select_dtypes(include=numtypes)

    @staticmethod
    def _get_columns(df: pd.DataFrame) -> List:
        return list(df.columns)

    @staticmethod
    def _get_quantiles(df: pd.DataFrame) -> np.ndarray:
        return df.quantile([.0, .25, .50, .75, 1.0]).values

    @staticmethod
    def _hist(data: pd.Series, bins: int) -> str:
        bars = u' ▁▂▃▄▅▆▇█'
        n, _ = np.histogram(data, bins=bins)
        temp = n * (len(bars) - 1) // (max(n))
        hist = u"".join(bars[i] for i in temp)
        return hist
