# DataPlotBot
This is a Twitter Bot that sends out visualized sentiment analysis of a Twitter account's recent tweets. The bot receives tweets via mentions and in turn performs sentiment analysis on the twitter account(s) specified in the mention 

For example, when a user tweets, __"@DataPlotBot Analyze: @CNN,"__ it will trigger a sentiment analysis on the CNN twitter feed. A plot from the sentiment analysis is then tweeted to the PlotBot5 twitter feed. 

## Bot Considerations:

* The bot scans its twitter account every __five minutes__ for mentions.
* The bot pulls __500__ most recent tweets to analyze for each incoming request.
* The bot prevents abuse by analyzing __only__ Twitter accounts that have not previously been analyzed.
* The bot mentions the Twitter account name of the requesting user in its analysis twitter post.
* The bot performs analysis on all twitter ids in the mention

## Setup and Configuration notes
You may use the application to run your own Twitter Bot. The following easy configuration steps will be needed
* The API Keys and Token information is saved in a config.py file which is not checked into GitHub. To use the application you much first 
add a config.py file in the same folder as the DataPlotBot.py. The keys generated for your Twitter App should be saved in this config.py file as indicated in the SampleConfig.py file here.
* The Twitter ID for your Bot should be specified in the config.py file as well. This is also given in the SampleConfig.py file

## APIs used

The following APIs were used for this application:

* __tweepy__ : This api was used to get the needed information for twitter and post to the twitter page
* __pandas__ : This api was used to assist in organizing the data for the analysis into a data frame for wasy plotting
* __matplotlib__ : This is the plotting api used to generate all the scatter plots for the analysis
* __vaderSentiment__: This api was used to generate the sentiment analysis for the twitter texts


## Sample Analysis
![@elonmusk.png](@elonmusk.png)
![@NASAdata.png](@NASAdata.png)

## Twitter Screen Shots
![Twitter_Brooklyn_BBQ.png](Twitter_Brooklyn_BBQ.png)
![Twitter_Economic_Times.png](Twitter_Economic_Times.png)
