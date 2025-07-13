import smtplib
from email.message import EmailMessage

def email_alert(subject,body,to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    msg['from'] = 'youpp208@gmail.com'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('youpp208@gmail.com', 'tsscafuyathxauua')
    server.send_message(msg)
    server.quit()
    print("Email sent successfully to",to)

#     email_alert("Test Email", "This is a test email", "naivaidyanegi@gmail.com"


