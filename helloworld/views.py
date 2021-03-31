import requests
from django.shortcuts import render, get_object_or_404, redirect
from .models import City
from .forms import CityForm
from django.http import Http404, HttpResponseRedirect
from collections import Counter
from django.urls import reverse
from . import views
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from .forms import LoginForm, RegistrationForm

def log_out(request):
    logout(request)
    redirect_url = request.GET.get('next') or reverse('index')
    return redirect(redirect_url)

def log_in(request):
    if request.method == 'POST':
        logout(request)
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET['next'])
            else:
                form.add_error('Invalid credentials!')
    else: # GET
        form = LoginForm()
    return render(request, 'helloworld/login.html', {'form': form})
def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            logout(request)
            #blog_title = form.cleaned_data['blog_title']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_again = form.cleaned_data['password_again']
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'User already exists!')
            elif password != password_again:
                form.add_error('password_again', 'Passwords mismatch!')
            else:
                user = User.objects.create_user(username, email, password)
                #blog = Blog.objects.create(author=user, title=blog_title)
                login(request, user)
                #context = {'blog': blog, 'posts': []}
                return render(request, 'helloworld/index.html')
    else: # GET
        form = RegistrationForm()
    return render(request, 'helloworld/signup.html', {'form': form})
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

