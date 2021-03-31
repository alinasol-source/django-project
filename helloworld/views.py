import requests
from django.shortcuts import render, get_object_or_404, redirect
from .models import City
from .forms import CityForm
from django.http import Http404, HttpResponseRedirect
from collections import Counter
from django.urls import reverse
from . import views

from django.shortcuts import get_object_or_404, render, redirect


def index(request):
    appid = 'b3059499f68247e4e31a88d7c9511698'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    err_msg = ''
    message = ''

    if(request.method == 'POST'):
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                res = requests.get(url.format(new_city)).json()
                if res['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Город не найден!'
            else:
                err_msg = 'Город уже показан!'
        if err_msg:
            message = err_msg
        else:
            message = None
    form = CityForm()

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city)).json()
        city_info = {
            'city': city.name,
            'temp': res["main"]["temp"],
            'icon': res["weather"][0]["icon"]
        }
        all_cities.append(city_info)

    context = {
        'all_info': all_cities,
        'form': form,
        'message': message
    }

    return render(request, 'helloworld/index.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('index')

