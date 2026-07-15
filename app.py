import os
from flask import Flask, render_template, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
import ssl
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
RESUME_PATH = os.path.join("resume", "Dhananjay_Sitap_DataEngineer_CV.pdf")

SUBJECT = "Application for Data Engineer - Dhananjay Sitap"

BODY = """Hello HR,

I'm Dhananjay Sitap, a Data Engineer with 1.6+ years of experience in Databricks, PySpark, SQL, Python, AWS (S3, Redshift, Athena), and GenAI (RAG, ChromaDB, LLM Tool Calling).

I have hands-on experience building production ETL/ELT pipelines for a leading U.S. retail client using Medallion Architecture.

I'm actively looking for Data Engineer opportunities. Please find my resume attached for your consideration.

Portfolio: https://dhananjay-portfolio.onrender.com
LinkedIn: https://www.linkedin.com/in/dhananjay-sitap-095677327
GitHub: https://github.com/DHANANJAYSITAP01

Thank you for your time. I look forward to hearing from you.

Best Regards,
Dhananjay Sitap
+91 9325538419
dhananjay.sitap.data@gmail.com
"""


def send_email(to_email: str):
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        return False, "Server not configured: GMAIL_USER / GMAIL_APP_PASSWORD missing."

    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = SUBJECT
    msg.attach(MIMEText(BODY, "plain"))

    if os.path.exists(RESUME_PATH):
        with open(RESUME_PATH, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(RESUME_PATH))
            part["Content-Disposition"] = f'attachment; filename="{os.path.basename(RESUME_PATH)}"'
            msg.attach(part)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, to_email, msg.as_string())
        return True, "Email sent successfully."
    except smtplib.SMTPAuthenticationError:
        return False, "Gmail login failed. Check GMAIL_USER / GMAIL_APP_PASSWORD."
    except Exception as e:
        return False, str(e)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    to_email = (data.get("email") or "").strip()

    if "@" not in to_email or "." not in to_email:
        return jsonify({"success": False, "message": "Please enter a valid email address."}), 400

    success, message = send_email(to_email)
    status_code = 200 if success else 500
    return jsonify({"success": success, "message": message, "email": to_email}), status_code


if __name__ == "__main__":
    app.run(debug=True)
