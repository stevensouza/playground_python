import datetime
from unittest import TestCase

from sqlalchemy import engine, create_engine

import utils


class UnitTests(TestCase):

    data = [
        ["obj_col", "int_col", "float_col", "date_col"],
        ["joe", 10, 10.5, "12/20/2000"],
        ["ed", 20, 20.5, "12/21/2000"],
        ["al", 30, 30.5, None],
    ]

    def test_is_str_number(self):
        self.assertTrue(utils.is_str_number("1.5"))
        self.assertTrue(utils.is_str_number("1"))
        self.assertFalse(utils.is_str_number(1))  # false - only strings can be true
        self.assertFalse(utils.is_str_number(1.5))
        self.assertFalse(utils.is_str_number("joe"))
        self.assertFalse(utils.is_str_number(None))

    def test_date_coercion(self):
        self.assertEqual(datetime.datetime(2013, 12, 2), utils.date_coercion("2013-12-2"))
        self.assertEqual("1999", utils.date_coercion("1999"))
        self.assertEqual("10.5", utils.date_coercion("10.5"))
        self.assertEqual("joe", utils.date_coercion("joe"))
        self.assertEqual(2000, utils.date_coercion(2000))
        self.assertEqual(datetime.datetime(2021, 1, 14, 20), utils.date_coercion("Thursday, January 14, 2021 at 8 pm"))
        self.assertIsNone(utils.date_coercion(None))

    def test_to_pandas_no_string_to_date_coercion(self):
        data = self.data.copy()
        header = data.pop(0)
        df = utils.to_pandas(data, header, strings_to_dates=False)
        print(df)

        # note there may be better ways to do this.  Comparing if fields are of expected types
        col_types = df.select_dtypes(["object"]).columns.tolist()
        self.assertListEqual(["obj_col", "date_col"], col_types)

        col_types = df.select_dtypes(["int64"]).columns.tolist()
        self.assertListEqual(["int_col"], col_types)

        col_types = df.select_dtypes(["float64"]).columns.tolist()
        self.assertListEqual(["float_col"], col_types)

    def test_to_pandas_with_string_to_date_coercion(self):
        data = self.data.copy()
        header = data.pop(0)
        df = utils.to_pandas(data, header)
        print(df)

        # note there may be better ways to do this.  Comparing if fields are of expected types
        col_types = df.select_dtypes(["object"]).columns.tolist()
        self.assertListEqual(["obj_col"], col_types)

        col_types = df.select_dtypes(["int64"]).columns.tolist()
        self.assertListEqual(["int_col"], col_types)

        col_types = df.select_dtypes(["float64"]).columns.tolist()
        self.assertListEqual(["float_col"], col_types)

        col_types = df.select_dtypes(["datetime64"]).columns.tolist()
        self.assertListEqual(["date_col"], col_types)

    def test_to_pandas_noheader_with_string_to_date_coercion(self):
        data = self.data.copy()
        header = data.pop(0)
        df = utils.to_pandas(data)
        print(df)

        # note there may be better ways to do this.  Comparing if fields are of expected types
        col_types = df.select_dtypes(["object"]).columns.tolist()
        self.assertListEqual([0], col_types)

        col_types = df.select_dtypes(["int64"]).columns.tolist()
        self.assertListEqual([1], col_types)

        col_types = df.select_dtypes(["float64"]).columns.tolist()
        self.assertListEqual([2], col_types)

        col_types = df.select_dtypes(["datetime64"]).columns.tolist()
        self.assertListEqual([3], col_types)

    def test_to_db(self):
        MYTABLE = "mytable"
        data = self.data.copy()
        header = data.pop(0)
        df = utils.to_pandas(data, header)
        """
        df = utils.to_pandas(data, header, strings_to_dates=False)

        CREATE TABLE mytable (
	        obj_col TEXT, 
	        int_col BIGINT, 
	        float_col FLOAT, 
	        date_col TEXT
        )       
        """
        engine = create_engine('sqlite://', echo=True)
        utils.to_db(engine=engine,
                    dataframe=df,
                    table_name=MYTABLE)
        """
        creates teh following table if it doesn't exist or uses the existing one if it does.  Note you can also
        drop the table if needed.
        
        CREATE TABLE mytable (
	        obj_col TEXT, 
	        int_col BIGINT, 
	        float_col FLOAT, 
	        date_col DATETIME
        )
        """
        table_results = engine.execute(f"SELECT * FROM {MYTABLE}").fetchall()
        self.assertEqual(3, len(table_results))


