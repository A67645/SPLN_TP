#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import re
import json

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
    if '+' in string and '*' in string:
        split = string.split("+")
        local_nasc, data_nasc = check_local_data(split[0])
        local_morte, data_morte = check_local_data(split[-1])
    elif '+' in string and '*' not in string:
        local_nasc = "null"
        data_nasc = "null"
        local_morte, data_morte = check_local_data(string)
    elif '*' in string and '+' not in string:
        local_nasc, data_nasc = check_local_data(string)
        local_morte = "null"
        data_morte = "null"
    return local_nasc, data_nasc, local_morte, data_morte

# perceber se temos local e data em cada main_info
def check_local_data(string): # confirm regex .search and .match
    re_local = re.compile("[*|+] (.+?)[0-9]")
    re_data = re.compile("([0-9][0-9].[0-9][0-9].[0-9][0-9][0-9][0-9]?)")
    data = "null"
    if re.search(re_data,string):
        data = re.search(re_data, string).group(0)
        if re.search(re_local, string):
            local = re.search(re_local, string).group(0)
        else:
            local = "null"
    else:
        local = string
    return local, data

# perceber que campos temos disponiveis dentro do casamento
def check_casamento(string):
    re_data = re.compile("([0-9][0-9].[0-9][0-9].[0-9][0-9][0-9][0-9]?)")
    re_local = re.compile("[^|*](.+?)[0-9][0-9].[0-9][0-9].[0-9][0-9][0-9][0-9]")
    re_local_sData = re.compile(".+(?=;)")
    re_id = re.compile("[0-9]+(?=\">)")
    data = ""
    local = ""
    id = ""
    if re.search(re_data, string):
        data = re.search(re_data, string).group(0)
        if re.search(re_local, string):
            local = re.search(re_local, string).group(0)
    else:
        if re.search(re_id, string):
            id = re.search(re_id, string).group(0)
        else:
            local=re.search(re_local_sData,string).group(0)

    if re.search(re_id, string):
        id = re.search(re_id, string).group(0)
    return id, local, data

# confirmar se existem casamentos na pagina
def exists_casamento(sopa):
    temp = sopa.find_all("div", { "class": "marcadorP" , "style": "margin-top: 10px;"})
    a=0
    for i in temp:
        if 'Casamentos' in i:
            a=1
    if a==1:
        return True
    else :
        return False

def exists_parents(sopa):
    temp = sopa.find_all("div", { "class": "marcadorP" , "style": "margin-top: 10px;"})
    a=0
    for i in temp:
        if 'Pais' in i:
            a=1
    if a==1:
        return True
    else:
        return False

def exists_filhos(sopa):
    temp = sopa.find_all("div", { "class": "marcadorP" , "style": "margin-top: 10px;"})
    a=0
    for i in temp:
        if 'Filhos' in i:
            a=1
    if a==1:
        return True
    else:
        return False

# definir função para extrair dados de pag de user
def parsePage(link_id):
    url = f"http://pagfam.geneall.net/3418/pessoas.php?id={link_id}"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    # get users general info
    name = soup.title.text
    familia = soup.find("div", {"class" : "head2"}).text

    # get the first block of information
    main_info = soup.find("div", {"align": "center", "class": "head1"}).next_element.next_element.next_element
    main_info = str(main_info).replace("<nobr>","")
    main_info = str(main_info).replace("</nobr>","")
    main_info = str(main_info).replace('<div align="center">',"")
    main_info = str(main_info).replace('</div>',"")
    local_nasc, data_nasc, local_morte, data_morte = birth_death_validator(main_info)

    # get parents info
    if exists_parents(soup):
        text_parents = soup.find_all("b")
        pai_string = text_parents[0].next_element.next_element.next_element
        mae_string = text_parents[1].next_element.next_element.next_element
        parents_pai = re.search("[0-9]+",str(pai_string)).group(0)
        parents_mae = re.search("[0-9]+",str(mae_string)).group(0)
    else :
        parents_pai="null"
        parents_mae="null"
    # get marriage info
    if exists_casamento(soup):
        paragraph = soup.find("td", {"width": "100%"})

        temp = str(paragraph).split('Casamentos')

        temp = temp[1]

        if exists_filhos(soup):

            temp = temp.split('<div class="marcadorP" style="margin-top: 10px;">Filhos')
            temp= temp[0]

        # acrescentar check para ver quantos casamentos é que há:
        lista_casamentos = [temp]

        if "Casamento" in temp:
            lista_casamentos = temp.split("Casamento")
         # print(lista_casamentos)
        l_lista_temp = []
        for i in lista_casamentos:

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
            l_lista_temp.append(string)

        dict_casamentos = {}
        a = 1
        for l in l_lista_temp:

            if(l==''):
                continue

            conjuge, casamento_local, casamento_data =check_casamento(str(l))
            dict_temp = { "conjuge": conjuge, "local": casamento_local, "data": casamento_data}
            dict_casamentos[a] =  dict_temp

            a += 1

    else:
        dict_casamentos = {}
    # get heritage info
    if exists_filhos(soup):
        paragraph = soup.find("td", {"width": "100%"})
        temp = str(paragraph).split('<div class="marcadorP" style="margin-top: 10px;">Filhos')
        temp = temp [-1]
        filhos_list = []
        temp = re.findall('(href\=\"pessoas\.php\?id=)([0-9]+:?)',temp)
        for f in temp:
            temp2 = f[1]
            filhos_list.append(temp2)
        dic_filhos = {}
        a = 1
        for i in filhos_list:
            dic_filhos[a] = i
            a += 1
    else:
        dic_filhos = {}
    # output dictionary with all info

    index_dic = {
        "id" : link_id,
        "familia": familia,
        "nome": name,
        "datadenascimento": data_nasc,
        "localNascimento": local_nasc,
        "dataMorte": data_morte,
        "localMorte": local_morte,
        "pais":{
            "pai": parents_pai,
            "mae": parents_mae
        },
        "casamentos": dict_casamentos,
        "filhos": dic_filhos
    }

    return index_dic


def main():
    # read main webpage
    content = requests.get("http://pagfam.geneall.net/3418/").content
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
    #lista_pessoas = listarPessoas('http://pagfam.geneall.net/3418/pessoas.php?id=1076019')
    print("Parsing individuals...")
    output = []
    timer = 1
    for i in lista_pessoas:
        indvData = parsePage(i)
        output.append(indvData)
        print(str(i) + "  | " + str(timer) + "/" + str(len(lista_pessoas)))
        timer += 1
    print("Parsing completed")
    print("Creating File...")
    familias = {"familias" : output}
    with open('familias.json', 'w') as file:
        file.write(json.dumps(familias,ensure_ascii=False, indent = 4))
    file.close()


main()