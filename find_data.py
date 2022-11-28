
import hashtables
import linked_list
import sparse_matrix
from models import *

max_usr_number = 1000






def find_user_given_by(key_type,key,value):
    # Creating a hash table with argument key as the hashed key
    users = User.query.all()
    users_ll = hashtables.BloomFilter(max_usr_number,5,hashtables.hashFunction)
    hashed = ""
    for elem in users:
        if key_type == 'name':
            hashed = elem.name
        elif key_type == 'id':
            hashed = elem.id
        elif key_type == 'email':
            hashed = elem.email
        elif key_type == 'phone':
            hashed = elem.phone
        users_ll.insert( hashed,
            {
                'id' : elem.id,
                'name' : elem.name,
                'address' : elem.address,
                'phone' : elem.phone,
                'email' : elem.email,
            }
        )
    if users_ll.contains(key):
        return users_ll.get(key)[value]
    else:
        raise KeyError("No user with such input")


def check_username_unique(username):
    users = User.query.all()
    users_ll = hashtables.BloomFilter(max_usr_number,5,hashtables.hashFunction)
    for elem in users:
        users_ll.insert( elem.name,
            {
                'id' : elem.id,
                'name' : elem.name,
                'address' : elem.address,
                'phone' : elem.phone,
                'email' : elem.email,
            }
        )
    if users_ll.contains(username):
        return False
    else:
        return True

def get_users():
    users = User.query.all()
    users_ll = hashtables.BloomFilter(max_usr_number,5,hashtables.hashFunction)
    for elem in users:
        users_ll.insert( elem.id,
            {
                'id' : elem.id,
                'name' : elem.name,
                'email' : elem.email,
                'address' : elem.address,
                'phone' : elem.phone,
            }
        )
    # This allows for a fast retrieval of the tweet's data given the id
    return users_ll


def tweet_id_hashmap():
    tweets = Tweet.query.all()
    tweets_ll = hashtables.BloomFilter(max_usr_number,5,hashtables.hashFunction)
    for elem in tweets:
        tweets_ll.insert( elem.id,
            {
                'id' : elem.id,
                'title' : elem.title,
                'date' : elem.date,
                'user_id' : elem.user_id,
                'body' : elem.body,
            }
        )
    # This allows for a fast retrieval of the tweet's data given the username
    #Once the hash table is full, we can find 
    return tweets_ll

def all_tweets():
    tweets = Tweet.query.all()
    tweets_ll = hashtables.BloomFilter(max_usr_number,5,hashtables.hashFunction)
    for elem in tweets:
        tweets_ll.insert(elem.id,elem)
    return tweets_ll




def username_tweets():
    tweets = Tweet.query.all()
    tweets_ll = hashtables.BloomFilter(max_usr_number,5,hashtables.hashFunction)
    for elem in tweets:
        if tweets_ll.contains(elem.user_id):
            tweets_ll.data[elem.user_id].append({
                    'id' : elem.id,
                    'title' : elem.title,
                    'date' : elem.date,
                    'user_id' : elem.user_id,
                    'body' : elem.body,
                })
        else:

            tweets_ll.insert( elem.user_id,[
                {
                    'id' : elem.id,
                    'title' : elem.title,
                    'date' : elem.date,
                    'user_id' : elem.user_id,
                    'body' : elem.body,
                }]
            )
    # This allows for a fast retrieval of the tweet's data given the username
    #Once the hash table is full, we can find 
    return tweets_ll

# Hashtable + sets as values
def establish_friendships():
    # We need to represent it as a graph but the issue would be memory,
    # if the graph is represented as an adjacency matrix
    #  as it would have a complexity of O(n^2) if n is the number of users.
    # Instead, a similar paradigm to sparse matrices will be used by 
    # implementing it as a hashmap user : hashtable of friends
    friend_matrix = {}
    people = Following.query.all()
    for pair in people:
        if pair.id_1 not in friend_matrix.keys():
            friend_matrix[pair.id_1] = set()
        friend_matrix[pair.id_1].add(pair.id_2)
        if pair.id_2 not in friend_matrix.keys():
            friend_matrix[pair.id_2] = set()
        friend_matrix[pair.id_2].add(pair.id_1)
    return friend_matrix

def are_friends(id_1,id_2,friend_matrix):
    ####################################### TO MODIFY ############################
    if id_1 in friend_matrix.keys():
        if id_2 in friend_matrix[id_1]:
            return True
    return False


        

# words as keys keys + sets as values
def build_vocab_hashtable():
    tweet_db = Tweet.query.all()
    vocab_hashtable = {}
    for elem in tweet_db:
        title = elem.title
        body = elem.body
        for word in title.split():
            if word in vocab_hashtable.keys():
                if elem.id not in vocab_hashtable[word]:
                    vocab_hashtable[word].add(elem.id)
            else:
                vocab_hashtable[word] = {elem.id}
        for word in body.split():
            if word in vocab_hashtable.keys():
                if elem.id not in vocab_hashtable[word]:
                    vocab_hashtable[word].add(elem.id)
            else:
                vocab_hashtable[word] = {elem.id}
    return vocab_hashtable


def find_tweets_keyword(vocab_hashmap,keyword):
    if keyword in vocab_hashmap:
        return vocab_hashmap[keyword]
    else:
        return "No tweets contains this keyword"


"""global friends
friends = establish_friendships()
global users_names
users_ids = get_users()
tweet_vocab = build_vocab_hashtable()
global username_tweet
username_tweet= username_tweets()"""

