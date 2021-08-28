from skimpy.helpers import columns_with_type, list_columns, calculate_quantiles


def test_list_columns_should_return_a_list_of_columns_name(iris_csv):
    exp_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species'] # noqa: 501
    res_cols = list_columns(iris_csv)
    assert exp_cols == res_cols


def test_columns_with_type_dtype_numeric_should_return_numeric_cols(iris_csv):
    exp_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    res_cols = columns_with_type(iris_csv, "numeric")
    assert exp_cols == list_columns(res_cols)


def test_columns_with_type_dtype_object_should_return_object_cols(iris_csv):
    exp_cols = ['species']
    res_cols = columns_with_type(iris_csv, "object")
    assert exp_cols == list_columns(res_cols)


def test_columns_with_type_dtype_category_should_return_no_cols(iris_csv):
    exp_cols = []
    res_cols = columns_with_type(iris_csv, "category")
    assert exp_cols == list_columns(res_cols)


def test_calculate_quantiles_should_return_quantiles_values(fake_data):
    exp = (["1.0", "3.0", "0.0"],
           ["2.5", "4.0", "3.0"],
           ["4.0", "5.0", "6.0"],
           ["5.5", "6.5", "7.5"],
           ["7.0", "8.0", "9.0"])
    res = calculate_quantiles(fake_data)
    assert exp == res
