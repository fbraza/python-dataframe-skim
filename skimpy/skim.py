import pandas as pd
import helpers as H
from collections import defaultdict
from typing import List, Dict, Union
from rich.console import Console
from rich.table import Table
from rich import box


@pd.api.extensions.register_dataframe_accessor("skim")
class Skim:
    """TODO"""

    def __init__(self, pandas_obj):
        self.__typecheck(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def __typecheck(input):
        if not isinstance(input, pd.DataFrame):
            raise AttributeError("skim accessor should called on a pandas DataFrame")

    def print(self):
        # instantiate the rich Console object
        console = Console()
        # instantiate the skimmer object
        data = self.__skim()

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
        # clear screen
        console.clear()
        for key, value in data.items():
            console.print(_build_rich_grid(value, key))

    def __summary(self):
        """
        TODO
        """
        rows, cols = self._obj.shape[0], self._obj.shape[1]
        data = defaultdict(list)
        data[" "] = ["Number of rows", "Number of columns"]
        data["Values"] = [str(rows), str(cols)]
        dtypes_freq = H.count_types_freq(self._obj)
        for k, v in dtypes_freq.items():
            data[" "].append("The frequency of {}".format(k))
            data["Values"].append(str(v))
        return data

    def __numeric(self) -> Union[Dict[str, List], Dict[str, bool]]:
        """
        TODO
        """
        data = defaultdict(list)
        subset = H.columns_with_type(self._obj, "numeric")
        cols = H.list_columns(subset)
        if not cols:
            return {"empty": True}
        # statistic calculations
        q0, q25, q50, q75, q100 = H.calculate_quantiles(subset)
        _min, _max = H.columns_min_max(subset, cols)
        data["Variable"] = cols
        data["Count_total"] = H.count_columns_values(subset, cols)
        data["Count_missing"] = H.count_missing_values(subset, cols)
        data["Min"] = _min
        data["Max"] = _max
        data["Mean"] = H.calculate_means(subset, cols)
        data["Std"] = H.calculate_sd(subset, cols)
        data["Q0"] = q0
        data["Q25"] = q25
        data["Q50"] = q50
        data["Q75"] = q75
        data["Q100"] = q100
        data["Skew"] = H.calculate_skew(subset, cols)
        data["Kurt"] = H.calculate_kurosis(subset, cols)
        data["Dist"] = H.draw_distribitions(subset, cols)
        return data

    def __skim(self):
        data = defaultdict(dict)
        data["summary"] = self.__summary()
        data["numeric"] = self.__numeric()
        return data
