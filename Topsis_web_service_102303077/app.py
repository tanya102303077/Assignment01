from flask import Flask, render_template, request, redirect, url_for
import os
import re
import pandas as pd
from topsis_logic import run_topsis
from flask_mail import Mail, Message

app = Flask(__name__)

# ------------------ FOLDERS ------------------
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ------------------ EMAIL CONFIG ------------------
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_USERNAME")

mail = Mail(app)

RESULT_FILE = os.path.join(OUTPUT_FOLDER, "result.csv")

# ------------------ HELPERS ------------------
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# ------------------ ROUTES ------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        weights = request.form.get("weights")
        impacts = request.form.get("impacts")

        if not file or not weights or not impacts:
            return render_template("index.html", message="All fields are required")

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        try:
            run_topsis(input_path, weights, impacts, RESULT_FILE)
        except Exception as e:
            return render_template("index.html", message=str(e))

        df = pd.read_csv(RESULT_FILE)

        return render_template(
            "result.html",
            headers=list(df.columns),
            rows=df.values.tolist()
        )

    return render_template("index.html")


@app.route("/send-email", methods=["POST"])
def send_email():
    email = request.form.get("email")

    if not email or not is_valid_email(email):
        return "Invalid email", 400

    msg = Message(
        subject="TOPSIS Result",
        recipients=[email],
        sender=app.config["MAIL_DEFAULT_SENDER"],
        body="Please find the attached TOPSIS result."
    )

    with open(RESULT_FILE, "rb") as f:
        msg.attach("result.csv", "text/csv", f.read())

    mail.send(msg)
    return redirect(url_for("index"))


# ------------------ MAIN ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
