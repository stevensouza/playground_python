import google.oauth2.service_account
import googleapiclient.discovery
import utils

# import tableau_metrics
# read google sheet - https://developers.google.com/sheets/api/samples/reading
scopes = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
          "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
"""
todo: 
x- move GoogleSheet test to standard test file
- get rid of tableau_metrics and load_from_gsheet
- create 2nd google sheets api 
- put parameters in json file
- come up with example driver program
- can i clean up scopes
- exception class 
- errors in general. i.e. what happens if exception is thrown?
- email code?
"""


class GoogleSheet:

    def __init__(self, credential_file):
        # get Google service account credentials from a local file
        self.creds = google.oauth2.service_account.Credentials.from_service_account_file(credential_file, scopes=scopes)

    def get_modified_time(self, google_sheet_id):
        # use Google Drive API to get the spreadsheet mod time in ISO Zulu
        with googleapiclient.discovery.build('drive', 'v3', credentials=self.creds) as service:
            return service.files().get(fileId=google_sheet_id, fields='modifiedTime').execute().get('modifiedTime')

    def get_data(self, google_sheet_id, sheet_a1_notation):
        """
            Returns dictionary where each row of the spreadsheet is an array.  The first row could contain
            the header if the spreadsheet is set up that way.
        """
        # use Google Sheets API to pull the spreadsheet data/rows
        # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/get?apix_params=%7B%22spreadsheetId%22%3A%2218VF0mB6usVkorgCULDqd4Ib9UrWf8MnaqYxrtnYcsvo%22%2C%22includeGridData%22%3Atrue%2C%22ranges%22%3A%5B%22Sheet1%22%5D%7D
        with googleapiclient.discovery.build('sheets', 'v4', credentials=self.creds) as service:
            data = service.spreadsheets().values().get(spreadsheetId=google_sheet_id,
                                                       range=sheet_a1_notation,
                                                       valueRenderOption="UNFORMATTED_VALUE",
                                                       dateTimeRenderOption="FORMATTED_STRING").execute()
            return data['values']
