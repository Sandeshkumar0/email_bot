from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        recipients = request.form.get("recipients").split(",")
        subject = request.form.get("subject")
        body = request.form.get("body")

        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = ", ".join(recipients)
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipients, message.as_string())
        server.quit()

        return jsonify({"status": "success", "sent_to": recipients})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
