from tkinter import *
from database.pedido_dao import obtener_detalle_por_pedido

def Mostrar_Productos_Pedido(id_pedido, usuario_id):  # CAMBIADO: id_pedido en vez de codigo
    from historial import Mostrar_Historial

    # =================================================================================
    # Funciones
    def regresar():
        raiz.destroy()
        Mostrar_Historial(usuario_id)

    # =================================================================================
    # Raiz
    raiz = Tk()
    raiz.title('Detalle del Pedido')
    raiz.resizable(1,1)
    raiz.state('zoomed')


    # =================================================================================
    # Titulo
    caja_titulo = Frame()
    caja_titulo.pack()

    titulo = Label(caja_titulo, text=f'Detalle del Pedido #{id_pedido}', 
                   pady=10, font=('Times New Roman', 25)).pack()


    # =================================================================================
    # Productos
    caja_productos = Frame()
    caja_productos.pack(pady=20)

    # Obtener los detalles del pedido desde la base de datos
    detalles = obtener_detalle_por_pedido(id_pedido)

    if not detalles:
        Label(caja_productos, text='No hay productos en este pedido', 
              font=('Arial', 15), fg='red').pack()
    else:
        # Encabezado
        frame_encabezado = Frame(caja_productos)
        frame_encabezado.pack(pady=5)
        
        Label(frame_encabezado, text='Producto', font=('Arial', 15, 'bold'), 
              width=30, anchor='w').grid(row=0, column=0, padx=5)
        Label(frame_encabezado, text='Cantidad', font=('Arial', 15, 'bold'), 
              width=10).grid(row=0, column=1, padx=5)
        Label(frame_encabezado, text='Precio Unit.', font=('Arial', 15, 'bold'), 
              width=12).grid(row=0, column=2, padx=5)
        Label(frame_encabezado, text='Subtotal', font=('Arial', 15, 'bold'), 
              width=12).grid(row=0, column=3, padx=5)

        # Línea separadora
        Frame(caja_productos, height=2, bg='black').pack(fill='x', pady=5)

        # Lista de productos
        total_pedido = 0
        for nombre, cantidad, precio in detalles:
            subtotal = cantidad * precio
            total_pedido += subtotal
            
            frame_item = Frame(caja_productos)
            frame_item.pack(pady=2)
            
            Label(frame_item, text=nombre, font=('Arial', 13), 
                  width=30, anchor='w').grid(row=0, column=0, padx=5)
            Label(frame_item, text=str(cantidad), font=('Arial', 13), 
                  width=10).grid(row=0, column=1, padx=5)
            Label(frame_item, text=f'${precio:.2f}', font=('Arial', 13), 
                  width=12).grid(row=0, column=2, padx=5)
            Label(frame_item, text=f'${subtotal:.2f}', font=('Arial', 13), 
                  width=12).grid(row=0, column=3, padx=5)

        # Línea separadora
        Frame(caja_productos, height=2, bg='black').pack(fill='x', pady=10)

        # Total
        frame_total = Frame(caja_productos)
        frame_total.pack(pady=10)
        
        Label(frame_total, text='TOTAL:', font=('Arial', 18, 'bold')).pack(side='left', padx=10)
        Label(frame_total, text=f'${total_pedido:.2f}', font=('Arial', 18, 'bold'), 
              fg='green').pack(side='left')


    # =================================================================================
    # Regresar al menu
    Button(raiz, text='Regresar', bg='black', fg='white', 
           font=('Times New Roman', 15), width=15, command=regresar).pack(pady=20)

    # =================================================================================
    raiz.mainloop()