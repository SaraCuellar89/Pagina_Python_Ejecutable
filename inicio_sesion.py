from tkinter import *
from tkinter import messagebox
from database.usuario_dao import verificar_usuario 

def Mostrar_Inicio_Sesion():
    from registro import Mostrar_Registro
    from inicio import Mostrar_Inicio

    # =================================================================================
    #Funciones
    def ir_registro():
        raiz.destroy()
        Mostrar_Registro()

    def entrar():
        correo = inp_correo.get()
        contrasena = inp_contrasena.get()

        if not correo or not contrasena:
            messagebox.showwarning("alerta", "Todos los campos son obligatorios")
        else:
            usuario = verificar_usuario(correo, contrasena)
            if usuario:
                usuario_id = usuario[0]
                messagebox.showinfo("Bienvenido", f"¡Hola {usuario[1]}!")  
                raiz.destroy()
                Mostrar_Inicio(usuario_id)
            else:
                messagebox.showerror("Error", "Correo o contraseña incorrectos")



    # =================================================================================
    #Raiz
    raiz = Tk()
    raiz.title('Inicio de Sesion')
    raiz.resizable(1,1) #(0,0) => no se puede modificar el tamaño de la ventana
    raiz.state('zoomed')


    # =================================================================================
    #Titulo
    caja_titulo = Frame()
    caja_titulo.pack()

    titulo = Label(caja_titulo, text='Inicio de Sesion', pady=10, font=('Times New Roman', 20)).pack()


    # =================================================================================
    #Formulario
    formu = Frame()
    formu.pack(pady=20)

    #correo
    label_correo = Label(formu, text='Correo', font=('Times New Roman', 15)).pack()
    inp_correo = Entry(formu, font=('Times New Roman', 15))
    inp_correo.pack()

    #contraseña
    label_contrasena = Label(formu, text='Contraseña', font=('Times New Roman', 15)).pack()
    inp_contrasena = Entry(formu, font=('Times New Roman', 15), show="*")
    inp_contrasena.pack()

    #Botones
    entrar = Button(formu, text='Entrar', bg='black', fg='white', font=('Times New Roman', 15), command=entrar).pack(pady=20)

    pregunta = Button(formu, text='¿No tienes cuenta? Registrate', font=('Times New Roman', 10), pady=10, fg='darkblue', border=0, command=ir_registro).pack()


    # =================================================================================
    raiz.mainloop()
