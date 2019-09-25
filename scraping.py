# -*- coding: utf-8 -*-
import threading
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from urllib.request import urlopen
# ubuntu from urllib import urlopen
# from urllib import urlopen
from bs4 import BeautifulSoup as bs
import json
import time
import random
from joblib import Parallel, delayed


def init_driver():

    # initiate the driver:
    options = Options()
    options.headless = True
    # driver = webdriver.Firefox(options=options, executable_path=r'C:\\geckodriver\\geckodriver.exe')
    driver = webdriver.Firefox()

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
    SCROLL_PAUSE_TIME = random.randint(7, 13)

    while True:
        # Get scroll height
        # This is the difference. Moving this *inside* the loop
        # means that it checks if scrollTo is still scrolling
        last_height = driver.execute_script(
            "let divs = document.getElementsByClassName('PermalinkOverlay'); return divs[0].scrollHeight")

        # Scroll down to bottom
        driver.execute_script(
            "let divs = document.getElementsByClassName('PermalinkOverlay')[0]; divs.scrollTo(0, document.getElementsByClassName('PermalinkOverlay')[0].scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script(
            "let divs = document.getElementsByClassName('PermalinkOverlay'); return divs[0].scrollHeight")

        print(last_height, " ", new_height)
        if new_height == last_height:

            # try again (can be removed)
            driver.execute_script(
                "let divs = document.getElementsByClassName('PermalinkOverlay')[0]; divs.scrollTo(0, document.getElementsByClassName('PermalinkOverlay')[0].scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script(
                "let divs = document.getElementsByClassName('PermalinkOverlay'); return divs[0].scrollHeight")

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


def open_page_search(driver, url):

    itens_url = url.split("/")

    query = "https://twitter.com/search?q=https%3A%2F%2Ftwitter.com%2F" + \
        itens_url[3] + "%2Fstatus%2F" + itens_url[5] + "&src=typed_query"
    time.sleep(1)
    driver.get(query)
    driver.find_element_by_class_name(
        "SearchNavigation-titleText").click()  # lose focus from login box

    SCROLL_PAUSE_TIME = random.randint(7, 13)
    time.sleep(SCROLL_PAUSE_TIME)

    while True:
        # Get scroll height
        # This is the difference. Moving this *inside* the loop
        # means that it checks if scrollTo is still scrolling

        last_height = driver.execute_script(
            "let divs = document.getElementsByClassName('AdaptiveSearchTimeline'); return divs[0].scrollHeight")

        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.getElementsByClassName('AdaptiveSearchTimeline')[0].scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script(
            "let divs = document.getElementsByClassName('AdaptiveSearchTimeline'); return divs[0].scrollHeight")

        print(last_height, " ", new_height)
        if new_height == last_height:

            # try again (can be removed)
            driver.execute_script(
                "window.scrollTo(0, document.getElementsByClassName('AdaptiveSearchTimeline')[0].scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script(
                "let divs = document.getElementsByClassName('AdaptiveSearchTimeline'); return divs[0].scrollHeight")

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


def get_data_tweet(elem, previous_id, quoted_id=None):

    if(previous_id is None):
        elem = elem.find("div", class_="tweet")
        user_details_div = elem

    tweet = {
        'tweet_id': elem['data-item-id'],
        'replie_to': previous_id,
        'quoting': quoted_id,
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

    soup = bs(page_source, "html.parser")
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

                    if(tweet['text'] is not None):
                        url = "https://twitter.com/" + \
                            tweet['user_screen_name'] + \
                            "/status/" + tweet['tweet_id']
                        try:
                            tweets[tweet['tweet_id']]
                        except:
                            replies.add(url)
                            tweets[tweet['tweet_id']] = tweet


def extract_quotes(page_source, quotes):

    soup = bs(page_source, "html.parser")

    for li in soup.find_all("li", class_='js-stream-item'):
        if 'data-item-id' not in li.attrs:
            # If our li doesn't have a tweet-id, we skip it as it's not going to be a tweet.
            continue

        else:
            tweet_details = li.find("div", class_="tweet")
            if tweet_details is not None:
                url = "https://twitter.com" + \
                    tweet_details['data-permalink-path']
                quotes.add(url)


def get_original_tweet(page_source, tweets, quoted_id):
    soup = bs(page_source, "html.parser")
    first = soup.find("div", class_='permalink-tweet-container')
    tweet = get_data_tweet(first, None, quoted_id)
    tweets[tweet['tweet_id']] = tweet


def bfs(driver, original, quoted_id):
    tweets = dict()
    try:
        source = open_page_tweet(driver, original)
        print("Peguei a página do tweet")
        get_original_tweet(source, tweets, quoted_id)
    except:
        print("N peguei ", original)

    replies = {original}
    while(len(replies) > 0):
        current = replies.pop()
        try:
            source = open_page_tweet(driver, current)
            print(current)
            extract_replies(source, replies, current, tweets)
        except:
            print("N peguei ", current)
    return tweets


def get_replies(driver, originals, quoted_id=None):
    for each in originals:
        print("Getting replies of", each)
        link = each.split("/")
        if(quoted_id is not None):
            file_name = "dados/celebs/replies_" + \
                quoted_id + "_" + link[5] + ".json"
        else:
            file_name = "dados/celebs/replies_" + link[5] + ".json"
        file = open(file_name, "w+", encoding='utf8')
        tweets = bfs(driver, each, quoted_id)
        file.write(json.dumps(tweets, ensure_ascii=False))


def get_quotes(driver, originals):

    for each in originals:
        print("Getting quotes of", each)
        quotes = set()
        try:
            source = open_page_search(driver, each)
            extract_quotes(source, quotes)
        except:
            print("Não abri busca de ", each)
        link = each.split("/")
        get_replies(driver, quotes, link[5])
        time.sleep(random.randint(7, 13))


def main():

    driver1 = init_driver()
    driver2 = init_driver()
    driver3 = init_driver()

    random.seed()

    part1 = [ "https://twitter.com/50cent/status/22201409032",
              "https://twitter.com/SHAQ/status/3435123096",
              "https://twitter.com/KimKardashian/status/22396212024"        
    ]

    part2 = [ "https://twitter.com/KrisJenner/status/243812456558903296",
              "https://twitter.com/edsheeran/status/6462855740",
              "https://twitter.com/justinbieber/status/10180145361"        
    ]

    part3 = [ "https://twitter.com/HulkHogan/status/21587600569",
               "https://twitter.com/piersmorgan/status/242303672569188354"
        
    ]

    # Parallel(n_jobs=2)(delayed(get_replies)(init_driver(), tweet) for tweet in tweets)
    x = threading.Thread(target=get_quotes, args=(driver1, part1,))
    y = threading.Thread(target=get_quotes, args=(driver2, part2,))
    z = threading.Thread(target=get_quotes, args=(driver3, part3,))
    x.start()
    y.start()
    z.start()
    x.join()
    y.join()
    z.join()
    # get_replies(driver, originals)
    # get_quotes(driver, originals)

    close_driver(driver1)
    close_driver(driver2)
    close_driver(driver3)


if __name__ == "__main__":
    main()
