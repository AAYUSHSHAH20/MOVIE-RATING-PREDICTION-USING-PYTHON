import requests

response = requests.get("https://api.themoviedb.org/3/search/movie",params={"api_key":"e35b8f1415cec2229f2b61f89ea5db75","query":"Matrix"})

data = response.json()["results"]

print(data[0]["release_date"].split("-")[0])


# response = requests.get("https://api.themoviedb.org/3/movie/ 554600",params={"api_key":"e35b8f1415cec2229f2b61f89ea5db75","query":"Matrix"})

# data = response.json()

# print(data)




# https://api.themoviedb.org/3/movie/{movie_id}