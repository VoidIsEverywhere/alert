import pickle
import re
import time

import mysql.connector
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sshtunnel import SSHTunnelForwarder

from webscrap import scrapper


def headless():
    display = Display(visible=0, size=(800, 600))
    display.start()
    return display


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

    def save_rows(self, sql, val):
        self.mycursor.executemany(sql, val)
        self.db.commit()

    def save_row(self, sql, val):
        self.mycursor.execute(sql, val)
        self.db.commit()

    def close(self):
        self.db.close()

    def read(self, sql):
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        return myresult

    def execute(self, sql):
        self.mycursor.execute(sql)
        self.db.commit()


def cookie_load(driver):
    driver.delete_all_cookies()
    for cookie in pickle.load(open("cookies.pkl", "rb")):
        if 'expiry' in cookie:
            del cookie['expiry']
        driver.add_cookie(cookie)


def cookie_save(driver):
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))


def search(entered_addresses, mode):
    try:
        database = DB("11$Tar11", "192.168.1.208")
        if mode == 1:
            display = headless()
        webscrap = scrapper()
        driver = webdriver.Chrome()
        driver.get("https://api-sabor.connectmls.com/sso/login")
        webscrap.wait_for_element("//*[@id='j_username']", 15, driver)
        webscrap.click("//*[@id='j_username']", driver)
        webscrap.type("651941", "//*[@id='j_username']", driver)
        webscrap.click("//*[@id='j_password']", driver)
        webscrap.type("C00kie05", "//*[@id='j_password']", driver)
        webscrap.click("//*[@name='go']", driver)
        driver.get(
            "http://sabor.connectmls.com/ssologin.jsp?storefront=true")
        webscrap.wait_for_element(
            "//*[@id='header']/div/div[2]/div[3]/div[1]/a[7]",  30, driver)
        time.sleep(1)
        webscrap.click_thro(
            "//*[@id='header']/div/div[2]/div[3]/div[1]/a[7]", driver)
        webscrap.wait_for_element(
            "//*[@id='dcModal']/div/div/div[2]/div/div/div[1]/div[11]/a/span",  5, driver)
        webscrap.click_thro(
            "//*[@id='dcModal']/div/div/div[2]/div/div/div[1]/div[11]/a/span", driver)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        webscrap.click_thro("//*[@id='secondTab']", driver)
        time.sleep(2)
        webscrap.wait_for_element(
            "//*[@id='root']/main/main/div/section[2]/div[2]/div[1]/div[1]/div/span[1]/span[1]",  5, driver)
        webscrap.click("//*[@id='root']/main/main/div/section[3]", driver)
        webscrap.type(entered_addresses,
                      "//*[@id='react-select-2-input']", driver)
        element = driver.find_element_by_xpath(
            "//*[@id='react-select-2-input']")
        time.sleep(2)
        element.send_keys(Keys.RETURN)
        time.sleep(2)
        webscrap.click(
            "//*[@id='root']/main/main/div/section[3]/div[2]/div[3]/section/div[3]", driver)
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        subdivision = webscrap.get_text(
            "//*[@id='Main_PropertyInfoMain_trSubdivisions']/td[1]", driver)
        sqaurefeet = webscrap.get_text(
            "//*[@id='udsqftedit']", driver)
        br = int(webscrap.get_text(
            "//*[@id='buildingSection1']/div/div[1]/table/tbody/tr[4]/td[1]", driver))
        yearbuilt = int(webscrap.get_text(
            "//*[@id='buildingSection1']/div/div[1]/table/tbody/tr[3]/td[1]", driver))
        bath_room = int(webscrap.get_text(
            "//*[@id='udfullbathroomsedit1']", driver))
        name = webscrap.get_text(
            "//*[@id='Main_PropertyInfoMain_SalesHistoryTableEx']/tbody/tr[3]/td[1]", driver)
        fname, lname = name.split(" ", 1)
        zip = ""
        zip_temp = re.findall(r'[0-9]{5}', webscrap.get_text(
            "//*[@id='Main_PropertyInfoMain_locationSection']/div/table/tbody/tr[1]/td[1]", driver))
        for l in zip_temp:
            zip += l
        print(entered_addresses, bath_room, br, sqaurefeet,
              yearbuilt, subdivision, fname, lname, zip)
        try:
            database.connect()
        except mysql.connector.errors.InterfaceError:
            database.connect()
        sql = "INSERT INTO CRS (Address, Bathroom, Bedroom, SQFT, YearBuilt, Subdivison, first_name, last_name, zip ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = entered_addresses, bath_room, br, sqaurefeet, yearbuilt, subdivision, fname, lname, zip
        database.save_row(sql, val)
    finally:
        driver.quit()
        database.close()
        try:
            display.stop()
        except NameError:
            pass

    return(entered_addresses, bath_room, br, sqaurefeet, yearbuilt, subdivision, fname, lname, zip)


def main():
    entered_addresses = input("What address do you want search crs for. ")
    mode = int(input("press 1 for headless anything else for head."))
    entered_addresses, bath_room, br, sqaurefeet, yearbuilt, subdivision, fname, lname, zip = search(
        entered_addresses, mode)
    return(entered_addresses, bath_room, br, sqaurefeet, yearbuilt, subdivision, fname, lname, zip)


if __name__ == "__main__":
    main()
