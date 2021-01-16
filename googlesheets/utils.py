from sqlalchemy import create_engine
import pandas as pd
from dateutil.parser import parse as parse_date


# class Utils:
#     def __init__(self, user, password, url):
#         print("hi")
#         # engine = create_engine('mysql://admin:root@localhost/delme')
#         self.engine = create_engine('sqlite://', echo=False)

def date_coercion(value, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param value: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        if isinstance(value, str):
            return parse_date(value, fuzzy=fuzzy)
        else:
            # if not isinstance(string, str) or string.isnumeric() or isfloat(string):
            return value

    except ValueError:
        return value

# def isfloat(string):
#     try:
#         float(string)
#         return True
#     except ValueError:
#         return False

def to_pandas(rows, header=None,strings_to_dates=True):
    df = pd.DataFrame(data=rows, columns=header)
    if strings_to_dates:
        # change string_to_date
        return df.applymap(lambda cell_value:  date_coercion(cell_value))
        # return df.applymap(lambda cell_value: parse_date(cell_value) if date_coercion(cell_value) else cell_value)
    else:
        return df


def to_db(df):
    engine = create_engine('sqlite://', echo=True)
    df.to_sql(name='users', con=engine, if_exists='append', index=False)
    delme1 = engine.execute("SELECT * FROM users").fetchall()
    print (delme1)

    # df = pd.DataFrame({'date1': ["2021-02-02", "2021-04-05", "2021-03-02"],
    #                    'fname': ["ed", "jo", "al"],
    #                    "date2": ["02/22/2021", "01/23/2021", "03/24/2021"],
    #                    'age': [5, 6, 7],
    #                    'fractionalage': [5.5, 6.5, 7.5], })
    # delme1 = df['date2'].apply(lambda x: parse_date(x) if date_coercion(x) else x)
    # print(delme1)
    # print(delme1.dtypes)
    # print("***")
    # delme1 = df[["fname","date1","date2","age","fractionalage"]].applymap(lambda x: parse_date(x) if date_coercion(x) else x)
    # delme1 = df.applymap(lambda cell_value: parse_date(cell_value) if date_coercion(cell_value) else cell_value)
    #
    # print("XXXX")
    # print(delme1)
    # print(delme1.dtypes)
    # print("YYYY")
    #
    # delme = pd.to_datetime(df["date1"], infer_datetime_format=True, errors="ignore")
    # df["date1"] = delme;
    # # df.astype()
    # print(delme)
    # delme = pd.to_datetime(df["date2"], infer_datetime_format=True, errors="ignore")
    # df["date2"] = delme;
    #
    # print(delme)
    # delme = pd.to_datetime(df["fractionalage"], infer_datetime_format=True, errors="ignore")
    # print(delme)
    # delme = pd.to_datetime(df["fname"], infer_datetime_format=True, errors="ignore")
    # print(delme)
    #
    # print("*****")
    # # df.astype(str).apply(pd.to_datetime, errors='coerce')
    # #  df.to_sql('users', con=self.engine)
    # print(df.info)
    # print(df.dtypes)
    # print(df["date2"].dtypes)
    # print(delme1)
    # print(pd.to_datetime("2013-01-01"))
    # print("&&&&&")
    # print(delme1)
    # print("******")
    # # u.todb("tablename",u.topandas(gs.get_data(xx))



'''

df.plot

sheet_data = google rest call for values
# header row
pd.DataFrame(sheet_data[1:], sheet_data[:1])
# no header row??
pd.DataFrame(sheet_data, None)

: format = lambda x: '%.2f' % x

In [121]: frame.applymap(format)
Summing up, apply works on a row / column basis of a DataFrame, applymap works element-wise on a DataFrame, and map works element-wise on a Series.


empDfObj = pd.DataFrame(empoyees, columns=['Name', 'DOB', 'City', 'Marks'])

pd.to_datetime() converts the date time strings in ISO8601 format to datetime64 type. Strings type that it can automatically handles are,

‘DD-MM-YYYY HH:MM AM/PM’
‘YYYY-MM-DDTHH:MM:SS’
‘YYYY-MM-DDT HH:MM:SS.ssssss’

:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    :param fuzzy:
        Whether to allow fuzzy parsing, allowing for string like "Today is
        January 1, 2047 at 8:21:00AM".
        
>>> df['Mycol'] = df['Mycol'].apply(lambda x: 
                                    dt.datetime.strptime(x,'%d%b%Y:%H:%M:%S.%f'))
    See Also
    --------
    DataFrame.astype : Cast argument to a specified dtype.
    to_timedelta : Convert argument to timedelta.
    convert_dtypes : Convert dtypes.
    '''
# db = Utils("a", "b", "c")
# print(db)
# db.to_db()
# print(db.is_date("2013-01-01"))
# print(db.is_date("2021-02-02"))
# print(db.is_date("10"))
# print(db.is_date("10.5"))
# print(db.is_date("1999"))
# print(db.is_date("ed"))
# print(parse_date("Thursday, January 14, 2021 at 8 pm"))


