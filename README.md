# playground_python
Place for Python experiments

This code contains some basic python syntax experiments as well as some experiments
with moving Pandas DataFrames (tabular data) from/to different formats. For example
call a GoogleSheet API, convert that to a Pandas DataFrame and save the
DataFrame to a database table.  Other sources and destination could be excel, csv, 
parquet, avro.  See the following for the possible pandas datasources and
datasinks: https://pandas.pydata.org/pandas-docs/stable/reference/io.html

To run these programs I used python3 v 3.7.3 and installed
the following (doing this by memory so there may be more, but I think that is it.)
- GoogleSheets - pip3  install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
- Pandas - pip3 install pandas --user
- DBAccess/Used with Pandas - pip3 install sqlalchemy --user
- DBAccess/Used with Pandas/Connect to MySql - pip3 install pymysql --user
