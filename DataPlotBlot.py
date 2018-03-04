################################################################################################
# This is the main script for the Data PlotBot Application. This PlotBot scans its Twitter account
# for mentions. For any tweet with its mention as "@DataPlotBot Analyze: <TwitterID>", it  pulls
# 500 most recent tweets for the Twitter ID mentioned and performs a Sentiment Analysis on them.
# It then plots a scatter plot showing the analysis.
################################################################################################

# Dependencies
import tweepy
import json
import time
import config as cfg
import pandas as pd
import matplotlib.pyplot as plt

# Import and Initialize Sentiment Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# Setup Tweepy API Authentication. The keys and tokens are specified in the config.py that
# is imported above. This is done to secure the keys. The config.py will NOT be a part of the
# files pushed on GitHub for this application. Anyone who wishes to run this script should do so
# with thier own keys and tokens
auth = tweepy.OAuthHandler(cfg.plotbot_consumer_key, cfg.plotbot_consumer_secret)
auth.set_access_token(cfg.plotbot_access_token, cfg.plotbot_access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# Constants used in the script mainly for readability
CAN_PERFORM_SEARCH = True

# If you wish to use this script for your bot, then you may change this to specify your twitter screen name
SEARCH_STR = "@DataPlotBot Analyze:"    

# The recent most tweet id that was analyzed is stored here to prevent any further analysis for
# tweets occuring before this one
recent_analyzed_id = ""

# The list of analyzed twitter ids is stored here to check for duplicates so that we do not
# analyze repeats
analyzed_ids = []

################################################################################################
# Function to perform the sentiment analysis
################################################################################################
def perform_sentiment_analysis(twitter_id):
    print("perform_sentiment_analysis started")
    
    # Add List to hold sentiment
    compounds = []
    positives = []
    negatives = []
    neutrals = []
    tweets_ago = []
    texts = []
    tweet_dates = []

    # Initialize the tweet counter. This is used for the x-axis of the plots
    tweet_ago_count = 1

    # Get the 500 tweets for this id. The api call returns only 20 tweets so we loop through 25 pages
    for pg in range(25) :
        user_tweets = api.user_timeline(twitter_id, page=pg)

        for tweet in user_tweets:
            #print(json.dumps(tweet, indent=3, sort_keys=True))
            #get tweet text for analysis
            tweet_text = tweet["text"]

            #  Run Vader Analysis on each tweet
            comp = analyzer.polarity_scores(tweet_text)["compound"]
            pos = analyzer.polarity_scores(tweet_text)["pos"]
            neu = analyzer.polarity_scores(tweet_text)["neu"]
            neg = analyzer.polarity_scores(tweet_text)["neg"]

            #  Add each value to the appropriate array
            compounds.append(comp)
            positives.append(pos)
            negatives.append(neg)
            neutrals.append(neu)
            tweets_ago.append(tweet_ago_count)
            texts.append(tweet_text)

            # Increment counter for the next tweet
            tweet_ago_count += 1
    
    # Logging
    print(len(compounds))
    
    # Create the Data Frame for the plots
    analysis_df = pd.DataFrame({"Tweets Ago": tweets_ago,
                            "Tweet Text": texts,
                            "Compound": compounds,
                            "Positive": positives,
                            "Negative": negatives,
                            "Neutral": neutrals})

    return analysis_df
  

################################################################################################
# Function to plot the sentiment analysis
################################################################################################
def plot_sentiment_analysis(tweet_df, twitter_user):
    
    # Create plot
    fig = plt.figure(figsize=(12,6))
    plt.plot(tweet_df['Tweets Ago'], tweet_df['Compound'], '-o')
    
    # Incorporate the other graph properties
    plt.xlabel("Tweets Ago")
    plt.ylabel("Tweet Polarity")
    plt.title("Sentiment Analysis for " + twitter_user)
    plt.axhline(color='black', linewidth='0.5')
    
    #plt.show()
    # Save the plot image for posting on twitter
    image_file_name = twitter_user+".png"
    plt.savefig(image_file_name)

    return image_file_name

################################################################################################
# This function posts a tweet on the DataPlotBot twitter page with the sentiment analysis
# that was done for the last 5 mins of data collected
################################################################################################
def post_tweet(target, user, filename):

    status_text = "Tweet Analysis #{} : {} (Thank you {}!!!)".format(len(analyzed_ids), target, user)
    print(status_text)

    api.update_with_media(filename, status_text)

################################################################################################
# This function takes a tweet, extracts the text, and the twitter id to analyze.
# Once it has a valid id, it gets calls other functions to get the data and then analyze it
################################################################################################
def process_tweet(tweet) :

    # Get the list of user mentions. We ignore the first one as it is always DataPlotBot
    user_mentions = tweet["entities"]["user_mentions"]
    num_to_analyze = len(user_mentions)-1

    # get the user information. This is used when we post a Thank You msg along with the tweet
    user_str = "@" + tweet["user"]["screen_name"]

    # Logging
    print("We have {} tweets to analyze from {}".format(num_to_analyze, user_str) )
    
    for x in range(1, len(user_mentions)):

        #target_str = str.strip(text.split(':')[1])
        target_str = "@" + user_mentions[x]["screen_name"]

        if target_str not in analyzed_ids:

            # Logging
            print("Target to analyze = "+ target_str)
        
            # Add the analyzed id in the list so that we don't repeat the analysis for it
            analyzed_ids.append(target_str)

            # process data
            target_df = perform_sentiment_analysis(target_str)
            image_filename = plot_sentiment_analysis(target_df, target_str)
            post_tweet(target_str, user_str, image_filename)

        else:
            # Logging as we do not analyze repeats
            print('"{}" has been analyzed before. Skipping it.'.format(target_str))

################################################################################################
# MAIN
################################################################################################
while CAN_PERFORM_SEARCH :
    print("starting our search : " + SEARCH_STR)
    print("Max id = " + recent_analyzed_id)

    # Search Twitter for any mentions
    public_tweets = api.search(SEARCH_STR, result_type="recent", since_id=recent_analyzed_id)

    #print(json.dumps(public_tweets, indent=3, sort_keys=True))

    # If there are no more tweets to  process then go to sleep
    if not public_tweets["statuses"]:
        print("There are no tasks to analyze....seeya after 5 mins")
        # sleep for 5 minutes
        time.sleep(10)
        print("Its been a long 5 mins nap....Lets see what we have to analyze")
    else:
        num = len(public_tweets["statuses"])
        print("Number of mentions found in 5 mins = " + str(num))
        recent_analyzed_id = public_tweets["statuses"][0]["id_str"]
        
        # Loop through all the tweets 
        for pub_tweet in public_tweets["statuses"]:
            process_tweet(pub_tweet)    
            
    
    
