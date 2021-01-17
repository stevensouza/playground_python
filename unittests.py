import datetime
from unittest import TestCase
from sqlalchemy import create_engine
import pandas as pd
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

    def test_to_db_string_to_date_coercion(self):
        """
        Creates the following table if it doesn't exist or uses the existing one if it does.
        This example converts the string formatted date columns to DATETIME

        CREATE TABLE mytable (
	        obj_col TEXT,
	        int_col BIGINT,
	        float_col FLOAT,
	        date_col DATETIME
        )
        """
        MYTABLE = "mytable"
        data = self.data.copy()
        header = data.pop(0)
        # defaults to convert any string cells to dates if they can be converted
        df = utils.to_pandas(data, header)
        engine = create_engine('sqlite://', echo=True)
        utils.to_db(engine=engine,
                    dataframe=df,
                    table_name=MYTABLE)

        table_results = engine.execute(f"SELECT * FROM {MYTABLE}").fetchall()
        self.assertEqual(3, len(table_results))

    def test_to_db_no_string_to_date_coercion(self):
        """
        Creates the following table if it doesn't exist or uses the existing one if it does.
        This example does not convert the string formatted date columns to DATETIME

        CREATE TABLE mytable (
            obj_col TEXT,
            int_col BIGINT,
            float_col FLOAT,
            date_col TEXT
        )
        """
        MYTABLE = "mytable"
        data = self.data.copy()
        header = data.pop(0)
        df = utils.to_pandas(data, header, strings_to_dates=False)
        engine = create_engine('sqlite://', echo=True)
        utils.to_db(engine=engine,
                    dataframe=df,
                    table_name=MYTABLE)

        table_results = engine.execute(f"SELECT * FROM {MYTABLE}").fetchall()
        self.assertEqual(3, len(table_results))

    def test_delme(self):
        engine = create_engine('mysql+pymysql://root:root@localhost/delme')
        # engine = create_engine('mysql+mysqldb://root:root@localhost/delme')
        # engine = create_engine('mysql+mysqlconnector://root:root@localhost/delme?auth_plugin=mysql_native_password',
        #                        connect_args={'auth_plugin': 'mysql_native_password'})
        print(engine)
        table_results = engine.execute(f"select * from pet").fetchall()
        print(table_results)

        df = pd.read_sql("select * from pet", engine)
        print(df)
        print(df['owner'].max())

        df = pd.read_excel(io="resources/names.xlsx", sheet_name="Sheet1", header=0)
        print(df)
        print(df["age"].sum())
        engine = create_engine('sqlite://', echo=True)
        utils.to_db(engine=engine,
                    dataframe=df,
                    table_name="names")

        table_results = engine.execute(f"SELECT * FROM names").fetchall()
        print(table_results)


    # The MySQL Connector/Python DBAPI has had many issues since its release, some of
        # which may remain unresolved, and the mysqlconnector dialect is not tested as part of
        # SQLAlchemy’s continuous integration. The recommended MySQL dialects are mysqlclient
        # and PyMySQL.


