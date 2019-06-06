from selenium import webdriver
import time
#from selenium.webdriver.support.ui import WebDriverWait

def main():
    driver = webdriver.Firefox(
        executable_path=r'C:\\geckodriver\\geckodriver.exe')
    driver.get('https://twitter.com/realDonaldTrump/status/238717783007977473')
    
    SCROLL_PAUSE_TIME = 1

    while True:
        # Get scroll height
        ### This is the difference. Moving this *inside* the loop
        ### means that it checks if scrollTo is still scrolling
        last_height = driver.execute_script("let divs = document.getElementsByClassName('PermalinkOverlay'); return divs[0].scrollHeight")

        # Scroll down to bottom
        driver.execute_script("let divs = document.getElementsByClassName('PermalinkOverlay')[0]; divs.scrollTo(0, document.getElementsByClassName('PermalinkOverlay')[0].scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("let divs = document.getElementsByClassName('PermalinkOverlay'); return divs[0].scrollHeight")
        if new_height == last_height:

            # try again (can be removed)
            driver.execute_script("let divs = document.getElementsByClassName('PermalinkOverlay')[0]; divs.scrollTo(0, document.getElementsByClassName('PermalinkOverlay')[0].scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("let divs = document.getElementsByClassName('PermalinkOverlay'); return divs[0].scrollHeight")

            # check if the page height has remained the same
            if new_height == last_height:
                # if so, you are done
                break
            # if not, move on to the next loop
            else:
                last_height = new_height
                continue


if __name__ == "__main__":
    main()