# This is a simple project creating a 100 greatest movies list through web scraping
# with beautiful soup.
from bs4 import BeautifulSoup
import requests
import lxml

WEB_URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

content = requests.get(WEB_URL).text
soup = BeautifulSoup(content, "html.parser")

movie_names = []
movie_links = []

movie_list = soup.find(name="div", class_="entity-info-items__list")
the_links = movie_list.select(selector="li a")

for link in the_links:
    mov_link = link.get('href')
    movie_links.append(mov_link)
    mov_name = link.getText()
    movie_names.append(mov_name)

with open("movies.txt", "w") as file:
    movie_names.reverse()
    num = 0
    for name in movie_names:
        num += 1
        file.write(f"({num}) {name}\n")




