# nilc-tweets

## Description
Tweets collected in support of NILC tasks.

## Data Dictionary

* [health4all.json](https://github.com/Data4Democracy/immigration-connect/tree/master/datasets/nilc-tweets/health4all.json) - JSON array of Tweets containing **#health4all**
* [healthforall.json](https://github.com/Data4Democracy/immigration-connect/tree/master/datasets/nilc-tweets/healthforall.json) - JSON array of Tweets containing **#healthforall**
  * Tweets were collected from **January 1st, 2014** through (the early morning of) **September 20th, 2017**
  * JSON objects in both arrays have the same structure
      * **account** (*string*) - the Twitter account name that posted the Tweet
      * **account_id** (*string*) - the unique ID for the Twitter account
      * **datetime** (*string*) - the time the Tweet was posted
      * **text** (*string*) - the text content of the Tweet (containing the hashtag)
      * **is_reply** (*bool*) - is this Tweet a reply to another Tweet?
      * **replies** (*int*) - number of replies to this Tweet
      * **is_retweet** (*bool*) - is this Tweet a retweet?
      * **retweets** (*int*) - number of times this Tweet was retweeted
      * **favorites** (*int*) - number of times this Tweet was favorited
* [legislators.json](https://github.com/Data4Democracy/immigration-connect/tree/master/datasets/nilc-tweets/legislators.json) - JSON array of Tweets by key Tennesee legislators **@rongant,@senatornorris,@billketron,@jimtracy**
  * Tweets were collected from **January 1st, 2012** through **October 28th, 2017**
  * JSON objects have the structure
      * **username** (*string*) - the Twitter account name that posted the Tweet
      * **date** (*string*) - the time the Tweet was posted
      * **retweets** (*int*) - number of times this Tweet was retweeted
      * **favorites** (*int*) - number of times the tweet was favorited
      * **text** (*string*) - body of tweet 
      * **geo** (*string*) - location of tweet 
      * **mentions** (*string*) - list of @users mentioned in tweet 
      * **hastags** (*string*) - list of #hashtags mentioned in tweet 
      * **id** (*int*) - id of tweet 
	  * **permalink** (*string*) - url 