import logging
import re
import time

import mysql.connector

import crs

LOG_FILENAME = 'alert.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


def convertTuple(tup):
    str = ''.join(tup)
    return str


class DB:
    def __init__(self, passwrd):
        self.passwrd = passwrd

    def connect(self):
        db = mysql.connector.connect(host='localhost',
                                     user='void',
                                     passwd=self.passwrd,
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
    database = DB("11$Tar11")
    database.connect()
    # for potenal muilt threading for when i need to check muiltpule tables at once
    # sql = "select min(date) from alerts;"
    # time_of_last_check = database.read(sql)
    # sql = "select * from alerts where date > " + str(time_of_last_check) + ";"
    # sql = "select  data_id from alerts"
    while True:
        table_name = []
        address = []
        success_crs = []
        num_alert = database.read(
            "select count(*) from alerts;")[0]
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
