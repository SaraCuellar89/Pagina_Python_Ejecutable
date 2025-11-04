from tkinter import *
from tkinter import messagebox
from carrito import carrito
import random
import string
from database.pedido_dao import crear_pedido_con_detalles
import sys
import os
from PIL import Image, ImageTk


# 🔥 Función para obtener la ruta real (funciona en .py y .exe)
def ruta_recurso(ruta_relativa):
    """Devuelve la ruta correcta del archivo, tanto en .py como en .exe."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    else:
        return os.path.join(os.path.abspath("."), ruta_relativa)


def Mostrar_Comprar(usuario_id):
    from menu import Mostrar_Menu
    from inicio import Mostrar_Inicio

    # =================================================================================
    # Funciones

    def generar_codigo():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

    def cancelar():
        confirmar = messagebox.askokcancel("Confirmar", "¿Quiere deshacer su compra?")
        if confirmar: 
            raiz.destroy()
            Mostrar_Menu(usuario_id)
            
    def finalizar_compra():
        if not carrito:
            messagebox.showwarning("Carrito vacío", "No hay productos en el carrito.")
            return
        
        confirmar = messagebox.askokcancel("Confirmar", "¿Desea finalizar la compra?")
        if not confirmar:
            return

        carrito_db = []
        for item in carrito:
            producto = item["producto"]
            carrito_db.append({
                "id_producto": producto[0], 
                "cantidad": item["cantidad"]
            })

        codigo = generar_codigo()
        id_pedido, codigo = crear_pedido_con_detalles(usuario_id, carrito_db)

        if id_pedido:
            messagebox.showinfo("Compra exitosa", f"Pedido registrado con código: {codigo}")
            carrito.clear()
            raiz.destroy()
            Mostrar_Inicio(usuario_id)
        else:
            messagebox.showerror("Error", "No se pudo registrar la compra.")

    # =================================================================================
    # Raíz
    raiz = Tk()
    raiz.title('Finalizar Compra')
    raiz.resizable(1, 1)
    raiz.state('zoomed')

    for i in range(10):
        raiz.grid_rowconfigure(i, weight=1)
    for i in range(3):
        raiz.grid_columnconfigure(i, weight=1)

    # =================================================================================
    # Título
    caja_titulo = Frame(raiz)
    caja_titulo.grid(row=0, column=0, columnspan=3, pady=10)
    Label(caja_titulo, text='Productos a comprar', font=('Times New Roman', 25)).grid()

    # =================================================================================
    # Productos
    frame_productos = Frame(raiz)
    frame_productos.grid(row=1, column=0, columnspan=3, pady=10, sticky="nsew")

    if not carrito:
        Label(frame_productos, text="No hay productos en el carrito", font=("Arial", 15), fg="red").grid()
    else:
        imagenes = []
        columnas = 3
        
        for i, item in enumerate(carrito):
            producto = item["producto"]
            cantidad = item["cantidad"]
            nombre = producto[1]
            precio = producto[3]
            imagen_path = producto[4]  
            subtotal = precio * cantidad
            
            fila = i // columnas
            col = i % columnas
            
            tarjeta = Frame(frame_productos, bg='black', padx=10, pady=10)
            tarjeta.grid(row=fila, column=col, padx=20, pady=10)
            
            Label(tarjeta, text=nombre, font=('Times New Roman', 20), 
                  bg='black', fg='white').grid(row=0, pady=5)
            
            # ✅ Cargar y mostrar imagen con PIL y ruta_recurso
            try:
                ruta_img = ruta_recurso(imagen_path)
                if not os.path.exists(ruta_img):
                    ruta_img = ruta_recurso(os.path.join("img", os.path.basename(imagen_path)))

                img = Image.open(ruta_img)
                img = img.resize((200, 200))
                foto = ImageTk.PhotoImage(img)
                imagenes.append(foto)
                Label(tarjeta, image=foto, bg='black').grid(row=1, pady=5)
            except Exception as e:
                print("❌ Error al cargar imagen:", e)
                Label(tarjeta, text="[Sin imagen]", font=("Arial", 12),
                      width=20, height=10, bg="gray", fg="white").grid(row=1, pady=5)
            
            info_frame = Frame(tarjeta, bg='black')
            info_frame.grid(row=2, pady=5)
            
            Label(info_frame, text=f"Cantidad: {cantidad}  |  Precio: ${precio:.2f}  |  Subtotal: ${subtotal:.2f}", 
                  font=("Arial", 12), bg='black', fg='white').pack()
        
        frame_productos.imagenes = imagenes
    
    # =================================================================================
    # Total
    caja_total = Frame(raiz)
    caja_total.grid(row=2, column=0, columnspan=3, pady=20)
    
    total = sum(item["producto"][3] * item["cantidad"] for item in carrito)
    Label(caja_total, text=f"Total: ${total:.2f}", 
          font=("Arial", 18, "bold")).pack()

    # =================================================================================
    # Botones
    Button(raiz, text='Finalizar Compra', bg='black', fg='white', font=('Times New Roman', 15),
           width=15, command=finalizar_compra).grid(row=2, column=0, columnspan=3, pady=10)

    Button(raiz, text='Cancelar', bg='darkred', fg='white', font=('Times New Roman', 15),
           width=15, command=cancelar).grid(row=3, column=0, columnspan=3, pady=10)

    raiz.mainloop()
