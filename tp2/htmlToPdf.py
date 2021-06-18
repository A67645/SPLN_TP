from bs4 import BeautifulSoup as bs
import sys

import page_parser as pp
import pdfkit as pdfk
import re
import requests as r

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
        htmls.append(pp.getPage(l))
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
    genPDF(link, pdf)

main()       
