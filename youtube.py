from tkinter import *
import os
from pytube import YouTube

# Funcion que descarga el video en el directorio en el que te encuentres
def download():
    # Recoge el link y lo localiza en Youtube
    url = YouTube(str(link.get()))
    # Obtiene el video con la mejor resolucion
    video = url.streams.get_highest_resolution()
    # Obtiene el path en el que te encuentras
    cwd = os.getcwd()
    # Descarga el video
    video.download(cwd)
    # Una vez se ha completado la descarga despliega un mensaje de "descargado"
    Label(root, text="Downloaded", font="arial 15").place(x=100, y=120)



root = Tk()
root.geometry("500x300")
# Hace que la ventana se pueda ajustar
root.resizable(0, 0)
root.title('youtube downloader')

Label(root, text="Download Youtube videos for free", font='san-serif 14 bold').pack()
link = StringVar() # Specifying the variable type
Label(root, text="Paste your link here", font='san-serif 15 bold').place(x=150, y=55)
link_enter = Entry(root, width=70, textvariable=link).place(x=30, y=85)
# Cuando se pulsa sobre el boton la funcion download se ejecuta
Button(root, text='Download', font='san-serif 16 bold', bg='red', padx=2,command=download).place(x=175, y=150)

root.mainloop()









