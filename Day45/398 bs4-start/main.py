from bs4 import BeautifulSoup

# import lxml    ## sometimes html.parser doesn't work on some websites then we use lxml instead

with open("website.html", encoding='utf-8') as file:
    #file.write("Hey, i did it!")
    contents = file.read()

soup = BeautifulSoup(contents, "html.parser")

#print(soup)
print(soup.prettify())
#print(soup.title)
#print(soup.title.name)
#print(soup.title.string)

all_anchor_tags = soup.find_all(name="a")
print(all_anchor_tags)

for tag in all_anchor_tags:         # for just the text
    print(tag.getText())

for tag in all_anchor_tags:         # for just the links
    print(tag.get("href"))

heading = soup.find(name="h1", id="name")
print(heading)
# heading1 = soup.h1        same thing but the top one has more perks, this one always gives the first tag
# print(heading1)             whereas the top one can play along as it also has the id or class_

section_heading = soup.find(name= "h3", class_="heading")
print(section_heading)
print(section_heading.getText())
print(section_heading.name)
print(section_heading.get("class"))

company_url = soup.select_one(selector="p a")   # The a tag that sits inside the p tag, ##css styling format
print(company_url)


name = soup.select_one(selector="#name")        # the css id
print(name)


headings = soup.select(selector=".heading")     # the css class
print(headings)

