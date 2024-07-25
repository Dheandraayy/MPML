from flask import Flask, render_template, request
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

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Memeriksa apakah file model ada dan memuatnya
model_file = 'best_model_xgb.pkl'
if os.path.exists(model_file):
    model = joblib.load(model_file)
    print(f"Model {model_file} berhasil dimuat.")
else:
    print(f"File {model_file} tidak ditemukan. Pastikan file tersebut ada di direktori yang benar.")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/enternew')
def new_customer():
    return render_template('datacustomer.html')

@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            # Mengambil data dari formulir
            id = request.form['id']
            age = request.form['Age']
            gender = request.form['Gender']
            monthly_income = request.form['Monthly_Income']
            family_size = request.form['Family_Size']

            # Memasukkan data ke database
            with sql.connect("customer.db") as con:
                cur = con.cursor()
                cur.execute('''
                    INSERT INTO customer (id, Age, Gender, Monthly_Income, Family_Size) 
                    VALUES (?, ?, ?, ?, ?)
                ''', (id, age, gender, monthly_income, family_size))
                con.commit()
                msg = "Rekaman berhasil ditambahkan"
        except Exception as e:
            con.rollback()
            msg = f"Terjadi kesalahan saat menambah rekaman: {str(e)}"
        finally:
            return render_template("result.html", msg=msg)
            con.close()

@app.route('/list')
def list():
    con = sql.connect("customer.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM customer")

    rows = cur.fetchall()
    return render_template("list.html", rows=rows)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Mengambil data dari formulir untuk prediksi
            age = float(request.form['Age'])
            family_size = float(request.form['Family_Size'])
            gender = request.form['Gender']
            monthly_income = request.form['Monthly_Income']

            # Konversi input menjadi format yang sesuai dengan model
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

            # Memasukkan fitur ke dalam array
            features = np.array([[age, gender, monthly_income, family_size]])
            prediction = model.predict(features)
            result = "Positive" if prediction[0] == 1 else "Negative"
        except Exception as e:
            result = f"Terjadi kesalahan dalam prediksi: {str(e)}"

        return render_template("result.html", msg=f"Prediksi Feedback: {result}")
    else:
        return render_template('predict.html')

if __name__ == '__main__':
    print(f"Direktori kerja saat ini: {os.getcwd()}")
    app.run(debug=True)
