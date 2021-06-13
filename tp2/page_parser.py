import requests as r
from bs4 import BeautifulSoup as bs
import os
from pathlib import Path
import shutil
import re
info_array = []
name_array = []
language = "html"
links = []
# regex
regex_name = re.compile(r'\/(\w+).asp')

#make dir
path = os.path.join("html/")
path = Path('html')
if path.exists() and path.is_dir():
    shutil.rmtree(path)
    os.makedirs(path)
else:
    os.makedirs(path)

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
        i = i.strip()
        data = get_soup(i)
        info_array.append(data)
        name_array.append(re.findall(regex_name, i)[0])
    print(" We have html")
    count = 0
    for i in info_array:
        write_path = os.path.join("html", name_array[count] + ".html")
        with open(write_path, "w") as f:
            f.write(str(i))
        f.close()
        count +=1

main()       