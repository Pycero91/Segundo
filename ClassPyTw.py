__author__ = 'Pycero91'

from twitter import *

OAUTH_TOKEN = "2286792452-PO1f2ZcyaLjV0VBKiJRn9LYmLjOkXKjZaEw05Uf"
OAUTH_SECRET = "768vUXw7KTkIskRcjSDmjWo2ZDSl21t3UT1uG3KN503s8"
CONSUMER_KEY = "EbSYy5URARf9EGxfZpS7PDABH"
CONSUMER_SECRET = "Qzx6y1AZ44LRuMxDx8EvjoxGq2MDiIvXvhiC9Pm62ciacp9uNY"

t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

class Tweet(object):

    def __init__(self, tweet):
        self.tweet = tweet
        self.username = ''
        self.mentions = []
        self.hashtags = []
        self.date = ''
        self.text = ''
        self.fav = 0
        self.rt = 0
        self.url = ''

    def getUsername(self):
        self.username = self.tweet['user']['screen_name']
        return self.username

    def getMentions(self):
        i = 0
        for elem in self.tweet['entities']['user_mentions']:
            self.mentions.append(self.tweet['entities']['user_mentions'][i]['screen_name'])
            i += 1
        return self.mentions

    def getHashtags(self):
        i = 0
        for elem in self.tweet['entities']['hashtags']:
            self.hashtags.append(self.tweet['entities']['hashtags'][i]['text'])
            i += 1
        return self.hashtags

    def getDate(self):
        self.date = self.tweet['created_at']
        return self.date

    def getText(self):
        self.text = self.tweet['text']
        return self.text

    def getFav(self):
        self.fav = self.tweet['favourite_count']
        return self.fav

    def getRt(self):
        self.rt = self.tweet['retweet_count']
        return self.rt

    def getUrl(self):
        i = 0
        for elem in self.tweet['entities']['urls']:
            self.mentions.append(self.tweet['entities']['urls'][i]['url'])
            i += 1
        return self.hashtags


class User(object):

    def __init__(self, username):
        self.username = username
        self.tweets = 0
        self.following = 0
        self.followers = 0
        self.listed = 0
        self.description = ''
        self.location = ''
        self.language = ''
        self.created_at = ''
        self.url = ''
        self.timeline = []

    def getUsername(self):
        return self.username

    def getTweets(self):
        tw = Tweet(self.getLastTweet())
        self.tweets = tw.tweet['user']['statuses_count']
        return self.tweets

    def getTimeLine(self):
        tl = t.statuses.user_timeline(screen_name=self.getUsername())
        return tl

    def getLastTweet(self):
        tweetlist = self.getTimeLine()
        return tweetlist[0]

    def getFollowing(self):
        tw = Tweet(self.getLastTweet())
        self.following = tw.tweet['user']['friends_count']
        return self.following

    def getFollowers(self):
        tw = Tweet(self.getLastTweet())
        self.followers = tw.tweet['user']['followers_count']
        return self.followers

    def getListed(self):
        tw = Tweet(self.getLastTweet())
        self.listed = tw.tweet['user']['llisst']
        return self.listed

    def getDescription(self):
        tw = Tweet(self.getLastTweet())
        self.description = tw.tweet['user']['description']
        return self.description

    def getLocation(self):
        tw = Tweet(self.getLastTweet())
        self.location = tw.tweet['user']['location']
        return self.location

    def getLanguage(self):
        tw = Tweet(self.getLastTweet())
        self.language = tw.tweet['user']['lang']
        return self.language

    def getCreatedAt(self):
        tw = Tweet(self.getLastTweet())
        self.created_at = tw.tweet['user']['created_at']
        return self.created_at

    def getUrl(self):
        tw = Tweet(self.getLastTweet())
        self.url = tw.tweet['user']['url']
        return self.url

def create_topic_list(topic):
    '''
    Crea un lista con los 100 tuits mas recientes en los que aparece el topic
    '''
    topic_list = t.search.tweets(q=topic, count = 100, result_type="recent")
    return topic_list

def create_users_list(lista):
    '''
    Crea una lista de los usuarios no duplicados autores de los tuits de la lista recibida
    '''
    users_list = []
    for el in lista['statuses']:
        tw = Tweet(el)
        if tw.getUsername() not in users_list:
            users_list.append(tw.getUsername())
    return users_list

def times_topic_in_timeline(user, topic):
    '''
    Devuelve la cantidad de veces que el usuario ha utilizado el topic en su timeline
    '''
    cont = 0
    us = User(user)
    tl = us.getTimeLine()
    for el in tl:
        tw = Tweet(el)
        text = tw.getText().lower()
        if topic in text:
            cont += 1
    return cont

def hashtag_list_form_timeline(user):
    '''
    Devuelve una lista con todos los hashtags utilizados por el usuario a lo largos de su timeline
    '''
    hl = []
    us = User(user)
    tl = us.getTimeLine()
    for el in tl:
        tw = Tweet(el)
        for hashtag in tw.getHashtags():
            hl.append(hashtag)
    return hl

def active_users(topic):
    '''
    Devuelve una lista ordenada de los usuarios mas activos con el topic dado en sus ultimos 20 tuits (timeline)
    Cada elemento de la lista es una lista con el user, numero de veces usado el topic, otros hashtags usados
    en el TL
    '''
    act_users=[]
    for user in create_users_list(create_topic_list(topic)):
        if times_topic_in_timeline(user, topic) != 0:
            act_users.append([times_topic_in_timeline(user, topic), user, hashtag_list_form_timeline(user)])
    return sorted(act_users, reverse=True)



#Test con el topic "betis"
for el in active_users("betis"):
    print el


