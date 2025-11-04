from database.conexion import crear_tablas
from inicio_sesion import Mostrar_Inicio_Sesion

if __name__ == "__main__":
    crear_tablas()  
    Mostrar_Inicio_Sesion()