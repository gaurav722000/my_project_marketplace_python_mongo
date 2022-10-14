import datetime
from shared.db import mdb
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def error_log(userid, method_type, received_json, description):
    try:
        mdb.error_log.insert_one(
            {
                "userid": userid,
                "method_type": method_type,
                "received_json": received_json,
                "description": description,
                "activity_time": datetime.datetime.now()
            }
        )
    except Exception as e:
        print("error_log error----->>>", e)

def activity_log(userid, method_type, received_json, description):
    try:
        mdb.activity_log.insert_one(
            {
                "userid": userid,
                "method_type": method_type,
                "received_json": received_json,
                "description": description,
                "activity_time": datetime.datetime.now()
            }
        )
    except Exception as e:
        print("activity_log error----->>>", e)
        error_log("activity_log", "entry-of-activity_log", "errr: in activity_log", e)

# def send_mail(email, html):
#     sender_email = "niqoxtechnology@gmail.com"
#     password = "niqox@123"

#     message = MIMEMultipart("alternative")
#     message["Subject"] = "VerificationCode"
#     message["From"] = sender_email
#     message["To"] = email
#     part1 = MIMEText(html, "html")
#     message.attach(part1)

#     context = ssl.create_default_context()
#     try:
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#             server.login(sender_email, password)
#             server.sendmail(
#                 sender_email, email, message.as_string()
#             )
#     except Exception as e:
#         return "Error {} occurred while sending email.".format(e)
