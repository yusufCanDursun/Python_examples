import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }

url ="https://www.imdb.com/chart/top/"
html = requests.get(url, headers=headers).content
soup = BeautifulSoup(html,"html.parser")
liste = soup.find("ul", {"class":"ipc-metadata-list"}).find_all("li", limit=10)

for item in liste:
    filmadi= item.find("h3", {"class":"ipc-title__text"}).text
    print(filmadi)
