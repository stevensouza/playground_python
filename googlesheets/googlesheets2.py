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



        """
            if s['properties'].get('hidden') :
                continue
    
            columns = []
            for c in s['data'][0]['rowData'][0]['values'] :
                fv = c.get('formattedValue')
                if fv is None :
                    break
    
                columns += [ {'name' : fv} ]
    
            values = []
            for r in s['data'][0]['rowData'][1:] :
                if 'values' not in r or 'effectiveValue' not in r['values'][0] :
                    break
    
                # use calculated cell effectiveValues, convert them to
                # Python datatypes and append them row-by-row to the sheet's
                # data values list
                # Google Sheets uses "days since 1899-12-30 00:00:00" for date/time values
                values.append( [ c.get('effectiveValue')
                                 and (c['effectiveValue'].get('numberValue')
                                      and ( c['effectiveFormat'].get('numberFormat')
                                            and (c['effectiveFormat']['numberFormat']['type'] == 'DATE'
                                                 and datetime.date(1899, 12, 30) + datetime.timedelta(c['effectiveValue']['numberValue']))
                                            or c['effectiveValue']['numberValue'])
                                      or c.get('effectiveValue').get('stringValue'))
                                 for c in r['values'][0:len(columns)] ] )
    
            # add the sheet data to the returned spreadsheet object data
            data.append( { 'table' : 'gsheet_' + s['properties']['title'], 'columns' : columns, 'values' : values } )
            return ret
    
    """

    def get_modified_time(self, google_sheet_id):
        # use Google Drive API to get the spreadsheet mod time in ISO Zulu
        return googleapiclient.discovery.build('drive', 'v3', credentials=self.creds).files().get(
            fileId=google_sheet_id, fields='modifiedTime').execute().get('modifiedTime')

    def get_data(self, google_sheet_id, sheet, has_header_row=True):
        first_row = 1 if has_header_row else 0
        # use Google Sheets API to pull the spreadsheet data
        # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/get?apix_params=%7B%22spreadsheetId%22%3A%2218VF0mB6usVkorgCULDqd4Ib9UrWf8MnaqYxrtnYcsvo%22%2C%22includeGridData%22%3Atrue%2C%22ranges%22%3A%5B%22Sheet1%22%5D%7D
        data = self.service.spreadsheets().values().get(spreadsheetId=google_sheet_id, range=sheet,
                                                        valueRenderOption="UNFORMATTED_VALUE",
                                                        dateTimeRenderOption="FORMATTED_STRING").execute()
        return data['values']


if __name__ == '__main__':
    # creds_file, id = sys.argv[1:3]
    creds_file = "/Users/stevesouza/.kettle/client_secret.json"
    id = "18VF0mB6usVkorgCULDqd4Ib9UrWf8MnaqYxrtnYcsvo"
    sheet = "Sheet1" # A1 notation
    google_sheet = GoogleSheet(creds_file)

    print(f"modifiedTime={google_sheet.get_modified_time(id)}")
    data = google_sheet.get_data(id, sheet)
    print(data)
    print(len(data))
    header = data.pop(0)
    print(header)
    # ,  orient='index'
    df = utils.to_pandas(data, header)
    print(df)
    print(df.dtypes)

    print("***")
    data = google_sheet.get_data(id, sheet)
    df = utils.to_pandas(data)
    print(df)
    print(df.dtypes)

    print("***")
    data = google_sheet.get_data(id, sheet)
    data.pop(0)
    df = utils.to_pandas(rows=data,  strings_to_dates=False)
    print(df)
    print(df.dtypes)

    data = google_sheet.get_data(id, sheet)
    header = data.pop(0)
    df = utils.to_pandas(data, header)
    utils.to_db(df)

# title: Sheet1, index: 0
    # title: Sheet2GeneratedFromPentaho, index: 1
    # title: ExcelToGoogleSheetFromPentaho, index: 2
    # title: testImportRange, index: 3
    # title: playground, index: 4

    # getColumnHeaders/getFirstRow?, Sheet object? get_data_with_metadata, get_data, sheetname

    # print(google_sheet.get_sheet_by_name("idonotexist"))
    # list.copy()
    # list.pop(0)


