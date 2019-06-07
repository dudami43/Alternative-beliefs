
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

def login_twitter(driver, username, password):

    # open the web page in the browser:
    driver.get("https://twitter.com/login")

    # find the boxes for username and password
    username_field = driver.find_element_by_class_name("js-username-field")
    password_field = driver.find_element_by_class_name("js-password-field")

    # enter your username:
    username_field.send_keys(username)
    driver.implicitly_wait(10)

    # enter your password:
    password_field.send_keys(password)
    driver.implicitly_wait(10)

    # click the "Log In" button:
    driver.find_element_by_class_name("EdgeButtom--medium").click()
    # login_twitter(driver, "MeoMTcc", "Twitter040399")
    # query = "https://twitter.com/realDonaldTrump/status/238717783007977473"
    # search_field = driver.find_elements_by_xpath("//input[@data-testid='SearchBox_Search_Input']")[0]
    # search_field.send_keys(query)
    # driver.implicitly_wait(1)
    # search_field.send_keys(Keys.ENTER)
    return

def search_twitter(driver, url):

    itens_url = url.split("/")

    query = "https://twitter.com/search?q=https%3A%2F%2Ftwitter.com%2F" + itens_url[3] + "%2Fstatus%2F" + itens_url[5] + "&src=typed_query"
    driver.get(query)
    
    driver.find_element_by_class_name("SearchNavigation-titleText").click() #lose focus from login box

    SCROLL_PAUSE_TIME = 3
    time.sleep(SCROLL_PAUSE_TIME)
    
    while True:
        # Get scroll height
        ### This is the difference. Moving this *inside* the loop
        ### means that it checks if scrollTo is still scrolling
        
        last_height = driver.execute_script("let divs = document.getElementsByClassName('AdaptiveSearchTimeline'); return divs[0].scrollHeight")

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.getElementsByClassName('AdaptiveSearchTimeline')[0].scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("let divs = document.getElementsByClassName('AdaptiveSearchTimeline'); return divs[0].scrollHeight")
        
        print(last_height, " ", new_height)
        if new_height == last_height:

            # try again (can be removed)
            driver.execute_script("window.scrollTo(0, document.getElementsByClassName('AdaptiveSearchTimeline')[0].scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("let divs = document.getElementsByClassName('AdaptiveSearchTimeline'); return divs[0].scrollHeight")

            # check if the page height has remained the same
            if new_height == last_height:
                break
            # if not, move on to the next loop
            else:
                last_height = new_height
                continue

    # extract the html for the whole lot:
    page_source = driver.page_source
    return page_source


driver = webdriver.Firefox(
        executable_path=r'C:\\geckodriver\\geckodriver.exe')

driver.wait = WebDriverWait(driver, 5)

search_twitter(driver, "https://twitter.com/globoesportecom/status/1137018982010183681")

# driver.close()