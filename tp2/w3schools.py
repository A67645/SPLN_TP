#!/usr/bin/python3

from os import remove
import requests as r
from bs4 import BeautifulSoup as bs
from pathlib import Path
from requests.api import get
import sys
import pdfkit as pdfk
import re
import warnings

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
    #remove links in buttons 
    btsl_s = soup.find_all("div",class_="w3-col m12 l12")
    if btsl_s :
        for btsl in btsl_s:
            btsl.decompose()

def replaceImg(soup,link):
    link_w3 = "https://www.w3schools.com/"
    lang_link = link.split("https://www.w3schools.com/")[1].split('/')[0]
    prefix = link_w3 +lang_link+'/'

    img_s = soup.find_all('img')
    #print(img_s)
    if img_s:
        for img in img_s:
                if '/' in  img['src'] :
                    img['src']= link_w3 + img['src']
                else :
                    img['src']= prefix + img['src']


def getPage(link):
    req = r.get(link)
    soup = bs(req.text,'html.parser')
    final_soup = soup.find("div", {"id":"main"})

    clearPage(final_soup)
    replaceImg(final_soup,link)

    return final_soup

def getLeftLinks(link) :

    pagIni = r.get(link)

    link_w3 = "https://www.w3schools.com"
    #print(link.split("https://www.w3schools.com/"))

    lang_link = link.split("https://www.w3schools.com/")[1].split('/')[0]

    soup = bs(pagIni.text,'html.parser')
    div =soup.find('div', id="sidenav")
    a_s = div.find_all('a')

    for a in a_s :
        tag = a.find({'href':re.compile(r'/')})
        if not tag == None:
            tag.decompose()


    links = []

    for a in a_s :
        if re.search(r'/',a.get('href')):
            link = link_w3+a.get('href')
        else:
            link=link_w3+'/'+lang_link+"/"
            link += a.get('href')
        links.append(link)

    return links

def get_all(link):
    lista = getLeftLinks(link)
    htmls =[]


    for l in lista :
        htmls.append(getPage(l))
    return htmls

def genPDF(link,lang_name):
    html_s = get_all(link)
   
    html_final = ""
    for html in html_s:
        html_final += str(html)

    pdfk.from_string(html_final,lang_name+'.pdf')

def list():
    url = 'https://www.w3schools.com/'
    pagina = r.get(url)
    soup = bs(pagina.text, 'html.parser')
    remover = ['typingspeed','codegame','whatis','tryit','browsers',
    'cert']
    map = {}

    divs = soup.find_all('div', class_ = 'w3-col l3 m6')
    for div in divs:
        for tutorial in div.find_all('a', class_ = 'w3-bar-item w3-button'):
            item = tutorial['href']
            split = item.split('/')
            if split[1] not in map:
                map[split[1]] = True

    for re in remover:
        if re in map :
            del map[re]

    i=0
    for key in map:
        
        print(key)
        


def main ():


    link = "https://www.w3schools.com/" + sys.argv[1] + "/default.asp"
    
    if (sys.argv[1] == 'cs' or
        sys.argv[1] ==  'kotlin' or
        sys.argv[1] ==  'statistics' or
        sys.argv[1] ==  'cybersecurity' or 
        sys.argv[1] == 'accessibility') :
        link = "https://www.w3schools.com/" + sys.argv[1] + "/index.php"

    if (sys.argv[1] == 'sass') :
        link = "https://www.w3schools.com/" + sys.argv[1] + "/default.php"    

    

    pdf = sys.argv[1]

    size =  len(sys.argv)

    if size >= 4 and sys.argv[2] == '-o':
        pdf = sys.argv[3]

    warnings.filterwarnings('error')

    if sys.argv[1] == '-l':
        list()

    else:
        try:
            print(link)
            genPDF(link, pdf)
            
        except RuntimeWarning :
            print('erro')



main()
