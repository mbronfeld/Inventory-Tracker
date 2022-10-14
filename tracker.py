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
    #options.add_argument("--auto-open-devtools-for-tabs")
    browser = webdriver.Chrome(options=options)
    finalList = []
    delay = 20 #seconds
    browser.get("https://www.clover.com/dashboard/login")
    #browser.maximize_window()
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
        #myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id='ember980']/table/tr[4]")))
        #myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "c-table-row")))
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Voids")))
    except TimeoutException:
        print("Browser failed to load transactions page time, check your internet connection")
    #browser.key()
    transactions = browser.find_elements(By.CSS_SELECTOR, '[roll="table"]')
    print(len(transactions))
    #for link in transactions:
        #print(link)
        #link.send_keys(Keys.CONTROL + 't')
    sleep(1000)

main()