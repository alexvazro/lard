import pymongo
import shop_
import requests
import json
from urllib import parse, request
import os
import random


#fetching the database
client_mongo = pymongo.MongoClient(
    "mongodb+srv://alex:j7WLycrEfzVhiYw8@botcluster.aiwbw2u.mongodb.net/?retryWrites=true&w=majority"
)
mydb = client_mongo.discord_main
products_db = mydb.products
counters_db = mydb.counters


def add_to_db(name, where, client):

    hulk = 0

    collections = list(counters_db.find({}))

    #iterating through the items in the collection
    for x in collections:

        #iterating through the (dictionary) values of the item
        for item, item_value in x.items():

            if item == "_id":
                item_id = item_value

            if item_value == name:
                hulk = 1
                #counter value for the user from the database (mongodb atlas)
                if where == "counter":
                    counter_value = int(list(x.items())[2][1])
                else:
                    counter_value = int(list(x.items())[3][1])
                myquery = {'_id': item_id}
                newvalues = {"$set": {where: counter_value + 1}}

                counters_db.update_one(myquery, newvalues)
                break

    #if no existing user is found, create a new one
    if hulk == 0:
        post = {"author": name, where: 1}
        counters_db.insert_one(post).inserted_id
        print("new user")
        hard_fix(client)
        print("and db fixed")


def get_gif2():
  api_key = os.getenv('GIPHY_API_KEY')
  url = "http://api.giphy.com/v1/gifs/search"

  params = parse.urlencode({
    "q": "monke",
    "api_key": api_key,
    "limit": "50"
  })
  
  with request.urlopen("".join((url, "?", params))) as response:
    data = json.loads(response.read())

  gif_choice = random.randint(0, 49)

  url = data['data'][gif_choice]['images']['original']['url']

  return(url)
  


#Getting the top 3 people who've sworn the most
def get_top(where):

    top1_count = 0
    top1_name = ""

    top2_count = 0
    top2_name = ""

    top3_count = 0
    top3_name = ""

    collections = list(counters_db.find({}))
    for x in collections:

        for item, item_value in x.items():

            if item == where:

                #username of the person from the database (mongodb atlas)
                user_name = list(x.items())[1][1]

                user_counter = item_value

                if user_counter > top3_count:
                    if user_counter > top2_count:
                        if user_counter > top1_count:
                            top3_name = top2_name
                            top3_count = top2_count
                            top2_name = top1_name
                            top2_count = top1_count
                            top1_name = user_name
                            top1_count = user_counter
                        else:
                            top3_name = top2_name
                            top3_count = top2_count
                            top2_name = user_name
                            top2_count = user_counter
                    else:
                        top3_name = user_name
                        top3_count = user_counter

    string1 = ":first_place: " + top1_name[:-5] + " -- " + str(top1_count)
    string2 = ":second_place: " + top2_name[:-5] + " -- " + str(top2_count)
    string3 = ":third_place: " + top3_name[:-5] + " -- " + str(top3_count)

    return (string1, string2, string3)


#returns how many bad words the user has said
def word_counter(name):
    collections = list(counters_db.find({}))

    #iterating through the items in the collection
    for x in collections:

        #iterating through the (dictionary) values of the item
        for item, item_value in x.items():

            if (item == "author") and (item_value == name):

                counter = str(list(x.items())[2][1])

                print_string = name[:-5] + " said " + counter + " bad words!"

                return print_string


def grand_counter(name):
    collections = list(counters_db.find({}))

    #iterating through the items in the collection
    for x in collections:

        #iterating through the (dictionary) values of the item
        for item, item_value in x.items():

            if (item == "author") and (item_value == name):

                counter = str(list(x.items())[3][1])

                print_string = " You have " + counter + " points."

                return print_string, int(counter)


def hard_fix(client):

    collections = list(counters_db.find({}))

    #iterating through the items in the collection
    for x in collections:

        counter_found = False
        counter_value = 1
        grand_found = False
        grand_value = 1
        #iterating through the (dictionary) values of the item
        for item, item_value in x.items():

            if item == "_id":
                item_id = item_value

            if item == "author":
                author = item_value

            if item == "counter":
                counter_value = item_value
                counter_found = True

            if item == "grand":
                grand_value = item_value
                grand_found = True

        #if something is missing, delete it and create a new one
        if (grand_found == False) or (counter_found == False):
            myquery = {"_id": item_id}
            counters_db.delete_one(myquery)

            mydict = {
                '_id': item_id,
                "author": author,
                "counter": counter_value,
                "grand": grand_value
            }
            counters_db.insert_one(mydict)


def remove_points(name, to_remove):

    collections = list(counters_db.find({}))

    #iterating through the items in the collection
    for x in collections:

        #iterating through the (dictionary) values of the item
        for item, item_value in x.items():

            if item == "_id":
                item_id = item_value

            if item_value == name:
                counter_value = int(list(x.items())[3][1])
                counter_value = counter_value - to_remove
                myquery = {'_id': item_id}
                newvalues = {"$set": {"grand": counter_value}}

                counters_db.update_one(myquery, newvalues)
                return counter_value


def add_purchase(name, product_name, client):
    hulk = 0

    hard_fix_products(client)

    collections = list(products_db.find({}))

    if product_name == "Get purred":
        here = 2
    elif product_name == "Kitten":
        here = 3
    else:
        here = 4

    #iterating through the items in the collection
    for x in collections:

        counter = -1

        #iterating through the (dictionary) values of the item
        for item, item_value in x.items():

            counter += 1

            if item == "_id":
                item_id = item_value

            if item_value == name:
                hulk = 1
                #counter value for the user from the database (mongodb atlas)
                counter_value = int(list(x.items())[here][1])
                myquery = {'_id': item_id}
                newvalues = {"$set": {product_name: counter_value + 1}}

                products_db.update_one(myquery, newvalues)
                break

    #if no existing user is found, create a new one
    if hulk == 0:
        post = {"author": name, product_name: 1}
        products_db.insert_one(post).inserted_id
        print("new user")


def hard_fix_products(client):

    collections = list(products_db.find({}))

    #iterating through the items in the collection
    for x in collections:

        purr_found = False
        purr_value = 0
        kitten_found = False
        kitten_value = 0
        woman_found = False
        woman_value = 0
        #iterating through the (dictionary) values of the item
        for item, item_value in x.items():

            if item == "_id":
                item_id = item_value

            if item == "author":
                author = item_value

            if item == "Get purred":
                purr_value = item_value
                purr_found = True

            if item == "Kitten":
                kitten_value = item_value
                kitten_found = True

            if item == "Woman":
                woman_value = item_value
                woman_found = True

        #if something is missing, delete it and create a new one
        if (purr_found == False) or (kitten_found == False) or (woman_found
                                                                == False):
            myquery = {"_id": item_id}
            products_db.delete_one(myquery)

            mydict = {
                '_id': item_id,
                "author": author,
                "Get purred": purr_value,
                "Kitten": kitten_value,
                "Woman": woman_value
            }
            products_db.insert_one(mydict)


def show_collection(name):

    collections = list(products_db.find({}))

    value1 = 0
    value2 = 0
    value3 = 0

    #iterating through the items in the collection
    for x in collections:

        for item, item_value in x.items():

            if item == "author":
                if item_value == name:
                    value1 = int(list(x.items())[2][1])
                    value2 = int(list(x.items())[3][1])
                    value3 = int(list(x.items())[4][1])
                    return value1, value2, value3

    return (value1, value2, value3)
