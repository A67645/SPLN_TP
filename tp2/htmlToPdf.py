import requests as r
from bs4 import BeautifulSoup as bs



def getLeftLinks(link) -> []:
        
    pagIni = r.get(link)
    link_w3 = "https://www.w3schools.com/"
    lang_link = link.split("https://www.w3schools.com/")[1].split('/')[0]

    soup = bs(pagIni.text,'html.parser')
    div =soup.find('div', id="sidenav")
    a_s = div.find_all('a') 

    links = []

    for a in a_s :
        link=link_w3+lang_link+"/"
        link += a.get('href')
        links.append(link)   

    return links


def main ():
    links = getLeftLinks("https://www.w3schools.com/html/default.asp") 
    with open("links.txt", "a") as f:
        for i in links:
            f.write(i + "\n")

main()       