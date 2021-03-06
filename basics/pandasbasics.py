from unittest import TestCase

import matplotlib.pyplot as plt
import pandas as pd

"""
  Pandas experiments
"""


class PandasUnitTests(TestCase):
    header = ["obj_col", "int_col", "float_col", "date_col"]
    data = [
        ["joe", 10, 10.5, "12/20/2000"],
        ["ed", 20, 20.5, "12/21/2000"],
        ["al", 30, 30.5, None],
        ["al", 40, 40.5, None],
    ]

    df = pd.DataFrame(data=data, columns=header)

    def test_info(self):
        df = self.df
        print(df.info())
        print(df.columns)

    def test_data_manipulation(self):
        df = self.df
        print(f"dataframe:\n {df}")
        print(f"head:\n {df.head()}")
        print(f"tail:\n {df.tail()}")
        print(f"shape:\n {df.shape}")
        print(f"num rows:\n {df.shape[0]}")
        print(f"num cols:\n {df.shape[1]}")
        print(f"num rows:\n {len(df)}")

        df.copy()
        print(f"obj_col: \n{df['obj_col']}")
        print(f"obj_col, int_col: \n{df[['int_col', 'obj_col']]}")
        print(f"slice: \n{df[:2]}")

        # get by row
        print(f"get first row by index: \n{df.iloc[0]}")
        print(f"get last row by index: \n{df.iloc[-1]}")
        print(f"get first row by label (in this case same as index): \n{df.loc[0]}")
        print(f"iloc [2],[1] cell value:\n {df.iloc[[2], [1]]}")
        print(f"return 2 columns starting with row 2:\n {df.loc[2:, ['obj_col', 'int_col']]}")
        print(f"return last columns from row 2:\n {df.iloc[2:, 1:]}")
        print(f"cell in 2nd row and 'obj_col':\n {df.loc[1, 'obj_col']}")
        print(f"first 2 rows and repeat first column:\n {df.iloc[[0, 1], [0, 0]]}")

        # equivalent of where clause
        print(f"where clause:\n {df[df['int_col'] >= 30]}")

    def test_column_manipulation(self):
        df = self.df.copy()
        df["new_str_col"] = "hi mom"
        df["new_int_col"] = 22
        print(df)
        del df["new_int_col"]
        # same as above, but more flexible.  For example can do it in place or not and it can take more
        # than 1 column and it is documented.  Though more cryptic
        # With inplace the original df is unchanged, so to capture change we must assign it.
        df_changed = df.drop('new_str_col', axis=1, inplace=False)
        print(df)
        print(df_changed)
        # remove column in place i.e. change the df
        df.drop('new_str_col', axis=1, inplace=True)
        print(df)
        # take all rows of the first 2 columns
        print(df.iloc[:, :2])
        # take all rows of the first 1rst and 4th columns (0 indexed)
        print(df.iloc[:, [0, 3]])

    def test_stats(self):
        df = self.df
        # some dataframe stats functions
        print(f"\ndataframe.describe():\n {df.describe()}")
        print(f"\ndataframe.sum():\n {df.sum()}")
        print(f"\ndataframe.median():\n {df.median()}")
        print(f"\ndataframe.mean():\n {df.mean()}")

        # some series/column stats functions
        print(f"\ndataframe['int_col'].describe():\n {df['int_col'].describe()}")
        print(f"\ndataframe['int_col'].sum():\n {df['int_col'].sum()}")
        print(f"\ndataframe['int_col'].median():\n {df['int_col'].median()}")
        print(f"\ndataframe['int_col'].mean():\n {df['int_col'].mean()}")

        # multiple series/column stats functions
        print(f"\ndataframe[['int_col','float_col']].describe():\n {df[['int_col', 'float_col']].describe()}")
        print(f"\ndataframe[['int_col','float_col']].sum():\n {df[['int_col', 'float_col']].sum()}")
        print(f"\ndataframe[['int_col','float_col']].median():\n {df[['int_col', 'float_col']].median()}")
        print(f"\ndataframe[['int_col','float_col']].mean():\n {df[['int_col', 'float_col']].mean()}")

        # groupby
        print(f"\ndataframe[['int_col','float_col']].describe():\n {df.groupby('obj_col').describe()}")
        print(
            f"\ndf.groupby(['obj_col', 'int_col'])['float_col'].describe():\n {df.groupby(['obj_col', 'int_col'])['float_col'].describe()}")

    def test_plot(self):
        # fig, ax = plt.subplots()
        # ax = self.df['int_col'].plot.hist()
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html

        self.df['int_col'].plot.hist()
        plt.show()
        self.df['int_col'].plot(kind="bar")
        plt.show()
        self.df['int_col'].plot(kind="barh")
        plt.show()
        self.df['int_col'].plot(kind="hist")
        plt.show()
        # kind    str
        # The kind of plot to produce:
        #     ‘line’ : line plot (default)
        #     ‘bar’ : vertical bar plot
        #     ‘barh’ : horizontal bar plot
        #     ‘hist’ : histogram
        #     ‘box’ : boxplot
        #     ‘kde’ : Kernel Density Estimation plot
        #     ‘density’ : same as ‘kde’
        #     ‘area’ : area plot
        #     ‘pie’ : pie plot
        #     ‘scatter’ : scatter plot
        #     ‘hexbin’ : hexbin plot.
