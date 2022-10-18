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



def main():
    options = webdriver.ChromeOptions() 
    browser = webdriver.Chrome(options=options)
    finalList = []
    delay = 30 #seconds
    browser.get("https://www.clover.com/dashboard/login")
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, "email-input")))
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
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Transactions")))
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
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="itemOptions"]')))
    except TimeoutException:
        print("Drop down button did not load in time")
    #sleep(1000)
    browser.find_element(By.XPATH, '//*[@id="itemOptions"]').click()
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember993"]/ul/li[8]')))
    except TimeoutException:
        print("Drop down menu did not load in time")
    browser.find_element(By.XPATH, '//*[@id="ember993"]/ul/li[8]').click()
    sleep(5)
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember980"]/table')))
    except TimeoutException:
        print("Browser failed to load transactions page in time, check your internet connection")
    transactions = browser.find_elements(By.LINK_TEXT, 'Details')
    print(len(transactions))
    linkList = []
    for link in transactions:
        linkList.append(link.get_attribute("href"))
    #for i in range(len(linkList)):
    for i in range(10):
        browser.execute_script("window.open('');")
        browser.switch_to.window(browser.window_handles[i + 1])
        browser.get(linkList[i])
    receiptLinks = []
    for j in range(1, 11):
        browser.switch_to.window(browser.window_handles[j])
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        except TimeoutException:
            print("Browser failed to transaction in time, check your internet connection")
        browser.switch_to.frame(browser.find_element(By.TAG_NAME, "iframe"))
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember345"]/div[2]/div[3]/div[2]/div[1]/section/p[4]/a')))
        except TimeoutException:
            print("Browser failed to transaction in time, check your internet connection")
        receiptLinks.append(browser.find_element(By.XPATH, '//*[@id="ember345"]/div[2]/div[3]/div[2]/div[1]/section/p[4]/a').get_attribute("href"))
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
        for item in products:
            product = item.find_element(By.CLASS_NAME, "label")
            #items = item.text.split("\n")[0].split("\n")
            items = product.text.split("\n")
            #print("items: " + str(items))
            print("items[0]: " + str(items[0]))
    sleep(1000)


main()