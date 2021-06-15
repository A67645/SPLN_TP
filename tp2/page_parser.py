import requests as r
from bs4 import BeautifulSoup as bs
import os
from pathlib import Path
import shutil
import re

from requests.api import get


def make_dir(language):
    #make dir
    path = os.path.join("{language}/")
    path = Path('{language}')
    if path.exists() and path.is_dir():
        shutil.rmtree(path)
        os.makedirs(path)
    else:
        os.makedirs(path)

def clearPage(soup):
    #remove w3-btn
    print(type(soup))
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


def getPage(link):
    req = r.get(link)
    soup = bs(req.text,'html.parser')
    final_soup = soup.find("div", {"id":"main"})

    #print(type(final_soup.find_all("a",class_="w3-btn")))
    if ((final_soup.find_all("a",class_="w3-btn")) != None):
        
        btns = final_soup.find_all("a",class_="w3-btn")
        if btns :
            for btn in btns:
                btn.decompose()

    if (final_soup.find_all("form",id="w3-exerciseform")!= None) :   
        #remove form id="w3-exerciseform"
        forms = final_soup.find_all("form",id="w3-exerciseform")
        if forms:
            for form in forms:
                form.decompose()

    if (final_soup.find_all("div",id="getdiploma")!= None) :  
        #remove div id="getdiploma"
        dipls = final_soup.find_all("div",id="getdiploma")
        if dipls :
            for dip in dipls:
                dip.decompose()
        
    return final_soup
   


'''
def main():
    link = "https://www.w3schools.com/html/html_intro.asp"
    #print(getPage(link))
    getPage(link)

main()
'''
