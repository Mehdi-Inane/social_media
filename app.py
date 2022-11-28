from ctypes import addressof
from datetime import datetime
from sqlite3 import Connection as SQLite3Connection
from unicodedata import name

from flask import (Flask, jsonify, redirect, render_template, request, session,
                   url_for)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

import hashtables
import linked_list
from config import *
from find_data import *
from models import *

global current_user_id
current_user_id=-1
    
@app.route("/friends", methods = ["POST","GET"])
def friends():
    data = User.query.all()
    users = linked_list.LinkedList()
    for elem in data:
        users.insert_beginning(
            {
                'id' : elem.id,
                'name' : elem.name,
                'address' : elem.address,
                'phone' : elem.phone,
                'email' : elem.email,
            }
        )
    people = users.to_list()
    people_ids = establish_friendships()
    
    if current_user_id in people_ids.keys():
        user_friends = people_ids[current_user_id]
    else:
        user_friends = []
    people_names = set()
    friend_names = set()
    tmp = ""
    for elem in user_friends:
        friend_names.add(find_user_given_by('id',elem,'name'))
    for elem in people:
        if elem['id'] not in user_friends and elem['id'] != current_user_id:
            people_names.add(elem['name'])
    if request.method =='POST': # follow new user
        for elem in people_names:
            if elem in request.form:
                tmp = elem
                new_friend = Following(
            id_1 = current_user_id,
            id_2 = find_user_given_by('name',elem,'id')
        )
                db.session.add(new_friend)
                db.session.commit()
        found = False
        friendships = Following.query.all()
        for elem in people:
            if elem['id'] == current_user_id:
                continue
            if elem['name'] in request.form and elem['name'] != tmp:
                for elem_2 in friendships:
                    if elem_2.id_1 == elem['id'] or elem_2.id_2 == elem['id']:
                        print("uoo")
                        db.session.delete(elem_2)
                        db.session.commit()
                        found = True
                        break
                if found:
                    break
        people_ids = establish_friendships()
    
        if current_user_id in people_ids.keys():
            user_friends = people_ids[current_user_id]
        else:
            user_friends = []
        people_names = set()
        friend_names = set()
        tmp = ""
        for elem in user_friends:
            friend_names.add(find_user_given_by('id',elem,'name'))
        for elem in people:
            if elem['id'] not in user_friends and elem['id'] != current_user_id:
                people_names.add(elem['name'])
    return render_template("friends.html",people =people_names ,friends = friend_names)





@app.route("/register",methods = ["GET","POST"])
def register():
    if request.method == 'POST':
        name,email,address,phone = request.form['name'],request.form['email'],request.form['address'],request.form['phone']
        if check_username_unique(name):
            new_user = User(
                name = name,
                email = email,
                address = address,
                phone = phone
            )
            db.session.add(new_user)
            db.session.commit()
            global current_user_id 
            current_user_id = new_user.id
            return redirect(url_for("landing_page"))
        else:
            return "Username already exists"
    return render_template("index.html")


@app.route("/login",methods = ["GET","POST"])
def log_in():
    if request.method == 'POST':
        name,phone = request.form['name_log_in'],request.form['phone_log_in']
        #try:
        pwd = find_user_given_by('name',name,"phone")
        print("pwd is",pwd)
        print("phone us",phone)
        if pwd == phone:
            global current_user_id 
            current_user_id= find_user_given_by('name',name,'id')
            return redirect(url_for("landing_page"))
        else:
            return "Wrong password"
        #except:
        #    return "Wrong input"
    return render_template("index.html")

@app.route("/delete_tweet",methods = ["POST"])
def delete_tweet():
    found = False
    tweets = Tweet.query.all()
    print(request.form)
    for elem in tweets:
        if str(elem.id) in request.form:
            print("we here")
            db.session.delete(elem)
            db.session.commit()
            found = True
            break
    tweets = username_tweets()
    answer = []
    if tweets.contains(current_user_id):
        answer = tweets.get(current_user_id)
    print(answer)
    return render_template("my_tweets.html",posts = answer)


@app.route("/my_tweets",methods = ["GET","POST"])
def my_tweets():
    tweets = username_tweets()
    answer = []
    if tweets.contains(current_user_id):
        answer = tweets.get(current_user_id)
    print(answer)
    return render_template("my_tweets.html",posts = answer)
    
@app.route("/log_out",methods = ["GET","POST"])
def log_out():
    current_user_id = -1
    return redirect(url_for('log_in'))


@app.route("/delete_user",methods = ["GET","POST"])
def delete_user():
    users = User.query.all()
    tweets = Tweet.query.all()
    user_tweets = username_tweets()
    friendships = Following.query.all()
    friends = establish_friendships()
    for user in users:
        if user.id == current_user_id:
            for elem_2 in tweets:
                if elem_2.id == current_user_id:
                    db.session.delete(elem_2)
                    db.session.commit()
            for elem in friendships:
                if elem.id_1 == current_user_id or elem.id_2 == current_user_id:
                    db.session.delete(elem)
                    db.session.commit()
            db.session.delete(user)
            db.session.commit()
            break
    return redirect(url_for("log_out"))


@app.route("/logged_in",methods=["GET","POST"])
def landing_page():
    if request.method == 'GET':
        """data = Tweet.query.all()
        tweets = linked_list.LinkedList()
        for elem in data:
            tweets.insert_at_end(
                {
                    'id' : elem.id,
                    'title' : elem.title,
                    'body' : elem.body,
                    'date' : elem.date,
                    'user_name' : find_user_given_by('id',elem.user_id,'name')
                }
            )"""
        data = username_tweets()
        friends = establish_friendships()
        if current_user_id in friends.keys():
            my_friends = friends[current_user_id]
        else:
            my_friends = []
        tweets = []
        my_tweets = []
        if data.contains(current_user_id):
            my_tweets = data.get(current_user_id)
        for elem in my_friends:
            if data.contains(elem):
                tweets += data.get(elem)
        tweets += my_tweets
        for elem in tweets:
            elem['user_name'] = find_user_given_by('id',elem['user_id'],'name')
        return render_template("feed.html",posts = tweets)
    elif request.method == 'POST':
        if "submit_browse" in request.form:
            return redirect(url_for("lookup"))
        title,body = request.form["title"],request.form["body"]
        new_tweet = Tweet(
            title = request.form["title"],
            body = request.form["body"],
            date = datetime.now(),
            user_id = current_user_id
        )
        db.session.add(new_tweet)
        db.session.commit()
        return redirect(url_for("landing_page"))

@app.route("/browse",methods = ["POST"])
def lookup():
    if request.method == 'POST':
        keyword = request.form["keyword"]
        tweet_words = build_vocab_hashtable()
        tweet_list = tweet_id_hashmap()
        tweeties = linked_list.LinkedList()
        if keyword in tweet_words:
            tweet_ids = tweet_words[keyword]
            for elem in tweet_ids:
                tweet = tweet_list.get(elem)
                tweeties.insert_at_end(
                {
                    'id' : tweet["id"],
                    'title' : tweet["title"],
                    'body' : tweet["body"],
                    'date' : tweet["date"],
                    'user_name' : find_user_given_by('id',tweet["user_id"],'name')
                }
            )
        return render_template("feed.html",posts = tweeties.to_list())



"""@app.route("/")
def home():
    #print(db.sesion)
    return "<h1>API Running</h1>"""


if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()
    app.run(debug=True, host = "localhost", port = int("5000"))
    print("yomothafucka")



