import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st
# Connect to Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("words-correction-a710f731b5e8.json", scope)
client = gspread.authorize(credentials)
# sheet = client.create("words correction")
# sheet.share('amadatiq786@gmail.com', perm_type='user', role='writer')

sheet = client.open("Corrected words").sheet1
a=sheet.get()
st.write(pd.DataFrame(a))
#df = pd.read_csv('football_news.csv')
#sheet.update([df.columns.values.tolist()] + df.values.tolist())
