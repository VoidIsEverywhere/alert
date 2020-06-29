import time
import re
import mysql.connector
import logging
import crs

LOG_FILENAME = 'alert.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

def convertTuple(tup):
    str =  ''.join(tup)
    return str


class DB:
    def __init__(self):
        pass

    def connect(self):

        db = mysql.connector.connect(host='localhost',
                                     user='void',
                                     passwd="11$Tar11",
                                     db='Production')
        self.db = db
        mycursor = self.db.cursor()
        self.mycursor = mycursor

    def close(self):
        self.db.close()

    def read(self, sql):
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchone()
        return myresult[0]

    def reads(self, sql):
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        return myresult

    def execute(self, sql):
        self.mycursor.execute(sql)
        self.db.commit()


def main():
    database = DB()
    database.connect()
    # for potenal muilt threading for when i need to check muiltpule tables at once
    # sql = "select min(date) from alerts;"
    # time_of_last_check = database.read(sql)
    # sql = "select * from alerts where date > " + str(time_of_last_check) + ";"
    sql = "select  data_id from alerts"
    while True:
        table_name = []
        address = []
        num_alert = int(database.read("select count(*) from alerts;"))
        # for potenal muilt threading for when i need to check muiltpule tables at once
        # print("select Address from WebsiteARV where id = " + str(id))
        # sql = "select table_name, data_id, date from alerts where$
        if num_alert >= 1:
            a_string = str(database.reads("select data_id from alerts"))
            data_id = [int(x) for x in re.findall(
                '\d+', str(database.reads("select data_id from alerts")))]
            to_CRS = str(database.reads("select Address from WebsiteARV"))
            logging.debug('the address started to be CRSed ' + to_CRS)
            # data_id = database.reads("select data_id from alerts")
            for id in data_id:
                print("select Address from WebsiteARV where id = " + str(id))
                search_sql = "select Address from WebsiteARV where id = " + \
                    str(id)
                address.append(convertTuple(database.reads(search_sql)[0]))
            for addy in address:
                try:
                    crs.search(addy, 1)
                except:
                    print("CRS failed for: " + addy)
                    logging.debug("CRS  failed for: " + addy)
                    continue
                print("CRS is complete for: " + addy)
                logging.debug("CRS is complete for: " + addy)
            for id in data_id:
                del_sql = "delete from WebsiteARV where id = " + str(id)
                database.execute(del_sql)
        else:
            time.sleep(60)


if __name__ == "__main__":
    try:
        main()
    finally:
        logging.debug('Alert stopped')
