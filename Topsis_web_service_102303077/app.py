from flask import Flask, render_template, request, redirect, url_for, flash
import os
import re
import csv
from topsis_logic import run_topsis
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = "topsis-secret-key"

# ------------------ FOLDERS ------------------
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ------------------ EMAIL CONFIG (RENDER SAFE) ------------------
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")

mail = Mail(app)

# ------------------ HELPERS ------------------
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def read_csv_as_table(path):
    with open(path, newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    return rows[0], rows[1:]  # header, data

# ------------------ ROUTES ------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        weights = request.form.get("weights")
        impacts = request.form.get("impacts")

        if not file or not weights or not impacts:
            flash("All fields are required")
            return redirect(url_for("index"))

        if not file.filename.endswith(".csv"):
            flash("Only CSV files allowed")
            return redirect(url_for("index"))

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(OUTPUT_FOLDER, "result.csv")

        file.save(input_path)

        try:
            run_topsis(input_path, weights, impacts, output_path)
        except Exception as e:
            flash(str(e))
            return redirect(url_for("index"))

        header, data = read_csv_as_table(output_path)

        return render_template(
            "result.html",
            header=header,
            data=data
        )

    return render_template("index.html")


@app.route("/send-email", methods=["POST"])
def send_email():
    email = request.form.get("email")

    if not email or not is_valid_email(email):
        flash("Invalid email address")
        return redirect(url_for("index"))

    output_path = os.path.join(OUTPUT_FOLDER, "result.csv")

    if not os.path.exists(output_path):
        flash("Result file not found. Generate result first.")
        return redirect(url_for("index"))

    try:
        msg = Message(
            subject="TOPSIS Result",
            sender=app.config["MAIL_USERNAME"],
            recipients=[email],
            body="Attached is your TOPSIS result CSV file."
        )

        with open(output_path, "rb") as f:
            msg.attach("result.csv", "text/csv", f.read())

        mail.send(msg)
        flash("Email sent successfully")

    except Exception as e:
        flash(f"Email failed: {e}")

    return redirect(url_for("index"))

# ------------------ MAIN ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
