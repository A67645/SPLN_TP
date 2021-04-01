#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import re


# definir função para ler todas as pessoas
def listarPessoas(link):
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')

    reID = re.compile("pessoas.php\?id=+[0-9]+") # pattern to check if is person entry
    reLink =re.compile("[0-9]+\-[0-9]+") # pattern to check if is a index entry
    findID = re.compile("[0-9]+") # get ID from string
    findLink = re.compile('(?<=")(.*?)(?=<\/a>)') # get Link from String

    # definir lista de users /links para lista de users
    lista = []
    lista_links = []

    # parse the first page
    for a in soup.find_all('a', href=True):
        data = a.decode()
        if re.search(reID, data):
            id = re.search(findID, data).group(0) # ,re.match(reID, data)
            lista.append(id)
        elif re.search(reLink, data):
            links = re.search(findLink, data).group(0).replace('">',"")
            lista_links.append(links)
    # parse the aditional indexes pages to get all the ids
    for i in lista_links:
        for a in soup.find_all('a', href=True):
            data = a.decode()
            if re.search(reID, data):
                id = re.search(findID, data).group(0) # ,re.match(reID, data)
                lista.append(id)
    return lista


# definir função para extrair dados de pag de user
def parsePage(link_id):

    re_data = re.compile("[0-9][0-9].[0-9][0-9].[0-9][0-9][0-9][0-9]?)")
    re_local = re.compile("\[*|+] (.+?)[0-9]")

    print("Outputs dictionary with the existing info")
    for i in link_id:
        url = "http://pagfam.geneall.net/3418/pessoas.php?id={}".format(i)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')

        # get users general info
        name = soup.title.name
        familia = soup.find("div", {"class" : "head2"}).text
        local_nasc = re.search(re_local,birth_death_list[0]).group(0)
        local_morte = re.search(re_local,birth_death_list[1]).group(0)
        data_nasc = re.search(re_data,birth_death_list[0]).group(0)
        data_morte = re.search(re_data,birth_death_list[1]).group(0)

        # get parents info

        # get marriage info

        # get heritage info


def createJson(dic):
    print("Outputs Json file") #not needed probably, serialize only

# definir função para validar output do bs4
def brith_death_validator(string):
    if '+' in string && '*' in string:
        return string.split("+",2)
    elif '+' in string && '*' not in string:
        list = ["null",string]
        return list
    elif '*' in string && '+' not in string:
        list = [string, "null"]
        return list

def main():
    # read main webpage
    content = requests.get("http://pagfam.geneall.net/3418/").content
    #change this, why download the html when we can get all from bsf directly?
    with open("file.html","wb") as f:
        f.write(content)
    f.close()

    with open("file.html","r") as b:
        soup = BeautifulSoup(b, features = "html.parser")
    b.close()

    #get links from the people directory
    link_pessoa = 'http://pagfam.geneall.net/3418/' + soup.find_all("option", string = "Pessoas")[0]['value']

    print("Parsing the people index...")
    lista_pessoas = listarPessoas(link_pessoa)
    #print("Parisng the families index")
    #lista_familia = listarFamilias(link_famila)
    print("Parsing individuals...")
    for i in lista_pessoas:
        indvData = parsePage('http://pagfam.geneall.net/3418//pessoas.php?id=' + id)
        output.append(createJson(indvData))

    with open("output.json","w") as f:
        f.write(ouput)
    f.close()

    print("Created Json List with {} obs.".format(lista_pessoas.len()))

main()