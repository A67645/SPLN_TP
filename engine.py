"""
{

familias : [
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
}
"""

#!/usr/bin/python3

from jjcli import *
from tkinter import *
import yaml, sys, json
import PySimpleGUI as sg

def load():
    with open('familias.json') as json_string:
        pessoas = json.load(json_string)
    return pessoas

def pessoa(nome, dict_pessoas):
    pessoas = dict_pessoas["familias"]
    result = ""
    for dict_pessoa in pessoas:
        if((dict_pessoa["nome"]==nome)):
            pessoa = dict_pessoa
            for key in pessoa:
                result += key + ": " + str(pessoa[key]) + "\n"
            return result
            break

def familia(nome_familia, dict_pessoas):
    pessoas = dict_pessoas["familias"]
    familia = []
    result = ""
    for pessoa in pessoas:
        if(pessoa["familia"] == nome_familia):
            familia.append(pessoa["nome"])
    i = 1
    for membro in familia:
        result += str(i) + "º membro: " + membro + "\n"
    return result

def casamentos(nome, dict_pessoas):
    pessoas = dict_pessoas["familias"]
    casamentos = {}
    result = ""
    for dict_pessoa in pessoas:
        if((dict_pessoa["nome"]==nome)):
            casamentos = dict_pessoa["casamentos"]
    for key in casamentos:
        result += key + ": " + str(casamentos[key]) + "\n"
    return result

def filhos(nome_pessoa, dict_pessoas):
    pessoas = dict_pessoas["familias"]
    filhos = {}
    result = ""
    for dict_pessoa in pessoas:
        if((dict_pessoa["nome"]==nome)):
            filhos = dict_pessoa["filhos"]
    for key in filhos:
        result += key + ": " + str(filhos[key]) + "\n"
    return result

def pais(nome, dict_pessoas):
    pessoas = dict_pessoas["familias"]
    pais = {}
    result = ""
    for dict_pessoa in pessoas:
        if((dict_pessoa["nome"]==nome)):
            pais = dict_pessoa["pais"]
    for key in pais:
        result += key + ": " + str(pais[key]) + "\n"
    return result


def nascimento(nome, dict_pessoas):
    pessoas = dict_pessoas["familias"]
    nascimento = []
    for dict_pessoa in pessoas:
        if((dict_pessoa["nome"]==nome)):
            nascimento.append(dict_pessoa["datadenascimento"])
    return nascimento

def main():

    dict_pessoas = load()

    sg.theme('LightBlue2')
    layout_menu = [[sg.Text("Search Engine for geneallogical tree")],
                    [sg.Button("Search the information of a person"), 
                    sg.Button("Search the members of a family")],
                    [sg.Button("Search the weddings of a person"),
                    sg.Button("Search the descendants of a person")],
                    [sg.Button("Search the progenitors of a person"),
                    sg.Button("Search the birthday of a person")],
                    [sg.Button("EXIT")]
            ]
    window_menu = sg.Window("Search Engine", layout_menu, size = (600,400))

    while True:
        event_menu, values_menu = window_menu.read()
        if event_menu == "EXIT" or event_menu == sg.WIN_CLOSED:
            break
        elif event_menu == "Search the information of a person":
            layout_q1 = [
                            [sg.Text("Enter the name and surname")],
                            [sg.Text("Name:"), sg.InputText()],
                            [sg.Button("Submit"), sg.Button("EXIT")]
                        ]

            window_q1 = sg.Window("Search the information of a person", layout_q1)

            while True:
                event_q1, values_q1 = window_q1.read()
                if event_q1 == "EXIT" or event_q1 == sg.WIN_CLOSED:
                    break
                elif event_q1 == "Submit" and values_q1[0] != "":
                    sg.popup('Information of target person', pessoa(values_q1[0], dict_pessoas))
            window_q1.close()

        elif event_menu == "Search the members of a family":
            layout_q2 = [
                            [sg.Text("Enter the surname of the family")],
                            [sg.Text("Surname"), sg.InputText()],
                            [sg.Button("Submit"), sg.Button("EXIT")]
                        ]

            window_q2 = sg.Window("Search the members of a family", layout_q2)

            while True:
                event_q2, values_q2 = window_q2.read()
                if event_q2 == "EXIT" or event_q2 == sg.WIN_CLOSED:
                    break
                elif event_q2 == "Submit" and values_q2[0] != "":
                    sg.popup('Information of target family', familia(values_q2[0], dict_pessoas))
            window_q2.close()

        elif event_menu == "Search the weddings of a person":
            layout_q3 = [
                            [sg.Text("Enter the name and surname")],
                            [sg.Text("Name:"), sg.InputText()],
                            [sg.Button("Submit"), sg.Button("EXIT")]
                        ]

            window_q3 = sg.Window("Search the weddings of a person", layout_q3)

            while True:
                event_q3, values_q3 = window_q3.read()
                if event_q3 == "EXIT" or event_q3 == sg.WIN_CLOSED:
                    break
                elif event_q3 == "Submit" and values_q3[0] != "":
                    sg.popup('Weddings of target person', casamentos(values_q3[0], dict_pessoas))
            window_q3.close()

        elif event_menu == "Search the descendants of a person":
            layout_q4 = [
                            [sg.Text("Enter the name and surname")],
                            [sg.Text("Name:"), sg.InputText()],
                            [sg.Button("Submit"), sg.Button("EXIT")]
                        ]

            window_q4 = sg.Window("Search the descendants of a person", layout_q4)

            while True:
                event_q4, values_q4 = window_q4.read()
                if event_q4 == "EXIT" or event_q4 == sg.WIN_CLOSED:
                    break
                elif event_q4 == "Submit" and values_q4[0] != "":
                    sg.popup('Descendants of target person', filhos(values_q4[0], dict_pessoas))
            window_q4.close()

        elif event_menu == "Search the progenitors of a person":
            layout_q5 = [
                            [sg.Text("Enter the name and surname")],
                            [sg.Text("Name:"), sg.InputText()],
                            [sg.Button("Submit"), sg.Button("EXIT")]
                        ]

            window_q5 = sg.Window("Search the progenitors of a person", layout_q5)

            while True:
                event_q5, values_q5 = window_q5.read()
                if event_q5 == "EXIT" or event_q5 == sg.WIN_CLOSED:
                    break
                elif event_q5 == "Submit" and values_q5[0] != "":
                    sg.popup('Progenitors of target person', pais(values_q5[0], dict_pessoas))
            window_q5.close()

        elif event_menu == "Search the birthday of a person":
            layout_q6 = [
                            [sg.Text("Enter the name and surname")],
                            [sg.Text("Name:"), sg.InputText()],
                            [sg.Button("Submit"), sg.Button("EXIT")]
                        ]

            window_q6 = sg.Window("Search the birthday of a person", layout_q6)

            while True:
                event_q6, values_q6 = window_q6.read()
                if event_q6 == "EXIT" or event_q6 == sg.WIN_CLOSED:
                    break
                elif event_q6 == "Submit" and values_q6[0] != "":
                    sg.popup('Birthday of target person', nascimento(values_q6[0], dict_pessoas))
            window_q6.close()

    window_menu.close()

main()
