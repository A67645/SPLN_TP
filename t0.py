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
    local_nasc = ""
    data_morte = ""
    data_nasc = ""
    local_morte = ""
    print("Entrou na funcao")
    if '+' in string and '*' in string:
        split = string.split("+",2)
        local_nasc, data_nasc = check_local_data(split[0])
        local_morte, data_morte = check_local_data(split[1])
    elif '+' in string and '*' not in string:
        local_nasc = "null"
        data_nasc = "null"
        local_morte, data_morte = check_local_data(string)
    elif '*' in string and '+' not in string:
        local_nasc = check_local_data(string)
        data_nasc = check_local_data(string)
        local_morte = "null"
        data_morte = "null"
    return local_nasc, data_nasc, local_morte, data_morte

# perceber se temos local e data em cada main_info
def check_local_data(string): # confirm regex .search and .match
    re_local = re.compile("[*|+] (.+?)[0-9]")
    re_data = re.compile("([0-9][0-9].[0-9][0-9].[0-9][0-9][0-9][0-9]?)")
    data = "null"
    if re.match(re_data,string):
        local = re.search(re_local, string)
        data = re.search(re_data, string)
    else:
        local = string
    print(local)
    print(data)
    return local, data

# percber que campos temos disponiveis dentro do casamento
def check_casamento(string):
    re_data = re.compile("([0-9][0-9].[0-9][0-9].[0-9][0-9][0-9][0-9]?)")
    re_local = re.compile("[*|+] (.+?)[0-9]")
    re_id = re.compile("[0-9]+")
    data = ""
    local = ""
    id = ""
    if re.match(re_data, string):
        data = re.search(re_data, string)
    if re.match(re_local, string):
        local = re.search(re_local, string)
    if re.match(re_id, string):
        id = re.search(re_id, string)
    return id, local, data

# confirmar se existem casamentos na pagina
def exists_casamento(sopa):
    temp = sopa.find_all("div", { "class": "marcadorP" , "style": "margin-top: 10px;"})
    for i in temp:
        if 'Casamentos' in i:
            return True
        else:
            return False

def exists_parents(sopa):
    temp = sopa.find_all("div", { "class": "marcadorP" , "style": "margin-top: 10px;"})
    for i in temp:
        if 'Pais' in i:
            return True
        else:
            return False

def exists_filhos(sopa):
    temp = sopa.find_all("div", { "class": "marcadorP" , "style": "margin-top: 10px;"})
    for i in temp:
        if 'Filhos' in i:
            return True
        else:
            return False

# definir função para extrair dados de pag de user
def parsePage(link_id):
    print(link_id)
    url = f"http://pagfam.geneall.net/3418/pessoas.php?id={link_id}"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    # get users general info
    name = soup.title.name
    familia = soup.find("div", {"class" : "head2"}).text

    # get the first block of information
    main_info = soup.find("div", {"align": "center", "class": "head1"}).next_element.next_element.next_element
    main_info = str(main_info).replace("<nobr>","")
    main_info = str(main_info).replace("</nobr>","")
    main_info = str(main_info).replace('<div align="center">',"")
    main_info = str(main_info).replace('</div>',"")
    print(main_info)
    local_nasc, data_nasc, local_morte, data_morte = birth_death_validator(main_info)

    print("main info parsed")
    # get parents info
    if exists_parents(soup):
        text_parents = soup.find_all("b")
        pai_string = text_parents[0].next_element.next_element.next_element
        mae_string = text_parents[1].next_element.next_element.next_element
        parents_pai = re.search("[0-9]+",str(pai_string)).group(0)
        parents_mae = re.search("[0-9]+",str(mae_string)).group(0)
        print("parents info parsed")
    # get marriage info
    if exists_casamento(soup):
        paragraph = soup.find("td", {"width": "100%"})
        temp = str(paragraph).split("Casamentos",2)
        temp = temp[1]
        if exists_filhos:
            temp = temp.split("Filhos",2)
            temp = temp[0]
        lista_casamentos = temp.split("Casamento")
        l_lista_casamentos = []
        l_lista_temp = []
        for i in lista_casamentos:
            print("chegou aquI!!!")
            # prepare string for parsing
            string = str(i)
            string = string.replace("</div>","")
            string = string.replace('</div><div align="center"><b>',"")
            string = string.replace("<b>","")
            string = string.replace("</b>","")
            string = string.replace("<nobr>","")
            string = string.replace("</nobr>","")
            string = string.replace("<a>","")
            string = string.replace("</a>","")
            string = string.replace('<div align="center" style="margin-bottom: 15px',"")
            string = string.replace('<div align="center">',"")
            string = string.replace('"><a',"")
            string = string.replace('>',";")
            string = string.split(";")
            l_lista_temp.append(string)
        l_lista_temp = [x for x in l_lista_temp if x != ['']]
        print(l_lista_temp)
        for l in l_lista_temp:
            conjuge, local, data = check_casamento(str(l))
            l_lista_casamentos.append([conjuge,local,data])
        print(l_lista_casamentos)
        # get heritage info
    if exists_parents(soup):
        print("Filhos")


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
    print(lista_pessoas)
    #print("Parisng the families index")
    #lista_familia = listarFamilias(link_famila)
    print("Parsing individuals...")
    for i in lista_pessoas:
        indvData = parsePage(i)
        #output.append(createJson(indvData))

    #with open("output.json","w") as f:
    #    f.write(ouput)
    #f.close()

    #print("Created Json List with {} obs.".format(lista_pessoas.len()))

main()