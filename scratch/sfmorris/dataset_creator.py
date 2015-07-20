#!/usr/bin/env python3

import rauth
import requests
import sys
import json
import pprint

def business_per_city(city_list):
    """
    returns a success code for printing a city json file 
    """

    params = {}
    params["limit"] = "3"

    consumer_key = "KUvBeJ9O5nV23Bg5lBGLUA"
    consumer_secret = "K-xQZ9Y8moKw1C71Qsn61MaM0t0"
    token = "VchJDQRV1LyH_ZHoawrotybgyuuVN-IW"
    token_secret = "eWqGCYQrFV9QcE2Ok6LuTvx6p7g"

    session = rauth.OAuth1Session(consumer_key = consumer_key, consumer_secret = consumer_secret, access_token = token, access_token_secret = token_secret)
    biz_list = []

    for city, city_urlized in (city_list):
        params["location"] = city 
        for term in ("veterinarian", "pet+groomer", "dog+park"):
            params["term"] = term
            # Get a json response and stuff it in response_r
            response_r = session.get("http://api.yelp.com/v2/search", params=params)
            # Create a (single-quoted) dict object out of response_r
            d = response_r.json()
            # Give the key value "businesses" and get just the (single-quoted) list_of_businesses value
            list_of_businesses = d["businesses"]
            # Add every business in list_of_businesses to biz_list
            biz_list += list_of_businesses

    # json.dumps() expects a dict    
    dict_to_dump = { "biz" : biz_list }
    # Print the double-quoted json string -- it will be parseable to later programs
    print(json.dumps(dict_to_dump, indent = 4))

    session.close()

def yelp_query(city, term, field_name):

    # setup for yelp requests
    yelp_params = {}
    consumer_key = "KUvBeJ9O5nV23Bg5lBGLUA"
    consumer_secret = "K-xQZ9Y8moKw1C71Qsn61MaM0t0"
    token = "VchJDQRV1LyH_ZHoawrotybgyuuVN-IW"
    token_secret = "eWqGCYQrFV9QcE2Ok6LuTvx6p7g"

    session = rauth.OAuth1Session(consumer_key = consumer_key, consumer_secret = consumer_secret, access_token = token, access_token_secret = token_secret)

    yelp_params["location"] = city 
    yelp_params["term"] = term
    yelp_params["limit"] = 1
    yelp_response = session.get("http://api.yelp.com/v2/search", params = yelp_params)
    d = yelp_response.json()
    #print(json.dumps(d, indent = 4))
    result = d["businesses"][0][field_name]
    #print(result)
    session.close()
    return result

def google_query(term):
    url = 'http://ajax.googleapis.com/ajax/services/search/web'
    payload = {"v" : 1.0, "q" : term}
    r = requests.get(url, params = payload)
    #print(json.dumps(r.json(), indent = 4))
    #print("google " + r.json()["responseData"]["results"][0]["visibleUrl"])
    return(r.json()["responseData"]["results"][0]["visibleUrl"])

def create_shelters_file(city_list, shelter_count):
    """
    given a city, find <25 shelters associated with it and only include them if their city field matches
    return the list of shelter objects
    costs one request per city in city_list
    """
    # query petfinder using shelters.find
    # parse the json as a list of shelter objects
    # later, do filtering
    # return it
    # http://api.petfinder.com/shelter.find?key=2933122e170793b4d4b60358e67ecb65&location=78723&format=json

    fixture_superlist = []
    pk = 1

    for city, city_urlized in city_list:
        petfinder_url = "http://api.petfinder.com/shelter.find"
        payload = {"key" : "2933122e170793b4d4b60358e67ecb65", "location" : city, "count" : shelter_count, "format" : "json"}
        r = requests.get(petfinder_url, params=payload)
        fixture_list = []
        #print(json.dumps(r.json(), indent = 4))
        for sh in r.json()["petfinder"]["shelters"]["shelter"]:
            #print(str(sh))
            try:
                shelter_fields = {  "shelter_id" : sh["id"]["$t"],
                                    "shelter_name" : sh["name"]["$t"],
                                    "shelter_address" : sh["name"]["$t"],
                                    "shelter_city" : sh["city"]["$t"],
                                    "shelter_state" : sh["state"]["$t"],
                                    "shelter_lattitude" : sh["latitude"]["$t"],
                                    "shelter_longitude" : sh["longitude"]["$t"],
                                    "shelter_phone" : sh["phone"]["$t"],
                                    "shelter_email" : sh["email"]["$t"],
                                    "shelter_city_urlized" : city_urlized,
                                    "shelter_hours" : "9 to 5",  # from yelp
                                    "shelter_pic" : yelp_query(city, sh["name"]["$t"], "image_url"),    # from yelp
                                    "shelter_url" : google_query(sh["name"]["$t"]),    # from google
                                    "shelter_blurb" : yelp_query(city, sh["name"]["$t"], "snippet_text")  # from yelp
                                 }
            except Exception as e:
                # do nothing on KeyError, but don't append an object missing attributes to the list
                #pass
                print("\ncreating shelter " + sh["name"]["$t"] + "\n" + str(e) + "\n" + str(e.args))
            else:
                fixture_element = {"model" : "nsaid.Shelter", "pk" : pk, "fields" : shelter_fields}
                fixture_list.append(fixture_element)
                pk += 1
        fixture_superlist += fixture_list
    shelter_file = open("../../nsaid/fixtures/shelters_fixture_test.json", "w")
    json.dump(fixture_superlist, shelter_file, indent = 4)
    shelter_file.close()



