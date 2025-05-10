import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
import json

# ===== FUNCTION DEFINITIONS =====

def add_date_column(df, date_str):
    df['Date'] = pd.to_datetime(date_str, format='%Y-%m-%d')
    df['Date'] = pd.to_datetime(df['Date']).dt.normalize()
    cols = [col for col in df.columns if col != 'Date'] + ['Date']
    return df[cols]

def load_and_clean_reports(br_file, ads_file, date_str):
    br = pd.read_csv(br_file)[['(Parent) ASIN', '(Child) ASIN', 'Sessions - Total', 'Units Ordered']]
    br.columns = ['Parent_ASIN', 'Child_ASIN', 'Sessions', 'Units_Ordered']
    br['Sessions'] = br['Sessions'].astype(str).str.replace(',', '').astype(int)
    br['Units_Ordered'] = br['Units_Ordered'].astype(str).str.replace(',', '').astype(int)
    
    br = add_date_column(br, date_str)

    ads = pd.read_csv(ads_file)[['Products', 'Clicks', 'Spend(USD)']]
    ads.columns = ['Child_ASIN', 'Clicks_Ads', 'Spend_Ads']
    ads['Child_ASIN'] = ads['Child_ASIN'].str[:10]
    ads = add_date_column(ads, date_str)

    merged = pd.merge(br, ads, on=["Child_ASIN", "Date"], how="left").fillna(0)
    merged["Date"] = merged.pop("Date")
    return merged

def export_to_gsheet(df, sheet_id, credential_json, worksheet_name):
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(credential_json, scopes=scopes)
    client = gspread.authorize(creds)
    worksheet = client.open_by_key(sheet_id).worksheet(worksheet_name)
    
    # Detect next empty row
    start_row = len(worksheet.get_all_values()) + 1
    set_with_dataframe(worksheet, df, row=start_row, include_column_header=False)

# ===== STREAMLIT UI =====

st.title("📊 Daily Data Merger & GSheet Exporter")

st.markdown("Upload 2 CSV files: Business Report + Ads Report")

br_file = st.file_uploader("📎 Upload Business Report CSV", type="csv")
ads_file = st.file_uploader("📎 Upload Ads Report CSV", type="csv")
date_input = st.text_input("📅 Enter Report Date (YYYY-MM-DD)", value=datetime.today().strftime("%Y-%m-%d"))

if br_file and ads_file and date_input:
    try:
        merged_df = load_and_clean_reports(br_file, ads_file, date_input)
        st.success("✅ File merged successfully!")
        st.dataframe(merged_df.head())

        buffer = BytesIO()
        merged_df.to_excel(buffer, index=False)
        st.download_button("📥 Download Merged Excel", buffer.getvalue(), file_name="merged_daily_summary.xlsx")

        if st.checkbox("📤 Push to Google Sheets"):
            uploaded_cred = st.file_uploader("🔐 Upload Google Credentials JSON", type="json")

            if uploaded_cred:
                cred_dict = json.loads(uploaded_cred.read())
                
                # Auto get min/max date from merged_df
                start_date = merged_df['Date'].min()
                end_date = merged_df['Date'].max()

                filtered_df = merged_df[(merged_df['Date'] >= start_date) & (merged_df['Date'] <= end_date)]
                df_final = filtered_df[['Child_ASIN', 'Sessions', 'Units_Ordered', 'Clicks_Ads', 'Spend_Ads', 'Date']].sort_values(['Date', 'Child_ASIN'])

                try:
                    export_to_gsheet(df_final, "18juLU-AmJ8GVnKdGFrBrDT_qxqxcu_aLNK-2LYOsuYk", cred_dict, "DAILY_TH")
                    st.success(f"✅ Data pushed to Google Sheets from {start_date.date()} to {end_date.date()}!")
                except Exception as e:
                    st.error(f"❌ Failed to push to Google Sheets: {e}")
    except Exception as e:
        st.error(f"❌ Error processing files: {e}")
