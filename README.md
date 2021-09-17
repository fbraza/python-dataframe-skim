![](assets/banner_SkimPy.png)

## Functionality

If pandas DataFrame `info()` and `describe()` methods had a baby this would be `skimpy`. It produces an extended statistics summary of your Pandas DataFrames. It is inspired by the skimR library and should give you a quick summary of your data.
**Work still in progress**.

## Setup

## Usage

I use the `api.extensions` for Pandas to produce statistical resume of your DataFrame. A quick example with the iris dataset.

```python
iris_data.skim.print()

"""
  Variable type: summary

                             Values
 ───────────────────────────────────
  Number of rows             150
  Number of columns          5
  The frequency of float64   4
  The frequency of object    1

  Variable type: numeric

  Variable       N_total   N_missing   Min   Max   Mean    Std     Q0    Q25   Q50    Q75   Q100   Skew     Kurt     Dist
 ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  sepal_length   150       0           4     7     5.843   0.828   4.3   5.1   5.8    6.4   7.9    0.315    -0.552   ▂▆▄█▄▇▅▁▁▁
  sepal_width    150       0           2     4     3.054   0.434   2.0   2.8   3.0    3.3   4.4    0.334    0.291     ▁▄▅█▆▁▂
  petal_length   150       0           1     6     3.759   1.764   1.0   1.6   4.35   5.1   6.9    -0.274   -1.402   █▂  ▁▅▆▃▂▁
  petal_width    150       0           0     2     1.199   0.763   0.1   0.3   1.3    1.8   2.5    -0.105   -1.34    █▁ ▁▁▆▁▄▁▂

  Variable type: object

  Variable   N_total   N_missing   Min   Max   N_empty_string   N_distinct
 ──────────────────────────────────────────────────────────────────────────
  species    150       0           6     10    0                3
"""
```

## Acknowledgments

# :exclamation: work in progress :exclamation:
