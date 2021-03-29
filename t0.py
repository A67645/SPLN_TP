#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import re


# definir função para ler todas as familias


# definir função para ler todas as pessoas
def listarPessoas(link):
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')

    reID = re.compile("pessoas.php\?id=+[0-9]+") # pattern to check if is person entry
    reLink =re.compile("[0-9]+\-[0-9]+") # pattern to check if is a index entry
    findID = re.compile("[0-9]+") # get ID from string
    findLink = re.compile() # get Link from String


    # parse the first page
    for a in soup.find_all('a', href=True):
        if re.search(reID, a):
            id = re.match(findID,re.match(reID, a))
            lista.append(id)
        elif re.search(reList, a)
            lista_links.append("href")
    # parse the aditional indexes pages to get all the ids
    for i in lista_links:
        print("Parsing do index" + i+2)
        for a in soup.find_all('a', href=True):
            if a == "regexParaVerseTemID":
                lista.append("RegexDeID")
    return lista
    print("Terminado parsing das pessoas")
    # daqui precisamos de uma lista com id apenas


# definir função para extrair dados de pag de user


# definir função para definir dados de pag de cada familia.


def main():
    # read main webpage
    content = requests.get("http://pagfam.geneall.net/3418/").content

    with open("file.html","wb") as f:
        f.write(content)
    f.close()

    with open("file.html","r") as b:
        soup = BeautifulSoup(b, features = "html.parser")
    b.close()

    #get links for family and people directory
    link_pessoa = 'http://pagfam.geneall.net/3418/' + soup.find_all("option", string = "Pessoas")[0]['value']
    link_famila = 'http://pagfam.geneall.net/3418/' + soup.find_all("option", string = "Famílias")[0]['value']

    print("Found the people and families indexes")

    print("Parsing the people index")
    lista_pessoas = listarPessoas(link_pessoa)
    #print("Parisng the families index")
    #lista_familia = listarFamilias(link_famila)



main()