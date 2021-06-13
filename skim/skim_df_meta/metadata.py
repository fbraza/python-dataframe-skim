import pandas as pd
import numpy as np
from typing import Union


class SkimDfDataSummary:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.types = [str(dtype) for dtype in df.dtypes.unique()]
        self.summary = self.data_summary()
        self.numeric = self.numeric_summary()

    def data_summary(self) -> pd.DataFrame:
        """
        Function defined to return a concatenated dataframe containing
        details about the number of row and columns and the column dtype
        frequency of the passed dataframe or series object
        """
        def _shape() -> pd.DataFrame:
            """
            Function defined to return a dataframe with details about
            the number of row and columns
            """
            row, col = self.df.shape
            return pd.DataFrame(data=[[row], [col]],
                                columns=['Values'],
                                index=['Number of rows', 'Number of columns'])

        def _dtypes_freq() -> pd.DataFrame:
            """
            Function defined to return a dataframe with details about
            the pandas dtypes frequency
            """
            counter, types = {}, self.df.dtypes
            for dtype in types:
                tmp = str(dtype)
                if tmp in counter.keys():
                    counter[tmp] += 1
                else:
                    counter[tmp] = 1
            values = [[value] for value in counter.values()]
            return pd.DataFrame(
                data=values,
                columns=['Values'],
                index=list(counter.keys())
                )
        return pd.concat([_shape(), _dtypes_freq()])

    def numeric_summary(self, bins: int = 10) -> Union[pd.DataFrame, None]:
        # check if dataframe has numeric values
        df = self._select_numeric()
        if df.columns.size == 0:
            return None
        # initialize the calculations and record in a dictionnary
        cols = list(df.columns)
        q0, q25, q50, q75, q100 = df.quantile([.0, .25, .50, .75, 1.0]).values
        summary_record = {
            "variable": cols[:4],
            "n_missing": [df[col].isnull().sum() for col in cols],
            "mean": [df[col].mean() for col in cols],
            "sd": [df[col].mean() for col in cols],
            "q0": q0,
            "q25": q25,
            "q50": q50,
            "q75": q75,
            "q100": q100,
            "hist": [self._hist(df[col], bins=bins) for col in cols]
        }
        return pd.DataFrame(summary_record)

    def _select_numeric(self) -> pd.DataFrame:
        """
        Function defined to select all DataFrame columns with a numeric dtype
        """
        def _is_numeric(dtype: str) -> bool:
            types = [
                'int8', 'int16', 'int32', 'int64',
                'uint8', 'uint16', 'uint32', 'uint64',
                'float16', 'float32', 'float64', 'float128'
            ]
            return dtype in types
        dtypes = list(filter(_is_numeric, self.types))
        return self.df.select_dtypes(include=dtypes)

    def _hist(self, data: pd.DataFrame, bins: int = 10) -> str:
        bars = u' ▁▂▃▄▅▆▇█'
        n, _ = np.histogram(data, bins=bins)
        temp = n * (len(bars) - 1) // (max(n))
        hist = u"".join(bars[i] for i in temp)
        return hist


test = pd.read_csv("skim/iris.csv")
print(SkimDfDataSummary(test).numeric_summary())
