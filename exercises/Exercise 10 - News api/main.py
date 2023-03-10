import requests
import json
key = "75e0af61a1df4cc5987bb1068c9f932a"

response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&category=sports&apiKey={key}")

data = response.json()

# print(response.text)
# print(data['title'])

print(len(data))

# for d in data:
#     print(type(d))
