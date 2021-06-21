import pytest
import pandas as pd
from skim.skim import skim


@pytest.fixture
def dummy_types():
    data = {
        "a_dict": {1: ['a', 'e', 'i', 'o', 'u'], 2: ['b', 'c', 'd', 'f', 'g']},
        "a_list": [1, 2, 3],
        "a_str": "string",
        "a_serie": pd.Series([1, 2, 3]),
    }
    return data


@pytest.fixture
def dummy_df():
    data, cols = [[1, 'a'], [2, 'b'], [3, 'c']], ['numbers', 'letters']
    df1 = pd.DataFrame(data=data, columns=cols)
    return df1


def test_skim_should_raise_error_if_incorrect_type_is_passed(dummy_types):
    types = ["a_dict", "a_list", "a_str", "a_serie"]
    for type in types:
        with pytest.raises(TypeError):
            skim(dummy_types[type])


# class TestDataSummary(unittest.TestCase):
#     def setUp(self):
#         data, cols = [[1, 'a'], [2, 'b'], [3, 'c']], ['numbers', 'letters']
#         self.df1 = pd.DataFrame(data=data, columns=cols)

#     def test_shape(self):
#         cols, idx = ['Values'], ['Number of rows', 'Number of columns']
#         data = [[3], [2]]
#         row, col = self.df1.shape
#         expected = pd.DataFrame(data=data, columns=cols, index=idx)
#         result = pd.DataFrame(data=[[row], [col]], columns=cols, index=idx)
#         self.assertTrue(result.equals(expected))

#     def test_type_freq(self):
#         counter, types = {}, self.df1.dtypes
#         for dtype in types:
#             tmp = str(dtype)
#             if tmp in counter.keys():
#                 counter[tmp] += 1
#             else:
#                 counter[tmp] = 1
#         values = [[value] for value in counter.values()]
#         cols, idx = ['Values'], list(counter.keys())
#         result = pd.DataFrame(data=values, columns=cols, index=idx)
#         # expected data
#         data = [[1], [1]]
#         expected = pd.DataFrame(data=data, columns=cols, index=idx)
#         self.assertTrue(result.equals(expected))

#     def test_data_summary(self):
#         data, cols = [[3], [2], [1], [1]], ['Values']
#         idx = ['Number of rows', 'Number of columns', 'int64', 'object']
#         result = SkimData(self.df1).data_summary()
#         expected = pd.DataFrame(data=data, columns=cols, index=idx)
#         print(result)
#         self.assertTrue(expected.equals(result))


# class TestNumericSummary(unittest.TestCase):
#     def setUp(self):
#         data = [[1, 'a', 3.4], [2, 'b', 5.5], [3, 'c', 6.8]]
#         cols = ['integer', 'letters', 'floats']
#         self.df2 = pd.DataFrame(data=data, columns=cols)

#     def test_select_numeric(self):
#         types = ['int8', 'int16', 'int32', 'int64',
#                  'uint8', 'uint16', 'uint32', 'uint64',
#                  'float16', 'float32', 'float64', 'float128']
#         data, cols = [[1, 3.4], [2, 5.5], [3, 6.8]], ['integer', 'floats']
#         result = self.df2.select_dtypes(include=types)
#         expected = pd.DataFrame(data=data, columns=cols)
#         self.assertTrue(result.equals(expected))
