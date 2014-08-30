__author__ = 'Pycero91'

from twitter import *

OAUTH_TOKEN = YOUR OAUTH_TOKEN
OAUTH_SECRET = YOUR OAUTH_SECRET
CONSUMER_KEY = YOUR CONSUMER_KEY
CONSUMER_SECRET = YOUR CONSUMER_SECRET

t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

class Tweet(object):

    def __init__(self, tweet):
        self.tweet = tweet
        self.username = ''
        self.hashtags = []

    def getUsername(self):
        self.username = self.tweet['user']['screen_name']
        return self.username

    def getText(self):
        self.text = self.tweet['text']
        return self.text

    def getHashtags(self):
        i = 0
        for elem in self.tweet['entities']['hashtags']:
            self.hashtags.append(self.tweet['entities']['hashtags'][i]['text'])
            i += 1
        return self.hashtags

class User(object):

    def __init__(self, username):
        self.username = username
        self.tweets = 0
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

class TopicList(object):

    def __init__(self, topic):
        self.topic = topic
        self.topic_list = []

    def GetTopicList(self):
        '''
        Devuelve un lista con los "count" tuits mas recientes en los que aparece el topic
        '''
        topic_list = t.search.tweets(q=self.topic, count= 10, result_type='recenr')
        return topic_list

class UsersList(object):

    def __init__(self, lista):
        self.lista = lista
        self.users_list = []

    def GetUsersList(self):
        '''
        Devuelve una lista de los usuarios no duplicados autores de los tuits de la lista recibida
        '''
        usersl = []
        for el in self.lista['statuses']:
            tw = Tweet(el)
            if tw.getUsername() not in usersl:
                usersl.append(tw.getUsername())
        return usersl

class HashtagsList(object):

    def __init__(self, user):
        self.user = user
        self.hashtagslist = []

    def GetHashtagsList(self):
        '''
        Devuelve una lista con todos los hashtags utilizados por el usuario a lo largos de su timeline
        '''
        hl = []
        us = User(self.user)
        tl = us.getTimeLine()
        for el in tl:
            tw = Tweet(el)
            for hashtag in tw.getHashtags():
                hl.append(hashtag)
        return hl

class TimesTopicInTl(object):

    def __init__(self, user, topic):
        self.user = user
        self.topic = topic
        self.times = 0

    def GetTimesTopicInTl(self):
        '''
        Devuelve la cantidad de veces que el usuario ha utilizado el topic en su timeline
        '''
        cont = 0
        us = User(self.user)
        tl = us.getTimeLine()
        for el in tl:
            tw = Tweet(el)
            text = tw.getText().lower()
            if self.topic in text:
                cont += 1
        return cont

def active_users(topic):
    '''
    Devuelve una lista ordenada de los usuarios mas activos con el topic dado en sus ultimos 20 tuits (timeline)
    Cada elemento de la lista es una lista con el user, numero de veces usado el topic, otros hashtags usados
    en el TL
    '''
    act_users=[]
    topl = TopicList(topic)
    tl = topl.GetTopicList()
    userl = UsersList(tl)
    userslist = userl.GetUsersList()

    for user in userslist:
        hashtagsl = HashtagsList(user)
        hl = hashtagsl.GetHashtagsList()
        t = TimesTopicInTl(user, topic)
        times = t.GetTimesTopicInTl()
        if times_topic_in_timeline(user, topic) != 0:
            act_users.append([times, user, hl])

    return sorted(act_users, reverse=True)



#Test con el topic "betis"
for el in active_users("betis"):
    print el


