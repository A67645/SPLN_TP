from tkinter import *
from tkinter import ttk

def calculate(*args):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass
# setup da main window
root = Tk()
root.title("Conversor de 'Feets' para Metros")

# setup da main frame que vai ter o conteudo da interface do utilizador
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1) # serve para, ao darmos resize à janela, a janela acompanhar o alterração do tamanho
root.rowconfigure(0, weight=1)


# criar o widget que recebe o valor a converter 
feet = StringVar() #ininiar o widget
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet) # criar entry
feet_entry.grid(column=2, row=1, sticky=(W, E)) # especificar onde fica a entry na grid


# criar resto dos widgets
meters = StringVar()
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E)) # display do numero de metros

ttk.Button(mainframe, text="Calcular", command=calculate).grid(column=3, row=3, sticky=W) # botao que calcula o nr de metros

ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W) # labels para mostrar como funciona a aplicação
ttk.Label(mainframe, text="equivale a").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="metros").grid(column=3, row=2, sticky=W)

#toques extra

for child in mainframe.winfo_children(): # ciclo que, para cada widget, adiciona padding para ficarem mais legiveis
    child.grid_configure(padx=5, pady=5) 

feet_entry.focus()  # diz ao Tk para por o focus no widget de introdução do nr de feets
root.bind("<Return>", calculate) # bind do "Return" ao comando calculate, para poder utilizar sem clickar no botão

root.mainloop()
