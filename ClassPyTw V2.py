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
        self.hashtags = []

    def getUsername(self):
        self.username = self.tweet['user']['screen_name']
        return self.username

    def getText(self):
        self.text = self.tweet['text']
        return self.text

    def getHashtags(self):
        '''
        Devuelve una lista con todos los hashtags usados en un tuit
        '''
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
        topic_list = t.search.tweets(q=self.topic, count= 100, result_type='recent')
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

    def __init__(self, lista, topic):
        self.topic = topic
        self.tweet_list = lista
        self.hashtagslist = []

    def GetHashtagsList(self):
        '''
        Devuelve una lista con todos los hashtags presentes en un listado de tweets
        '''
        for el in self.tweet_list:
            tw = Tweet(el)
            for hashtag in tw.getHashtags():
                self.hashtagslist.append(hashtag.lower())
        return self.hashtagslist

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
    Cada elemento de la lista es una lista con el user y el numero de veces usado el topic.
    '''
    act_users=[]
    topl = TopicList(topic)
    tl = topl.GetTopicList()
    userl = UsersList(tl)
    userslist = userl.GetUsersList()

    for user in userslist:
        t = TimesTopicInTl(user, topic)
        times = t.GetTimesTopicInTl()
        if t != 0:
            act_users.append([times, user])
    return sorted(act_users, reverse=True)

def semantic_field(topic):
    '''
    Devuelve el campo semantico de un topic.
    '''
    dep_list = []
    sem_field = []
    topic_list = TopicList(topic)
    tlist = topic_list.GetTopicList()
    htagsl = HashtagsList(tlist['statuses'], topic)
    hl = htagsl.GetHashtagsList()

    for el in hl:
        if el not in dep_list:
            dep_list.append(el)

    for elem in dep_list:
        aux = [hl.count(elem), "#"+elem]
        sem_field.append(aux)

    return sorted(sem_field, reverse= True)



#Test con el topic "varlion"

topic = "varlion"

# --> Campo semantico #
print semantic_field(topic)


# --> Ususarios mas activos #
for el in active_users(topic):
    print el


