from tkinter import *
from database.pedido_dao import obtener_pedidos_por_usuario


def Mostrar_Historial(usuario_id):
    from menu import Mostrar_Menu
    from inicio import Mostrar_Inicio
    from productos_pedido import Mostrar_Productos_Pedido

    # =================================================================================
    #Funciones
    def ir_inicio():
        raiz.destroy()
        Mostrar_Inicio(usuario_id)
    
    def ir_menu():
        raiz.destroy()
        Mostrar_Menu(usuario_id)

    def ver_productos(id_pedido):
        raiz.destroy()
        Mostrar_Productos_Pedido(id_pedido,usuario_id)


    # =================================================================================
    #Raiz
    raiz = Tk()
    raiz.title('Inicio de Sesion')
    raiz.resizable(1,1) #(0,0) => no se puede modificar el tamaño de la ventana
    raiz.state('zoomed')


    # =================================================================================
    #Menu Desplegable
    barra = Menu(raiz)
    raiz.config(menu=barra)
    archivo = Menu(barra, tearoff=0)
    archivo.add_command(label='Inicio', command=ir_inicio)
    archivo.add_command(label='Menu', command=ir_menu)
    archivo.add_command(label='Historial')
    barra.add_cascade(label='Menu', menu=archivo)
    

    # =================================================================================
    #Titulo
    caja_titulo = Frame()
    caja_titulo.pack()

    titulo = Label(caja_titulo, text='Historial de pedidos', pady=10, font=('Times New Roman', 25)).pack()


    # =================================================================================
    #Tarjetas Historial

    caja_historial = Frame()
    caja_historial.pack()

    pedidos = obtener_pedidos_por_usuario(usuario_id)

    for i, pedido in enumerate(pedidos):
        id_pedido, codigo, estado, fecha = pedido  # desempacamos
        tarjeta = Frame(caja_historial, bg='black', padx=20, pady=10)
        tarjeta.pack(pady=10)

        Label(tarjeta, text=f'Pedido {codigo} ({estado}) - {fecha}', 
            pady=10, font=('Times New Roman', 15), bg='black', fg='white').pack()
    
        Button(tarjeta, text='Ver productos', pady=5, font=('Times New Roman', 15), 
            bg='grey', fg='white', command=lambda   c=id_pedido: ver_productos(c)).pack()




    # =================================================================================
    raiz.mainloop()