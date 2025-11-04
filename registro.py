from tkinter import *
from tkinter import messagebox
from database.usuario_dao import registrar_usuario 

def Mostrar_Registro():
    from inicio_sesion import Mostrar_Inicio_Sesion

    # =================================================================================
    #Funciones
    def ir_inicio_sesion():
        raiz.destroy()
        Mostrar_Inicio_Sesion()

    def registrar():
        nombre = inp_nombre.get()
        correo = inp_correo.get()
        contrasena = inp_contrasena.get()
        telefono = inp_telefono.get()
        direccion = inp_direccion.get()


        #Validaciones
        if not nombre or not correo or not contrasena:
            messagebox.showwarning("alerta", "Todos los campos son obligatorios")
        elif '@' not in correo or '.' not in correo:
            messagebox.showwarning("alerta", "Correo invalido")
        elif len(contrasena) < 3:
            messagebox.showwarning("alerta", "La cotraseña debe ser igual o mayor a 3 caracteres")
        else:
            exito = registrar_usuario(nombre, correo, contrasena, telefono, direccion)
            if exito:
                messagebox.showinfo("¡Proceso Exitoso!", "Registro Finalizado con Exito")
                raiz.destroy()
                Mostrar_Inicio_Sesion()
            else:
                messagebox.showerror("Error", "El correo ya está registrado o ocurrió un error")


    # =================================================================================
    #raiz
    raiz = Tk()
    raiz.title('Registro')
    raiz.resizable(1,1) #(0,0) => no se puede modificar el tamaño de la ventana
    raiz.state('zoomed')


    # =================================================================================
    #Titulo
    caja_titulo = Frame()
    caja_titulo.pack()

    titulo = Label(caja_titulo, text='Registro', pady=10, font=('Times New Roman', 20)).pack()


    # =================================================================================
    #Formulario
    formu = Frame()
    formu.pack(pady=20)

    #nombre
    label_nombre = Label(formu, text='Nombre', font=('Times New Roman', 15)).pack()
    inp_nombre = Entry(formu, font=('Times New Roman', 15))
    inp_nombre.pack()

    #correo
    label_correo = Label(formu, text='Correo', font=('Times New Roman', 15)).pack()
    inp_correo = Entry(formu, font=('Times New Roman', 15))
    inp_correo.pack()


    #telefono
    label_telefono= Label(formu, text='Telefono', font=('Times New Roman', 15)).pack()
    inp_telefono = Entry(formu, font=('Times New Roman', 15))
    inp_telefono.pack()
    
    #direccion
    label_direccion = Label(formu, text='Dirección', font=('Times New Roman', 15)).pack()
    inp_direccion = Entry(formu, font=('Times New Roman', 15))
    inp_direccion.pack()

    #contraseña
    label_contrasena = Label(formu, text='Contraseña', font=('Times New Roman', 15)).pack()
    inp_contrasena = Entry(formu, font=('Times New Roman', 15), show="*")
    inp_contrasena.pack()

    #Botones
    registrar = Button(formu, text='Registrarse', bg='black', fg='white', font=('Times New Roman', 15), command=registrar).pack(pady=20)

    pregunta = Button(formu, text='¿Ya tienes cuenta? Inicia Sesion', font=('Times New Roman', 10), pady=10, fg='darkblue', border=0, command=ir_inicio_sesion).pack()


    # =================================================================================
    raiz.mainloop()