from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from datetime import date, timedelta, time
#import matplotlib.pyplot as plt
import numpy as np

#Croissant Butter, Croissant Chocolate, Croissant Almond, Croissant Ham And Cheddar, Muffin Blueberry, Muffin Morning Glory, Cookie Chocolate Chip, Scone Blueberry, Coffee Cake, Cinnamon Bun, Scone Cheese and Cheddar, Scone Chocolate Chip, Bread Pumpkin, Pumpkin Cruffin
#Croissant Butter, Croissant Chocolate, Croissant Almond, Croissant Ham And Cheddar, Muffin Blueberry, Muffin Morning Glory, Cookie Chocolate Chip, Scone Blueberry, Cinnamon Bun, Scone Cheese and Cheddar, Scone Chocolate Chip, Bread Pumpkin, Pumpkin Cruffin


#TODO: plotting


def getStart():
    today = date.today()
    yesterday = str(today - timedelta(days = 1)).split("-")
    formatted = yesterday[1] + yesterday[2] + yesterday[0] + "800A"
    return formatted

def getDate():
    today = str(date.today()).split("-")
    formatted = today[1] + today[2] + today[0] + "200A"
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

IF YOU ARE GOING TO ENTER A PRODUCT NAME, MAKE SURE IT IS EXACTLY HOW IT APPEARS IN CLOVER!!!
    
    """)
    print("Please enter the products you want to search for, separate by a comma and a space: ")
    print()
    vape = input()
    productsToSearchFor = vape.split(", ")
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
        print("Browser failed to load log-in page in time, check your internet connection")
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
        print("Browser failed to load main page time, check your internet connection")
    reportingTab = browser.find_element(By.PARTIAL_LINK_TEXT, "Transactions")
    reportingTab.click()
    try:
        myElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Payments')))
    except TimeoutException:
        print("Browser failed to load transactions page time, check your internet connection")
    browser.find_element(By.LINK_TEXT, "Payments").click()
    browser.switch_to.frame(browser.find_element(By.TAG_NAME, "iframe"))
    browser.find_element(By.LINK_TEXT, "Yesterday").click()
    browser.find_element(By.XPATH, '//*[@id="itemOptions"]').click()
    try:
        myElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember988"]/ul/li[2]')))
    except TimeoutException:
        print("drop down failed")
    browser.find_element(By.XPATH, '//*[@id="ember993"]/ul/li[2]').click()
    sleep(1)
    startDate = browser.find_element(By.XPATH, '//*[@id="ember904"]/section/div[2]/div/div[1]/label')
    startDate.click()
    browser.find_element(By.XPATH, '//*[@id="startDate-1"]').send_keys(getStart())
    endDate = browser.find_element(By.XPATH, '//*[@id="ember904"]/section/div[2]/div/div[2]/label')
    endDate.click()
    browser.find_element(By.XPATH, '//*[@id="endDate-2"]').send_keys(getDate())
    sleep(2)
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember980"]/table')))
    except TimeoutException:
        print("Browser failed to load transactions page in time, check your internet connection")
    transactions = browser.find_elements(By.LINK_TEXT, 'Details')
    print(len(transactions))
    linkList = []
    for link in transactions:
        linkList.append(link.get_attribute("href"))
    breakSwitch = False
    while not breakSwitch:
        browser.switch_to.window(browser.window_handles[0])
        if (len(linkList) == 0):
            #linkVerifier = False
            browser.switch_to.frame(browser.find_element(By.TAG_NAME, "iframe"))
            browser.find_element(By.XPATH, '//*[@id="ember1003"]/button[2]').click()
            try:
                myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember980"]/table')))
            except TimeoutException:
                print("Browser failed to load transactions page in time, check your internet connection")
            transactions = browser.find_elements(By.LINK_TEXT, 'Details')
            for link in transactions:
                linkList.append(link.get_attribute("href"))
        browser.switch_to.window(browser.window_handles[0])
        for i in range(len(linkList)):
            browser.execute_script("window.open('');")
            browser.switch_to.window(browser.window_handles[i + 1])
            browser.get(linkList[i])
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
                print("Browser failed to load transactions in time, check your internet connection")
            browser.switch_to.frame(browser.find_element(By.TAG_NAME, "iframe"))
            try:
                myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember345"]/div[2]/div[3]/div[2]/div[1]/section/p[4]/a')))
                receiptLinks.append(browser.find_element(By.XPATH, '//*[@id="ember345"]/div[2]/div[3]/div[2]/div[1]/section/p[4]/a').get_attribute("href"))
            except TimeoutException:
                print("Failed transaction skipped")
            except NoSuchElementException:
                print("Failed transaction skipped")
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
                print("Browser failed to load receipt in time")
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