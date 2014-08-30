__author__ = 'Pycero91'

from twitter import *

OAUTH_TOKEN = "2286792452-PO1f2ZcyaLjV0VBKiJRn9LYmLjOkXKjZaEw05Uf"
OAUTH_SECRET = "768vUXw7KTkIskRcjSDmjWo2ZDSl21t3UT1uG3KN503s8"
CONSUMER_KEY = "EbSYy5URARf9EGxfZpS7PDABH"
CONSUMER_SECRET = "Qzx6y1AZ44LRuMxDx8EvjoxGq2MDiIvXvhiC9Pm62ciacp9uNY"
t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))


def create_user_list(topic):
    '''
    Crea la lista de los usuarios (sin duplicar) que han tuiteado con el topic dado
    en los ultimos 100 tuits sobre el topic
    '''
    twitter_list = t.search.tweets(q=topic, count = 100, result_type="recent")
    user_list = []
    unique_users_list=[]

    for tweet in twitter_list['statuses']:
        user_list.append(tweet['user']['screen_name'])

    for user in user_list:
        if user not in unique_users_list:
            unique_users_list.append(user)

    return unique_users_list


def get_user_timeline(username):
    '''
    Devuelve el TL (solo 20 tuits) del user
    '''
    tl = t.statuses.user_timeline(screen_name=username)
    return tl

def is_topic_in_tweet(topic, tweet):
    '''
    Comprueba si el topic esta en etexto del tuit
    '''
    is_in = False
    if topic in tweet['text']:
        is_in = True
    return is_in

def times_twitted_topic(username, topic, list):
    '''
    Cuenta el numero de veces que se ha usado el topic en una lista de tweets
    '''
    cont = 0
    for tweet in list:
        if is_topic_in_tweet(topic, tweet):
            cont += 1
    return cont


def lista(topic):
    '''
    Devuelve una lista compuesta de lista de dos elementos donde el primer elemento es el username y el segundo
    elemento es el numero de veces que el user ha utilizado el topic en sus ultimos 20 tuits (timeline)
    '''
    final_list = []
    for user in create_user_list(topic):
        user_times = []
        user_times.append(times_twitted_topic(user, topic, get_user_timeline(user)))
        user_times.append(user)
        final_list.append(user_times)
    return final_list

def get_hashtag(tweet):
    '''
    Devuelve una lista con los hashtags empleados en un tuit
    '''
    hashtags = []
    i = 0
    for elem in tweet['entities']['hashtags']:
        hashtags.append(tweet['entities']['hashtags'][i]['text'])
        i += 1
    return hashtags


def active_users(topic):
    '''
    Devuelve una lista ordenada de los usuarios mas activos con el topic dado en sus ultimos 20 tuits (timeline)
    Cada elemento de la lista es una lista con el user, numero de veces usado el topic, otros hashtags usados
    en el TL
    '''
    act_users = []
    for user in lista(topic):
        if user[0] != 0:
            act_users.append(user)

    for user in act_users:
        hashtags_list = []
        for el in get_user_timeline(user[1]):
            if len(get_hashtag(el)) > 0:
                hashtags_list.append(get_hashtag(el))
        user.append(hashtags_list)

    return sorted(act_users, reverse=True)



#Test con el topic "#socialmedia"
for el in active_users("#betis"):
    print el
    print " "
