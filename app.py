import os
from flask import Flask, render_template, request, redirect, session, send_from_directory, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "gizli_anahtar_123")

KULLANICI = os.environ.get("ADMIN_USER", "admin")
SIFRE = os.environ.get("ADMIN_PASS", "1234")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"pdf"}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") == KULLANICI and request.form.get("password") == SIFRE:
            session["giris"] = True
            return redirect("/anasayfa")
    return render_template("login.html")

@app.route("/cikis")
def cikis():
    session.clear()
    return redirect("/")

@app.route("/anasayfa")
def anasayfa():
    if not session.get("giris"):
        return redirect("/")
    return render_template("index.html")

@app.route("/kitaplar")
def kitaplar():
    if not session.get("giris"):
        return redirect("/")
    files = os.listdir(UPLOAD_FOLDER)
    pdfler = [f for f in files if f.lower().endswith(".pdf")]
    return render_template("kitaplar.html", pdfler=pdfler)

@app.route("/yukle", methods=["POST"])
def yukle():
    if not session.get("giris"):
        return redirect("/")
    if "pdf" not in request.files:
        return redirect("/kitaplar")
    file = request.files["pdf"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)
    return redirect("/kitaplar")

@app.route("/dosya/<path:filename>")
def dosya(filename):
    if not session.get("giris"):
        return redirect("/")
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=False)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
