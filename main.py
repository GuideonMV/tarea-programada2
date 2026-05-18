import tkinter as tk
import funciones
import pickle

#Variables Globales
tiposSangre = ("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-")

lugaresDonacion = {
    "1": ["El Banco Nacional de sangre", "Hospital México", "Hospital San Juan de Dios"],
    "2": ["Hospital San Rafael de Alajuela", "Hospital de San Ramón", "Hospital del Cantón Norteño"],
    "3": ["Hospital Max Peralta"],
    "4": ["Hospital San Vicente de Paúl"],
    "5": ["Hospital La Anexión en Nicoya", "Hospital Enrique Baltodano de Liberia"],
    "6": ["Hospital Monseñor Sanabria"],
    "7": ["Hospital Tony Facio", "Hospital de Guápiles"],
    "8": []
}
archivoDonadores = "datos/donadores.pkl"
donadores = [] 

def ventanaPrincipal():
    donadores = funciones.cargarDonadores()
    
    ventana = tk.Tk()
    ventana.title("Banco de Sangre - TEC")
    ventana.geometry("300x400")

    tk.Label(ventana, text="Sistema de Donación de Sangre", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Button(ventana, text="1. Insertar donador",              width=30).pack(pady=5)
    tk.Button(ventana, text="2. Generar donadores",             width=30).pack(pady=5)
    tk.Button(ventana, text="3. Actualizar datos del donador",  width=30).pack(pady=5)
    tk.Button(ventana, text="4. Eliminar donador",              width=30).pack(pady=5)
    tk.Button(ventana, text="5. Insertar lugar de donación",    width=30).pack(pady=5)
    tk.Button(ventana, text="6. Reportes",                      width=30).pack(pady=5)
    tk.Button(ventana, text="7. Salir",                         width=30).pack(pady=5)

    ventana.mainloop()

ventanaPrincipal()