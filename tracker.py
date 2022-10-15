from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import re
from bs4 import BeautifulSoup
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
        print("Browser failed to load transactions page time, check your internet connection")
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
    sleep(1000)


main()