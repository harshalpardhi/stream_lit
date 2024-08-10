
import streamlit as st
import requests
from datetime import datetime

# Constants
API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'  # Replace with your OpenWeatherMap API key

# Function to get weather
def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    if data.get('weather'):
        return data['weather'][0]['description'], data['main']['temp']
    else:
        return None, None

# Define suggestions based on mood, age, weather, time of day, and vitamin deficiency
def get_suggestions(mood, age, weather, vitamin_deficiency, time_of_day):
    suggestions = {'food': '', 'workout': ''}

    # Food and workout suggestions based on mood and age
    if mood == 'low':
        suggestions['food'] = 'Eat foods rich in complex carbs and proteins such as oatmeal, eggs, and nuts. Hydrate well.'
        suggestions['workout'] = 'Consider light activities like walking or stretching to boost your mood.'
    else:
        suggestions['food'] = 'Maintain a balanced diet with lean proteins, vegetables, and whole grains.'
        suggestions['workout'] = 'Engage in regular exercise like running, cycling, or a fitness class.'

    if age < 30:
        suggestions['food'] += ' You might also enjoy some quick energy-boosting snacks like yogurt or fruit.'
        suggestions['workout'] += ' High-intensity workouts and strength training might be more suitable for you.'
    elif age >= 30 and age < 60:
        suggestions['food'] += ' Ensure you are consuming enough fiber and antioxidants for optimal health.'
        suggestions['workout'] += ' Moderate exercise like jogging, swimming, or strength training is ideal.'
    else:
        suggestions['food'] += ' Focus on nutrient-dense foods that support bone and joint health.'
        suggestions['workout'] += ' Low-impact exercises such as walking, water aerobics, or gentle yoga are beneficial.'

    # Time of day suggestions
    if time_of_day in ['morning', 'afternoon']:
        suggestions['food'] += ' Start your day with a hearty breakfast or lunch, depending on the time.'
        suggestions['workout'] += ' A good time for a workout session to energize your day.'
    else:
        suggestions['food'] += ' Opt for a lighter dinner or snack in the evening.'
        suggestions['workout'] += ' Evening workouts should be gentle to avoid disrupting sleep.'

    # Weather-based suggestions
    if weather in ['clear sky', 'few clouds']:
        suggestions['workout'] += ' The weather is perfect for outdoor exercises like running or hiking.'
    elif weather in ['rain', 'snow', 'drizzle']:
        suggestions['workout'] += ' Consider indoor workouts such as yoga, bodyweight exercises, or a home workout routine.'
    else:
        suggestions['workout'] += ' Choose a workout based on your preference and available resources.'

    # Vitamin deficiency suggestions
    if vitamin_deficiency == 'Vitamin D':
        suggestions['food'] += ' Include Vitamin D-rich foods such as fatty fish, fortified dairy products, and egg yolks.'
    elif vitamin_deficiency == 'Vitamin B12':
        suggestions['food'] += ' Add Vitamin B12 sources like meat, dairy, eggs, and fortified cereals to your diet.'
    elif vitamin_deficiency == 'Iron':
        suggestions['food'] += ' Incorporate iron-rich foods such as spinach, red meat, lentils, and fortified cereals.'

    return suggestions

# Streamlit UI
st.title('Personalized Health and Wellness Suggestions')

# Input fields
city = st.text_input('Enter your city:')
mood = st.radio('How is your mood today?', ['low', 'normal'])
age = st.number_input('Enter your age:', min_value=0, max_value=120)
vitamin_deficiency = st.selectbox('Do you have any known vitamin deficiencies?', ['None', 'Vitamin D', 'Vitamin B12', 'Iron'])

# Determine the time of day
current_hour = datetime.now().hour
if 5 <= current_hour < 12:
    time_of_day = 'morning'
elif 12 <= current_hour < 17:
    time_of_day = 'afternoon'
elif 17 <= current_hour < 21:
    time_of_day = 'evening'
else:
    time_of_day = 'night'

# Get weather data
if city:
    weather, temp = get_weather(city)
    if weather:
        st.write(f'Current weather in {city}: {weather} with a temperature of {temp}°C')

        # Get suggestions
        suggestions = get_suggestions(mood, age, weather, vitamin_deficiency, time_of_day)

        # Display suggestions
        st.subheader('Suggestions for You')
        st.write('**Food Suggestions:**', suggestions['food'])
        st.write('**Workout Suggestions:**', suggestions['workout'])
    else:
        st.write('Unable to fetch weather data. Please check the city name and try again.')
