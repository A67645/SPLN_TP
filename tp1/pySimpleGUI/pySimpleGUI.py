#!/usr/bin/python3

from tkinter import *
import io
import os
from os import *
import pafy
import PySimpleGUI as sg
from PIL import Image
import vlc
from sys import platform as PLATFORM
from random import randint
import math

GRAPH_SIZE = (440, 440)
DATA_SIZE = (440, 440)

#
PLOTS_NUMBER = 30
RAND_MAX = 300

#For polygonal lines
LINE_BAR_WIDTH = 10
LINE_BAR_SPACING = 16
LINE_EDGE_OFFSET = 3

#bar graph
BAR_WIDTH = 50
BAR_SPACING = 75
EDGE_OFFSET = 3

#Sign graph
SIZE_X = GRAPH_SIZE[0]//2
SIZE_Y = GRAPH_SIZE[1]//2
NUMBER_MARKER_FREQUENCY = 25

#Animation
GRAPH_STEP_SIZE = 5
DELAY = 15  #Time interval

file_types = [("JPEG (*.jpeg)", "*.jpeg"),
              ("All files (*.*)", "*.*")]

def btn(name):  # a PySimpleGUI "User Defined Element" (see docs)
    return sg.Button(name, size=(6, 1), pad=(1, 1))

def draw_axis():
    """Draw auxiliary lines on the X and Y axes

Origin at the bottom left of the graph element(0,0)Is set as
Moving with the center of the graph area as the origin
    """

    graph.draw_line((0, SIZE_Y), (SIZE_X*2, SIZE_Y))  #origin
    graph.draw_line((SIZE_X, 0), (SIZE_X, SIZE_Y*2))

    for x in range(0, SIZE_X*2, NUMBER_MARKER_FREQUENCY):
        graph.draw_line((x, SIZE_Y-3), (x, SIZE_Y+3))  #Draw a scale
        if x != 0:
            graph.draw_text(str(x-SIZE_X), (x, SIZE_Y-10),
                            color='green')  #Draw the value of the scale

    for y in range(0, SIZE_Y*2+1, NUMBER_MARKER_FREQUENCY):
        graph.draw_line((SIZE_X-3, y), (SIZE_X+3, y))
        if y != 0:
            graph.draw_text(str(y-SIZE_Y), (SIZE_X-10, y), color='blue')

sg.theme('DarkBlue') # Definir cor da janela
# Definição do layout de um menu
layout_menu = [[sg.Text("O que consigo fazer")], # Título do menú
                [sg.Button("Input & Output Textual"), # Definir um botão da janela
                 sg.Button("Visualizador de Imagens")], # cada collection de botões é uma linha de botões
                [sg.Button("Calculadora"),
                 sg.Button("Graficos")],
                [sg.Button("EXIT")] # Operação de término de janela
              ]
# Definição do menú com nome da janela, tamanho da janela e o layout do mesmo
window_menu = sg.Window("Interface em PySimpleGUI", layout_menu, size = (600,400))

