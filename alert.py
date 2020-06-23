import mysql.connector
import time
import crs
import MLS_comp

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
    print("select Address from WebsiteARV where id = " + str(id))
    print(num_alert)
    #sql = "select table_name, data_id, date from alerts where$
    if num_alert > 1:
        data_id = database.reads("select data_id from alerts")
        for id in data_id:
            print("select Address from WebsiteARV where id = " + str(id))
            search_sql = "select Address from WebsiteARV where id = " + str(id)
            address.append(database.reads(search_sql))
        crs.main(address)
        for id in data_id:
            del_sql = "delete from WebsiteARV where id = " + str(id)
            database.execute(del_sql)
    elif num_alert > 0:
        id = int(database.read("select data_id from alerts"))
        search_sql = "select Address from WebsiteARV where id = " + str(id)
        print(id)
        address = (database.read(search_sql))
        print(address)
        property = list(crs.main(address))
        del_sql = "delete from alerts where data_id = " + str(id)
        database.execute(del_sql)
        MLS_comp.main(property)
    else:
        time.sleep(60)
