import pandas as pd
import helpers as H
from typing import Dict, List, Optional
from rich.console import Console
from rich.table import Table
from rich import box
from collections import defaultdict


class Skimer:
    """
    TODO
    """
    def __init__(
        self,
        data: pd.DataFrame,
        name: str = "My Dataset"
    ):
        self.data = data
        self.name = name
        self.rows = data.shape[0]
        self.cols = data.shape[1]
        # have a a attribute called skimmers that is a defaultdict(dict)
        self.skimmer: Dict[str, Dict[str, List]] = defaultdict(dict)

    def set_skimmers(self):
        self._set_sumskim()
        self._set_numskim()

    def _set_sumskim(self):
        """
        TODO
        """
        _sumskim: Dict[str, List] = defaultdict(list)
        _sumskim[" "] = ["Number of rows", "Number of columns"]
        _sumskim["Values"] = [str(self.rows), str(self.cols)]
        dtypes_freq = H.count_types_freq(self.data)
        for k, v in dtypes_freq.items():
            _sumskim[" "].append("The frequency of {}".format(k))
            _sumskim["Values"].append(str(v))
        self.skimmer["summary"] = _sumskim

    def _set_numskim(self) -> Optional[None]:
        """
        TODO
        """
        _numskim: Dict[str, List] = defaultdict(list)
        data = H.columns_with_type(self.data, "numeric")
        cols = H.list_columns(data)
        if not cols:
            self.skimmer["numeric"] = {}
        # statistic calculations
        q0, q25, q50, q75, q100 = H.calculate_quantiles(data)
        _min, _max = H.columns_min_max(data, cols)
        _numskim["Variable"] = cols
        _numskim["Count_total"] = H.count_columns_values(data, cols)
        _numskim["Count_missing"] = H.count_missing_values(data, cols)
        _numskim["Min"] = _min
        _numskim["Max"] = _max
        _numskim["Mean"] = H.calculate_means(data, cols)
        _numskim["Std"] = H.calculate_sd(data, cols)
        _numskim["Q0"] = q0
        _numskim["Q25"] = q25
        _numskim["Q50"] = q50
        _numskim["Q75"] = q75
        _numskim["Q100"] = q100
        _numskim["Skew"] = H.calculate_skew(data, cols)
        _numskim["Kurt"] = H.calculate_kurosis(data, cols)
        _numskim["Dist"] = H.draw_distribitions(data, cols)
        self.skimmer["numeric"] = _numskim


def skim(data: pd.DataFrame, choices: List[str] = None) -> None:
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
        raise TypeError(
            """
            For now,the skim functions only accepts Pandas DataFrames
            """
            )
    # instantiate the rich Console object
    console = Console()
    # instantiate the skimmer object
    skimmer = Skimer(data)
    skimmer.set_skimmers()

    def _build_rich_grid(summary: dict, title: str) -> Table:
        columns, values = summary.keys(), list(summary.values())
        size = len(values[0])
        rows = [[row[i] for row in values] for i in range(size)]
        grid = Table(
            box=box.SIMPLE,
            show_header=True,
            header_style="italic",
            title="  Variable type: {}".format(title),
            title_justify="left",
            title_style="bold",
            )
        for col in columns:
            grid.add_column(col)
        for row in rows:
            grid.add_row(*row)
        return grid
    console.clear()

    for key, value in skimmer.skimmer.items():
        console.print(_build_rich_grid(value, key))


data = pd.read_csv("tests/data/iris.csv")
skim(data)
