import requests as r
from bs4 import BeautifulSoup as bs
from pathlib import Path
from requests.api import get


def clearPage(soup):
    #remove w3-btn
    btns = soup.find_all("a",class_="w3-btn")
    if btns :
        for btn in btns:
            btn.decompose()
    
    #remove form id="w3-exerciseform"
    forms = soup.find_all("form",id="w3-exerciseform")
    if forms:
        for form in forms:
            form.decompose()

    #remove div id="getdiploma"
    dipls = soup.find_all("div",id="getdiploma")
    if dipls :
        for dip in dipls:
            dip.decompose()
    #remove input id="searchstring"
    s_s = soup.find_all("input",id="searchstring")
    if s_s :
        for s in s_s:
            s.decompose()

def getPage(link):
    req = r.get(link)
    soup = bs(req.text,'html.parser')
    final_soup = soup.find("div", {"id":"main"})

    clearPage(final_soup)
    
    return final_soup
   


