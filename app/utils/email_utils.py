
 
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from jinja2 import Environment, FileSystemLoader
# from app.core.config import settings
# from email.message import EmailMessage
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent.parent
# TEMPLATES_DIR = BASE_DIR / "app" / "templates" 

# def send_email(
#     to_email: str,
#     subject: str,
#     context: dict,
# ):
  
#     env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
#     template = env.get_template("email.html")
#     html_content = template.render(**context)

#     msg = MIMEMultipart("alternative")
#     msg["From"] = settings.EMAIL_ADDRESS
#     msg["To"] = to_email
#     msg["Subject"] = subject

#     msg.attach(MIMEText(html_content, "html"))

#     with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
#          server.starttls()
#          server.login(
#              settings.EMAIL_ADDRESS,
#              settings.EMAIL_PASSWORD
#          )
#          server.send_message(msg)


#UPDATED EMAIL_UTIL.PY
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from app.core.config import settings
from pathlib import Path

# Robust pathing: find the 'templates' folder relative to this file's location
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"

def send_email(
    to_email: str,
    subject: str,
    context: dict,
):
    """
    Renders an HTML template and sends an email via SMTP.
    """
    try:
        # 1. Setup Jinja2 Environment
        if not TEMPLATES_DIR.exists():
            print(f"CRITICAL: Template directory not found at {TEMPLATES_DIR}")
            return

        env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
        template = env.get_template("email.html")
        html_content = template.render(**context)

        # 2. Construct the Email Message
        msg = MIMEMultipart("alternative")
        msg["From"] = settings.EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(html_content, "html"))

        # 3. Connect to Server and Send
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(
                settings.EMAIL_ADDRESS,
                settings.EMAIL_PASSWORD
            )
            server.send_message(msg)
            print(f"SUCCESS: Email sent to {to_email}")

    except Exception as e:
        # This will print the exact error (Auth error, Connection error, etc.) to your Uvicorn terminal
        print(f"ERROR: Failed to send email to {to_email}. Reason: {str(e)}")
        # We don't raise the error here so the API call doesn't crash if the email fails
