import requests as r
from bs4 import BeautifulSoup as bs
import page_parser as pp
import pdfkit as pdf
from w3lib.html import remove_tags

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

def get_all(link):
    lista = getLeftLinks(link)
    htmls =[]
    print(lista[75])
    
    for l in lista : 
        htmls.append(pp.getPage(l))
    return htmls    
    



def main ():
    link = "https://www.w3schools.com/html/default.asp"
    pdf.from_string(str(get_all(link)[0]),'teste2.pdf')
    

main()       