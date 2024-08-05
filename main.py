from openai import OpenAI
import requests
import json

# INITIALIZE API KEYS/CUSTOMIZABLE VARIABLES BELOW
openWeatherAPIKey= ""
openaiAPIKey= ""
city = ""

# initialize variables

client = OpenAI(api_key=openaiAPIKey)

weatherRequest = requests.get("http://api.openweathermap.org/data/2.5/weather?appid=" + openWeatherAPIKey + "&q=" + city)
forecastRequest = requests.get("http://api.openweathermap.org/data/2.5/forecast?&appid=" + openWeatherAPIKey + "&q=" + city)

cityWeather = weatherRequest.json()
cityForecast = forecastRequest.json()

currentDay = cityForecast["list"][0]["dt_txt"].split(" ")[0]
weatherData = f"Currently, {cityWeather["main"]["temp"] - 272.15:.2f} degrees Celsius, " + cityWeather["weather"][0]["description"]

# loop through data and collect today's forecast

for item in cityForecast["list"]:
    if currentDay not in item["dt_txt"]:
        weatherData += "."
        break
    else:
        weatherData += f". On {item["dt_txt"].split(" ")[1]}, {item["main"]["temp"] - 272.15:.2f} degrees Celsius, {item["weather"][0]["description"]}"

# Send data to chatGPT and print the response

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": f"Using the following data, give me a summary of today's weather (in 12-hour clock format): {weatherData}"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")

# insert line break
print("")