def create_pets_file(pet_count):
    """
    given a shelter (json object)
    query for all pets associated with a shelter
    return a list of pets (json objects)
    costs one request per shelter (4) in EACH city
    """
    fixture_superlist = []
    pk = 1

    shelters_file = json.loads(open("../../nsaid/fixtures/shelters_fixture_test.json").read())
    master_pets = []
    for shelter in shelters_file:
        #pets = pet_validate(city.city_name, city.city_state, "pet_city", "pet_state", pets_per_shelter(shelter))
        #print(shelter["fields"]["shelter_id"] + " " + shelter["fields"]["shelter_city"])
        petfinder_url = "http://api.petfinder.com/shelter.getPets"
        payload = {"key" : "2933122e170793b4d4b60358e67ecb65", "id" : shelter["fields"]["shelter_id"], "count" : pet_count, "format" : "json"}
        r = requests.get(petfinder_url, params = payload)
        fixture_list = []
        pets = r.json()
        #print(json.dumps(r.json(), indent = 4))
        try:
            for p in r.json()["petfinder"]["pets"]["pet"]:
                try:
                    thumb = ""
                    big = ""
                    photo_list = p["media"]["photos"]["photo"]
                    for photo in photo_list:
                        if photo["@id"] == "1":
                            if photo["@size"] == "pnt":
                                thumb = photo["$t"]
                            elif photo["@size"] == "x":
                                big = photo["$t"]
                    pet_fields = {  "pet_id" : p["id"]["$t"],
                                    "pet_name" : p["name"]["$t"],
                                    "pet_age" : p["age"]["$t"],
                                    "pet_sex" : p["sex"]["$t"],
                                    "pet_size" : p["size"]["$t"],
                                    "pet_breed" : p["breeds"]["breed"]["$t"],
                                    "pet_shelter" : p["shelterId"]["$t"],
                                    "pet_city" : shelter["fields"]["shelter_city"],
                                    "pet_city_urlized" : shelter["fields"]["shelter_city_urlized"],
                                    "pet_state" : shelter["fields"]["shelter_state"],
                                    "pet_pic_url" : thumb,
                                    "pet_pic_large" : big,
                                    "pet_url" : "pets/" + p["shelterId"]["$t"] + "_" + p["id"]["$t"],
                                    "pet_shelter_url" : "shelters/" + p["shelterId"]["$t"],
                                    "pet_city_url" : "cities/" + shelter["fields"]["shelter_city_urlized"],
                                 }
                except Exception as e:
                    #pass
                    print("\ncreating pet "  + "\n" + str(e) + "\n" + str(e.args))
                else:
                    fixture_element = {"model" : "nsaid.Pet", "pk" : pk, "fields" : pet_fields}
                    fixture_list.append(fixture_element)
                    pk += 1
        except Exception as e:
            #pass
            print("\nno pets in shelter " + shelter["fields"]["shelter_name"] + "\n" + str(e) + "\n" + str(e.args));
        fixture_superlist += fixture_list
    pet_file = open("../../nsaid/fixtures/pets_fixture_test.json", "w")
    json.dump(fixture_superlist, pet_file, indent = 4)    
    #rint(json.dumps(fixture_superlist, indent = 4))
    #return fixture_superlist



if __name__ == "__main__" :
    #city_list = ["austin tx", "san antonio tx", "houston+tx", "san+francisco+ca", "dallas+tx", "el+paso+tx", "new+orleans+la"]

    city_list = [("austin tx", "austin"), ("san antonio tx", "san_antonio"), ("houston tx", "houston"), ("san francisco ca", "san_francisco"), ("new orleans la", "new_orleans")]
    
    #business_per_city([("austin tx", "austin")])

    #yelp_query("austin tx", "Small Chance Rescue", "image_url")
    #print(google_query("Austin pets alive"))
    
    create_shelters_file(city_list, 2)
    create_pets_file(2)
    
    #create_city_file(city_list)

