from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from datetime import date, timedelta, time, datetime
#import matplotlib.pyplot as plt
import numpy as np
import sys

#Croissant Butter, Croissant Chocolate, Croissant Almond, Croissant Ham And Cheddar, Muffin Blueberry, Muffin Morning Glory, Cookie Chocolate Chip, Scone Blueberry, Scone Orange Cranberry, Scone Maple Walnut, Coffee Cake, Cinnamon Bun, Scone Cheese and Cheddar, Scone Chocolate Chip, Bread Pumpkin, Pumpkin Cruffin

#Croissant Butter, Croissant Chocolate, Croissant Almond, Croissant Ham And Cheddar, Muffin Blueberry, Muffin Morning Glory, Cookie Chocolate Chip, Scone Blueberry, Scone Orange Cranberry, Scone Maple Walnut, Cinnamon Bun, Scone Chocolate Chip, Bread Pumpkin, Pumpkin Cruffin


#TODO: make it work better and catch errors please

def getDatesAndProducts():
    productList = ["Croissant Butter", "Croissant Chocolate", "Croissant Almond", "Croissant Ham And Cheddar", "Muffin Blueberry", "Muffin Morning Glory", "Cookie Chocolate Chip", "Scone Blueberry", "Scone Orange Cranberry", "Scone Maple Walnut", "Coffee Cake", "Cinnamon Bun", "Scone Cheese and Cheddar", "Scone Chocolate Chip", "Bread Pumpkin", "Pumpkin Cruffin"]
    BOOLEANProductList = [False] * len(productList)
    print("Please copy and paste the row from the spoilage sheet corresponding to the day you'd like analyzed: \n")
    row = input()
    row = row.split("\t")
    #Croissant Butter
    if row[13] == "0":
        BOOLEANProductList[0] = True
    #Croissant Chocolate
    if row[14] == "0":
        BOOLEANProductList[1] = True
    #Croissant Almond
    if row[15] == "0":
        BOOLEANProductList[2] = True
    #Croissant Ham And Cheddar
    if row[16] == "0":
        BOOLEANProductList[3] = True
    #Muffin Blueberry
    if row[17] == "0":
        BOOLEANProductList[4] = True
    #Muffin Morning Glory
    if row[18] == "0":
        BOOLEANProductList[5] = True
    #Cookie Chocolate Chip
    if row[19] == "0":
        BOOLEANProductList[6] = True
    #Scone Blueberry
    if row[20] == "0":
        BOOLEANProductList[7] = True
    #Scone Orange Cranberry
    if row[21] == "0":
        BOOLEANProductList[8] = True
    #Scone Maple Walnut
    if row[22] == "0":
        BOOLEANProductList[9] = True
    #Coffee Cake
    if row[24] == "0":
        BOOLEANProductList[10] = True
    #Cinnamon Bun
    if row[35] == "0":
        BOOLEANProductList[11] = True
    #Scone Cheese and Cheddar
    if row[36] == "0":
        BOOLEANProductList[12] = True
    #Scone Chocolate Chip
    if row[37] == "0":
        BOOLEANProductList[13] = True
    #Bread Pumpkin
    if row[40] == "0":
        BOOLEANProductList[14] = True
    #Pumpkin Cruffin
    #if row[42] == "0":
    #    BOOLEANProductList[15] = True
    finalList = []
    for i in range(len(productList)):
        if BOOLEANProductList[i]:
            finalList.append(productList[i])
    dateTemp = row[0].split(" ")[0].split("/")
    if len(dateTemp[1]) == 1:
        dateTemp[1] = "0" + dateTemp[1]
    formattedDate = date.fromisoformat(dateTemp[2] + "-" + dateTemp[0] + "-" + dateTemp[1])
    tempTime = row[0].split(" ")[1].split(":")
    if len(tempTime[0]) == 1:
        tempTime[0] = "0" + tempTime[0]
    formattedTime = time.fromisoformat(tempTime[0] + ":" + tempTime[1] + ":" + tempTime[2])
    timeCutOff = time.fromisoformat("04:00:00")
    if formattedTime < timeCutOff:
        operatingDay = formattedDate
    else:
        operatingDay = formattedDate + timedelta(days = 1)
    startTime = getStart(operatingDay)
    endTime = getEnd(operatingDay)
    return startTime, endTime, finalList

