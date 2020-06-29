import csv
import json
import os
import time
from datetime import datetime

import mysql.connector
from selenium import webdriver

import webscrap

timeOfLastSearch = time.time()
NOW = datetime.now()
TIME_STAMP_OF_SCRAP = NOW.strftime("%m.%d.%Y,%H:%M")


class DB:
    def __init__(self, passwrd):
        self.passwrd = passwrd

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


def load_from_file(filelocation):
    """Loads subdivison, year built, number of baths, number of bedrooms and
square feet from file passed and passes back a list with all the info"""

    with open(filelocation, 'rb') as f:
        reader = csv.reader(f)
        file = list(reader)
    return(file)


def start_driver():
    # PROXY = "23.80.166.29:29842"  # IP:PORT or HOST:PORT
    #
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--proxy-server=%s' % PROXY)

    chrome = webdriver.Chrome()
    return(chrome)


def MLScomp(DRIVER, current_date, subdivision,
            yearbuilt, numbath, numbedrooms, sqft, address, database):
    os.system("mkdir -p /home/void/Documents/MLScomp/" +
              str(current_date) + "/" + str(subdivision))
    DRIVER.switch_to.default_content()
    DRIVER.switch_to.frame('main')
    DRIVER.switch_to.frame('workspace')
    webscrap.click(
        "//*[@id='searchFieldContainerOuterBox']/div[1]/table/tbody/tr[1]/td[3]/table/tbody/tr/td[2]/span/i", DRIVER)
    webscrap.type("SLD", "//*[@id='STATUSID']", DRIVER)
    webscrap.type(subdivision, "//*[@id='SUBDIVISION_ALLID']", DRIVER)
    webscrap.click(
        "//*[@id='searchFieldContainerOuterBox']/div[1]/table/tbody/tr[18]/td[3]/table/tbody/tr/td[2]/span/i", DRIVER)
    webscrap.type("9 Months", "//*[@id='MONTHS_BACKID']", DRIVER)

    if yearbuilt > 1999:
        yearmax = yearbuilt + 5
        yearmin = yearbuilt - 5
    else:
        yearmax = yearbuilt + 15
        yearmin = yearbuilt - 15

    maxbath = numbath + 1
    minbath = numbath - 1
    maxsqft = sqft + ((sqft / 100) * 20)
    minsqft = sqft - ((sqft / 100) * 20)

    webscrap.type(numbedrooms, "//*[@id='minBEDROOMS']", DRIVER)
    webscrap.type(numbedrooms, "//*[@id='maxBEDROOMS']", DRIVER)
    webscrap.type(yearmin, "//*[@id='minYEAR_BUILT_RANGE']", DRIVER)
    webscrap.type(yearmax, "//*[@id='maxYEAR_BUILT_RANGE']", DRIVER)
    webscrap.type(minbath, "//*[@id='minFULLBATHS']", DRIVER)
    webscrap.type(maxbath, "//*[@id='maxFULLBATHS']", DRIVER)
    webscrap.type(str(int(maxsqft)), "//*[@id='maxSQFEET']", DRIVER)
    webscrap.type(str(int(minsqft)), "//*[@id='minSQFEET']", DRIVER)


