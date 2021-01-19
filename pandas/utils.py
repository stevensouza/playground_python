import json

import pandas as pd
from dateutil.parser import parse as parse_date
from sqlalchemy import create_engine

"""
Utilities for 
    * Converting tabular data to a Pandas DataFrame
    * Saving Pandas DataFrames to a database
    * Converting strings to dates
"""


def date_coercion(value: object, fuzzy: bool = False) -> object:
    """
    Return a date if the value passed can be converted to a date otherwise return the passed value unchanged.

    :return: date or original value of any type
    :rtype: object
    :param value: any object type, but if it is a string the code tries to convert it to a date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        # parse any string except numbers i.e.: "10", "10.5".  These will normally parse to dates but we
        # don't want to do that.
        if isinstance(value, str) and not is_str_number(value):
            return parse_date(value, fuzzy=fuzzy)
        else:
            # if not isinstance(string, str) or string.isnumeric() or isfloat(string):
            return value

    except ValueError:
        return value


def is_str_number(value: str) -> bool:
    """
        Test to see if a passed in string is a float (ex: "200", "22.34". Non string arguments will return false.

        :param value: Any object
        :return: True if the value is a string that can be converted to a number
        :rtype: bool
    """
    try:
        if not isinstance(value, str):
            return False
        elif value.isnumeric():
            return True
        else:
            float(value)
            return True
    except ValueError:
        return False


def to_pandas(rows, header=None, strings_to_dates=True):
    """
        Convert lists of rows to a Pandas DataFrame.  DataFrames are flexible and powerful way to manipulate tabular data.

        :param rows: Rows containing any number of cells as a list of lists. Rows should not contain a header. Example:
            [["joe",22,"12/20/1975"],["bill",33,"08/25/1980"]
        :param header: Column header in list form for the data or None. Example: ["name","age","birthday"]
        :param strings_to_dates: True if dates strings should be converted to a 'date' type. The parsing mechanism
            is quite flexible so many date formats are automatically converted if True. Example: "12/20/200" would be
            converted from a string to a date if True. It will be left alone and returned as a string if this parameter
            is False.
        :return: A Pandas DataFrame
    """
    df = pd.DataFrame(data=rows, columns=header)
    if strings_to_dates:
        # Change all dataframe string values of format date (for example: "12/10/2013" to actual dates.
        # Leave all other cells alone.
        return dataframe_date_coercion(df)
    else:
        return df


def dataframe_date_coercion(df):
    return df.applymap(lambda cell_value: date_coercion(cell_value))


def to_db(dataframe, table_name, schema=None, chunksize=None, engine=None):
    """
    Save a Pandas DataFrame to a database.  Note a table will be created if it doesn't already exist.
    Records are currently appended if the table already exists.

    :param dataframe: Pandas DataFrame tabular data
    :param table_name: Table to save the data into
    :param schema: DB Schema to save to.  If not provide it will use the default schema
    :param chunksize: Batch commit size.
    :param engine: Connection to a specific database type (for example mysql, sqllite, postgress). If engine isn't
        passed then a sqllite internal database will be used.
    :return: No return value
    """
    if engine is None:
        engine = create_engine('sqlite://', echo=True)

    dataframe.to_sql(name=table_name, con=engine, schema=schema, chunksize=chunksize, if_exists='append', index=False)


def load_json(filename):
    """
        Load a json file into a python dictionary

        :param filename: json file
        :return: dictionary of json file
    """
    with open(filename) as file:
        return json.load(file)
