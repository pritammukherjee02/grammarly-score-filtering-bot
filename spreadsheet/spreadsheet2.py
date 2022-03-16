import gspread
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('<PATH TO SECRET_KEY FILE>', SCOPES)

client = gspread.authorize(creds)

sheet = client.open('Grammarly Bot File').sheet1

data = sheet.get_all_records()

def append_data_to_spreadsheet(database):
    sheet.append_rows(database)

'''
#The Code underneath works fine but now the code above
#########

sheet.append_rows([
    ['BRUH', 1, 2, 3],
    ['BRUH2', 1, 2, 3],
    ['BRUH3', 1, 2, 3]
])
print("done")
'''
