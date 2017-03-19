import os
import sys
import argparse
import time
import datetime
import re
import string
import json
import csv
import pickle

from tweepy import API
from tweepy import OAuthHandler
from tweepy import Cursor

from xvfbwrapper import Xvfb
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException 
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import TweetTokenizer

from config import *

# COMMAND LINE OPTIONS
def mining_cml():
    """Command line arguments for mining.                                  
                                                                                
    Options                                                                      
    --------                
    virtual : bool (optional, default True)
            Use virtual display (i.e., use on EC2 instances).

    tweets_lim : int (default -1)
            Maximum number of tweets to be mined. 
            Default `-1` will either be limited by the twitter API or by
            the range of dates provided.
    
    search : bool (optional, default True)
            Search for tweets.
    
    multisearch : bool (optional, default True)
            Perform multiple searches in parallel.
    
    write : bool (optional, default True)
            Get the entire tweet obtained from a previous search.
    
    compile_docs : bool (optional, default True)
            Compile all obtained tweets into a dataset - assumes a directory
            structure in which there is a dir `users` containing a subdir for
            each user in the search..

    Returns                                                                     
    -------                                                                     
    {argparse-obj} cml arguments container.                                     
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", 
                        help="increase output verbosity",        
                        action="store_true")
    parser.add_argument("-d", "--virtual",                                      
                        help="Use virtual display (use on EC2 instance).",                       
                        action="store_true")
    parser.add_argument("-l", "--tweet_lim",  
                        help="Max number of tweets to mine (default: -1).",
                        default=-1,  
                        type=int)
    parser.add_argument("-s", "--search",                                      
                        help="Search tweets.",      
                        action="store_true")
    parser.add_argument("-ms", "--multisearch",
                        help="Searh tweets with multiprocessing enabled.",      
                        action="store_true")
    parser.add_argument("-w", "--write",  
                        help="write(save) tweets to file.",      
                        action="store_true")
    parser.add_argument("-c", "--compile_docs",
                        help="Compile pertinent information from documents.", 
                        action="store_true")
    args = parser.parse_args()   


    return args 


# TWITTER AUTHENTICATION
def get_twitter_auth():
    """Setup Twitter Authentication.
    
    Returns
    --------
    {tweepy.OAuthHandler}
    """
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth


def get_twitter_client():
    """Setup Twitter API Client.
    
    Return
    -------
    {tweepy.API object}
    """
    auth = get_twitter_auth()
    client = API(auth, 
                 wait_on_rate_limit=True, 
                 wait_on_rate_limit_notify=True,
                 compression=True)
    return client


# FILE MANAGEMENT
def makedir(screen_name):
    """Create subdirectory 'users/screen_name' to store mined data.
    
    Params
    -------
    screen_name : str
    """
    dirname = 'users/{}'.format(screen_name)

    try:
        os.makedirs(dirname, mode=0o755, exist_ok=True)
    except OSError:
        print('Directory {} already exists.'.format(dirname))
    except Exception as e:
        print('Error while creating directory {}'.format(dirname))
        print(e)
        sys.exit(1)


def twitter_url(screen_name, no_rt, start, end, topics=[]):
    """Form url to access tweets via Twitter's search page.

    Params
    -------
    screen_name : str
    topics : list of strings
    no_rt : bool
    start : datetime-onj
    end : datetime-obj
    
    Returns
    -------
    {string} search url for twitter
    """
    # join url parts
    union = '%20'
    union_topic = '%20OR%20'
    # construct the various parts of the search url
    url = ['https://twitter.com/search?f=tweets&q=']
    url.append( union_topic.join(topics)  )
    url.append( 'from%3A' + screen_name )
    url.append( 'since%3A' + start.strftime('%Y-%m-%d') )
    url.append( 'until%3A' + end.strftime('%Y-%m-%d') )
    if no_rt:                                                                   
        url.append( '&src=typd' )      
    else:                                                                       
        url.append( 'include%3Aretweets&src=typd' )
    
    return union.join( url )


def increment_day(date, i):
    """Increment day object by i days.
    
    Params
    -------
    date : datetime-obj
    i : int
    
    Returns
    -------
    {datetime-obj} next day.
    """
    return date + datetime.timedelta(days=i)


# GETTTING TWEETS
def get_all_user_tweets(screen_name, 
                        start, end, day_step=2, 
                        topics=[], tweet_lim=3200, no_rt=True,
                        virtuald=False):
    """
    Params
    ------
    screen_name : str
    start       : datetime object
    end         : datetime object
    day_step    : int (default 2)
    topics      : list (default [])
    tweet_lim   : int (default 3,200)
    no_rt       : bool (default True)
    virtuald    : bool (default False)
    

    returns
    -------
    Writes tweets ids to users/{}/usr_tweetids_{}.jsonl
    {int} total number of tweet ids obtained
    """
    # Make dir structure                                                        
    makedir(screen_name)

    # name of file for saving tweet ids
    fname_tweet_ids = 'users/{0}/usr_tweetids_{0}.jsonl'.format(screen_name)
    fcheck = 'users/{0}/search_checkpoints_{0}.txt'.format(screen_name)

    # Headless displays with Xvfb (X virtual framebuffer)
    if virtuald:
        vdisplay = Xvfb()
        vdisplay.start()
    # Selenium parames
    # time to wait on each page load before reading the page
    delay = 1 
    driver = webdriver.Firefox() #Chrome() 


    if not os.path.isfile(fcheck):           
        check_p = open(fcheck, 'w')                                         
    else:                                                                   
        check_p = open(fcheck, 'r+')                                        
        checkpoints = check_p.readlines()                                   
        checkpoints = [check.strip('\n') for check in checkpoints 
                       if check.strip('\n')!='']
        # go to last checkpoint                                         
        start = datetime.datetime.strptime(checkpoints[-1],"%Y-%m-%d %H:%M:%S")
        print('Resuming from: {}\n'.format(start))

    ids_total = 0
    while start<=end:
        # save checkpoint
        check_p.write( '{}\n'.format(start) )
        # Get Twitter search url
        start_date = increment_day(start, 0)
        end_date = increment_day(start, day_step)
        url = twitter_url(screen_name, no_rt, start_date, end_date, topics)

        try:
            driver.get(url)
            driver.implicitly_wait(delay)

            found_tweets = \
            driver.find_elements_by_css_selector('li.js-stream-item')
            increment = 10
            
            # Scroll through the Twitter search page
            while len(found_tweets) >= increment:
                # scroll down for more results
                driver.execute_script(
                    'window.scrollTo(0, document.body.scrollHeight);'
                )
                time.sleep(delay)
                # select tweets
                found_tweets = driver.find_elements_by_css_selector(
                    'li.js-stream-item'
                )
                increment += 10

            # Get the IDs for all Tweets
            ids = []
            with open(fname_tweet_ids, 'a') as fout:
                for tweet in found_tweets:
                    try:
                        # get tweet id
                        tweet_id = tweet.get_attribute('data-item-id') 
                        ids.append(tweet_id)
                        ids_total += 1

                        # BREAK IF tweet_lim has been reached                           
                        if ids_total == tweet_lim:      
                            # Save ids to file
                            data_to_write = list(set(ids))                                  
                            fout.write(json.dumps(data_to_write)+'\n')

                            # Close selenium driver                                                     
                            driver.quit()   
                            if virtuald:                                                                
                                vdisplay.stop()
                            return ids_total

                    except StaleElementReferenceException as e:
                        print('Lost element reference.', tweet)
                        
                # Save ids to file
                if ids:
                    data_to_write = list(set(ids))
                    fout.write(json.dumps(data_to_write)+'\n')
        
        except NoSuchElementException as e:
            time.sleep(1*60)
            continue

        except TimeoutException:
            driver.implicitly_wait(1*60)
            continue
        start = increment_day(start, day_step)
    
    check_p.close()
    # Close selenium driver
    driver.quit()
    if virtuald:
        vdisplay.stop()
    return ids_total


### PREPROCESSING
stop = stopwords.words('english')
def preprocessor(doc):
    """Proportion of characters in document                                     
                                                                                
    :( :) :P :p :O :3 :| :/ :\ :$ :* :@                                         
    :-( :-) :-P :-p :-O :-3 :-| :-/ :-\ :-$ :-* :-@                             
    :^( :^) :^P :^p :^O :^3 :^| :^/ :^\ :^$ :^* :^@                             
    ): (: $: *:                                                                 
    )-: (-: $-: *-:                                                             
    )^: (^: $^: *^:                                                             
    <3 </3 <\3                                                                  
    o.O O.O O.o                                                                 
    :smile: :hug: :pencil:                                                      
    """                                                                         
    re_url = r"(http|https):\/\/.\S+"                                           
    re_emoji = r"(\:\w+\:|\<[\/\\]?3|[\(\)\\\D|\*\$][\-\^]?[\:\;\=]|"\
            "[\:\;\=B8][\-\^]?[3DOPp\@\$\*\\\)\(\/\|])(?=\s|[\!\.\?]|$)"    
    # remove urls                                                               
    doc = re.sub(re_url, "", doc)                                               
    # remove emoticons                                                          
    doc = re.sub(re_emoji, "", doc)                                             
    # remove emojis   
    try:
        # UCS-4
        extra = re.compile(u'[U00010000-U0010ffff]')
        doc = extra.sub('', doc)
    except re.error:
        # UCS-2
        extra = re.compile(u'[uD800-uDBFF][uDC00-uDFFF]')
        doc = extra.sub('', doc)
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    doc = regex.sub('', doc)
    
    return doc


def tokenizer(text):
    return text.split()


porter = PorterStemmer()
def tokenizer_porter(text):
    return [porter.stem(word) for word in text.split()]


tweet_token = TweetTokenizer()
def tokenizer_twitter(text):
    return tweet_token.tokenize(text)

