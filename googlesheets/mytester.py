import googlesheets2
import utils
import googlesheets2 as gs

def googlesheets_to_pandas():
    creds_file = "/Users/stevesouza/.kettle/client_secret.json"
    id = "18VF0mB6usVkorgCULDqd4Ib9UrWf8MnaqYxrtnYcsvo"
    sheet = "Sheet1" # A1 notation
    spreadsheet = gs.GoogleSheet(creds_file)
    data = spreadsheet.get_data(id, sheet)
    print("** spreadsheet data")
    print(data)
    print(f"length: {len(data)}")

    # The first row of this spreadsheet contains the header
    # Note this is also required to remove the first row from the data if the header was included
    header = data.pop(0)
    print(f"\n** header: {header}\n")

    df = utils.to_pandas(data, header)
    print("** dataframe")
    print(df)

    print("\n** dataframe,dtypes")
    print(df.dtypes)


def get_example_googlesheets():
    creds_file = "/Users/stevesouza/.kettle/client_secret.json"
    id = "18VF0mB6usVkorgCULDqd4Ib9UrWf8MnaqYxrtnYcsvo"
    spreadsheet = gs.GoogleSheet(creds_file)
    print(spreadsheet.get_data(id, "Sheet1"))
    print(spreadsheet.get_data(id, "Sheet2GeneratedFromPentaho"))
    print(spreadsheet.get_data(id, "ExcelToGoogleSheetFromPentaho"))
    print(spreadsheet.get_data(id, "testImportRange"))
    print(spreadsheet.get_data(id, "playground"))


if __name__ == '__main__':
    # todo:
    #     do a test case for "10" and fix number to date conversion if needed
    #     mysql
    #     exceptions
    #     tests
    #     performance
    #     directory structure and names
    #     header logic?
    #     test multiple sheets
    #     better understand main function
    #     clean up code, imports, dead code
    #     add comments
    #     proper case on files and classes
    #     proper variable and function names
    googlesheets_to_pandas()
    get_example_googlesheets()


