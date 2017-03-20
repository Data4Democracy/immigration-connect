# Muslim Ban
Compile and analyze public statements by D. Trump, his administration officials, 
associates, surrogates, and others, to prove discriminatory intent. 
(Including statements made during the campaign and earlier.)

# USE                                                                           
One can use [get_all_user_tweets](https://github.com/alejandrox1/muslim_ban/blob/master/mining_functions.py#L186)
In order to go around the `Twitter API` limit of 3,200 tweets.

The workflow we use for this work is described in
[twitter_mining](https://github.com/alejandrox1/muslim_ban/blob/master/twitter_mining.py).

The process can be divided in three different tasks `(python twitter_mining.py -h)`:

* Search for tweets `(python twitter_mining.py -s)` </br>
  Use `Selenium` to search tweets via Twitter's search option.
* Writing/saving tweets `(python twitter_mining.py -w)` </br>
  Use `tweepy` to look up tweets by ID and save them to a file.
* Compiling tweets `(python twitter_mining.py -c)` </br>
  Compile all tweets into a `csv` file.
  In the future this dataset will be made available.

For further clean up check
[search_tweets](https://github.com/alejandrox1/muslim_ban/blob/master/search_tweets.ipynb).

## White House Press
[whpress](https://github.com/alejandrox1/muslim_ban/blob/master/whpress/whpress/spiders/blog.py)
is a `scrapy spider` that can be used to scrape all the press briefings from
the white house. 

# SET UP
To search obtain tweets we use a `Python Selenium`.
In order to get `Selenium` working you will need to install `chromedriver` for
`Google chrome` or `geckodriver` for `Firefox`.

## Firefox
```
cd ~/bin
wget https://github.com/mozilla/geckodriver/releases/download/v0.15.0/geckodriver-v0.15.0-linux64.tar.gz 
tar -xvzf geckodriver-v0.15.0-linux64.tar.gz
rm geckodriver-v0.15.0-linux64.tar.gz
chmod +x geckodriver
```

In `~/.bashrc`
```
export PATH=$PATH:/home/<user>/bin/geckodriver
```

## Chrome
```
wget -N http://chromedriver.storage.googleapis.com/2.26/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver

sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
```
