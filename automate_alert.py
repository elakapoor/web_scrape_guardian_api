import smtplib
import ssl
from email.mime.text import MIMEText as MT
from email.mime.multipart import MIMEMultipart as MM
from email.mime.image import MIMEImage as MI
from datetime import date

def email_func(subject, receiver_email_address, sender_email_address, sender_password):
    """
    The function will attach the image and send the automatic email from the sender to all the receivers
    :param subject: The subject of the email to be sent
    :param receiver_email_address: The email address of the receiver
    :param sender_email_address: The email address of the sender
    :param sender_password: The password of the sender
    """
    receiver = receiver_email_address
    sender = sender_email_address
    sender_password = sender_password
    currnetdate = date.today()

    # create MIMEMultipart object
    msg = MM()
    msg["Subject"] = subject + " " + str(currnetdate)

    # assumes the image is in the current directory
    fp = open('article_numbers_' + str(currnetdate) + '.jpeg', 'rb')
    msgImage = MI(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image>')
    msgImage.add_header('Content-Disposition', 'inline', filename='article number')
    msg.attach(msgImage)

    # create the html for the message
    HTML = """
    <html>
        <body>
        <p><b> Number of Articles about Justin Trudeau over Time </b></p>
        </body>
    </html>
    """

    # create HTML MIMEtext object
    MTObj = MT(HTML, "html")

    # attach the MIMEtext object into the message container
    msg.attach(MTObj)

    # create a secure connection over the server and send the email
    # create secure socket layer (SSL) context object
    SSL_context = ssl.create_default_context()

    # create the secure Simple Mail Transfer Protocol (SMTP) connection
    server = smtplib.SMTP_SSL(host = "smtp.gmail.com", port = 465, context = SSL_context)

    # login to the email account
    server.login(sender, sender_password)

    # send the email
    for r in receiver:
        server.sendmail(sender, r, msg.as_string())

    server.quit()

if __name__ == '__main__':
    subject = "Articles about Canadian Prime Minister Justin Trudeau till"
    receiver_email_address = ["example1@gmail.com", "example2@gmail.com"]
    sender_email_address = "example@gmail.com"
    sender_password = "example password"

    email_func(subject, receiver_email_address, sender_email_address, sender_password)



