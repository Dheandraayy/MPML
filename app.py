import streamlit as st
import sqlite3 as sql
import joblib
import numpy as np
import os

# Menghubungkan ke database dan membuat tabel jika belum ada
conn = sql.connect('customer.db')
print("Membuat database baru")

conn.execute('''
CREATE TABLE IF NOT EXISTS customer (
    id INTEGER NOT NULL PRIMARY KEY,
    Age INTEGER,
    Gender TEXT,
    Monthly_Income TEXT,
    Family_Size INTEGER
)
''')
print("Tabel berhasil dibuat")
conn.close()

# Memeriksa apakah file model ada dan memuatnya
model_file = 'best_model_xgb.pkl'
if os.path.exists(model_file):
    model = joblib.load(model_file)
    print(f"Model {model_file} berhasil dimuat.")
else:
    st.error(f"File {model_file} tidak ditemukan. Pastikan file tersebut ada di direktori yang benar.")
    st.stop()

# Halaman Utama
st.title("Customer Feedback Prediction App")

# Pilihan Menu
menu = ["Home", "Add Customer", "List Customers", "Predict Feedback"]
choice = st.sidebar.selectbox("Menu", menu)

# Fungsi untuk menambah data pelanggan
def add_customer():
    st.subheader("Enter Customer Information")
    with st.form(key="customer_form"):
        id = st.text_input("ID")
        age = st.number_input("Age", min_value=0, step=1)
        gender = st.selectbox("Gender", ["Male", "Female"])
        monthly_income = st.selectbox("Monthly Income", ["No Income", "Below Rs.10000", "10001 to 25000", "25001 to 50000", "More than 50000"])
        family_size = st.number_input("Family Size", min_value=1, step=1)
        submit_button = st.form_submit_button(label="Add Record")

    if submit_button:
        try:
            with sql.connect("customer.db") as con:
                cur = con.cursor()
                cur.execute('''
                    INSERT INTO customer (id, Age, Gender, Monthly_Income, Family_Size) 
                    VALUES (?, ?, ?, ?, ?)
                ''', (id, age, gender, monthly_income, family_size))
                con.commit()
                st.success("Record added successfully")
        except Exception as e:
            con.rollback()
            st.error(f"Error occurred: {str(e)}")
        finally:
            con.close()

# Fungsi untuk menampilkan daftar pelanggan
def list_customers():
    st.subheader("Customer List")
    con = sql.connect("customer.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM customer")
    data = cur.fetchall()
    con.close()
    if data:
        st.table(data)
    else:
        st.warning("No customer data found")

# Fungsi untuk prediksi feedback pelanggan
def predict_feedback():
    st.subheader("Predict Customer Feedback")
    with st.form(key="predict_form"):
        age = st.number_input("Age", min_value=0, step=1)
        gender = st.selectbox("Gender", ["Male", "Female"])
        monthly_income = st.selectbox("Monthly Income", ["No Income", "Below Rs.10000", "10001 to 25000", "25001 to 50000", "More than 50000"])
        family_size = st.number_input("Family Size", min_value=1, step=1)
        predict_button = st.form_submit_button(label="Predict Feedback")

    if predict_button:
        try:
            gender_map = {'Male': 0, 'Female': 1}
            income_map = {
                'No Income': 0,
                'Below Rs.10000': 1,
                '10001 to 25000': 2,
                '25001 to 50000': 3,
                'More than 50000': 4
            }
            gender = gender_map[gender]
            monthly_income = income_map[monthly_income]
            features = np.array([[age, gender, monthly_income, family_size]])
            prediction = model.predict(features)
            result = "Positive" if prediction[0] == 1 else "Negative"
            st.success(f"Predicted Feedback: {result}")
        except Exception as e:
            st.error(f"Error occurred: {str(e)}")

# Menampilkan konten berdasarkan pilihan menu
if choice == "Home":
    st.write("Welcome to the Customer Feedback Prediction App")
elif choice == "Add Customer":
    add_customer()
elif choice == "List Customers":
    list_customers()
elif choice == "Predict Feedback":
    predict_feedback()
