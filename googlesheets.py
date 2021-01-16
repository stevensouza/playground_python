import google.oauth2.service_account
import googleapiclient.discovery
import utils

import json
import sys, os
import datetime

# import tableau_metrics
# read google sheet - https://developers.google.com/sheets/api/samples/reading
scopes = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
          "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]


class GoogleSheet:

    def __init__(self, credential_file):
        # get Google service account credentials from a local file
        self.creds = google.oauth2.service_account.Credentials.from_service_account_file(credential_file, scopes=scopes)
        self.service = googleapiclient.discovery.build('sheets', 'v4', credentials=self.creds)

    def get_modified_time(self, google_sheet_id):
        # use Google Drive API to get the spreadsheet mod time in ISO Zulu
        return googleapiclient.discovery.build('drive', 'v3', credentials=self.creds).files().get(
            fileId=google_sheet_id, fields='modifiedTime').execute().get('modifiedTime')

    """
      Returns dictionary where each row of the spreadsheet is an array.  The first row could contain
      the header if the spreadsheet is set up that way.
    """
    def get_data(self, google_sheet_id, sheet_a1_notation):
        # use Google Sheets API to pull the spreadsheet data/rows
        # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/get?apix_params=%7B%22spreadsheetId%22%3A%2218VF0mB6usVkorgCULDqd4Ib9UrWf8MnaqYxrtnYcsvo%22%2C%22includeGridData%22%3Atrue%2C%22ranges%22%3A%5B%22Sheet1%22%5D%7D
        data = self.service.spreadsheets().values().get(spreadsheetId=google_sheet_id,
                                                        range=sheet_a1_notation,
                                                        valueRenderOption="UNFORMATTED_VALUE",
                                                        dateTimeRenderOption="FORMATTED_STRING").execute()
        return data['values']


if __name__ == '__main__':
    creds_file = "/Users/stevesouza/.kettle/client_secret.json"
    spreadsheet_id = "18VF0mB6usVkorgCULDqd4Ib9UrWf8MnaqYxrtnYcsvo"
    sheet = "Sheet1" # A1 notation
    spreadsheet = GoogleSheet(creds_file)

    print(f"modifiedTime={spreadsheet.get_modified_time(spreadsheet_id)}")
    data = spreadsheet.get_data(spreadsheet_id, sheet)
    print(data)
    print(len(data))
    header = data.pop(0)
    print(header)
    # ,  orient='index'
    df = utils.to_pandas(data, header)
    print(df)
    print(df.dtypes)

    print("***")
    data = spreadsheet.get_data(spreadsheet_id, sheet)
    df = utils.to_pandas(data)
    print(df)
    print(df.dtypes)

    print("***")
    data = spreadsheet.get_data(spreadsheet_id, sheet)
    data.pop(0)
    df = utils.to_pandas(rows=data,  strings_to_dates=False)
    print(df)
    print(df.dtypes)

    data = spreadsheet.get_data(spreadsheet_id, sheet)
    header = data.pop(0)
    df = utils.to_pandas(data, header)
    utils.to_db(df)



