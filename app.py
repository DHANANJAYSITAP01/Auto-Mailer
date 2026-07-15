import os
import base64
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BREVO_API_KEY = os.environ.get("BREVO_API_KEY")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_NAME = "Dhananjay Sitap"
RESUME_PATH = os.path.join("resume", "Dhananjay_Sitap_DataEngineer_CV.pdf")

SUBJECT = "Application for Data Engineer - Dhananjay Sitap"

BODY_HTML = """
<p>Hello HR,</p>
<p>I'm Dhananjay Sitap, a Data Engineer with 1.6+ years of experience in Databricks, PySpark, SQL, Python, AWS (S3, Redshift, Athena), and GenAI (RAG, ChromaDB, LLM Tool Calling).</p>
<p>I have hands-on experience building production ETL/ELT pipelines for a leading U.S. retail client using Medallion Architecture.</p>
<p>I'm actively looking for Data Engineer opportunities. Please find my resume attached for your consideration.</p>
<p>
Portfolio: <a href="https://dhananjay-portfolio.onrender.com">https://dhananjay-portfolio.onrender.com</a><br>
LinkedIn: <a href="https://www.linkedin.com/in/dhananjay-sitap-095677327">https://www.linkedin.com/in/dhananjay-sitap-095677327</a><br>
GitHub: <a href="https://github.com/DHANANJAYSITAP01">https://github.com/DHANANJAYSITAP01</a>
</p>
<p>Thank you for your time. I look forward to hearing from you.</p>
<p>
Best Regards,<br>
Dhananjay Sitap<br>
+91 9325538419<br>
dhananjay.sitap.data@gmail.com
</p>
"""


def send_email(to_email: str):
    if not BREVO_API_KEY or not SENDER_EMAIL:
        return False, "Server not configured: BREVO_API_KEY / SENDER_EMAIL missing."

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json",
    }

    payload = {
        "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
        "to": [{"email": to_email}],
        "subject": SUBJECT,
        "htmlContent": BODY_HTML,
    }

    if os.path.exists(RESUME_PATH):
        with open(RESUME_PATH, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        payload["attachment"] = [
            {"content": encoded, "name": os.path.basename(RESUME_PATH)}
        ]

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        if response.status_code in (200, 201):
            return True, "Email sent successfully."
        else:
            return False, f"Brevo error ({response.status_code}): {response.text}"
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
