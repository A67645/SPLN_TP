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

def main ():
    link = "https://www.w3schools.com/" + sys.argv[1] + "/default.asp"
    if sys.argv[1] == 'cs':
        link = "https://www.w3shcools.com/" + sys.argv[1] + "/index.php"
    pdf = sys.argv[1]
    if sys.argv[2] == '-o':
        pdf = sys.argv[3]

    warnings.filterwarnings('error')
    try:
        genPDF(link, pdf)
    except RuntimeWarning :
        pass



main()