while True:
    # controlo de eventos permite mapear que botões são pressionados
    event_menu, values_menu = window_menu.read() # leitura de botões
    # Um "if case" para cada opção no menú, "sg.WIN_CLOSED" correspode a [X]
    # "event_menu" será uma string igual ao nome do botão escolhido
    if event_menu == "EXIT" or event_menu == sg.WIN_CLOSED:
        break
    # Definir o layout do menú de input e output de forma semelhante
    elif event_menu == "Input & Output Textual":
        layout_tio = [
                        [sg.Text("Qual é o seu primeiro nome?", font='Courier 12')],
                        [sg.Text("Nome:", font='Courier 12', background_color='green'), sg.InputText()], # caixa de texto
                        [sg.Text("Qual é o seu sobrenome?", font='Courier 12')],
                        [sg.Text("Sobrenome:", font='Courier 12', background_color='green'), sg.InputText()],
                        [sg.Button("Submit"), sg.Button("EXIT")]
                    ]

        window_tio = sg.Window("Search the information of a person", layout_tio)

        while True:
            # Valores inseridos nas caixas de texto armazenados na collection values_tio
            event_tio, values_tio = window_tio.read()
            if event_tio == "EXIT" or event_tio == sg.WIN_CLOSED:
                break
            elif event_tio == "Submit" and values_tio[0] != "":
                # Popup window com a resposta
                sg.popup('O seu nome é: ', values_tio[0] + " " + values_tio[1])
        window_tio.close() # término de janela

    elif event_menu == "Visualizador de Imagens":
        layout_gal = [[sg.Image(key="-IMAGE-")],
                      [
                        sg.Text("Ficheiro de Imagem"),
                        sg.Input(size=(25, 1), key="-FILE-"),
                        sg.FileBrowse(file_types=file_types),
                        sg.Button("Carregar Imagem"),
                      ],
                     ]

        window_gal = sg.Window("Visualizador de Imagens", layout_gal)

        while True:
            event, values = window_gal.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == "Carregar Imagem":
                filename = values["-FILE-"]
                if os.path.exists(filename):
                    image = Image.open(values["-FILE-"])
                    image.thumbnail((800, 800))
                    bio = io.BytesIO()
                    image.save(bio, format="PNG")
                    window_gal["-IMAGE-"].update(data=bio.getvalue())
        window_gal.close()

    elif event_menu == "Calculadora":
        # Layout                                                         # Creat GUI
        layout = [[sg.Txt(''  * 10)],
            [sg.Text('', size=(15, 1), font=('Helvetica', 18), text_color='red', key='input')],
            [sg.Txt(''  * 10)],
            [sg.ReadFormButton('('), sg.ReadFormButton(')'), sg.ReadFormButton('c'), sg.ReadFormButton('«')],
            [sg.ReadFormButton('7'), sg.ReadFormButton('8'), sg.ReadFormButton('9'), sg.ReadFormButton('÷')],
            [sg.ReadFormButton('4'), sg.ReadFormButton('5'), sg.ReadFormButton('6'), sg.ReadFormButton('x')],
            [sg.ReadFormButton('1'), sg.ReadFormButton('2'), sg.ReadFormButton('3'), sg.ReadFormButton('-')],
            [sg.ReadFormButton('.'), sg.ReadFormButton('0'), sg.ReadFormButton('='), sg.ReadFormButton('+')],
            ]

        # Set PySimpleGUI
        form = sg.FlexForm('13411_CALCULATOR', default_button_element_size=(5, 2), auto_size_buttons=False, grab_anywhere=False)
        form.Layout(layout)

        # Set Process
        Equal = ''
        List_Op_Error =  ['+','-','*','/','(']

        # Loop
        while True:
            button, value = form.Read()                            # call GUI

            # Press Button
            if button == 'c':
                Equal = ''
                form.FindElement('input').Update(Equal)
            elif button == '«':
                Equal = Equal[:-1]
                form.FindElement('input').Update(Equal)
            elif len(Equal) == 16 :
                pass
            elif str(button) in '1234567890+-().':
                Equal += str(button)
                form.FindElement('input').Update(Equal)
            elif button == 'x':
                Equal += '*'
                form.FindElement('input').Update(Equal)
            elif button == '÷':
                Equal += '/'
                form.FindElement('input').Update(Equal)

                # Process Conditional
            elif button == '=':
                # Error Case
                for i in List_Op_Error :
                    if '*' == Equal[0] or '/' == Equal[0] or ')' == Equal[0]  or i == Equal[-1]:   # Check Error Case
                        Answer = "Error Operation"
                        break
                    elif Equal == '6001012630187':
                        Answer = 'Apisit.Khomcharoen'
                        break
                    elif '/0' in Equal or '*/' in Equal or '/*' in Equal :
                        Answer = "Error Operation"
                        break
                    elif '(' in Equal :
                        if ')' not in Equal :
                            Answer = "Error Operation"
                            break
                    elif '(' not in Equal:
                        if ')' in Equal:
                            Answer = "Error Operation"
                            break

                # Calculate Case
                else :
                    Answer = str("%0.2f" %(eval(Equal)))                         # eval(Equal)
                    if '.0' in Answer:
                        Answer = str(int(float(Answer)))                         # convert float to int
                form.FindElement('input').Update(Answer)                         # Update to GUI
                Equal = Answer

            elif button == 'Quit'  or button == None:                            # QUIT Program
                break
    elif event_menu == "Graficos":
        #Layout
        #Setting the drawing area of the graph
        graph = sg.Graph(GRAPH_SIZE, (0, 0), DATA_SIZE, key='-GRAPH-', background_color='white',)

        layout = [[sg.Text('Exemplo de Grafico')],
                  [graph],
                  [sg.Button('LINE'), sg.Button('chart'), sg.Button('Both'), sg.Button('pie chart'), sg.Button('Sine wave'),sg.Button('animation') ]]

        window = sg.Window('Exemplo de Graficos', layout)

        before_value = 0  #Initialize line graph
        delay = x = lastx = lasty = 0  #Animation initialization

        is_animated = False

        while True:

            if is_animated:
                #Regularly'__TIMEOUT__'Event is issued
                event, values = window.Read(timeout=DELAY)
            else:
                event, values = window.Read()

            if event is None:
                break

            if event == 'LINE':
                is_animated = False
                #Show labeled line chart
                graph.Erase()  #Graph display Delete both machines

                for i in range(PLOTS_NUMBER):
                    graph_value = randint(0, 400)
                    if i > 0:
                        graph.DrawLine(((i-1) * LINE_BAR_SPACING + LINE_EDGE_OFFSET + LINE_BAR_WIDTH/2,  before_value),
                                       (i * LINE_BAR_SPACING + LINE_EDGE_OFFSET + LINE_BAR_WIDTH/2, graph_value), color='green', width=1)

                    #Display line label (y value)
                    graph.DrawText(text=graph_value, location=(
                                   i * LINE_BAR_SPACING+EDGE_OFFSET+2, graph_value+10))

                    graph.DrawPoint((i * LINE_BAR_SPACING + LINE_EDGE_OFFSET +
                             LINE_BAR_WIDTH/2, graph_value), size=3, color='green',)

                    before_value = graph_value

            if event == 'chart':
                is_animated = False

                #Delete bar chart
                graph.Erase()
                for i in range(PLOTS_NUMBER):
                    graph_value = randint(0, 400)
                    graph.DrawRectangle(top_left=(i * BAR_SPACING + EDGE_OFFSET, graph_value),
                                        bottom_right=(i * BAR_SPACING + EDGE_OFFSET + BAR_WIDTH, 0), fill_color='blue')
                    graph.DrawText(text=graph_value, location=(
                                   i*BAR_SPACING+EDGE_OFFSET+25, graph_value+10))

            if event == 'Both':
                is_animated = False

            #Show both line and bar charts
                graph.Erase()
                for i in range(PLOTS_NUMBER):
                    graph_value = randint(0, 400)
                    graph.DrawRectangle(top_left=(i * BAR_SPACING + EDGE_OFFSET, graph_value),
                                        bottom_right=(i * BAR_SPACING + EDGE_OFFSET + BAR_WIDTH, 0), fill_color='blue')
                    graph.DrawText(text=graph_value, location=(
                                   i*BAR_SPACING+EDGE_OFFSET+25, graph_value+10))

                    if i > 0:
                        graph.DrawLine(((i-1) * LINE_BAR_SPACING + LINE_EDGE_OFFSET + LINE_BAR_WIDTH/2,  before_value),
                                       (i * LINE_BAR_SPACING + LINE_EDGE_OFFSET + LINE_BAR_WIDTH/2, graph_value), color='green', width=1)

                    graph.DrawText(text=graph_value, location=(
                                   i * LINE_BAR_SPACING+EDGE_OFFSET+2, graph_value+10))

                    graph.DrawPoint((i * LINE_BAR_SPACING + LINE_EDGE_OFFSET +
                                    LINE_BAR_WIDTH/2, graph_value), size=3, color='green',)
                    before_value = graph_value

            if event == 'pie chart':
                is_animated = False
                graph.erase()

                # create_arc()Can't be filled because there is no fill
                graph.DrawArc( (50,50), (DATA_SIZE[0]-50, DATA_SIZE[1]-50), extent=-200, start_angle=90)
                graph.DrawArc( (50,50), (DATA_SIZE[0]-50, DATA_SIZE[1]-50), extent=-400, start_angle=-110 ,arc_color="yellow")
                graph.DrawArc( (50,50), (DATA_SIZE[0]-50, DATA_SIZE[1]-50), extent=-50,  start_angle=-510 , arc_color="blue")
                graph.DrawArc( (50,50), (DATA_SIZE[0]-50, DATA_SIZE[1]-50), extent=-50,  start_angle=-560 , arc_color="red")
                graph.DrawArc( (50,50), (DATA_SIZE[0]-50, DATA_SIZE[1]-50), extent=-20,  start_angle=-610 , arc_color="green")

            if event == 'Sine wave':
                is_animated = False
                graph.erase()

                draw_axis()
                prev_x = prev_y = None
                for x in range(0, SIZE_X*2):
                    y = math.sin(x/75)*100 + SIZE_Y
                    if prev_x is not None:
                        graph.draw_line((prev_x, prev_y), (x, y), color='red')
                    prev_x, prev_y = x, y

            if event == 'animation' or is_animated:

                if not is_animated:
                    graph.Erase()  #Delete the graph once

                is_animated = True

                #Display a graph that moves in chronological order
                step_size, delay = GRAPH_STEP_SIZE, DELAY
                y = randint(0, GRAPH_SIZE[1])
                if x < GRAPH_SIZE[0]:  #First time
                    # window['-GRAPH-'].DrawLine((lastx, lasty), (x, y), width=1)
                    graph.DrawLine((lastx, lasty), (x, y), width=1)
                else:
                    # window['-GRAPH-'].Move(-step_size, 0)  #Shift the entire graph to the left
                    # window['-GRAPH-'].DrawLine((lastx, lasty), (x, y), width=1)
                    graph.Move(-step_size, 0)  #Shift the entire graph to the left
                    graph.DrawLine((lastx, lasty), (x, y), width=1)
                    x -= step_size
                    lastx, lasty = x, y
                lastx, lasty = x, y
                x += step_size

        window.Close()


window_menu.close()
