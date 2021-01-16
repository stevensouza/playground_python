import google.oauth2.service_account
import googleapiclient.discovery

import json
import sys, os
import datetime

# import tableau_metrics
# read google sheet - https://developers.google.com/sheets/api/samples/reading
scopes = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
          "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]


class GoogleSheet:

    def __init__(self, credential_file, google_sheet_id):
        # get Google service account credentials from a local file
        self.creds = google.oauth2.service_account.Credentials.from_service_account_file(creds_file, scopes=scopes)
        # use Google Drive API to get the spreadsheet mod time in ISO Zulu
        self.modified_time = googleapiclient.discovery.build('drive', 'v3', credentials=self.creds).files().get(
            fileId=google_sheet_id, fields='modifiedTime').execute().get('modifiedTime')
        print(self.modified_time)
        service = googleapiclient.discovery.build('sheets', 'v4', credentials=self.creds)
        # use Google Sheets API to pull the spreadsheet data
        # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/get?apix_params=%7B%22spreadsheetId%22%3A%2218VF0mB6usVkorgCULDqd4Ib9UrWf8MnaqYxrtnYcsvo%22%2C%22includeGridData%22%3Atrue%2C%22ranges%22%3A%5B%22Sheet1%22%5D%7D
        self.google_sheet = service.spreadsheets().get(
            spreadsheetId=google_sheet_id, includeGridData=True).execute()
        self.data2 = service.spreadsheets().values().get(spreadsheetId=google_sheet_id, range="Sheet1",
                                                         valueRenderOption="UNFORMATTED_VALUE",
                                                         dateTimeRenderOption="FORMATTED_STRING").execute()


    def get_sheet_by_name(self, sheet_name):
        for current_sheet in self.google_sheet["sheets"]:
            # print(f'****{current_sheet["properties"]["title"]}')
            if sheet_name == current_sheet["properties"]["title"]:
                sheet_index = current_sheet["properties"]["index"]
                return self.get_sheet(sheet_index)

        raise Exception(f"Sheetname '{sheet_name}' not found")


    def get_sheet(self, sheet_index):
        return self.google_sheet["sheets"][sheet_index]

    def get_data2(self):
        return self.data2["values"]


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

    def get_data_with_metadata(self, sheet_index, has_header_row=True):
        first_row = 1 if has_header_row else 0
        return self.get_sheet(sheet_index)['data'][0]['rowData'][first_row:]

    def get_data(self, sheet_index, has_header_row=True):
        first_row = 1 if has_header_row else 0
        return self.data2['values'][first_row:]


if __name__ == '__main__':
    # creds_file, id = sys.argv[1:3]
    creds_file = "/Users/stevesouza/.kettle/client_secret.json"
    id = "18VF0mB6usVkorgCULDqd4Ib9UrWf8MnaqYxrtnYcsvo"
    google_sheet = GoogleSheet(creds_file, id)
    sheet = google_sheet.get_sheet(0)

    print(sheet)
    print(f"modifiedTime={google_sheet.modified_time}")
    data = google_sheet.get_data_with_metadata(0)
    print(data)
    print(len(data))
    data = google_sheet.get_data(0, False)
    print(data)
    print(len(data))
    for item in data:
        print(item)


    # title: Sheet1, index: 0
    # title: Sheet2GeneratedFromPentaho, index: 1
    # title: ExcelToGoogleSheetFromPentaho, index: 2
    # title: testImportRange, index: 3
    # title: playground, index: 4

    # getColumnHeaders/getFirstRow?, Sheet object? get_data_with_metadata, get_data, sheetname
    print(google_sheet.get_sheet_by_name("Sheet1"))
    print(google_sheet.get_sheet_by_name("Sheet2GeneratedFromPentaho"))
    print(google_sheet.get_sheet_by_name("ExcelToGoogleSheetFromPentaho"))
    print(google_sheet.get_sheet_by_name("testImportRange"))
    print(google_sheet.get_sheet_by_name("playground"))
    # print(google_sheet.get_sheet_by_name("idonotexist"))
    print("****")
    # list.copy()
    d = google_sheet.get_data2()
    print(len(d))
    print(d.pop(0))
    print(len(d))
    print(json.dumps(d, indent=2))
