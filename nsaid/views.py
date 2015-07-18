from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, render_to_response
from django.db import connection
from nsaid.models import *
from rest_framework import status
from rest_framework.decorators import api_view
import json
from datetime import datetime
from elasticsearch import Elasticsearch


def test(request):
    html = "<html><body>Hey that somehow worked!</body></html>"
    return HttpResponse(html)

def home(request):
    template = loader.get_template('Home.html')
    return HttpResponse(template.render())

def shelters(request):
    shelters_list = Shelter.objects.all()
    context = {"shelters_list": shelters_list}
    return render_to_response("Shelters.html", context)

def pets(request):
    pets_list = Pet.objects.all()
    context = {"pets_list": pets_list}
    return render_to_response("Pets.html", context)

def cities(request):
    cities_list = City.objects.all()
    context = {"cities_list": cities_list}
    return render_to_response("Cities.html", context)

def about(request):
    template = loader.get_template('About.html')
    return HttpResponse(template.render())

def cats(request):
    template = loader.get_template('Cats.html')
    return HttpResponse(template.render())

def dogs(request):
    template = loader.get_template('Dogs.html')
    return HttpResponse(template.render())

def shelter_apa(request):
    template = loader.get_template('Shelter_APA.html')
    return HttpResponse(template.render())

def cat_sari(request):
    template = loader.get_template('Cat_Sari.html')
    return HttpResponse(template.render())

def dog_earl(request):
    template = loader.get_template('Dog_Earl.html')
    return HttpResponse(template.render())

def dog_Rangel(request):
    template = loader.get_template('Dog_Rangel.html')
    return HttpResponse(template.render())

def shelter_HPPL(request):
    template = loader.get_template('Shelter_HPPL.html')
    return HttpResponse(template.render())

def shelter_Muttville(request):
    template = loader.get_template('Shelter_Muttville.html')
    return HttpResponse(template.render())

def city_Austin(request):
    template = loader.get_template('City_Austin.html')
    return HttpResponse(template.render())

def city_Houston(request):
    template = loader.get_template('City_Houston.html')
    return HttpResponse(template.render())

def city_SF(request):
    template = loader.get_template('City_SF.html')
    return HttpResponse(template.render())

def pet_template(request, id):
    pet = Pet.objects.filter(pet_id = id)
    context = {'pet': pet[0]}
    return render(request, 'Pet_template.html', context)

def shelter_template(request, id):
    shelter = Shelter.objects.filter(shelter_id = id)
    context = {'shelter': shelter[0]}
    return render(request, 'Shelter_template.html', context)

def city_template(request, name):
    city = City.objects.filter(city_name = name)
    context = {'city': city[0]}
    return render(request, 'City_template.html', context)

@api_view(['GET'])
def pet_list(request):
    if request.method == 'GET':
        pet_list = Pet.objects.all()
        info = {}
        for pet_obj in pet_list:
            pet_info = {}
            pet_info["pet_id"]          = pet_obj.pet_id
            pet_info["pet_name"]        = pet_obj.pet_name
            pet_info["pet_age"]         = pet_obj.pet_age
            pet_info["pet_sex"]         = pet_obj.pet_sex
            pet_info["pet_size"]        = pet_obj.pet_size
            pet_info["pet_breed"]       = pet_obj.pet_breed
            pet_info["pet_shelter"]     = pet_obj.pet_shelter
            pet_info["pet_city"]        = pet_obj.pet_city
            pet_info["pet_pic_url"]     = pet_obj.pet_pic_url
            pet_info["pet_pic_large"]   = pet_obj.pet_pic_large
            pet_info["pet_url"]         = pet_obj.pet_url
            pet_info["pet_shelter_url"] = pet_obj.pet_shelter_url
            pet_info["pet_city_url"]    = pet_obj.pet_city_url
            info[pet_obj.pet_id] = pet_info
        return HttpResponse(json.dumps(info), content_type="application/json")

@api_view(['GET'])
def shelter_list(request):
    """
    List all shelters, maybe later create?
    """
    if request.method == 'GET':
        shelter_list = Shelter.objects.all()
        info = {}
        for shelter_obj in shelter_list:
            shelter_info = {}
            shelter_info["shelter_id"]       = shelter_obj.shelter_id
            shelter_info["shelter_name"]     = shelter_obj.shelter_name
            shelter_info["shelter_address" ] = shelter_obj.shelter_address
            shelter_info["shelter_city"]     = shelter_obj.shelter_city
            shelter_info["shelter_state"]    = shelter_obj.shelter_state
            shelter_info["shelter_phone"]    = shelter_obj.shelter_phone
            shelter_info["shelter_email"]    = shelter_obj.shelter_email
            shelter_info["shelter_hours"]    = shelter_obj.shelter_hours
            shelter_info["shelter_pic"]      = shelter_obj.shelter_pic
            shelter_info["shelter_url"]      = shelter_obj.shelter_url
            shelter_info["shelter_city_url"] = shelter_obj.shelter_city_url
            info[shelter_obj.shelter_id] = shelter_info
        return HttpResponse(json.dumps(info), content_type="application/json")

@api_view(['GET'])
def city_list(request):
    """
    List all cities, maybe later create?
    """
    if request.method == 'GET':
        city_list = City.objects.all()
        info = {}
        for city_obj in city_list:
            city_info = {}
            city_info["city_name"]        = city_obj.city_name
            city_info["city_state"]       = city_obj.city_state
            city_info["city_country"]     = city_obj.city_country
            city_info["city_vet_url"]     = city_obj.city_vet_url
            city_info["city_groomer_url"] = city_obj.city_vet_url
            city_info["city_park_url"]    = city_obj.city_park_url
            city_info["city_pic"]           = city_obj.city_pic
            city_info["city_vet_pic"]       = city_obj.city_vet_pic
            city_info["city_park_pic"]      = city_obj.city_park_pic
            city_info["city_groomer_pic"]   = city_obj.city_groomer_pic
            city_info["city_url"]           = city_obj.city_url
            info[str(city_obj.city_name + '_' + city_obj.city_state)] = city_info
        return HttpResponse(json.dumps(info), content_type="application/json")

def search (request):
    q = request.GET.get('q')
    es = Elasticsearch()
    #res = es.search(index="gtp_index", doc_type="city", body={"query": {"match": q}})
    """
    print("%d documents found" % res['hits']['total'])
    for doc in res['hits']['hits']:
        print("%s) %s" % (doc['_id'], doc['_source']['content']))
    """
    data = {
        "query": {
            "query_string": { "query": q }
        }
    }
    response = requests.post('http://127.0.0.1:9200/gtp_index/_search', data=json.dumps(data))

    return render_to_response('search/search.html', response.json())
    """
    context = RequestContext(request)
    context_dict = {}
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
    """