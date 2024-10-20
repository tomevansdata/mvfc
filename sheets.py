import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st


@st.cache_data(ttl=900) 
def get_data(sheet_name: str) -> pd.DataFrame: 
    """
    Call Google Sheets and return dataframe
    """
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    google_sheets_creds = st.secrets["google_sheets"]
    
    #creds = ServiceAccountCredentials.from_json_keyfile_name("creds/tom_mvfc.json", scope)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(google_sheets_creds, scope)
    client = gspread.authorize(creds)

    spreadsheet_name = "MVFC Coaches"
    spreadsheet = client.open(spreadsheet_name)

    sheet = spreadsheet.worksheet(sheet_name)

    data = sheet.get_all_records()
    
    return pd.DataFrame(data)
