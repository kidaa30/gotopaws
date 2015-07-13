#!/usr/bin/env python3

import os
import io
import json

from nsaid.models import * 

city_file = open("Cities.json", "r")
city_dict = json.loads(city_file.read())
city_dict_list = city_dict["all_cities"]
#print(city_dict_list)

shelter_file = open("Shelters.json", "r")
shelter_dict = json.loads(shelter_file.read())
shelter_dict_list = shelter_dict["shelters"]

pet_file = open("Pets.json", "r")
pet_dict = json.loads(pet_file.read())
pet_dict_list = pet_dict["all_pets"]

for c in city_dict_list:
	#print(c["name"])
	cq = City(city_name=c["name"],
		city_state=c["state"],
		city_country=c["country"],
		city_vet_url=c["vet_url"],
		city_groomer_url=c["groomer_url"],
		city_park_url=c["park_url"]
		)
	cq.save()

for s in shelter_dict_list:
	#print(s["name"])
	sq = Shelter(shelter_id=s["id"],
		shelter_name=s["name"],
		shelter_address=s["address1"],
		shelter_city=s["city"],
		shelter_state=s["state"],
		shelter_phone=s["phone"],
		shelter_email=s["email"],
		shelter_hours=s["hours"]
		)
	sq.save()

for p in pet_dict_list:
	#print(p["name"])
	pq = Pet(pet_id=p["petsid"],
		pet_name=p["name"],
		pet_age=p["age"],
		pet_size=p["size"],
		pet_breed=p["breed"],
		pet_shelter=p["shelter"],
		pet_city=p["city"],
		pet_pic_url=p["pic_url"]
		)
	pq.save()


#q = City(name="nameasdf", state="state", country="country", vet_url="vet_url", groomer_url="groomer_url", park_url="park_url")
#q.save()
#print(City.objects.all())


