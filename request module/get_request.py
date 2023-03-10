import requests

# getting html of a webpage with its url
response = requests.get("https://www.codewithharry.com")


# printing text of response
print(response.text)