# This section exports the list as a tsv file so comps can be done
    webscrap.click("//*[@id='exportbuttonLink']", DRIVER)
    webscrap.click("//*[@id='Next>>']", DRIVER)
    DRIVER.switch_to.default_content()
    DRIVER.switch_to.frame("main")
    DRIVER.switch_to.frame("workspace")
    webscrap.click("//*[@id='Continue']", DRIVER)
    webscrap.click("//*[@id=' OK ']", DRIVER)
    os.system("mv /home/void/Documents/MLScomp/ConnectMLS_export.TSV /home/void/Documents/MLScomp/" +
              str(current_date) + "/" + subdivision + "/data.tsv")
    # this is for saving pdf file
    # webscrap.click("//*[@id='searchButtonBottom']", DRIVER)
    # webscrap.click("//*[@id='alldcidnull']", DRIVER)
    # DRIVER.switch_to.default_content()
    # DRIVER.switch_to.frame("main")
    # DRIVER.switch_to.frame("subheader")
    # webscrap.click("//*[@id='printButtonLink']", DRIVER)
    # DRIVER.switch_to.default_content()
    # DRIVER.switch_to.frame("main")
    # DRIVER.switch_to.frame("workspace")
    # webscrap.click("/html/body/form/div/div[2]/div/fieldset[2]/div/div/div[1]/div[2]/div[2]", DRIVER)
    # webscrap.click("/html/body/form/div/div[2]/div/fieldset[2]/div/div/div[2]/input[1]", DRIVER)
    # webscrap.click("/html/body/form/div/div[2]/div/fieldset[2]/div/div/div[1]/div[2]/div[9]", DRIVER)
    # webscrap.click("/html/body/form/div/div[2]/div/fieldset[2]/div/div/div[2]/input[1]", DRIVER)
    # webscrap.click("//*[@id='summaryChoicemapfirst']", DRIVER)
    # webscrap.click("//*[@id='searchButtonTop']", DRIVER)
    # DRIVER.switch_to.default_content()
    # DRIVER.switch_to.frame("main")
    # DRIVER.switch_to.frame("workspace")
    # DRIVER.execute_script('window.print();')
    # os.system("mv '/home/void/Documents/MLScomp/Luis Alonso _ connectMLS.pdf' /home/void/Documents/MLScomp/"
    #           + str(current_date) + "/" + subdivision + "/report.pdf")
    tsv_file = open("/home/void/Documents/MLScomp/" +
                    str(current_date) + "/" + subdivision + "/data.tsv")
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    addresses = []
    prices = []
    beds = []
    baths = []
    SQFTs = []
    pricesqft = []
    Subdivision = []
    x = 0
    for row in read_tsv:
        if x != 0:
            pricesqft.append(int(row[6]) / int(row[11]))
            addresses.append(row[3] + " " + row[4] + row[5])
            prices.append(row[6])
            beds.append(row[8])
            baths.append(row[9])
            SQFTs.append(row[11])
            Subdivision.append(subdivision)

        x = x + 1

    len_pricesqft = len(pricesqft)
    if len_pricesqft % 2 == 0:
        median1 = pricesqft[len_pricesqft // 2]
        median2 = pricesqft[len_pricesqft // 2 - 1]
        median = (median1 + median2) / 2
    else:
        median = pricesqft[len_pricesqft // 2]

    runinng_sum = 0
    for num in pricesqft:
        runinng_sum = runinng_sum + num

        average = runinng_sum / len_pricesqft
    offer = (average + median) / 2
    offer = offer * sqft
    offer = (offer * .7) - 20000
    print("The max price of sqft")
    print(int(max(pricesqft)))
    print("The min price of sqft")
    print(int(min(pricesqft)))
    print("The median of price")
    print(int(median))
    print("The average of price sqft")
    print(int(average))
    file = open(subdivision + '.txt', 'w')
    file.write("The max price of sqft: " + str(int(max(pricesqft))) +
               "   The min price of sqft:" + str(int(min(pricesqft))) +
               " The median of price:" + str(int(median)) +
               "  The average of price sqft: " + str(int(average)))
    os.system("mv " + subdivision + ".txt /home/void/Documents/MLScomp/" +
              str(current_date) + "/" + subdivision + "/" + subdivision + ".txt")
    file.close()

    try:
        database.connect()
    except mysql.connector.errors.InterfaceError:
        database.connect()

    val = address, numbath, numbedrooms, sqft, yearbuilt, subdivision, offer
    sql = "INSERT INTO MLS (Address, Bathrooms, BedRooms, SQFT, YearBuilt, Subdivison, offer) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    database.save_row(sql, val)
    vals = []
    sql = "INSERT INTO Comp (Address, Subdivison, SQFT, BR, FB, ListPrice) VALUES (%s, %s, %s, %s, %s, %s)"

    for (var_address, var_subdivision, var_SQFT, var_bed, var_bath, var_price) in zip(addresses, Subdivision, SQFTs, beds, baths, prices):
        insert = var_address, var_subdivision, var_SQFT, var_bed, var_bath, var_price
        vals.append(insert)
    database.save_rows(sql, vals)

    return


def main(propeties):
    try:
        now = datetime.now()
        current_date = now.strftime("%m-%d-%Y")
        database = DB("192.168.1.208", "11$Tar11")
        settings = {
            "appState": {
                "recentDestinations": [{
                    "id": "Save as PDF",
                    "origin": "local"
                }],
                "selectedDestinationId": "Save as PDF",
                "version": 2
            }
        }
        prefs = {'printing.print_preview_sticky_settings': json.dumps(settings), 'download.default_directory': '/home/void/Documents/MLScomp', 'savefile.default_directory': '/home/void/Documents/MLScomp'
                 }
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument('--kiosk-printing')
        DRIVER = webdriver.Chrome(options=chrome_options)
        DRIVER.get("https://api-sabor.connectmls.com/sso/login")
        webscrap.wait_for_element("//*[@id='j_username']", 15, DRIVER)
        webscrap.click("//*[@id='j_username']", DRIVER)
        webscrap.type("651941", "//*[@id='j_username']", DRIVER)
        webscrap.click("//*[@id='j_password']", DRIVER)
        webscrap.type("C00kie05", "//*[@id='j_password']", DRIVER)
        webscrap.click("//*[@name='go']", DRIVER)
        DRIVER.get("http://sabor.connectmls.com/ssologin.jsp?storefront=true")
        webscrap.wait_for_element(
            "//*[@id='header']/div/div[2]/div[2]/div[2]/div/div/div/a", 15, DRIVER)
        webscrap.click_thro(
            "//*[@id='header']/div/div[2]/div[2]/div[2]/div/div/div/a", DRIVER)
        property = propeties
        subdivision = property[0]
        yearbuilt = int(property[1])
        numbath = property[2]
        numbedrooms = property[3]
        sqft = property[4]
        address = property[5]
        subdivision = subdivision.replace(" ", "_")
        MLScomp(DRIVER, current_date, subdivision, yearbuilt, numbath,
                numbedrooms, sqft, address, database)
        # for property in propeties:
        #     subdivision = property[3]
        # MLScomp(DRIVER, subdivision, current_date)

    finally:
        DRIVER.quit()
        database.close()

    return()
