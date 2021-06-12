import requests as r
from bs4 import BeautifulSoup as bs
import os
info_array = []
language = "html"
links = []
with open("links.txt","r") as f:
    for link in f.readlines():
        links.append(link)
f.close()
print(links)


def get_soup(link):
    req = r.get(link)
    soup = bs(req.content,'html.parser')
    final_soup = soup.find("div", {"id":"main"})
    return final_soup


def main ():
    print("Getting links")
    for i in links:
        data = get_soup(i)
        info_array.append(data)
        print(i)
    print(" We have html")
    count = 0
    for i in info_array:
        count +=1
        path = os.path.join("html", str(count), ".txt")
        os.makedirs (path)
        with open(path, "w") as f:
            f.write(i)
        f.close()
        print("added: " + path)

main()       