from os import getenv
import basilica
import tweepy
import twitter_scraper
from twitter_scraper import get_tweets, Profile
from dotenv import load_dotenv
from .model import db, User, Tweet
load_dotenv()

TWITTER_AUTH = tweepy.OAuthHandler(getenv('TWITTER_CONSUMER_API_KEY'),
                                   getenv('TWITTER_CONSUMER_API_SECRET'))
TWITTER_AUTH.set_access_token(getenv('TWITTER_ACCESS_TOKEN'),
                              getenv('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(getenv('BASILICA_KEY'))

public_tweets = TWITTER.home_timeline()
#for tweet in public_tweets:
    #print(tweet.text)

def add_user_tweepy(username):
    #'''Add a user and their tweets to database'''
    try:
        # Get user info from tweepy
        twitter_user = TWITTER.get_user(username)
        # Add to User table(or check if they exist already)
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id,
                        username=username,
                        follower_count=twitter_user.followers_count))
        db.session.add(db_user)
        #Get tweets ignoring re-tweets and replies
        tweets = twitter_user.timeline(count=200,
                                       exclude_replies=True,
                                       include_rts=False,
                                       tweet_mode='extended',
                                       since_id=db_user.newest_tweet_id)
    
        #Add newest_tweet_id to the User table
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
   
        # Loop over tweets, get embedding and add to Tweet table
        for tweet in tweets:
            # Get an example basilica embedding for first tweet
            embedding = BASILICA.embed_sentence(tweets[0].full_text, model='twitter')

            # Add tweet info to Tweet table
            db_tweet = Tweet(id=tweet.id,
                             text=tweet.full_text[:300],
                             embedding=embedding)
            db_user.tweet.append(db_tweet)
            db.session.add(db_tweet)

    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e
    else:
        db.session.commit()


'''
##### Using Twitter Scraper
def add_user_twitter_scraper(username):
    """Add a user and their tweets to database."""
    try:
        # Get user profile   
        user_profile = Profile(username) #change variable names to user_profile and use bracket notation []
        # Add to User table(or check if they exist already)
        db_user = (User.query.get(twitter_user.id)) or
                   User(id=twitter_user.id, # 
                        username=username,
                        follower_count=twitter_user.followers_count))
        db.session.add(db_user)
        # Get most recent tweets
        tweets = list(get_tweets(username, pages=10))
        original_tweets = [d for d in tweets if d['username']==username]
        
        # Loop through original tweets
            #Get tweet text
            # Get tweet ID
            # Get embedding from tweet text
            #Create a new tweet object- id , text, embedding
            # insert that tweet object into database
        
        #database commit to save






     # Get an example Basilica embedding for first tweet

        embedding = BASILICA.embed_sentence(original_tweets[0]['text'], model='twitter')
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e
    return original_tweets, embedding
#####
elon_tweets, elon_embedding = add_user_twitter_scraper('elonmusk')
print(len(elon_tweets), len(elon_embedding))
####





#return tweets, embedding
'''