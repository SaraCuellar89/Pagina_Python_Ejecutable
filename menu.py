from tkinter import *
from tkinter import messagebox
from database.producto_dao import obtener_productos
import sys
import os
from PIL import Image, ImageTk


# 🔥 Función para obtener la ruta real (funciona en .py y .exe)
def ruta_recurso(ruta_relativa):
    """Devuelve la ruta correcta del archivo, tanto en .py como en .exe."""
    if hasattr(sys, '_MEIPASS'):
        # Si estamos en un .exe (PyInstaller)
        return os.path.join(sys._MEIPASS, ruta_relativa)
    else:
        # Si estamos ejecutando el script normal
        return os.path.join(os.path.abspath("."), ruta_relativa)


def Mostrar_Menu(usuario_id):
    from inicio import Mostrar_Inicio
    from producto import Mostrar_Producto
    from historial import Mostrar_Historial
    from comprar import Mostrar_Comprar

    # =================================================================================
    #Funciones
    def ir_inicio():
        raiz.destroy()
        Mostrar_Inicio(usuario_id)
    
    def ir_historial():
        raiz.destroy()
        Mostrar_Historial(usuario_id)

    def ver_producto(nombre):
        raiz.destroy()
        Mostrar_Producto(nombre, usuario_id)

    def ir_comprar():
        raiz.destroy()
        Mostrar_Comprar(usuario_id)

    # =================================================================================
    #raiz
    raiz = Tk()
    raiz.title('Menu')
    raiz.resizable(1,1)
    raiz.state('zoomed')

    raiz.grid_rowconfigure(0, weight=1)
    raiz.grid_rowconfigure(2, weight=1)
    raiz.grid_columnconfigure(0, weight=1)
    raiz.grid_columnconfigure(2, weight=1)


    # =================================================================================
    #Menu Desplegable
    barra = Menu(raiz)
    raiz.config(menu=barra)
    archivo = Menu(barra, tearoff=0)
    archivo.add_command(label='Inicio', command=ir_inicio)
    archivo.add_command(label='Menu')
    archivo.add_command(label='Historial', command=ir_historial)
    barra.add_cascade(label='Menu', menu=archivo)


    # =================================================================================
    #Caja Titulo
    caja_titulo = Frame()
    caja_titulo.grid(row=1, column=1)

    titulo = Label(caja_titulo, text='Menu', pady=10, font=('Times New Roman', 25)).grid()


    # =================================================================================
    #Menu
    caja_menu = Frame(raiz)
    caja_menu.grid(row=2, column=1)
    
    # Obtener productos desde la base de datos
    productos = obtener_productos()  # [(nombre, precio, imagen), ...]

    if not productos:
        Label(caja_menu, text="No hay productos disponibles", 
              font=("Arial", 15), fg="red").grid()
    else:
        columnas = 3
        imagenes = []  # Lista para mantener referencias a las imágenes

        for i, producto in enumerate(productos):
            nombre, precio, imagen_path = producto
            
            fila = i // columnas
            col = i % columnas
        
            tarjeta = Frame(caja_menu, bg='black', padx=10, pady=10)
            tarjeta.grid(row=fila, column=col, padx=20, pady=10)

            try:
                # 🔥 Obtiene la ruta del recurso correctamente
                ruta_img = ruta_recurso(imagen_path)

                # Si la ruta no existe, intenta buscar dentro de la carpeta 'img'
                if not os.path.exists(ruta_img):
                    ruta_img = ruta_recurso(os.path.join("img", os.path.basename(imagen_path)))

                print("Intentando cargar:", ruta_img)  # 🧠 útil para debug

                # Cargar imagen con PIL
                img = Image.open(ruta_img)
                img = img.resize((200, 200))
                foto = ImageTk.PhotoImage(img)
                imagenes.append(foto)

                Label(tarjeta, text=nombre, font=('Times New Roman', 20),
                    bg='black', fg='white').grid(row=0, pady=5)
                Label(tarjeta, image=foto, bg='black').grid(row=1, pady=5)
                Button(tarjeta, text='Ver', bg='black', fg='white',
                    font=('Times New Roman', 15), width=15,
                    command=lambda n=nombre: ver_producto(n)).grid(row=2, pady=5)

            except Exception as e:
                print(f"❌ Error al cargar imagen {imagen_path}: {e}")
                Label(tarjeta, text=nombre, font=('Times New Roman', 20),
                    bg='black', fg='white').grid(row=0, pady=5)
                Label(tarjeta, text="[Sin imagen]", font=("Arial", 12),
                    width=20, height=10, bg="gray", fg="white").grid(row=1, pady=5)
                Button(tarjeta, text='Ver', bg='black', fg='white',
                    font=('Times New Roman', 15), width=15,
                    command=lambda n=nombre: ver_producto(n)).grid(row=2, pady=5)
        
        # Guardar referencias de imágenes
        caja_menu.imagenes = imagenes
    
    # =================================================================================
    #Boton de ir a comprar
    Button(raiz, text='Mirar carrito', bg='black', fg='white', 
           font=('Times New Roman', 15), width=15, 
           command=ir_comprar).grid(row=3, column=1, pady=20)


    # =================================================================================
    raiz.mainloop()
