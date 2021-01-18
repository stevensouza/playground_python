import sys

from sqlalchemy import create_engine
import pandas as pd
import utils
import googlesheets

"""
    Program that uses a config file that contains a 'source' (excel file, google sheet, database etc) and takes this tabular
    data and copies/etl's it to the 'destination' (source->destination).  If in the pandas directory sample 
    config files are kept in 'pandas/resources' and they may be invoked in the following way:
    
        * python3 pandas_etl.py resources/memory_to_sqllitedb_config.json 
        * python3 pandas_etl.py resources/excel_to_sqllitedb_config.json
        * python3 pandas_etl.py resources/googlesheet_to_sqllitedb_config.json
        * python3 pandas_etl.py resources/googlesheet_to_mysqldb_config.json
        * python3 pandas_etl.py resources/excel_to_excel_config.json
        
    Here is further documentation on the source/destination types pandas allows: 
    https://pandas.pydata.org/pandas-docs/stable/reference/frame.html#serialization-io-conversion
             
"""


class PandasEtl:
    memory_data = [
        ["obj_col", "int_col", "float_col", "date_col"],
        ["joe", 10, 10.5, "12/20/2000"],
        ["ed", 20, 20.5, "12/21/2000"],
        ["al", 30, 30.5, None],
    ]

    def __init__(self, config_file):
        self.config = utils.load_json(config_file)

    def run(self):
        dataframe = self.from_source()
        print(dataframe)
        self.to_destination(dataframe)

    def from_source(self):
        source_type = self.config['source']['type']
        print(f"source.type: {source_type}")

        if source_type == "memory":
            data = self.memory_data.copy()
            header = data.pop(0)
            dataframe = utils.to_pandas(data, header)
            return dataframe
        elif source_type == "excel":
            excel_file = self.config['source']['file']
            sheet = self.config['source']['sheet']
            print(f" source.file: {excel_file}, source.sheet: {sheet}")

            dataframe = pd.read_excel(io=excel_file, sheet_name=sheet, header=0)
            return dataframe
        elif source_type == "googlesheets":
            spreadsheet_id = self.config['source']['spreadsheet_id']
            sheet = self.config['source']['sheet']
            print(f" source.spreadsheet_id: {spreadsheet_id}, source.sheet: {sheet}")

            spreadsheet = googlesheets.GoogleSheet(self.config['source']['credentials_file'])
            data = spreadsheet.get_data(spreadsheet_id, sheet)
            header = data.pop(0)
            dataframe = utils.to_pandas(data, header)
            return dataframe

        # TODO fall through should be exception
        return None

    def to_destination(self, dataframe):
        dest_type = self.config['destination']['type']
        print(f"destination.type: {dest_type}")

        if dest_type == "db":
            table = self.config['destination']['table']
            print(f" destination.table: {table}")
            engine = create_engine(self.config['destination']['url'], echo=True)
            utils.to_db(engine=engine,
                        dataframe=dataframe,
                        table_name=table)
        elif dest_type == "excel":
            excel_file = self.config['destination']['file']
            sheet = self.config['destination']['sheet']
            print(f" destination.file: {excel_file}, destination.sheet: {sheet}")
            with pd.ExcelWriter(excel_file,
                                datetime_format=self.config['destination']['datetime_format'],
                                date_format=self.config['destination']['date_format']) as writer:
                dataframe.to_excel(excel_writer=writer, sheet_name=sheet, index=False)


if __name__ == '__main__':
    # Example: python3 pandas_etl.py resources/memory_to_sqllitedb_config.json
    # TODO exception could trigger email etc.
    if len(sys.argv) == 2:
        configuration_file = sys.argv[1]
        etl = PandasEtl(configuration_file)
        etl.run()
    else:
        print(
            "Pass a configuration file that defines the source of where to get tabular data from and the destination of where to copy it to.")
        print("Example: python3 pandas_etl.py resources/memory_to_sqllitedb_config.json")