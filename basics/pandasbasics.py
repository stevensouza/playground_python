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

    df = pd.DataFrame(data, columns=header)

    def test_me(self):
        print(self.df)
        print(self.df.copy())
        print(self.df["obj_col"])
        print(self.df[:2])

    def test_plot(self):
        # fig, ax = plt.subplots()
        # ax = self.df['int_col'].plot.hist()
        self.df['int_col'].plot.hist()
        plt.show()









