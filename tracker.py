from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from datetime import date

def getDate():
    today = str(date.today()).split("-")
    formatted = today[1] + today[2] + today[0] + "200A"
    return formatted

def main():
    print("""
Welcome to the product sales tracker. My goal with this project is to find out when we sell out of specific items.

IF YOU ARE GOING TO ENTER A PRODUCT NAME, MAKE SURE IT IS EXACTLY HOW IT APPEARS IN CLOVER!!!
    
    """)
    vape = input("Please enter the products you want to search for, separate by a comma and a space: ")
    productsToSearchFor = vape.split(", ")
    finalDict = {}
    for prod in productsToSearchFor:
        finalDict[prod] = ""
    print(finalDict)
    options = webdriver.ChromeOptions() 
    browser = webdriver.Chrome(options=options)
    delay = 30 #seconds
    browser.get("https://www.clover.com/dashboard/login")
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

    sleep(1)
    endDate = browser.find_element(By.XPATH, '//*[@id="endDate-2"]')
    endDate.click()
    endDate.send_keys(getDate())
    sleep(1)
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
            #print("going to next")
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
            browser.switch_to.window(browser.window_handles[j])
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
                if (thing in productsToSearchFor) and (finalDict[thing] == ""):
                    print(finalDict[thing])
                    print("found it!")
                    finalDict[thing] = str(time)
                    print(thing + " at " + finalDict[thing])
            tester = True
        for value in finalDict.values():
            if value == "":
                tester = False
        if tester:
            breakSwitch = True
        else:
            try:
                del linkList[:10]
            except IndexError:
                print("end of day")
            while (len(browser.window_handles) > 1):
                browser.switch_to.window(browser.window_handles[1])
                browser.close()
    print(finalDict)

main()