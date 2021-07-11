import pandas as pd
import helpers as H
from typing import Dict, List, Union
from rich.console import Console
from rich.table import Table
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
        self._sumskim: Dict[str, List] = defaultdict(list)
        self._numskim: Dict[str, List] = defaultdict(list)

    def _set_sumskim(self):
        """
        TODO
        """
        self._sumskim[" "] = ["Number of rows", "Number of columns"]
        self._sumskim["Values"] = [str(self.rows), str(self.cols)]
        dtypes_freq = H.count_types_freq(self.data)
        for k, v in dtypes_freq.items():
            self._sumskim[" "].append("The frequency of {}".format(k))
            self._sumskim["Values"].append(str(v))

    def _set_numskim(self):
        """
        TODO
        """
        data = H.columns_with_type(self.data, "numeric")
        cols = H.columns_to_list(data)
        if not cols:
            self._numskim["Empty"] = [True]
        # intialize some variables
        q0, q25, q50, q75, q100 = H.calculate_quantiles(data)
        _min, _max = H.columns_min_max(data, cols)
        # set the _numeric dictionnary
        self._numskim["Variable"] = cols
        self._numskim["Count_total"] = H.count_columns_values(data, cols)
        self._numskim["Count_missing"] = H.count_missing_values(data, cols)
        self._numskim["Min"] = _min
        self._numskim["Max"] = _max
        self._numskim["Mean"] = H.calculate_means(data, cols)
        self._numskim["Std"] = H.calculate_sd(data, cols)
        self._numskim["Q0"] = q0
        self._numskim["Q25"] = q25
        self._numskim["Q50"] = q50
        self._numskim["Q75"] = q75
        self._numskim["Q100"] = q100
        self._numskim["Skew"] = H.calculate_skew(data, cols)
        self._numskim["Kurt"] = H.calculate_kurosis(data, cols)
        self._numskim["Dist"] = H.draw_distribitions(data, cols)


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
    # sk_summary = Skimer(data, name).summary
    skimmer = Skimer(data)
    skimmer._set_numskim()
    numeric = skimmer._numskim
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

#    def _build_sum(summary: List) -> Table:
#        grid = Table(show_header=True, header_style="bold magenta")
#        columns = ["", "Values"]
#        rows = summary
#        for col in columns:
#            grid.add_column(col)
#        for row in rows:
#            grid.add_row(*row)
#        return grid
#
#    console.print(" [u][bold]Data Summary[/bold][/u]")
#    console.print(_build_sum(sk_summary))
#    print()
    console.print(" [u][bold]Variable Type: Numeric[/bold][/u]")
    console.print(_build_num(numeric))


data = pd.read_csv("tests/data/iris.csv")
skim(data)

