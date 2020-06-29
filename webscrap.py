import csv
import os
import random
import re
import sys
import time
import urllib
from datetime import datetime

from selenium.webdriver.common.keys import Keys


def check_if_element_is_there(xpath, driver):
    """Check to see if the element at the passed xpath is present."""
    x_values = 0
    while x_values < 10:
        element = driver.find_elements_by_xpath(xpath)
        if element != []:
            return 1
        time.sleep(.25)
        x_values = x_values + 1
    return 0


def wait_for_element(xpath, how_long_to_wait, driver):
    """Wait for a element to apear for the passed amount of time."""
    x_values = how_long_to_wait
    i = 0
    if how_long_to_wait == 0:
        while True:
            element = driver.find_elements_by_xpath(xpath)
            if element == []:
                time.sleep(1)
            else:
                return()
    else:
        while i < x_values:
            element = driver.find_elements_by_xpath(xpath)
            if element == []:
                time.sleep(1)
                i = i + 1
            else:
                return()
        return("N/A")


def rand_type(string, xpath, driver):
    """Types passed string to the element passed at random speeds."""
    element = driver.find_element_by_xpath(xpath)
    i = 0
    length = len(string)
    while i < length:
        time.sleep(random.uniform(.05, .25))
        element.send_keys(string[i])
        i = i + 1
    return()


def type(string, xpath, driver):
    """Types passed string to the element passed at random speeds."""
    element = driver.find_element_by_xpath(xpath)
    if string == "ENTER":
        element.send_keys(Keys.RETURN)
    element.send_keys(string)
    return()


def click(xpath, driver):
    """Will click element located at xpath."""
    button = driver.find_element_by_xpath(xpath)
    button.click()
    return()


# def speed_limiter(timeOfLastSearch):
#     """Limits the speed of searching."""
#     while (timeOfLastSearch + time.sleep(random.uniform(.5, 1))) > time.time():
#         time.sleep(1)
#     timeOfLastSearch = time.time()
#     return timeOfLastSearch


def get_text(xpath, driver):
    """Get the text from the passed xpath."""
    element_present = check_if_element_is_there(xpath, driver)
    if element_present == 1:
        element_with_text = driver.find_element_by_xpath(xpath)
        text = element_with_text.text
    else:
        text = "N/A"
    return text


def get_texts(xpath, driver):
    """Get the texts from the passed xpath."""
    text = []
    element_present = check_if_element_is_there(xpath, driver)
    if element_present == 1:
        elements_with_text = driver.find_elements_by_xpath(xpath)
        for element in elements_with_text:
            text.append(element.text)
    else:
        text = "N/A"
    return text


def get_url(xpath, driver):
    """Get the url from passed element xpath."""
    element_present = check_if_element_is_there(xpath, driver)
    if element_present == 0:
        return "N/A"
    element = driver.find_element_by_xpath(xpath)
    url = element.get_attribute("xlink:href")
    print(url)
    return url


def get_img(xpath, driver):
    """Get the photo from passed element xpath."""
    element_present = check_if_element_is_there(xpath, driver)
    if element_present == 0:
        return "N/A"
    element = driver.find_element_by_xpath(xpath)
    photo = element.get_attribute('src')
    return photo

# x_values = 0
# loopNum is to track how may loops since the last browser reset
# loop_num = 0


def click_thro(xpath, driver):
    """It clicks buttons that would can be useing the other method."""
    element_present = check_if_element_is_there(xpath, driver)
    if element_present == 1:
        element = driver.find_element_by_xpath(xpath)
        driver.execute_script("arguments[0].click();", element)
        return
    return


def do_nothing():
    """Absoulty nothing."""
    return()


# def save_to_sql(address, doc_num, my_cursor, x_values):
#     """Save address and doc number to the SQL database."""
#     os.system("clear")
#     print("Address of property:              " + str(address))
#     print("")
#     print("# of address:                     " + str(x_values))
#     print("")
#     sql = "INSERT INTO BCAD (owner, mail_address, address) VALUES (%s, %s, %s)"
#     val = (address, doc_num)
#     my_cursor.execute(sql, val)
#     DB.commit()
#     print(MYCURSOR.rowcount, "record inserted.")
#     return()


def save_to_file(address, doc_num, x_values):
    """Save address and doc number to csv file."""
    os.system("clear")
    os.system("clear")
    print("Address of property:              " + str(address))
    print("")
    print("# of address:                     " + str(x_values))
    print("")

    fields = [address, doc_num]
    with open(r'output.csv', 'a') as f_values:
        writer = csv.writer(f_values)
        writer.writerow(fields)

    return()


def save_failure(address, x_values):
    """Save all failed searches to CSV file for later review."""
    os.system("clear")
    print("Failure to find at address:" + str(address))
    print("")
    print("")
    print("")
    print("")
    print("# of address:              " + str(x_values))
    print("")
    fields = [address, x_values]
    with open(r'failedSearches.csv', 'a') as f_values:
        writer = csv.writer(f_values)
        writer.writerow(fields)
    return()


# driver.set_window_position(0, 0)
# driver.set_window_size(500, 500)
# time_of_last_search = time.time()
#
# driver.get("https://whatismyipaddress.com/")
#
# input("press enter to countue")
#
# driver.quit()
# os.system("clear")

# everyone needs some positivity no and again
# print("Congrates you finished the scan !")
# DB.close()
# SERVER.stop()
