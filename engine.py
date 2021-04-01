"""
[
{
   "familia":"Macieira",
   "nome":"Jose",
   "datadenascimento": "31/07/1784",
   "pais":{
      "pai":"Jose",
      "mae":"Maria",
    },
   "casamentos":{
      "casamento1":{
          "local": "Quinta da Beira",
          "data": "31/07/1794",
          "conjuge": "Maria Eduarda"
        }
    },
   "filhos":{
       "1":"filho1",
       "2":"filho2"
   }
},

{
   "familia":"Pereira",
   "nome":"Manel",
   "datadenascimento": "31/07/1984",
   "pais":{
      "pai":"Erasmo Carlos",
      "mae":"Constança",
    },
   "casamentos":{
      "casamento1":{
          "local": "Quinta de Longe",
          "data": "31/07/2000",
          "conjuge": "Antonieta Soares"
        }
    },
   "filhos":{
       "1":"Joaquim Maria",
       "2":"Maria Joaquina"
   }
}
]
"""

#!/usr/bin/python3

from jjcli import *
import yaml, sys, json

def load():
    with open('pessoas.json') as json_string:
        pessoas = json.load(json_string)
    return pessoas

def pessoa(nome_pessoa, dict_pessoas):
    pessoas = dict_pessoas["familias"]
    nome = nome_pessoa.split(' ')[0]
    sobrenome =  nome_pessoa.split(' ')[1]
    for dict_pessoa in pessoas:
        if((dict_pessoa["familia"]==sobrenome)and(dict_pessoa["nome"]==nome)):
            pessoa = dict_pessoa
            break
    print(pessoa)

def familia(nome_familia, dict_pessoas):
    pessoas = dict_pessoas["familias"]
    familia = []
    for pessoa in pessoas:
        if(pessoa["familia"] == nome_familia):
            familia.append(pessoa["nome"])
    print(familia)

def casamentos(nome_pessoa, dict_pessoas):
    pessoas = dict_pessoas["familias"]
    nome = nome_pessoa.split(' ')[0]
    sobrenome =  nome_pessoa.split(' ')[1]
    casamentos = []
    for dict_pessoa in pessoas:
        if((dict_pessoa["familia"]==sobrenome)and(dict_pessoa["nome"]==nome)):
            casamentos.append(dict_pessoa["casamentos"])
    print(casamentos)

def filhos(nome_pessoa, dict_pessoas):
    pessoas = dict_pessoas["familias"]
    nome = nome_pessoa.split(' ')[0]
    sobrenome =  nome_pessoa.split(' ')[1]
    for dict_pessoa in pessoas:
        if((dict_pessoa["familia"]==sobrenome)and(dict_pessoa["nome"]==nome)):
            print(dict_pessoa["filhos"])

def pais(nome_pessoa, dict_pessoas):
    pessoas = dict_pessoas["familias"]
    nome = nome_pessoa.split(' ')[0]
    sobrenome =  nome_pessoa.split(' ')[1]
    for dict_pessoa in pessoas:
        if((dict_pessoa["familia"]==sobrenome)and(dict_pessoa["nome"]==nome)):
            print(dict_pessoa["pais"])

def nascimento(nome_pessoa, dict_pessoas):
    pessoas = dict_pessoas["familias"]
    nome = nome_pessoa.split(' ')[0]
    sobrenome =  nome_pessoa.split(' ')[1]
    for dict_pessoa in pessoas:
        if((dict_pessoa["familia"]==sobrenome)and(dict_pessoa["nome"]==nome)):
            print(dict_pessoa["datadenascimento"])

def main():
    dict_pessoas = load()
    print("Info do Jose Macieira")
    print(pessoa("Jose Macieira", dict_pessoas))
    print("\nInfo da familia Macieira")
    print(familia("Macieira", dict_pessoas))
    print("\nInfo dos casamentos do Jose Macieira")
    print(casamentos("Jose Macieira", dict_pessoas))
    print("\nFilhos do Jose Macieira")
    print(filhos("Jose Macieira", dict_pessoas))
    print("\nPais do Jose Macieira")
    print(pais("Jose Macieira", dict_pessoas))
    print("\nData de nascimento do Jose Macieira")
    print(nascimento("Jose Macieira", dict_pessoas))

main()
