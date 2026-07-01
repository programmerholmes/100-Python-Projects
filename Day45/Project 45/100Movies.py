from bs4 import BeautifulSoup
import requests


response = requests.get("https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/")

movies_site = response.text

soup = BeautifulSoup(movies_site, "html.parser")

movies = soup.find_all(name="h3", class_="title")

movies_list = []

for movie in movies:
    save = movie.getText()
    movies_list.append(save)

#reverse_order = movies_list[::-1]    ## One way is through slicing, but this creates a new list,
                                        ## if we don't care for the original list and want to change the order
                                        ##  then we could also do the following,
                                        ## as it doesn't create a new list and saves memory

movies_list.reverse()
print(movies_list)

# We could also use a for loop to reverse it
# for i in range(len(movies_list), -1, -1):
#   print(movies_list[i])

# All three ways gives us the reverse order of the list

with open("movies.txt", 'w', encoding="utf-8") as file:
    for movie in movies_list:
        file.write(movie + "\n")   # or f"{movie}\n"

print("Done!")
