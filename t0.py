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

    # definir lista de users/links para lista de users
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

# definir função para validar output do bs4
def birth_death_validator(string):
    if '+' in string and '*' in string:
        return string.split("+",2)
    elif '+' in string and '*' not in string:
        list = ["null",string]
        return list
    elif '*' in string and '+' not in string:
        list = [string, "null"]
        return list


# definir função para extrair dados de pag de user
def parsePage(link_id):

    re_data = re.compile("([0-9][0-9].[0-9][0-9].[0-9][0-9][0-9][0-9]?)")
    re_local = re.compile("[*|+] (.+?)[0-9]")

    print("Outputs dictionary with the existing info")
    for i in link_id:
        url = "http://pagfam.geneall.net/3418/pessoas.php?id={}".format(i)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')

        # get users general info
        name = soup.title.name
        familia = soup.find("div", {"class" : "head2"}).text

        # get the first block of information
        main_info = soup.find("div", {"align": "center", "class": "head1"}).next_element.next_element.next_element
        main_info = str(text2).replace("<nobr>","")
        main_info = str(text2).replace("</nobr>","")
        main_info = str(text2).replace('<div align="center">',"")
        main_info = str(text2).replace('</div>',"")
        birth_death_list = birth_death_validator(main_info)

        local_nasc = re.search(re_local,birth_death_list[0]).group(0)
        local_morte = re.search(re_local,birth_death_list[1]).group(0)
        data_nasc = re.search(re_data,birth_death_list[0]).group(0)
        data_morte = re.search(re_data,birth_death_list[1]).group(0)

        # get parents info
        text_parents = soup.find_all("b")
        pai_string = text_parents[0].next_element.next_element.next_element
        mae_string = text_parents[1].next_element.next_element.next_element

        parents_pai = re.search("[0-9]+",pai_string).group(0)
        parents_mae = re.search("[0-9]+",mae_string).group(0)

        # get marriage info
        paragraph = soup2.find("div", {"class": "txt2", "align": "center"})
        temp = str(paragraph).split("Casamentos",2)
        lista_casamentos = temp[1].split("Casamento")
        for i in lista_casamentos:
                str(i).replace("</div>","")
                str(i).replace('</div><div align="center"><b>',"")
                str(i).replace("<b>","")
                str(i).replace("</b>","")
                str(i).replace("<nobr>","")
                str(i).replace("</nobr>","")
                str(i).replace("<a>","")
                str(i).replace("</a>","")
                str(i).replace('<div align="center" style="margin-bottom: 15px',"")

        # get heritage info


def createJson(dic):
    print("Outputs Json file") #not needed probably, serialize only


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