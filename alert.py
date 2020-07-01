import logging
import re
import time

import mysql.connector
from sshtunnel import SSHTunnelForwarder

import crs

LOG_FILENAME = 'alert.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


def convertTuple(tup):
    str = ''.join(tup)
    return str


class DB:
    def __init__(self, passwrd, tunnel):
        self.tunnel = tunnel
        self.passwrd = passwrd
        server = SSHTunnelForwarder(
            (tunnel, 90),
            ssh_host_key=None,
            ssh_username="void",
            ssh_password=None,
            ssh_private_key="/home/void/.ssh/id_rsa",
            remote_bind_address=("127.0.0.1", 3306))
        self.server = server

    def connect(self):
        self.server.start()
        db = mysql.connector.connect(host='localhost',
                                     user='void',
                                     passwd=self.passwrd,
                                     port=self.server.local_bind_port,
                                     db='Production')
        self.db = db
        mycursor = self.db.cursor()
        self.mycursor = mycursor

    def close(self):
        self.db.close()

    def read(self, sql):
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchone()
        return myresult

    def reads(self, sql):
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        return myresult

    def execute(self, sql):
        self.mycursor.execute(sql)
        self.db.commit()


def main():
    database = DB("11$Tar11", "192.168.1.208")
    database.connect()
    # for potenal muilt threading for when i need to check muiltpule tables at once
    # sql = "select min(date) from alerts;"
    # time_of_last_check = database.read(sql)
    # sql = "select * from alerts where date > " + str(time_of_last_check) + ";"
    # sql = "select  data_id from alerts"
    while True:
        table_name = []
        address = []
        num_alert = int(database.read("select count(*) from alerts;"))
        # for potenal muilt threading for when i need to check muiltpule tables at once
        # print("select Address from WebsiteARV where id = " + str(id))
        # sql = "select table_name, data_id, date from alerts where$
        if num_alert >= 1:
            data_id = [int(x) for x in re.findall(
                '\d+', str(database.reads("select data_id from alerts")))]
            to_CRS = str(database.reads("select Address from WebsiteARV"))
            logging.debug('the address started to be CRSed ' + to_CRS)
            # data_id = database.reads("select data_id from alerts")
            for id in data_id:
                print("select Address from WebsiteARV where id = " + str(id))
                addy = (database.read(
                    "select Address from WebsiteARV where id = " + str(id))[0])
                logging.debug('the address returned is: ' + addy)
                address.append(addy)
            print(address)
            for addy in address:
                try:
                    logging.debug('the address CRSed is: ' + addy)
                    crs.search(addy, 1)
                except:
                    print("CRS failed for: " + addy)
                    logging.debug("CRS  failed for: " + addy)
                    continue
                print("CRS is complete for: " + addy)
                logging.debug("CRS is complete for: " + addy)
            for id in data_id:
                del_sql = "delete from alerts where id = " + str(id)
                database.execute(del_sql)
        else:
            time.sleep(60)


if __name__ == "__main__":
    try:
        main()
    finally:
        logging.debug('Alert stopped')
