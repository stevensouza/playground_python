from sqlalchemy import create_engine
import pandas as pd
from dateutil.parser import parse as parse_date


def date_coercion(value: object, fuzzy: bool = False) -> object:
    """
    Return a date if value passed can be converted to a date otherwise return the passed value unchanged.

    :return: date or original value
    :rtype: object
    :param value: str, string to check for date
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
    df = pd.DataFrame(data=rows, columns=header)
    if strings_to_dates:
        # Change all dataframe string values of format date (for example: "12/10/2013" to actual dates.
        # Leave all other cells alone.
        return df.applymap(lambda cell_value: date_coercion(cell_value))
    else:
        return df


def to_db(df):
    engine = create_engine('sqlite://', echo=True)
    df.to_sql(name='users', con=engine, if_exists='append', index=False)
    delme1 = engine.execute("SELECT * FROM users").fetchall()
    print(delme1)
#         # engine = create_engine('mysql://admin:root@localhost/delme')


