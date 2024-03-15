import gspread
from google.oauth2.service_account import Credentials
import barcode
import apikey
scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)
SHEET_ID = apikey.SHEET_ID

def getWorksheet():
        if SHEET_ID is None:
             return None
        else:
             sheet = client.open_by_key(SHEET_ID)
             worksheet1 = sheet.get_worksheet(0)
             return worksheet1
    
