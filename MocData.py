import streamlit as st
import pandas as pd
import requests
st.title("อ่านข้อมูล JSON จาก API")

url = "https://opendata.moph.go.th/api/report_data/s_kpi_head_injury/2562"

st.write("แหล่งข้อมูล:", url)

# ดึงข้อมูลจาก API
response = requests.get(url)
data = response.json()

# แปลงเป็น DataFrame
df = pd.DataFrame(data)

st.subheader("ข้อมูลผู้ใช้งานจาก API")
st.dataframe(df.head(10))
