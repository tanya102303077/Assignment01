from flask import Flask, render_template, request
import os
import re
from topsis_logic import run_topsis
from flask_mail import Mail, Message

app = Flask(__name__)

# ------------------ FOLDERS ------------------
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ------------------ EMAIL CONFIG ------------------
# IMPORTANT:
# MAIL_USERNAME and MAIL_PASSWORD must be set in Render Environment Variables

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_USERNAME")

mail = Mail(app)

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
        email = request.form.get("email")

        # -------- BASIC VALIDATION --------
        if not file or not weights or not impacts or not email:
            return render_template("index.html", message="All fields are required")

        if not file.filename.endswith(".csv"):
            return render_template("index.html", message="Only CSV files are allowed")

        if not is_valid_email(email):
            return render_template("index.html", message="Invalid email format")

        weights_list = [w.strip() for w in weights.split(",")]
        impacts_list = [i.strip() for i in impacts.split(",")]

        if len(weights_list) != len(impacts_list):
            return render_template(
                "index.html",
                message="Number of weights must be equal to number of impacts"
            )

        try:
            weights_list = [float(w) for w in weights_list]
        except ValueError:
            return render_template(
                "index.html",
                message="Weights must be numeric values"
            )

        for i in impacts_list:
            if i not in ["+", "-"]:
                return render_template(
                    "index.html",
                    message="Impacts must be either + or -"
                )

        # -------- FILE PATHS --------
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(
            OUTPUT_FOLDER,
            f"result_{email.split('@')[0]}.csv"
        )

        file.save(input_path)

        # -------- RUN TOPSIS --------
        try:
            run_topsis(input_path, weights, impacts, output_path)
        except Exception as e:
            return render_template(
                "index.html",
                message=f"TOPSIS processing error: {str(e)}"
            )

        # -------- SEND EMAIL (NON-BLOCKING SAFE) --------
        try:
            msg = Message(
                subject="TOPSIS Result File",
                recipients=[email],
                body=(
                    "Hello,\n\n"
                    "Please find the attached TOPSIS result CSV file.\n\n"
                    "Regards,\n"
                    "TOPSIS Web Service"
                )
            )

            with open(output_path, "rb") as f:
                msg.attach("result.csv", "text/csv", f.read())

            mail.send(msg)

        except Exception as e:
            print("Email error:", e)
            return render_template(
                "index.html",
                message="TOPSIS result generated, but email delivery failed"
            )

        return render_template(
            "index.html",
            message="Result generated successfully. Check your email."
        )

    return render_template("index.html")

# ------------------ MAIN ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
