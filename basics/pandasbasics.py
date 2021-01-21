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


    def test_plot(self):
        # fig, ax = plt.subplots()
        # ax = self.df['int_col'].plot.hist()
        self.df['int_col'].plot.hist()
        plt.show()









