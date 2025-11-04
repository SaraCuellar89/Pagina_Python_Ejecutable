from tkinter import *
from tkinter import messagebox
from carrito import agregar_producto
from database.producto_dao import obtener_producto_por_nombre
from PIL import Image, ImageTk
import os, sys

# 🔥 Función para obtener la ruta correcta (igual que en menu.py)
def ruta_recurso(ruta_relativa):
    """Devuelve la ruta correcta del archivo, tanto en .py como en .exe."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    else:
        return os.path.join(os.path.abspath("."), ruta_relativa)


def Mostrar_Producto(nombre, usuario_id):

    # =================================================================================
    def aumentar():
        cantidad.set(cantidad.get() + 1)

    def disminuir():
        if cantidad.get() > 1:
            cantidad.set(cantidad.get() - 1)

    def regresar():
        raiz.destroy()
        from menu import Mostrar_Menu
        Mostrar_Menu(usuario_id)

    def agregar():
        producto = obtener_producto_por_nombre(nombre)
        if not producto:
            messagebox.showerror("Error", "No se encontró el producto.")
            return
        agregar_producto(producto, cantidad.get())
        messagebox.showinfo("Agregado", f"{nombre} agregado al carrito.")
        regresar()

    # =================================================================================
    raiz = Tk()
    raiz.title(f'Producto - {nombre}')
    raiz.resizable(1, 1)
    raiz.geometry('500x500')
    raiz.configure(bg="white")

    for i in range(6):
        raiz.grid_rowconfigure(i, weight=1)
    for i in range(3):
        raiz.grid_columnconfigure(i, weight=1)

    # =================================================================================
    # Obtener producto
    producto = obtener_producto_por_nombre(nombre)
    if not producto:
        messagebox.showerror("Error", "No se encontró el producto.")
        raiz.destroy()
        return

    _, _, _, precio, imagen_ruta = producto

    # =================================================================================
    # IMAGEN (💡 versión corregida)
    try:
        ruta_img = ruta_recurso(imagen_ruta)

        # Si la ruta no existe, intenta dentro de la carpeta img/
        if not os.path.exists(ruta_img):
            ruta_img = ruta_recurso(os.path.join("img", os.path.basename(imagen_ruta)))

        print("Cargando imagen:", ruta_img)  # debug

        img = Image.open(ruta_img)
        img = img.resize((250, 250))  # Ajusta el tamaño
        img_tk = ImageTk.PhotoImage(img)

        label_img = Label(raiz, image=img_tk, bg='white')
        label_img.image = img_tk  # Mantiene la referencia
        label_img.grid(row=0, column=0, columnspan=3, pady=(20, 10))

    except Exception as e:
        print("❌ No se pudo cargar la imagen:", e)
        Label(raiz, text="[Imagen no disponible]", bg='white', fg='gray').grid(
            row=0, column=0, columnspan=3, pady=(20, 10)
        )

    # =================================================================================
    Label(raiz, text=f'{nombre}', font=('Times New Roman', 25), bg="white").grid(row=1, column=0, columnspan=3, pady=5)
    Label(raiz, text=f"${precio:.2f}", font=('Arial', 18), bg='white', fg='green').grid(row=2, column=0, columnspan=3, pady=5)

    # =================================================================================
    caja_cantidad = Frame(raiz, bg="white")
    caja_cantidad.grid(row=3, column=0, columnspan=3, pady=10)

    Label(caja_cantidad, text='Cantidad:', font=('Times New Roman', 15), bg="white").grid(row=0, column=0, columnspan=3, pady=(0, 5))
    cantidad = IntVar(value=1)
    Button(caja_cantidad, text='-', font=('Times New Roman', 15), command=disminuir).grid(row=1, column=0, padx=5)
    Label(caja_cantidad, textvariable=cantidad, font=('Times New Roman', 15), bg="white").grid(row=1, column=1, padx=5)
    Button(caja_cantidad, text='+', font=('Times New Roman', 15), command=aumentar).grid(row=1, column=2, padx=5)

    # =================================================================================
    Button(raiz, text='Agregar', bg='darkred', fg='white', font=('Times New Roman', 15), width=15, command=agregar).grid(row=4, column=1, pady=10)
    Button(raiz, text='Regresar', bg='black', fg='white', font=('Times New Roman', 15), width=15, command=regresar).grid(row=5, column=1, pady=10)

    raiz.mainloop()
