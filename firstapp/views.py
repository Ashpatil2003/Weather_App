from django.shortcuts import render
import requests,datetime
from django.contrib import messages

# def home(request):
#     if 'city' in request.POST:
#         city = request.POST.get('city', 'Hyderabad').strip()
#     else:
#         city='Hyderabad'
#
#     url= f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=31a5a9a726f317938bdc96f12a6c0338'
#     PARAMS={'units':'metric'}
#
#     API_KEY='AIzaSyBvMY2qYlXgnmoomJN6lLiaGTJXE5rypOQ'
#     SEARCH_ENGINE_ID = 'c56aec6d8c04d4c21'
#
#     query = city + " 1920x1080"
#     page = 1
#     start = (page-1) * 10+1
#     searchType = 'image'
#     city_url = f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&searchType={searchType}&start={start}&searchType=image'
#
#     data= requests.get(city_url).json()
#     print(data)
#     count=1
#     search_items=data.get("items")
#
#     if search_items and len(search_items) > 1:
#         image_url = search_items[1]['link']
#     else:
#         image_url = "https://via.placeholder.com/600x400?text=Weather"
#
#
#     try:
#         data=requests.get(url,PARAMS).json()
#
#         description= data['weather'][0]['description']
#         icon=data['weather'][0]['icon']
#         temp=data['main']['temp']
#
#         day=datetime.date.today()
#
#         return render(
#             request,
#             'weatherapp/index.html',
#             {
#                 'description': description,
#                 'icon': icon,
#                 'temp': temp,
#                 'day': day,
#                 'city': city,
#                 'exception_occurred': False,
#                 'image_url': image_url
#                  }
#         )
#     except:
#         exception_occurred=True
#         messages.error(request,'enter data is not available in api')
#         day=datetime.date.today()
#
#         return render(
#             request,
#             'weatherapp/index.html',
#             {
#                 'description': "clear sky",
#                 'icon': '01d',
#                 'temp': 25,
#                 'day': day,
#                 'city': "Hyderabad",
#                 'exception_occurred':True
#             }
#         )




from django.shortcuts import render
import requests
import datetime
from django.contrib import messages


def home(request):

    # Get city from search form
    if request.method == 'POST':
        city = request.POST.get('city', 'Hyderabad').strip()

        if not city:
            city = 'Hyderabad'
    else:
        city = 'Hyderabad'

    # OpenWeather API key
    API_KEY = '31a5a9a726f317938bdc96f12a6c0338'

    url = 'https://api.openweathermap.org/data/2.5/weather'

    PARAMS = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(url, params=PARAMS)

        print("STATUS CODE:", response.status_code)
        print("RESPONSE:", response.json())

        weather_data = response.json()

        if response.status_code != 200:
            raise Exception(weather_data.get('message', 'Weather API error'))

        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']

        day = datetime.date.today()

        return render(
            request,
            'weatherapp/index.html',
            {
                'description': description,
                'icon': icon,
                'temp': temp,
                'day': day,
                'city': weather_data['name'],
                'exception_occurred': False,
                'image_url': ''
            }
        )

    except Exception as e:

        print("ERROR:", e)

        messages.error(
            request,
            f"Weather data not available for {city}"
        )

        day = datetime.date.today()

        return render(
            request,
            'weatherapp/index.html',
            {
                'description': 'clear sky',
                'icon': '01d',
                'temp': 25,
                'day': day,
                'city': city,
                'exception_occurred': True,
                'image_url': ''
            }
        )