import streamlit as st
import requests

# 1. กำหนดค่า API (แทนที่ YOUR_API_KEY ด้วยคีย์จริง)
API_KEY = "0fec19a7f74aaa811fd1289e"
API_URL = f"https://api.exchangerate-api.com/v4/latest/USD" # ตัวอย่างใช้ USD เป็นฐาน

# 2. ฟังก์ชันสำหรับดึงอัตราแลกเปลี่ยน
def get_exchange_rates():
    try:
        response = requests.get(API_URL)
        data = response.json()
        return data['rates']
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการดึงข้อมูลอัตราแลกเปลี่ยน: {e}")
        return {}

# 3. ส่วนหลักของ Streamlit App
st.title("💰 เครื่องคำนวณอัตราแลกเปลี่ยนเงินตรา")

rates = get_exchange_rates()
currencies = list(rates.keys())

if rates:
    # สร้างคอลัมน์สำหรับช่องเลือกสกุลเงิน
    col1, col2 = st.columns(2)
    
    with col1:
        amount = st.number_input("จำนวนเงินที่ต้องการแลก", min_value=0.01, value=100.0)
        from_currency = st.selectbox("จากสกุลเงิน", currencies, index=currencies.index('THB')) # ตั้งค่าเริ่มต้นเป็น THB
        
    with col2:
        st.write(" ") # เพื่อจัดตำแหน่งให้ตรงกัน
        to_currency = st.selectbox("ไปยังสกุลเงิน", currencies, index=currencies.index('USD')) # ตั้งค่าเริ่มต้นเป็น USD
    
    # คำนวณอัตราแลกเปลี่ยน
    if from_currency in rates and to_currency in rates:
        
        # แปลงจากสกุลเงินตั้งต้นเป็น USD ก่อน
        rate_from_usd = 1 / rates[from_currency] # สมมติฐานว่า API เป็นแบบ USD-base
        
        # แปลงจาก USD ไปยังสกุลเงินปลายทาง
        final_rate = rates[to_currency] * rate_from_usd

        converted_amount = amount * final_rate
        
        # แสดงผลลัพธ์
        st.markdown(f"## ผลลัพธ์:")
        st.success(f"{amount:,.2f} **{from_currency}** = **{converted_amount:,.2f}** **{to_currency}**")
        st.info(f"อัตราแลกเปลี่ยน: 1 {from_currency} = {final_rate:,.4f} {to_currency}")
