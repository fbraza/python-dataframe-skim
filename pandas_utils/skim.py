import pandas as pd
import numpy as np
from typing import List, Union
from rich.console import Console
from rich.table import Table
from collections import Counter
from os import system


class Skimer:
    """
    """
    def __init__(self, data: pd.DataFrame, name: str = None):
        self.data = data
        self.name = name
        self.numeric = self.numeric_summary()
        self.summary = self.dataframe_summary()

    def dataframe_summary(self):
        dim = self.data.shape
        summary = [
            ("Number of rows", str(dim[0])),
            ("Number of columns", str(dim[1]))
            ]
        freq = self._get_types_freq(self.data)
        for k, v in freq.items():
            summary.append(("The frequency of {}".format(k), str(v)))
        return summary

    def numeric_summary(self, bins: int = 10) -> Union[dict, None]:
        """Function defined to return statistics about numeric types present
        in a DataFrame

        Parameters:
        -----------
        - bins: int

            used to determine the required bin for the histogram

        Return:
        -------
        - dict or None:

        A dictionnary with all statistics or `None` if the DataFrame has no
        numeric values
        """
        data = self._select_numeric(self.data)
        if data.columns.size == 0:
            return None
        else:
            cols = self._get_columns(data)
            q0, q25, q50, q75, q100 = self._get_quantiles(data)
            summary = {
                "variable": [str(col) for col in cols],
                "missing": [str(data[col].isnull().sum()) for col in cols],
                "min": [str(data[col].min()) for col in cols],
                "max": [str(data[col].max()) for col in cols],
                "mean": [str(round(data[col].mean(), 3)) for col in cols],
                "sd": [str(round(data[col].std(), 3)) for col in cols],
                "q0": [str(value) for value in q0],
                "q25": [str(value) for value in q25],
                "q50": [str(value) for value in q50],
                "q75": [str(value) for value in q75],
                "q100": [str(value) for value in q100],
                "dist": [self._hist(data[col], bins=bins) for col in cols]
            }
            return summary

    @staticmethod
    def _select_numeric(data: pd.DataFrame) -> pd.DataFrame:
        """
        Function defined to select all DataFrame columns with a numeric
        dtype
        """
        def _is_numeric(dtype: str) -> bool:
            """
            Function defined to determine if a column's dtype is numeric
            """
            types = [
                'int8', 'int16', 'int32', 'int64',
                'uint8', 'uint16', 'uint32', 'uint64',
                'float16', 'float32', 'float64', 'float128'
                ]
            return dtype in types
        alltypes = [str(dtype) for dtype in data.dtypes.unique()]
        numtypes = list(filter(_is_numeric, alltypes))
        return data.select_dtypes(include=numtypes)

    @staticmethod
    def _get_columns(data: pd.DataFrame) -> List:
        return list(data.columns)

    @staticmethod
    def _get_quantiles(data: pd.DataFrame) -> np.ndarray:
        return data.quantile([.0, .25, .50, .75, 1.0]).values

    @staticmethod
    def _hist(data: pd.Series, bins: int) -> str:
        bars = u' ▁▂▃▄▅▆▇█'
        n, _ = np.histogram(data, bins=bins)
        temp = n * (len(bars) - 1) // (max(n))
        hist = u"".join(bars[i] for i in temp)
        return hist

    @staticmethod
    def _get_types_freq(data: pd.DataFrame) -> Counter:
        types = [str(dtype) for dtype in data.dtypes]
        return Counter(types)


def skim(data: pd.DataFrame) -> None:
    """
    Summarize data present in a Pandas DataFrame

    Parameters:
    -----------
    - data: A Pandas DataFrame

    Raise
    -----
    An TypeError if an object other than a Pandas DataFrame is passed
    as an argument
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("The skim functions only accepts Pandas DataFrames")
    console = Console()
    sk_summary = Skimer(data).summary
    sk_numeric = Skimer(data).numeric
    # sk_object: TODO
    # sk_dates: TODO
    # sk_category: TODO

    def _build_num(summary: Union[dict, None]) -> Union[Table, None]:
        if summary is None:
            return
        else:
            columns, values = summary.keys(), list(summary.values())
            size = len(values[0])
            rows = [[row[i] for row in values] for i in range(size)]
            grid = Table(show_header=True, header_style="bold magenta")
            for col in columns:
                grid.add_column(col)
            for row in rows:
                grid.add_row(*row)
            return grid

    def _build_sum(summary: List) -> Table:
        grid = Table(show_header=True, header_style="bold magenta")
        columns = ["", "Values"]
        rows = summary
        for col in columns:
            grid.add_column(col)
        for row in rows:
            grid.add_row(*row)
        return grid

    system('clear')
    console.print(" [u][bold]Data Summary[/bold][/u]")
    console.print(_build_sum(sk_summary))
    print()
    console.print(" [u][bold]Variable Type: Numeric[/bold][/u]")
    console.print(_build_num(sk_numeric))


data = pd.read_csv("tests/data/iris.csv")
skim(data)
