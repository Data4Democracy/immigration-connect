import csv                                                                      
import json
import pandas as pd

from mining_functions import *
from tweepy import TweepError
from multiprocessing import freeze_support
from multiprocessing import Pool
from itertools import repeat



def search_tweets(screen_name, 
                  virtuald, 
                  tweet_lim,
                  no_rt=True,
                  start=datetime.datetime(2015, 1, 1), 
                  end=datetime.datetime.today(), 
                  day_step=2,
                  topics=[]):
    # tweepy API
    client = get_twitter_client()
    print('Getting {}\'s Tweets...'.format(screen_name))

    # check that 'start' is after account was created
    user_data = client.get_user(screen_name)
    created = user_data.created_at
    if start<created:
        start = created
    
    # save tweet ids to jsonl file
    total_tweets = []
    num_tweets = get_all_user_tweets(screen_name, 
                                     start, end, 
                                     day_step=day_step,
                                     topics=topics,
                                     tweet_lim=tweet_lim,
                                     no_rt=no_rt,
                                     virtuald=virtuald)
    total_tweets.append(num_tweets)
    print('Found {} tweets from {}.'.format(sum(total_tweets), screen_name))



def write_tweets(screen_names, verbosity):
    # tweepy API                                                                
    client = get_twitter_client()
    
    print('Writing results...')
    for screen_name in screen_names:
        # use selenium extension
        fid = 'users/{0}/usr_tweetids_{0}.jsonl'.format(screen_name)
        ftweet = 'users/{0}/usr_timeline_{0}.jsonl'.format(screen_name)
        fcheck = 'users/{0}/checkpoints_{0}.txt'.format(screen_name)
        
        # if no checkpoint file
        if not os.path.isfile(fcheck):
            check_p = open(fcheck, 'w')
        else:
            check_p = open(fcheck, 'r+')
            checkpoints = check_p.readlines()
            checkpoints = [check.strip('\n') for check in checkpoints
                           if check.strip('\n')!='']

        with open(fid, 'r') as f_id, open(ftweet, 'a') as f_tweet: 
            if not os.path.isfile(fcheck):
                f_id.seek(int(checkpoints[-1]))

            for line in iter(f_id.readline, ''):
                # save the location of file
                check_p.write( '{}\n'.format(f_id.tell()) )
                # load ids
                ids = json.loads(line)
                    
                for tweetId in ids:
                    try:
                        tweet = client.get_status(tweetId)
                        f_tweet.write(json.dumps(tweet._json)+'\n')

                    except TweepError as e:
                        if verbosity:
                            print(e)
                        time.sleep(60*15)
        check_p.close()
        print('done writing results.\nCheck: {}'.format(ftweet))



def compile_tweets(all_tweets):
    print('Compiling results...') 
    with open(all_tweets, 'w') as fout:
        writer = csv.writer(fout)                                                   
        # Header                                      
        writer.writerow(['user', 'datetime','text','id', 'entities'])
        
        for screen_name in screen_names:
            ftweet = 'users/{0}/usr_timeline_{0}.jsonl'.format(screen_name)
            with open(ftweet, 'r') as fin:
                for line in fin:
                    # reading
                    tweet = json.loads(line)

                    # processing                                                  
                    informat = '%a %b %d %H:%M:%S %z %Y'                
                    outformat = '%Y-%m-%d %H:%M:%S %Z'
                    date = datetime.datetime.strptime(
                        tweet['created_at'], informat)
                    date = date.strftime(outformat)
                    urls = []
                    for url in tweet['entities']['urls']:
                        urls.append(url['expanded_url'])
                    
                    # writing
                    writer.writerow([tweet['user']['screen_name'],
                                     date,
                                     tweet['text'], 
                                     tweet['id'],
                                     '   '.join(urls)
                                    ])
    # clean tweets
    df = pd.read_csv(all_tweets)
    df.drop_duplicates(inplace=True)
    df.to_csv(all_tweets, mode='w', index=False)



if __name__=='__main__':
    
    start   = datetime.datetime(2015, 1, 1)                       
    end     = datetime.datetime.today()

    screen_names = [
        'realDonaldTrump', 'POTUS', 'WhiteHouse', 'PressSec',
        'RudyGiuliani', 'StephenBannon', 'jeffsessions', 'KellyannePolls',
        'GenFlynn',
        #'NBCNews', 'CNN', 'cnnbrk', 'FoxNews', 'AP', 'nytimes', 
        #'BreitbartNews', 'guardian',
                   ]                                 
    topics = [
        'muslims', 'muslim', 'islam', 'islamic', 'mosque', 'mosques',
        'radical', 'radicals', 'terrorism', 'terrorists', 'terrorist', 
        'terror', 'ISIS', 
        'travel', 'ban', 'eo', 'executive', 'order','orders', 'screening', 
        'resist', 'protect', 'protection',
        'airport', 'airports', 'visa', 'visas','target', 'targets',  
        'refugee', 'refugees', 'middle', 'east', 'eastern', 'easterners'
        'Iran', 'Iraq', 'Libya', 'Somalia', 'Sudan', 'Yemen', 'Syria',
             ]
    topics = []

    # command line arguments                                                        
    args         = mining_cml()                                                             
    verbosity    = args.verbose                                                        
    virtuald     = args.virtual                                                         
    tweet_lim    = args.tweet_lim 
    search       = args.search
    multisearch  = args.multisearch
    write        = args.write
    compile_docs = args.compile_docs
    no_rt        = False                # include RTs

    # search for tweets
    if search:
        for screen_name in screen_names:
            search_tweets(screen_name, 
                          virtuald, 
                          tweet_lim,
                          no_rt=no_rt,
                          start=start,
                          end=end,
                          day_step=3,
                          topics=topics)
    if multisearch:
        freeze_support()
        pool = Pool()
        pool.starmap(search_tweets, 
                    zip(screen_names, 
                        repeat(virtuald), 
                        repeat(tweet_lim), 
                        repeat(no_rt=no_rt),
                        repeat(start=start), 
                        repeat(end=end),
                        repeat(topics=topics)))

    # save tweets -> save entire tweet  
    if write:
        write_tweets(screen_names, verbosity) 

    # compile pertinent info from tweets
    if compile_docs:
        compile_tweets('users/all_tweets.csv')
