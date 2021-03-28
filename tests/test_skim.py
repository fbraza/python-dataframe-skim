from .skim import check_types, data_summary
import unittest
import pandas as pd


class TestObjectTypes(unittest.TestCase):
    def setUp(self) -> None:
        self.dc = {1: ['a', 'e', 'i', 'o', 'u'], 2: ['b', 'c', 'd', 'f', 'g']}
        self.ls = [1, 2, 3]
        self.st = "string"
        self.sr = pd.Series(self.ls)
        self.df = pd.DataFrame(self.dc)

    def test_is_dataframe(self) -> None:
        # initialize variables
        with_dc = True if isinstance(self.dc, pd.DataFrame) else False
        with_ls = True if isinstance(self.ls, pd.DataFrame) else False
        with_st = True if isinstance(self.st, pd.DataFrame) else False
        with_sr = True if isinstance(self.sr, pd.DataFrame) else False
        with_df = True if isinstance(self.df, pd.DataFrame) else False
        # test values
        self.assertFalse(with_dc)
        self.assertFalse(with_ls)
        self.assertFalse(with_st)
        self.assertFalse(with_sr)
        self.assertTrue(with_df)

    def test_exception_raised_if_not_good_type(self) -> None:
        self.assertRaises(AttributeError, check_types, self.ls)


class TestDataSummary(unittest.TestCase):
    def setUp(self) -> None:
        self.df = pd.DataFrame(
            data=[[1, 'a'], [2, 'b'], [3, 'c']],
            columns=['numbers', 'letters']
            )

    def test_data_summary(self) -> None:
        result = data_summary(self.df)
        expected = pd.DataFrame(
            data=[[3], [2], [1], [1]],
            columns=['Values'],
            index=['Number of rows', 'Number of columns', 'int64', 'object']
            )
        self.assertTrue(expected.equals(result))


if __name__ == '__main__':
    unittest.main()
