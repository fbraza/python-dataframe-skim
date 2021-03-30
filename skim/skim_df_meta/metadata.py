import pandas as pd


class SkimDfDataSummary:
    def __init__(self, df: pd.DataFrame):
        self.types = [str(dtype) for dtype in df.dtypes.unique()]
        self.summary = self.data_summary(df)
        self.numeric = self.numeric_summary(df) if self._has_numeric(df) else None

    def data_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """Function defined to return a concatenated dataframe containing
        details about the number of row and columns and the column dtype
        frequency of the passed dataframe or series object"""
        def _shape(df: pd.DataFrame) -> pd.DataFrame:
            """Function defined to return a dataframe with details about
            the number of row and columns"""
            row, col = df.shape
            return pd.DataFrame(data=[[row], [col]],
                                columns=['Values'],
                                index=['Number of rows', 'Number of columns'])

        def _dtypes_freq(df: pd.DataFrame) -> pd.DataFrame:
            """Function defined to return a dataframe with details about
            the pandas dtypes frequency"""
            dtypes, counter = [str(dtype) for dtype in df.dtypes.values], {}
            for dtype in dtypes:
                if dtype in counter.keys():
                    counter[dtype] += 1
                else:
                    counter[dtype] = 0
            values = [[value] for value in counter.values()]
            return pd.DataFrame(data=values, columns=['Values'], index=dtypes)
        return pd.concat([_shape(df), _dtypes_freq(df)])

    def numeric_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        dtypes = filter(_is_numeric, self.types)
        pass

    def _has_numeric(self, df: pd.DataFrame) -> bool:
        for element in self.types:
            if self._is_numeric(element):
                return True

    def _is_numeric(self, dtype: str) -> bool:
        types = [
            'int8', 'int16','int32', 'int64',
            'uint8', 'uint16', 'uint32', 'uint64',
            'float16', 'float32', 'float64', 'float128'
        ]
        return dtype in types
