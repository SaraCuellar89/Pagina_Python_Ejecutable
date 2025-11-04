from tkinter import *
from tkinter import messagebox

def Mostrar_Inicio( usuario_id):
    from inicio_sesion import Mostrar_Inicio_Sesion
    from menu import Mostrar_Menu
    from historial import Mostrar_Historial

    # =================================================================================
    #Funciones
    def ir_menu():
        raiz.destroy()
        Mostrar_Menu(usuario_id)

    def ir_historial():
        raiz.destroy()
        Mostrar_Historial(usuario_id)

    def cerrar_sesion():
        confirmar = messagebox.askokcancel("Confirmar", "¿Quiere salir de su cuenta?")

        if confirmar: 
            raiz.destroy()
            Mostrar_Inicio_Sesion()


    # =================================================================================
    #raiz
    raiz = Tk()
    raiz.title('Inicio')
    raiz.resizable(1,1) #(0,0) => no se puede modificar el tamaño de la ventana
    raiz.state('zoomed')


    # =================================================================================
    #Menu
    barra = Menu(raiz)
    raiz.config(menu=barra)
    archivo = Menu(barra, tearoff=0)
    archivo.add_command(label='Inicio')
    archivo.add_command(label='Menu', command=ir_menu)
    archivo.add_command(label='Historial', command=ir_historial)
    barra.add_cascade(label='Menu', menu=archivo)

    # =================================================================================
    #Titulo
    caja_titulo = Frame()
    caja_titulo.pack(pady=20)

    titulo = Label(caja_titulo, text='Bienvenido ', pady=10, font=('Times New Roman', 25)).pack()


    # =================================================================================
    #Pregunta
    caja_pregunta = Frame().pack()
    pregunta = Label(caja_pregunta, text='¿Que quieres hacer?', font=('Times New Roman', 15)).pack()

    # =================================================================================
    #Opciones
    caja_opciones = Frame().pack(pady=10)

    btn_menu = Button(caja_opciones, text='Ver menu', bg='black', fg='white', font=('Times New Roman', 15), width=15, command=ir_menu).pack(pady=10)

    btn_historial = Button(caja_opciones, text='Ver Historial', bg='black', fg='white', font=('Times New Roman', 15), width=15, command=ir_historial).pack(pady=10)

    btn_salir = Button(caja_opciones, text='Cerrar Sesion', bg='darkred', fg='white', font=('Times New Roman', 15), width=15, command=cerrar_sesion).pack(pady=10)
    


    # =================================================================================
    raiz.mainloop()