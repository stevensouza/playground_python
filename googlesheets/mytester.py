import googlesheets2
import utils
import googlesheets2 as gs

if __name__ == '__main__':
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

