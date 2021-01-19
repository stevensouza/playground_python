import datetime
from unittest import TestCase

import pandas as pd
from sqlalchemy import create_engine

import utils
import googlesheets

"""
    * Tests for converting various tabular data sets to a Pandas dataframe. For example: excel, lists
    * Tests for saving Pandas DataFrames to a database.
    * Tests for other utility methods such as data coercion

    Assertions - https://www.kite.com/python/docs/unittest.TestCase
"""
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

    def test_to_sqlite_db_string_to_date_coercion(self):
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

    def test_to_sqlite_db_no_string_to_date_coercion(self):
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

    def test_to_mysql_db_string_to_date_coercion(self):
        """
        Creates the following table if it doesn't exist or uses the existing one if it does.
        This example converts the string formatted date columns to DATETIME. If dates aren't
        coerced note that the inserts would fail the following table structure as a string of
        format '12/20/2020' is not considered a date.

            CREATE TABLE mytable (
                obj_col TEXT,
                int_col BIGINT,
                float_col FLOAT(53),
                date_col DATETIME
            )

        """
        # Because the following test requires mysql to be running it is disabled by default.
        enabled = False
        if enabled:
            MYTABLE = "mytable"
            data = self.data.copy()
            header = data.pop(0)
            # defaults to convert any string cells to dates if they can be converted
            df = utils.to_pandas(data, header)
            # username: root, password: root, database: delme.  All of these can be anything as long
            # as they allow you to connect to the mysql instance.
            engine = create_engine('mysql+pymysql://root:root@localhost/delme', echo=True)
            utils.to_db(engine=engine,
                        dataframe=df,
                        table_name=MYTABLE)

            table_results = engine.execute(f"SELECT * FROM {MYTABLE}").fetchall()
            print(table_results)
            # For mysql test this is a permanent table and will append so it may have greater than 3 rows.
            self.assertLessEqual(3, len(table_results))
        else:
            print("This test is disabled")

    def test_to_mysql_db_no_string_to_date_coercion(self):
        """
        Creates the following table if it doesn't exist or uses the existing one if it does.
        This example does not convert the string formatted date columns to DATETIME. It leaves them as
        text.

            CREATE TABLE mytable_text (
                obj_col TEXT,
                int_col BIGINT,
                float_col FLOAT(53),
                date_col TEXT
            )

        """
        # Because the following test requires mysql to be running it is disabled by default.
        enabled = False
        if enabled:
            MYTABLE = "mytable_text"
            data = self.data.copy()
            header = data.pop(0)
            df = utils.to_pandas(data, header, strings_to_dates=False)
            # username: root, password: root, database: delme.  All of these can be anything as long
            # as they allow you to connect to the mysql instance.
            engine = create_engine('mysql+pymysql://root:root@localhost/delme', echo=True)
            utils.to_db(engine=engine,
                        dataframe=df,
                        table_name=MYTABLE)

            table_results = engine.execute(f"SELECT * FROM {MYTABLE}").fetchall()
            print(table_results)
            # For mysql test this is a permanent table and will append so it may have greater than 3 rows.
            self.assertLessEqual(3, len(table_results))
        else:
            print("This test is disabled")

    def test_excel_to_sqlite_db_string_to_date_coercion(self):
        """
        Based on the data in the excel spreadsheet the following table is created if it doesn't exist or use
        the existing one if it does exist. This example converts the string formatted date columns to DATETIME

            CREATE TABLE mytable (
                obj_col TEXT,
                int_col BIGINT,
                float_col FLOAT,
                date_col DATETIME
            )
        """
        MYTABLE = "mytable"
        df = pd.read_excel(io="resources/python_excel_test.xlsx", sheet_name="Sheet1", header=0)
        print(f"Excel sheet dataFrame: \n{df}")
        self.assertEqual(60, df["int_col"].sum())

        engine = create_engine('sqlite://', echo=True)
        utils.to_db(engine=engine,
                    dataframe=df,
                    table_name=MYTABLE)

        table_results = engine.execute(f"SELECT * FROM {MYTABLE}").fetchall()
        print(table_results)
        self.assertEqual(3, len(table_results))

    def test_google_sheets_to_db_string_to_date_coercion(self):
        """
            This test requires access to a google service account secrets json file.  This file won't be checked
            into source control so the test can be disabled.
        """
        enabled = True
        if enabled:
            MYTABLE = "mytable_googlesheet"
            creds_file = "/Users/stevesouza/.kettle/client_secret.json"
            spreadsheet_id = "18VF0mB6usVkorgCULDqd4Ib9UrWf8MnaqYxrtnYcsvo"
            sheet = "Sheet1"  # A1 notation
            spreadsheet = googlesheets.GoogleSheet(creds_file)

            spreadsheet.get_modified_time(spreadsheet_id)
            self.assertIsNotNone(spreadsheet.get_modified_time(spreadsheet_id))
            data = spreadsheet.get_data(spreadsheet_id, sheet)
            print(data)
            header = data.pop(0)
            print(header)

            df = utils.to_pandas(data, header)
            engine = create_engine('sqlite://', echo=True)
            utils.to_db(engine=engine,
                    dataframe=df,
                    table_name=MYTABLE)

            table_results = engine.execute(f"SELECT * FROM {MYTABLE}").fetchall()
            print(table_results)
            self.assertLess(1, len(table_results))

    def test_google_sheets_overwrite(self):
        """
            This test requires access to a google service account secrets json file.  This file won't be checked
            into source control so the test can be disabled.
        """
        enabled = True
        if enabled:
            creds_file = "/Users/stevesouza/.kettle/client_secret.json"
            spreadsheet_id = "18VF0mB6usVkorgCULDqd4Ib9UrWf8MnaqYxrtnYcsvo"
            # TODO Note as is currently written this sheet must exist before it is executed.
            sheet = "PythonDestination"  # A1 notation
            spreadsheet = googlesheets.GoogleSheet(creds_file)
            results = spreadsheet.put_data(spreadsheet_id, sheet, self.data)
            print(results)
            self.assertEqual(4, results['updates']['updatedRows'])

    def test_google_sheets_append(self):
        """
            This test requires access to a google service account secrets json file.  This file won't be checked
            into source control so the test can be disabled.
        """
        enabled = True
        if enabled:
            creds_file = "/Users/stevesouza/.kettle/client_secret.json"
            spreadsheet_id = "18VF0mB6usVkorgCULDqd4Ib9UrWf8MnaqYxrtnYcsvo"
            # TODO Note as is currently written this sheet must exist before it is executed.
            sheet = "PythonDestination"  # A1 notation
            spreadsheet = googlesheets.GoogleSheet(creds_file)
            results = spreadsheet.put_data(spreadsheet_id, sheet, self.data, overwrite_or_append="APPEND")
            print(results)
            self.assertEqual(4, results['updates']['updatedRows'])

    def test_load_json(self):
        json = utils.load_json("resources/memory_to_sqllitedb_config.json")
        print(json)
        self.assertIsNotNone(json.get("source"))
        self.assertEqual("memory", json["source"]["type"])






