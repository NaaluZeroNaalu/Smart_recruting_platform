import smtplib
from email.mime.text import MIMEText


password = "smartai1234"
email = "samrtairecruit@gmail.com"
app_password = "twcb lkxn iviy pakp"  # Use the app password here

msg = MIMEText("ai generated inivte text")
msg["Subject"] = "Invite"
msg["From"] = email
msg["To"] = "recievermail@gmail.com"

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Upgrade to a secure connection
        server.login(email, app_password)  # Login using the app password
        server.sendmail(email, ["recievermail@gmail.com"], msg.as_string())  # Send email
        print("Email sent successfully!")
except smtplib.SMTPAuthenticationError as e:
    print(f"Authentication error: {e}")
