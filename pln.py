import tkinter.messagebox



# Funcon que comprueba que la categoria que se le pasa es valida para poder entrenar con ella
def comprobarCategoria(rutaCategoria, indexOpcion, rutasCategorias):

    txt_otherpath = False

    if indexOpcion not in rutasCategorias:

        for indice in rutasCategorias.values():

            if rutaCategoria in indice:
                txt_otherpath = True
                tkinter.messagebox.showerror("Error", "La carpeta seleccionada ya está asociada a otra categoría.")

        if txt_otherpath == False:
            rutasCategorias[indexOpcion] = []
            rutasCategorias[indexOpcion].append(rutaCategoria)
            tkinter.messagebox.showinfo("Información", "Se ha añadido la ruta correctamente.")


    else:
        for indice in rutasCategorias.values():
            if rutaCategoria in indice:
                txt_otherpath = True
                tkinter.messagebox.showerror("Error", "La carpeta seleccionada ya tiene esta ruta asociada.")

        if txt_otherpath == False:
            rutasCategorias[indexOpcion] = []
            rutasCategorias[indexOpcion].append(rutaCategoria)
            tkinter.messagebox.showinfo("Información", "Se ha modificado la ruta correctamente.")



    return rutasCategorias











