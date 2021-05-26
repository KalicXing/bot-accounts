import MySQLdb
import os

from dotenv import load_dotenv

load_dotenv()


class SQLConnect:
    def __init__(self):
        self.cursor = None
        self.cursor1 = None
        self.cursor2 = None
        self.db = None
        self.clean_ke = None
        self.clean_ug = None
        self.ke1 = None
        self.ug1 = None
        self.tz1 = None
        self.ke = None
        self.ug = None
        self.accounts = []

    def sql_connection(self):
        # Open database connection
        self.db = MySQLdb.connect(os.getenv('IP'), os.getenv('sql_username'),
                                  os.getenv('sql_password'), os.getenv('sql_db'))
        # prepare a cursor object using cursor() method
        self.cursor = self.db.cursor()
        self.cursor1 = self.db.cursor()
        self.cursor2 = self.db.cursor()

        self.clean_ke = self.db.cursor()
        self.clean_ug = self.db.cursor()

    def clear_empty_accounts(self):
        # clear unresponsive data
        clear_ke = "delete from {} where account='';".format(os.getenv('TABLE'))
        clear_ug = "delete from {}UG where account='';".format(os.getenv('TABLE'))

        self.clean_ke.execute(clear_ke)
        self.db.commit()
        self.clean_ug.execute(clear_ug)
        self.db.commit()

        self.clean_ke.fetchone()
        self.clean_ug.fetchone()

    def get_accounts(self):
        # Get the accounts
        sql = "select count(account) from {} where assignedto='' and account !='';".format(os.getenv('TABLE'))
        sql1 = "select count(account) from {}UG where assignedto='' and account !='';".format(os.getenv('TABLE'))
        sql2 = "select count(account) from {}TZ where assignedto='' and account !='';".format(os.getenv('TABLE'))

        try:
            self.cursor.execute(sql)
            self.cursor1.execute(sql1)
            self.cursor2.execute(sql2)

            # Fetch all the rows in a list of lists.
            ke_accounts = int(self.cursor.fetchone()[0])
            ug_accounts = int(self.cursor1.fetchone()[0])
            tz_accounts = int(self.cursor2.fetchone()[0])

            # save account
            self.accounts.extend([ke_accounts, ug_accounts, tz_accounts])

            # Close the DB Connection
            self.db.close()

            # Now return fetched result
            return self.accounts

        except MySQLdb.Error:
            return "Error: unable to fetch data"

            # disconnect from server
