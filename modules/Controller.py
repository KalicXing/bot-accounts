from time import sleep

from sql_connect import SQLConnect
from send_email import SendEmail
from datetime import datetime


class BOT:
    def __init__(self):

        self.first_record = []
        self.last_record = []

        self.style = []
        self.findings = []
        self.now = datetime.now()
        self.current_time = self.now.strftime("%H:%M")
        self.time_to_send = "08:00"

    def get_time(self, time):
        if self.current_time == time:
            return True

    def check_acc(self):
        # Get the first Round
        sql_connect = SQLConnect()

        sql_connect.sql_connection()
        self.first_record.extend(sql_connect.get_accounts())

        # Sleep for a minute for enough accounts to be created
        sleep(60)

        # Get Second Round
        sql_connect = SQLConnect()

        sql_connect.sql_connection()
        self.last_record.extend(sql_connect.get_accounts())

    def check_ke(self):
        # Check if KE accounts less than 100
        if self.last_record[0] < 100 and self.last_record[0] <= self.first_record[0]:
            self.style.extend(["background-color:#ffcccc"])
            return self.findings.append("True")
        else:
            self.style.extend(["background-color:#ccffcc"])
            return self.findings.append("False")

    def check_ug(self):
        # Check if UG accounts less than 15
        if self.last_record[1] < 15 and self.last_record[1] <= self.first_record[1]:
            self.style.extend(["background-color:#ffcccc"])
            return self.findings.append("True")
        else:
            self.style.extend(["background-color:#ccffcc"])
            return self.findings.append("False")

    def check_tz(self):
        # Check if TZ accounts less than 700
        if self.last_record[2] < 700 and self.last_record[2] <= self.first_record[2]:
            self.style.extend(["background-color:#ffcccc"])
            return self.findings.append("True")
        else:
            self.style.extend(["background-color:#ccffcc"])
            return self.findings.append("False")

    def send_email(self, subject=""):
        send_email = SendEmail(self.last_record)

        send_email.create_message(self.style, subject)
        send_email.send_mail()

    def compare(self):
        # Check Accounts
        self.check_ke()
        self.check_ug()
        self.check_tz()

        if 'True' in self.findings:
            self.send_email()

        # Send the report at 08:00
        elif self.get_time(self.time_to_send):
            self.send_email("as at {}".format(self.time_to_send))

    def run(self):
        self.check_acc()
        self.compare()