def getStart(operatingDay):
    yesterday = str(operatingDay - timedelta(days = 1)).split("-")
    formatted = yesterday[1] + yesterday[2] + yesterday[0] + "300"
    print("start date: ", formatted)
    return formatted

def getEnd(operatingDay):
    day = str(operatingDay).split("-")
    formatted = day[1] + day[2] + day[0] + "300"
    print("end date: ", formatted)
    return formatted

def graph(finalDict):
    pastries = []
    for item in finalDict:
        pastries.append(item)
    times = finalDict.values()
    timeList = []
    for t in times:
        hours_minutes = t[:-3]
        t_list = hours_minutes.split(":")
        if (t[-2:] == "pm"):
            t_list[0] = str(int(t_list[0]) + 12)
        timeList.append(time(int(t_list[0]), int(t_list[1]), 0))
    hours = [8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1]
    hourPrinter = ""
    lines = ""
    for i in range(72):
        addSpace = True
        if (i % 4) == 0:
            lines += "|"
            hourPrinter += str(hours[i//4])
            if i//4 in [2, 3, 4, 14, 15, 16]:
                addSpace = False
        lines += "-"
        if addSpace:
            hourPrinter += " "
    lines += "|"
    hourPrinter += "2"
    print(lines)
    print(hourPrinter)


def getTimes():
    print("""
Welcome to the product sales tracker. My goal with this project is to find out when we sell out of specific items.
    
    """)
    startTime, endTime, productsToSearchFor = getDatesAndProducts()
    finalDict = {}
    for prod in productsToSearchFor:
        finalDict[prod] = ""
    print(finalDict)
    options = webdriver.ChromeOptions() 
    browser = webdriver.Chrome(options=options)
    delay = 100 #seconds
    browser.get("https://www.clover.com/dashboard/login")
    browser.maximize_window()
    try:
        myElem = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.ID, "email-input")))
    except TimeoutException:
        print("Browser failed to load log-in page in time, check your internet connection", file=sys.stderr)
    emailSection = browser.find_element(By.ID, "email-input")
    emailSection.send_keys("doda.midnight@thecorp.org")
    passwordSection = browser.find_element(By.ID, "password-input")
    passwordSection.send_keys("Jfk1961.")
    logInButton = browser.find_element(By.ID, "log-in")
    logInButton.send_keys()
    logInButton.click()
    try:
        myElem = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Transactions")))
    except TimeoutException:
        print("Browser failed to load main page time, check your internet connection", file=sys.stderr)
    reportingTab = browser.find_element(By.PARTIAL_LINK_TEXT, "Transactions")
    reportingTab.click()
    try:
        myElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Payments')))
    except TimeoutException:
        print("Browser failed to load transactions page time, check your internet connection", file=sys.stderr)
    browser.find_element(By.LINK_TEXT, "Payments").click()
    browser.switch_to.frame(browser.find_element(By.TAG_NAME, "iframe"))
    sleep(1)
    browser.find_element(By.XPATH, '//*[@id="startDate-1"]').send_keys(startTime)
    browser.find_element(By.XPATH, '//*[@id="endDate-2"]').send_keys(endTime)
    sleep(5)
    browser.find_element(By.XPATH, '//*[@id="itemOptions-content"]').click()
    #browser.find_element(By.XPATH, '//*[@id="ember958"]/section/div[2]/div/button').click()
    try:
        myElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember995"]/ul/li[2]/a')))
    except TimeoutException:
        print("drop down failed", file=sys.stderr)
    browser.find_element(By.XPATH, '//*[@id="ember995"]/ul/li[2]/a').click()
    sleep(5)
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember982"]/table')))
    except TimeoutException:
        print("Browser failed to load transactions page in time, check your internet connection", file=sys.stderr)
    transactions = browser.find_elements(By.LINK_TEXT, 'Details')
    linkList = []
    for link in transactions:
        linkList.append(link.get_attribute("href"))
    breakSwitch = False
    while not breakSwitch:
        browser.switch_to.window(browser.window_handles[0])
        if (len(linkList) == 0):
            browser.switch_to.frame(browser.find_element(By.TAG_NAME, "iframe"))
            browser.find_element(By.XPATH, '//*[@id="ember1005"]/button[2]').click()
            try:
                myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember982"]/table')))
            except TimeoutException:
                print("Browser failed to load transactions page in time, check your internet connection", file=sys.stderr)
            transactions = browser.find_elements(By.LINK_TEXT, 'Details')
            for link in transactions:
                linkList.append(link.get_attribute("href"))
        browser.switch_to.window(browser.window_handles[0])
        #print(linkList)
        for i in range(len(linkList)):
            try:
                browser.execute_script("window.open('');")
                browser.switch_to.window(browser.window_handles[i + 1])
                browser.get(linkList[i])
            except IndexError:
                break
        receiptLinks = []
        for j in range(1, 11):
            try:
                browser.switch_to.window(browser.window_handles[j])
            except IndexError:
                print("end of day")
                print(finalDict)
                breakSwitch = True
            try:
                myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            except TimeoutException:
                print("Browser failed to load transactions in time, check your internet connection", file=sys.stderr)
            browser.switch_to.frame(browser.find_element(By.TAG_NAME, "iframe"))
            try:
                myElem = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember345"]/div[2]/div[3]/div[2]/div[1]/section/p[4]/a')))
                receiptLinks.append(browser.find_element(By.XPATH, '//*[@id="ember345"]/div[2]/div[3]/div[2]/div[1]/section/p[4]/a').get_attribute("href"))
            except TimeoutException:
                print("Failed transaction skipped", file=sys.stderr)
            except NoSuchElementException:
                print("Failed transaction skipped", file=sys.stderr)
        while (len(browser.window_handles) > 1):
            browser.switch_to.window(browser.window_handles[1])
            browser.close()
        browser.switch_to.window(browser.window_handles[0])
        for k in range(len(receiptLinks)):
            browser.execute_script("window.open('');")
            browser.switch_to.window(browser.window_handles[k + 1])
            browser.get(receiptLinks[k])
        for l in range(len(receiptLinks)):
            browser.switch_to.window(browser.window_handles[l + 1])
            try:
                myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'line-item')))
            except TimeoutException:
                print("Browser failed to load receipt in time", file=sys.stderr)
            products = browser.find_elements(By.CLASS_NAME, "line-item")
            time = browser.find_element(By.CLASS_NAME, "time").text
            for item in products:
                product = item.find_element(By.CLASS_NAME, "label")
                items = product.text.split("\n")
                thing = str(items[0])
                if thing[-4:-1] == " x ":
                    thing = thing[:-4]
                if (thing in productsToSearchFor):
                    print(finalDict[thing])
                    print("found it!")
                    finalDict[thing] = str(time)
                    print(thing + " at " + finalDict[thing])
                    productsToSearchFor.remove(thing)
            tester = True
        for value in finalDict.values():
            if value == "":
                tester = False
        if tester:
            breakSwitch = True
        else:
            del linkList[:10]
            while (len(browser.window_handles) > 1):
                browser.switch_to.window(browser.window_handles[1])
                browser.close()
    return finalDict
    

def main():
    final = getTimes()
    print(final)
    #final = {'Croissant Butter': '8:35 pm', 'Croissant Chocolate': '3:09 pm', 'Croissant Almond': '5:45 pm', 'Croissant Ham And Cheddar': '5:09 pm', 'Muffin Blueberry': '5:14 pm', 'Muffin Morning Glory': '11:43 pm', 'Cookie Chocolate Chip': '1:35 pm', 'Scone Blueberry': '11:05 pm', 'Coffee Cake': '11:52 pm', 'Cinnamon Bun': '10:06 pm', 'Scone Cheese and Cheddar': '3:40 pm', 'Scone Chocolate Chip': '10:28 pm', 'Bread Pumpkin': '2:25 pm', 'Pumpkin Cruffin': '4:15 pm'}
    #graph(final)

main()