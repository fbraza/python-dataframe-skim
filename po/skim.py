import pandas as pd
import numpy as np
from typing import Dict, List, Union, Tuple
from rich.console import Console
from rich.table import Table
from collections import Counter, defaultdict
from dataclasses import dataclass


TYPES = {
    "numeric": [
        'int8',
        'int16',
        'int32',
        'int64',
        'uint8',
        'uint16',
        'uint32',
        'uint64',
        'float16',
        'float32',
        'float64',
        'float128'
        ],
    "object": [
        'object'
        ]
}


@dataclass
class Skimer:
    """
    """
    data: pd.DataFrame
    name: str = "My Dataset"
    _summary: Dict[str, List] = defaultdict(list)
    _numeric: Dict[str, List] = defaultdict(list)

    def __post_init__(self):
        self.rows: int = self.data.shape[0]
        self.cols: int = self.data.shape[1]

    def _set_summary(self, **kwargs):
        """
        TODO
        """
        self._summary[" "] = ["Number of rows", "Number of columns"]
        self._summary["Values"] = [str(self.rows), str(self.cols)]
        dtypes_freq = count_types_freq(self.data)
        for k, v in dtypes_freq.items():
            self._summary[" "].append("The frequency of {}".format(k))
            self._summary["Values"].append(str(v))

    def _set_numeric(self, bins: int = 10):
        """
        TODO
        """
        data = columns_with_type(self.data, "numeric")
        cols = columns_to_list(data)
        if not cols:
            self._numeric["Empty"] = [True]
        q0, q25, q50, q75, q100 = calculate_quantiles(data)
        _min, _max = columns_min_max(data, cols)
        self._numeric["Variable"] = cols
        self._numeric["Count_total"] = count_columns_values(data, cols)
        self._numeric["Count_missing"] = count_missing_values(data, cols)
        self._numeric["Min"] = _min
        self._numeric["Max"] = _max
        # mean
        # sd
        self._numeric["q0"] = q0
        self._numeric["q25"] = q25
        self._numeric["q50"] = q50
        self._numeric["q75"] = q75
        self._numeric["q100"] = q100
        # is_normal ?
        # skew factor
        # Distribution

        #     "mean": [str(round(data[col].mean(), 3)) for col in cols],
        #     "sd": [str(round(data[col].std(), 3)) for col in cols],
        #     "dist": [self._hist(data[col], bins=bins) for col in cols]
        # }


def columns_with_type(data: pd.DataFrame, dtype: str) -> pd.DataFrame:
    """
    Function defined to select all DataFrame columns with a specified
    type. You can choose between numeric, object, category and date.
    """
    def is_type_in(_dtype: str) -> bool:
        return _dtype in TYPES[dtype]
    alltypes = [str(dtype) for dtype in data.dtypes.unique()]
    filtered_type = list(filter(is_type_in, alltypes))
    return data.select_dtypes(include=filtered_type)


def columns_to_list(data: pd.DataFrame) -> List:
    """
    TODO
    """
    return list(data.columns)


def calculate_quantiles(data: pd.DataFrame) -> Tuple[List[str], ...]:
    """
    TODO
    """
    q0, q25, q50, q75, q100 = data.quantile([.0, .25, .50, .75, 1.0]).values
    q0 = [str(value) for value in q0]
    q25 = [str(value) for value in q25]
    q50 = [str(value) for value in q50]
    q75 = [str(value) for value in q75]
    q100 = [str(value) for value in q100]
    return (q0, q25, q50, q75, q100)


def spark_bar(data: pd.Series, bins: int) -> str:
    """
    TODO
    """
    bars = u' ▁▂▃▄▅▆▇█'
    n, _ = np.histogram(data, bins=bins)
    temp = n * (len(bars) - 1) // (max(n))
    hist = u"".join(bars[i] for i in temp)
    return hist


def count_types_freq(data: pd.DataFrame) -> Counter:
    """
    TODO
    """
    types = [str(dtype) for dtype in data.dtypes]
    return Counter(types)


def count_columns_values(data: pd.DataFrame, columns: List[str]) -> List[str]:
    """
    TODO
    """
    return [str(data.column.count()) for column in columns]


def count_missing_values(data: pd.DataFrame, columns: List[str]) -> List[str]:
    """
    TODO
    """
    return [str(data.column.isnull().sum()) for column in columns]


def columns_min_max(data: pd.DataFrame, columns: List[str]) -> Tuple[List[str], ...]:
    """
    TODO
    """
    _min = [str(data.column.min()) for column in columns]
    _max = [str(data.column.max()) for column in columns]
    return (_min, _max)


def skim(data: pd.DataFrame, name: str) -> None:
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
    sk_summary = Skimer(data, name).summary
    sk_numeric = Skimer(data, name).numeric
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

    console.print(" [u][bold]Data Summary[/bold][/u]")
    console.print(_build_sum(sk_summary))
    print()
    console.print(" [u][bold]Variable Type: Numeric[/bold][/u]")
    console.print(_build_num(sk_numeric))
