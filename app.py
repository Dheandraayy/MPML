import streamlit as st
import sqlite3 as sql
import joblib
import numpy as np
import os

# Memeriksa apakah file model ada dan memuatnya
model_file = 'best_model_xgb.pkl'
if os.path.exists(model_file):
    model = joblib.load(model_file)
    print(f"Model {model_file} berhasil dimuat.")
else:
    st.error(f"File {model_file} tidak ditemukan. Pastikan file tersebut ada di direktori yang benar.")
    st.stop()

# Fungsi untuk prediksi feedback pelanggan
def predict_feedback():
    # Tambahkan CSS kustom untuk latar belakang dan ikon
    st.markdown(
        """
        <style>
        body {
            background-image: url('https://www.abestfashion.com/wp-content/uploads/2019/09/Online-Food-Delivery-Takeaway.jpg');  /* Ganti URL ini dengan URL gambar latar belakang Anda */
            background-size: cover;
        }
        .stApp {
            background: rgba(0, 0, 0, 0.5);
            color: white;
        }
        .icon {
            width: 100px;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.image('https://icon-library.com/images/food-app-icon/food-app-icon-0.jpg', width=100)  # Ganti URL ini dengan URL ikon Anda
    st.title("Customer Feedback Prediction App")
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

# Menampilkan halaman prediksi feedback
predict_feedback()
