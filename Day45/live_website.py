import requests
from bs4 import BeautifulSoup

response = requests.get(url="https://news.ycombinator.com/news")

yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, "html.parser")

article_links = []
article_texts = []

articles_link = soup.select(selector=".titleline a")
for article in articles_link:
    link = article.get("href")
    article_links.append(link)

# We were able to achieve only the even indexes in a list through list slicing, it was the only way as it was
# strings and not integers, that would've been a lot easier
pure_list = article_links[::2]




#upvotes = soup.find_all(name="span", class_="score").getText()   # find_all gives us a list, and we can't call
                                                                # getText() on list so we need to change it to list
                                                                # comprehension

## This was just for practice to see the values
# for upvote in upvotes:
#     score = upvote.getText()
#     print(score)


# The updated version using list comprehension, btw the above written for loop does the same thing
# but whatever we need to do better

upvotes = [int(score.getText().split()[0]) for score in soup.find_all(name="span", class_="score")]


article_text = soup.find_all(name="span", class_= "titleline")
for title in article_text:
    text = title.getText()
    article_texts.append(text)

# OR
# article_title = soup.select(selector= ".titleline")
# for title in article_text:
#     text = title.getText()
#     article_texts.append(text)
# Both work the same way, you can use both to get the same results

print(article_texts)
print(pure_list)
print(upvotes)

# print(upvotes[0].split()[0])   Wow, this is how we were able to remove the string "points" altogether

maxi = upvotes[0]
for i in upvotes:
    if i > maxi:
        maxi = i

#   We could also use the max function maxi = max(upvotes), that's it

largest_number = maxi
largest_index = upvotes.index(largest_number)
print(largest_index)

print(article_texts[largest_index])
print(article_links[largest_index])




