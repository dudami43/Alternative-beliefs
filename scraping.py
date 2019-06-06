# -*- coding: utf-8 -*-
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
#from urllib import urlopen
from bs4 import BeautifulSoup as bs
import json
import time
import itertools


def init_driver():

    # initiate the driver:
    driver = webdriver.Firefox(
        executable_path=r'C:\\geckodriver\\geckodriver.exe')
    # driver = webdriver.Firefox()

    # set a default wait time for the browser [5 seconds here]:
    driver.wait = WebDriverWait(driver, 5)

    return driver


def close_driver(driver):

    driver.close()

    return


def login_twitter(driver, username, password):

    # open the web page in the browser:
    driver.get("https://twitter.com/login")

    # find the boxes for username and password
    username_field = driver.find_element_by_class_name("js-username-field")
    password_field = driver.find_element_by_class_name("js-password-field")

    # enter your username:
    username_field.send_keys(username)
    driver.implicitly_wait(1)

    # enter your password:
    password_field.send_keys(password)
    driver.implicitly_wait(1)

    # click the "Log In" button:
    driver.find_element_by_class_name("EdgeButtom--medium").click()

    return

def open_page_tweet(driver, url):

    driver.get(url)
 
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

    # extract the html for the whole lot:
    page_source = driver.page_source
 
    return page_source



def get_data_tweet(elem, previous_id):

    if(previous_id is None):
        elem = elem.find("div", class_="tweet")
        user_details_div = elem

    tweet = {
        'tweet_id': elem['data-item-id'],
        'replie_to': previous_id,
        'text': None,
        'user_id': None,
        'user_screen_name': None,
        'user_name': None,
        'created_at': None,
        'retweets': 0,
        'likes': 0,
        'replies': 0
    }
    # Tweet Text
    text_p = elem.find("p", class_="tweet-text")
    if text_p is not None:
        tweet['text'] = text_p.get_text()

    # Tweet date
    date_span = elem.find("span", class_="_timestamp")
    if date_span is not None:
        tweet['created_at'] = float(date_span['data-time-ms'])

    # Tweet Retweets
    retweet_span = elem.select(
        "span.ProfileTweet-action--retweet > span.ProfileTweet-actionCount")
    if retweet_span is not None and len(retweet_span) > 0:
        tweet['retweets'] = int(
            retweet_span[0]['data-tweet-stat-count'])

    # Tweet Likes
    like_span = elem.select(
        "span.ProfileTweet-action--favorite > span.ProfileTweet-actionCount")
    if like_span is not None and len(like_span) > 0:
        tweet['likes'] = int(like_span[0]['data-tweet-stat-count'])

    # Tweet Replies
    reply_span = elem.select(
        "span.ProfileTweet-action--reply > span.ProfileTweet-actionCount")
    if reply_span is not None and len(reply_span) > 0:
        tweet['replies'] = int(
            reply_span[0]['data-tweet-stat-count'])

    # Tweet User ID, User Screen Name, User Name
    if (previous_id is not None):
        user_details_div = elem.find("div", class_="tweet")

    if user_details_div is not None:
        tweet['user_id'] = user_details_div['data-user-id']
        tweet['user_screen_name'] = user_details_div['data-screen-name']
        tweet['user_name'] = user_details_div['data-name']

    return tweet


def extract_replies(page_source, replies, current, tweets):

    soup = bs(page_source, 'lxml')
    current_split = current.split("/")
    previous_id = current_split[5]

    for ol in soup.find_all("ol", class_='stream-items'):

        pick_first_tweet = False
        is_ancestor = ((ol.parent).parent).parent

        if (is_ancestor.get('id') != "ancestors"):
            # If our ol is an ancestor, it is already in our list.

            for li in ol.find_all("li", class_='js-stream-item'):

                if 'data-item-id' not in li.attrs:
                    # If our li doesn't have a tweet-id, we skip it as it's not going to be a tweet.
                    continue

                elif (not pick_first_tweet):

                    pick_first_tweet = True
                    tweet = get_data_tweet(li, previous_id)
                    url = "https://twitter.com/" + \
                        tweet['user_screen_name'] + \
                        "/status/" + tweet['tweet_id']
                    try:
                        tweets[tweet['tweet_id']]
                    except:
                        replies.add(url)
                        tweets[tweet['tweet_id']] = tweet


def get_original_tweet(page_source, tweets):
    soup = bs(page_source, 'lxml')
    first = soup.find("div", class_='permalink-tweet-container')
    tweet = get_data_tweet(first, None)
    tweets[tweet['tweet_id']] = tweet


def search(driver, replies):
    tweets = dict()
    
    for each in replies:
        source = open_page_tweet(driver, each)
        print("Peguei a página do tweet")
        get_original_tweet(source, tweets)

    while(len(replies) > 0):
        current = replies.pop()
        source = open_page_tweet(driver, current)
        print(current)
        extract_replies(source, replies, current, tweets)

    return tweets


def main():
    file = open("replies.json", "w+", encoding='utf8')
    replies = {"https://twitter.com/realDonaldTrump/status/238717783007977473"}
    driver = init_driver()

    tweets = search(driver, replies)

    file.write(json.dumps(tweets, ensure_ascii=False))

    close_driver(driver)


if __name__ == "__main__":
    main()
