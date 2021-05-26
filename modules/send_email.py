import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()


class SendEmail:
    def __init__(self, accounts):
        self.accounts = accounts

        self.message = MIMEMultipart("alternative")
        self.email = os.getenv('EMAIL_USERNAME')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.receiver = os.getenv('SEND_TO_EMAIL')

    def create_message(self, style, subject=""):
        # create the email message
        self.message['Subject'] = "Bot Accounts {}".format(subject)
        self.message['From'] = self.email
        self.message['To'] = self.receiver

        # Send Html message
        heading = """\
                    <html>
                      <body>
                      <style>
                            th {
                                font-family:verdana;
                            }
                            th, td {
                                border-bottom: 1px solid #ddd;
                                padding: 15px;
                                text-align: left;
                            }
                            table {
                                border-collapse: collapse;
                                width: 100%;
                            }
                        </style>
                           <table>
                            <tr>
                                <th>Country</th>
                                <th>Accounts Left</th>
                            </tr>
                           """

        middle = "<tr style={}>".format(style[0])
        middle += "<td>Kenya</td>"
        middle += "<td>{}</td>".format(self.accounts[0])
        middle += "<tr style={}>".format(style[1])
        middle += "<td>Uganda</td>"
        middle += "<td>{}</td>".format(self.accounts[1])
        middle += "<tr style={}>".format(style[2])
        middle += "<td>Tanzania</td>"
        middle += "<td>{}</td>".format(self.accounts[2])

        bottom = """
                </table>
                </body>
                </html>
        """

        html = heading + middle + bottom
        self.message.attach(MIMEText(html, "html"))

    def send_mail(self):
        server = smtplib.SMTP(os.getenv('SERVER_EMAIL'), 25)
        server.login(self.email, self.email_password)
        server.sendmail(self.email, self.receiver, self.message.as_string())
        server.quit()
