import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


def get_sheet_data(sheet_name: str) -> pd.DataFrame: 
    """
    Call Google Sheets and return dataframe
    """
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds/tom_mvfc.json", scope)
    client = gspread.authorize(creds)

    spreadsheet_name = "MVFC Coaches"
    spreadsheet = client.open(spreadsheet_name)

    sheet = spreadsheet.worksheet(sheet_name)

    data = sheet.get_all_records()
    
    return pd.DataFrame(data)
