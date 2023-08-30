from django.shortcuts import render,redirect
from .forms import CityForm
from .models import City
import requests
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def weather(request):
    url='https://api.openweathermap.org/data/2.5/weather?q={}&appid=836146208744976db40ff35fda4e3c53&units=metric'
   #to add the data in database

    if request.method=='POST':
        form=CityForm(request.POST)
       
        if form.is_valid():
            NCity=form.cleaned_data['name']# to take the city name form the input field
            #print(NCity)
            CCity=City.objects.filter(name=NCity).count()#to check the data already in the form or not . if its not it take into form
            #print(NCity)

            if CCity==0:
                res=requests.get(url.format(NCity)).json()# to fetch the api data

                #print(res)
                if res['cod']==200:
                    form.save()
                    
                    messages.success(request," "+NCity+" Added successsfully...!")
                else:
                    messages.error(request,res['message'])
            else:
                messages.error(request," "+NCity+"Already Exists..!!!")


    
    form=CityForm()
    cities=City.objects.all()
    data=[]
    for city in cities:
        res=requests.get(url.format(city)).json()
        city_weather={
            'city':city,
            'temperature':res['main']['temp'],
            'description':res['weather'][0]['description'],
            'country':res['sys']['country'],
            'icon':res['weather'][0]['icon'],
        }
        data.append(city_weather)
    context={
        'data':data,
        'form':form
    }
    return render(request,"weatherapp.html",context)

def delete_city(request,CName):
    City.objects.get(name=CName).delete()
    messages.success(request," "+CName+" Removed Successfully..!!")
    return redirect('Weather')
