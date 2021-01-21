from unittest import TestCase
import pandas as pd
import matplotlib.pyplot as plt

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
        print(self.df.info)
        print(self.df.describe)

    def test_data_manipulation(self):
        df = self.df
        print(f"dataframe:\n {df}")
        print(f"head:\n {df.head()}")
        print(f"shape:\n {df.shape}")
        df.copy()
        print(f"obj_col: \n{df['obj_col']}")
        print(f"slice: \n{df[:2]}")

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
        print(f"\ndataframe[['int_col','float_col']].describe():\n {df[['int_col','float_col']].describe()}")
        print(f"\ndataframe[['int_col','float_col']].sum():\n {df[['int_col','float_col']].sum()}")
        print(f"\ndataframe[['int_col','float_col']].median():\n {df[['int_col','float_col']].median()}")
        print(f"\ndataframe[['int_col','float_col']].mean():\n {df[['int_col','float_col']].mean()}")

        # groupby
        print(f"\ndataframe[['int_col','float_col']].describe():\n {df.groupby('obj_col').describe()}")
        print(f"\ndataframe[['int_col','float_col']].describe():\n {df.groupby(['obj_col','int_col'])['float_col'].describe()}")


def test_plot(self):
        # fig, ax = plt.subplots()
        # ax = self.df['int_col'].plot.hist()
        self.df['int_col'].plot.hist()
        plt.show()









