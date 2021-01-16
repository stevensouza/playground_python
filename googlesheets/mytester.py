import googlesheets2
import utils
import googlesheets2 as gs

if __name__ == '__main__':
    creds_file = "/Users/stevesouza/.kettle/client_secret.json"
    id = "18VF0mB6usVkorgCULDqd4Ib9UrWf8MnaqYxrtnYcsvo"
    sheet = "Sheet1"  # A1 notation
    google_sheet = gs.GoogleSheet(creds_file)
    data = google_sheet.get_data(id, sheet)
    print(data)
