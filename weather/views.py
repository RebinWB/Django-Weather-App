from django.shortcuts import render
from .forms import CityForm
from .models import City
import requests

def index(request):
    
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=71f9c3aba3dc034f5b2dab711e095c5b'
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
    
    form = CityForm()
    
    cities = City.objects.all().order_by('-id')
    weather_data = []
    
    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)
    
    context = {
        'weather_data' : weather_data,
        'form' : form,
    }
    
    return render(request, 'index.html', context)

# Create your views here.
