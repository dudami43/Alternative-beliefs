
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

class wait_for_more_than_n_elements_to_be_present(object):
    def __init__(self, locator, count):
        self.locator = locator
        self.count = count
 
    def __call__(self, driver):
        try:
            elements = EC._find_elements(driver, self.locator)
            return len(elements) > self.count
        except StaleElementReferenceException:
            return False

def search_twitter(driver, url):
 
    driver.get(url)
 
    # initial wait for the search results to load
    wait = WebDriverWait(driver, 20)
 
    try:
        # wait until the first search result is found. Search results will be tweets, which are html list items and have the class='data-item-id':
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li.stream-item")))
 
        # scroll down to the last tweet until there are no more tweets:
        while True:
 
            # extract all the tweets:
            tweets = driver.find_elements_by_css_selector("li.stream-item")
 
            # find number of visible tweets:
            number_of_tweets = len(tweets)
            print(number_of_tweets)
            # keep scrolling:
            driver.execute_script("arguments[0].scrollIntoView();", tweets[-1])
            # driver.execute_script("window.scrollBy(0,500);") 
            # ActionChains(driver).key_down(Keys.CONTROL).send_keys(u'\ue010').key_up(Keys.CONTROL).perform()
            try:
                # wait for more tweets to be visible:
                wait.until(wait_for_more_than_n_elements_to_be_present(
                    (By.CSS_SELECTOR, "li.stream-item"), number_of_tweets))
 
            except TimeoutException:
                print("A")
                # if no more are visible the "wait.until" call will timeout. Catch the exception and exit the while loop:
                break
 
        # extract the html for the whole lot:
        page_source = driver.page_source
 
    except TimeoutException:
 
        # if there are no search results then the "wait.until" call in the first "try" statement will never happen and it will time out. So we catch that exception and return no html.
        page_source=None
 
    return page_source


driver = webdriver.Firefox(
        executable_path=r'C:\\geckodriver\\geckodriver.exe')

driver.wait = WebDriverWait(driver, 5)

search_twitter(driver, "https://twitter.com/realDonaldTrump/status/238717783007977473")