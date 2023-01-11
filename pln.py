import tkinter.messagebox
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import *



opciones = ["Arroz y pasta", "Bebida", "Carne", "Dulce", "Pescado", "Variado", "Vegetal"]



# Para cada categoria que pulse se necesita pedirle al usuario que seleccione una carpeta


def comprobarCategoria(rutaCategoria, indexOpcion, rutasCategorias):

    txt_otherpath = False


    if indexOpcion not in rutasCategorias:

        for indice in rutasCategorias.values():
            if rutaCategoria in indice:
                txt_otherpath = True
                tkinter.messagebox.showerror("Error", "La carpeta seleccionada ya está asociada a otra categoría.")
                print("La categoria no existe pero la ruta si")
        if txt_otherpath == False:
            rutasCategorias[indexOpcion] = []
            rutasCategorias[indexOpcion].append(rutaCategoria)
            tkinter.messagebox.showinfo("Información", "Se ha añadido la ruta correctamente.")
            print("La categoria no existe y la ruta tampoco")

    else:
        for indice in rutasCategorias.values():
            if rutaCategoria in indice:
                txt_otherpath = True
                tkinter.messagebox.showerror("Error", "La carpeta seleccionada ya tiene esta ruta asociada.")
                print("La categoria existe y la ruta tmb")
        if txt_otherpath == False:
            rutasCategorias[indexOpcion] = []
            rutasCategorias[indexOpcion].append(rutaCategoria)
            tkinter.messagebox.showinfo("Información", "Se ha modificado la ruta correctamente.")
            print("La categoria existe pero la ruta no")

    return rutasCategorias











