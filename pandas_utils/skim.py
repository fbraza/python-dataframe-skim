import pandas as pd
from skimer import Skimer
from rich.console import Console
from rich.table import Table


def skim(data: pd.DataFrame) -> None:
    """
    Summarize data present in dataframe

    Raise
    -----
    An TypeError if an object other than a Pandas DataFrame is passed
    as an argument
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("The skim functions only accepts DataFrames")
    sk = Skimer(data).numeric
    columns = sk.keys()
    values = list(sk.values())
    size = len(values[0])
    rows = [[row[i] for row in values] for i in range(size)]
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    for col in columns:
        table.add_column(col)
    for row in rows:
        table.add_row(*row)
    console.print(table)


data = pd.read_csv("tests/data/iris.csv")
skim(data)