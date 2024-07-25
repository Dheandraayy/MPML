import streamlit as st
import joblib
import pandas as pd
import os

# Memuat model
model_path = 'best_model_xgb.pkl'
if not os.path.isfile(model_path):
    raise FileNotFoundError(f"File model {model_path} tidak ada.")
model = joblib.load(model_path)

# Aplikasi Streamlit
def main():
    st.title('Customer Feedback Prediction App')

    # Form untuk input
    with st.form(key='prediction_form'):
        age = st.number_input('Age', min_value=0)
        gender = st.selectbox('Gender', ['Male', 'Female'])
        monthly_income = st.selectbox('Monthly Income', ['No Income', 'Below Rs.10000', '10001 to 25000', '25001 to 50000', 'More than 50000'])
        family_size = st.number_input('Family Size', min_value=1, max_value=10)

        submit_button = st.form_submit_button(label='Predict')

        if submit_button:
            # Konversi input ke DataFrame dengan nama kolom yang sesuai dengan model
            gender_map = {'Male': 0, 'Female': 1}
            income_map = {
                'No Income': 0,
                'Below Rs.10000': 1,
                '10001 to 25000': 2,
                '25001 to 50000': 3,
                'More than 50000': 4
            }

            data = pd.DataFrame({
                'Age': [age],
                'Gender': [gender_map[gender]],
                'Monthly Income': [income_map[monthly_income]],
                'Family size': [family_size]
            })

            st.write("Input Data for Prediction:")
            st.write(data)

            # Prediksi
            try:
                prediction = model.predict(data)[0]
                st.write(f'Prediction: {"Positive" if prediction == 1 else "Negative"}')
            except ValueError as e:
                st.write(f'Error in prediction: {e}')

if __name__ == "__main__":
    main()
