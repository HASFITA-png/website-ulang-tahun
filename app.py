from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Folder untuk menyimpan 5 foto
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS wishes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        message TEXT
    )''')

    conn.commit()
    conn.close()

init_db()


# Token rahasia untuk yang ulang tahun
SECRET_TOKEN = "UCAPAN ULANG TAHUN RESTY"


# ================= HALAMAN UTAMA =================
@app.route('/')
def index():
    images = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', images=images)


# ================= FORM UCAPAN =================
@app.route('/kirim', methods=['GET', 'POST'])
def kirim():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO wishes (name,message) VALUES (?,?)", (name, message))
        conn.commit()
        conn.close()

        return redirect('/success')

    return render_template('greeting_form.html')


# ================= SUKSES =================
@app.route('/success')
def success():
    return render_template('success.html')


# ================= DASHBOARD PRIVATE =================
@app.route('/dashboard/<token>')
def dashboard(token):
    if token != SECRET_TOKEN:
        return "Akses ditolak!"

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM wishes ORDER BY id DESC")
    data = c.fetchall()
    conn.close()

    return render_template('dashboard.html', data=data)

# ================= HAPUS UCAPAN =================
@app.route('/delete/<int:id>', methods=['POST'])
def delete_wish(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM wishes WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(request.referrer)


# ================= RUN =================
if __name__ == "__main__":
    app.run()

