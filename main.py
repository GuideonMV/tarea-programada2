import tkinter as tk
from tkinter import messagebox
import funciones
import pickle

#Variables Globales
tiposSangre = ("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-")

nombresProvincias = {
    "1": "San José", "2": "Alajuela", "3": "Cartago",
    "4": "Heredia", "5": "Guanacaste", "6": "Puntarenas", "7": "Limón"
}

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

#Opcion Salir
def salir(ventana):
    messagebox.showinfo("Salir", "Donar sangre, es donar vida") #Muestra este mensaje cuando se selecciona salir. El primer parámetro es el nombre de la mini ventana
    ventana.destroy() #Se cierra la ventana

def limpiarCampos(entryCedula, entryNombre, entryFecha, entryPeso, entryTelefono, entryCorreo):
    #Borra el contenido de los espacios
    #Desde la posición 0 hasta el último carácter (tk.END)
    entryCedula.delete(0, tk.END)
    entryNombre.delete(0, tk.END)
    entryFecha.delete(0, tk.END)
    entryPeso.delete(0, tk.END)
    entryTelefono.delete(0, tk.END)
    entryCorreo.delete(0, tk.END)

#Crea el formulario para insertar donadores y modificarlos

def crearFormulario(ventana, tiposSangre):
    #Crea los campos del formulario y los retorna para usarlos en insertar y actualizar
    tk.Label(ventana, text="Cédula (#-####-####):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entryCedula = tk.Entry(ventana, width=30)
    entryCedula.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Nombre Completo:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entryNombre = tk.Entry(ventana, width=30)
    entryNombre.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Fecha de nacimiento (DD/MM/AAAA):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entryFecha = tk.Entry(ventana, width=30)
    entryFecha.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Tipo de sangre:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    tipoSangreVar = tk.StringVar(value=tiposSangre[0]) #Guarda lo que está seleccionado en el optionMenu
    tk.OptionMenu(ventana, tipoSangreVar, *tiposSangre).grid(row=3, column=1, padx=10, pady=5) #Le ponemos "*" a tiposSangre para desempacar todo lo que hay en la tupla

    tk.Label(ventana, text="Sexo:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    sexoVar = tk.BooleanVar(value=True) #Guarda el valor seleccionado en RadioButton (femenino o masculino). Masculino como default
    #Botones de selección
    tk.Radiobutton(ventana, text="Masculino", variable=sexoVar, value=True).grid(row=4, column=1, sticky="w")
    tk.Radiobutton(ventana, text="Femenino",  variable=sexoVar, value=False).grid(row=5, column=1, sticky="w")

    tk.Label(ventana, text="Peso (kg):").grid(row=6, column=0, padx=10, pady=5, sticky="w")
    entryPeso = tk.Entry(ventana, width=30)
    entryPeso.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Teléfono:").grid(row=7, column=0, padx=10, pady=5, sticky="w")
    entryTelefono = tk.Entry(ventana, width=30)
    entryTelefono.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Correo:").grid(row=8, column=0, padx=10, pady=5, sticky="w")
    entryCorreo = tk.Entry(ventana, width=30)
    entryCorreo.grid(row=8, column=1, padx=10, pady=5)

    return entryCedula, entryNombre, entryFecha, tipoSangreVar, sexoVar, entryPeso, entryTelefono, entryCorreo


def registrar(ventana, entryCedula, entryNombre, entryFecha, tipoSangreVar, sexoVar, entryPeso, entryTelefono, entryCorreo, donadores):
    #Guarda lo que se digitó en los entrys en variables
    cedula     = entryCedula.get().strip()
    nombre     = entryNombre.get().strip()
    fecha      = entryFecha.get().strip()
    tipoSangre = tipoSangreVar.get()
    sexo       = sexoVar.get()
    peso       = entryPeso.get().strip()
    telefono   = entryTelefono.get().strip()
    correo     = entryCorreo.get().strip()

    error = funciones.validarDonador(cedula, nombre, fecha, telefono, correo, peso, donadores)
    if error:
        messagebox.showerror("Error", error)
        return

    partes = nombre.split()
    dia, mes, anno = fecha.split("/")

    funciones.insertarDonador(donadores, tiposSangre, cedula, partes[0], partes[1], partes[2], tipoSangre, sexo, int(dia), int(mes), int(anno), peso, correo, telefono)
    funciones.guardarDonadores(donadores)

    #Ventana de realimentación con información del donador
    mensajes = funciones.obtenerRealimentacion(cedula, (int(dia), int(mes), int(anno)), peso, tipoSangre, lugaresDonacion)
    ventanaRealimentacion = tk.Toplevel(ventana)
    ventanaRealimentacion.title("Información del Donador")
    ventanaRealimentacion.geometry("500x300")
    tk.Label(ventanaRealimentacion, text="¡Donador registrado exitosamente!", font=("Arial", 10, "bold"), fg="green").pack(padx=10, pady=10, anchor="w")
    for mensaje in mensajes:
        tk.Label(ventanaRealimentacion, text=mensaje, wraplength=450, justify="left").pack(padx=10, pady=5, anchor="w")
    tk.Button(ventanaRealimentacion, text="Regresar", command=ventanaRealimentacion.destroy).pack(pady=10)

#Opcion 1 del menu
def insertarDonador(ventanaPrincipal, donadores):
    ventana = tk.Toplevel(ventanaPrincipal) #Crea una ventana encima de la principal
    ventana.title("Insertar Donador")
    ventana.geometry("400x500")
    #Utilizamos "grid" para visualizar todo en forma de tabla, crearFormulario retorna los campos
    entryCedula, entryNombre, entryFecha, tipoSangreVar, sexoVar, entryPeso, entryTelefono, entryCorreo = crearFormulario(ventana, tiposSangre)
    #Botones
    tk.Button(ventana, text="Registrar", width=12,
        command=lambda: registrar(ventana, entryCedula, entryNombre, entryFecha, tipoSangreVar, sexoVar, entryPeso, entryTelefono, entryCorreo, donadores)
    ).grid(row=9, column=0, padx=10, pady=15)
    tk.Button(ventana, text="Limpiar", width=12,
        command=lambda: limpiarCampos(entryCedula, entryNombre, entryFecha, entryPeso, entryTelefono, entryCorreo)
    ).grid(row=9, column=1, padx=10, pady=15)
    tk.Button(ventana, text="Regresar", width=12, command=ventana.destroy).grid(row=9, column=2, padx=10, pady=15)


#Opcio 2 del menu
def generarMensaje(ventana, entryCantidad, donadores):
    cantidad = entryCantidad.get().strip()
    if not cantidad.isdigit() or int(cantidad) <= 0:
        messagebox.showerror("Error", "Ingrese un número mayor a 0")
        return
    funciones.generarDonadores(donadores, tiposSangre, int(cantidad))
    funciones.guardarDonadores(donadores)
    messagebox.showinfo("Éxito", f"¡{cantidad} donadores generados exitosamente!")
    ventana.destroy()

def generarDonadores(ventanaPrincipal, donadores):
    ventana = tk.Toplevel(ventanaPrincipal) #Crea una ventana encima de la principal
    ventana.title("Generar Donadores")
    ventana.geometry("300x150")
    tk.Label(ventana, text="Cantidad de donadores a generar:").pack(padx=10, pady=10)
    entryCantidad = tk.Entry(ventana, width=20)
    entryCantidad.pack(padx=10, pady=5)
    tk.Button(ventana, text="Generar", width=12,
        command=lambda: generarMensaje(ventana, entryCantidad, donadores)
    ).pack(pady=10)

#Opcion 3 del menu
def confirmarActualizar(ventana, donadores, indice, entryCedula, entryNombre, entryFecha, tipoSangreVar, sexoVar, entryPeso, entryTelefono, entryCorreo):
    #Guarda lo que se digitó en los entrys en variables
    nombre     = entryNombre.get().strip()
    fecha      = entryFecha.get().strip()
    tipoSangre = tipoSangreVar.get()
    sexo       = sexoVar.get()
    peso       = entryPeso.get().strip()
    telefono   = entryTelefono.get().strip()
    correo     = entryCorreo.get().strip()
    cedula     = donadores[indice][1]

    error = funciones.validarDonadorActualizar(cedula, nombre, fecha, telefono, correo, peso)
    if error:
        messagebox.showerror("Error", error)
        return

    partes = nombre.split()
    dia, mes, anno = fecha.split("/")
    funciones.actualizarDonador(donadores, tiposSangre, indice, partes[0], partes[1], partes[2], tipoSangre, sexo, int(dia), int(mes), int(anno), peso, correo, telefono)
    funciones.guardarDonadores(donadores)
    messagebox.showinfo("Éxito", "¡Datos actualizados exitosamente!")
    ventana.destroy()

def mostrarFormularioActualizar(donadores, indice):
    donador = donadores[indice]
    ventana = tk.Toplevel() #Crea una ventana encima de la principal
    ventana.title("Actualizar Donador")
    ventana.geometry("400x500")
    #Utilizamos crearFormulario para reutilizar los campos
    entryCedula, entryNombre, entryFecha, tipoSangreVar, sexoVar, entryPeso, entryTelefono, entryCorreo = crearFormulario(ventana, tiposSangre)

    #Precargamos los datos del donador en los campos
    entryCedula.insert(0, donador[1])
    entryCedula.config(state="readonly") #La cédula no se puede modificar
    entryNombre.insert(0, " ".join(donador[0]))
    dia, mes, anno = donador[4]
    entryFecha.insert(0, f"{dia:02d}/{mes:02d}/{anno}")
    tipoSangreVar.set(tiposSangre[donador[2]])
    sexoVar.set(donador[3])
    entryPeso.insert(0, str(donador[5]))
    entryTelefono.insert(0, donador[7])
    entryCorreo.insert(0, donador[6])

    #Botones
    tk.Button(ventana, text="Confirmar", width=12,
        command=lambda: confirmarActualizar(ventana, donadores, indice, entryCedula, entryNombre, entryFecha, tipoSangreVar, sexoVar, entryPeso, entryTelefono, entryCorreo)
    ).grid(row=9, column=0, padx=10, pady=15)
    tk.Button(ventana, text="Regresar", width=12, command=ventana.destroy).grid(row=9, column=1, padx=10, pady=15)

def buscarParaActualizar(entryCedula, donadores, ventana):
    cedula = entryCedula.get().strip()
    if not funciones.validarCedula(cedula):
        messagebox.showerror("Error", "Cédula inválida. Ejemplo de formato: #-####-####")
        return
    indice = funciones.buscarDonador(cedula, donadores)
    if indice == -1:
        messagebox.showerror("Error", f"La persona con el número de cédula: {cedula} no está registrada en la base de datos del Banco de Sangre aún")
        return
    ventana.destroy()
    mostrarFormularioActualizar(donadores, indice)

def actualizarDonador(ventanaPrincipal, donadores):
    ventana = tk.Toplevel(ventanaPrincipal) #Crea una ventana encima de la principal
    ventana.title("Actualizar Donador")
    ventana.geometry("300x150")
    tk.Label(ventana, text="Ingrese el número de cédula:").pack(padx=10, pady=10)
    entryCedula = tk.Entry(ventana, width=30)
    entryCedula.pack(padx=10, pady=5)
    tk.Button(ventana, text="Buscar", width=12,
        command=lambda: buscarParaActualizar(entryCedula, donadores, ventana)
    ).pack(pady=10)

#Opcion 4
def confirmarEliminacion(ventanaConfirm, cedula, donadores, justificacionVar):
    justificacion = int(justificacionVar.get().split(" - ")[0])
    funciones.eliminarDonador(cedula, donadores, justificacion)
    funciones.guardarDonadores(donadores)
    messagebox.showinfo("Éxito", "¡Donador eliminado exitosamente!")
    ventanaConfirm.destroy()

def buscarParaEliminar(entryCedula, donadores, ventana):
    cedula = entryCedula.get().strip()
    if not funciones.validarCedula(cedula):
        messagebox.showerror("Error", "Cédula inválida. Ejemplo de formato: #-####-####")
        return
    indice = funciones.buscarDonador(cedula, donadores)
    if indice == -1:
        messagebox.showinfo("No encontrado",
            f"La persona con el número de cédula: {cedula} no está registrado en la base de datos del Banco de Sangre aún")
        return
    if donadores[indice][8] == 0:
        messagebox.showinfo("Aviso", f"El donador con cédula {cedula} ya se encuentra inactivo")
        return

    donador = donadores[indice]
    ventanaConfirm = tk.Toplevel(ventana)
    ventanaConfirm.title("Confirmar eliminación")
    ventanaConfirm.geometry("450x250")

    nombre = " ".join(donador[0])
    tk.Label(ventanaConfirm, text=f"Donador encontrado: {nombre}", font=("Arial", 10, "bold")).pack(pady=10)

    tk.Label(ventanaConfirm, text="Seleccione la justificación:").pack()
    opcionesJustificacion = [
        f"{codigo} - {descripcion[:50]}..." 
        for codigo, descripcion in funciones.justificaciones.items()
    ]
    justificacionVar = tk.StringVar(value=opcionesJustificacion[0])
    tk.OptionMenu(ventanaConfirm, justificacionVar, *opcionesJustificacion).pack(padx=10, pady=5)

    tk.Label(ventanaConfirm, text="¿Está seguro de que desea eliminarlo?").pack(pady=8)

    frameBotones = tk.Frame(ventanaConfirm)
    frameBotones.pack(pady=5)
    tk.Button(frameBotones, text="Confirmar", width=12,
        command=lambda: confirmarEliminacion(ventanaConfirm, cedula, donadores, justificacionVar)
    ).grid(row=0, column=0, padx=10)
    tk.Button(frameBotones, text="Cancelar", width=12,
        command=ventanaConfirm.destroy
    ).grid(row=0, column=1, padx=10)

def eliminarDonador(ventanaPrincipal, donadores):
    ventana = tk.Toplevel(ventanaPrincipal)
    ventana.title("Eliminar Donador")
    ventana.geometry("350x150")
    tk.Label(ventana, text="Cédula del donador a eliminar:").grid(row=0, column=0, padx=10, pady=15, sticky="w")
    entryCedula = tk.Entry(ventana, width=25)
    entryCedula.grid(row=0, column=1, padx=10, pady=15)
    tk.Button(ventana, text="Buscar", width=12,
        command=lambda: buscarParaEliminar(entryCedula, donadores, ventana)
    ).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(ventana, text="Regresar", width=12, command=ventana.destroy).grid(row=1, column=1, padx=10, pady=10)

#Opcion 5
def insertarLugar(provinciaVar, entryLugar, labelMensaje):
    codigo    = provinciaVar.get().split(" - ")[0]  # obtiene el "1", "2", etc.
    nuevoLugar = entryLugar.get().strip()

    if not nuevoLugar:
        labelMensaje.config(text="Debe ingresar un lugar", fg="red")
        return

    if nuevoLugar in lugaresDonacion[codigo]:
        labelMensaje.config(text="Ese lugar ya está registrado en esa provincia", fg="red")
        return

    lugaresDonacion[codigo].append(nuevoLugar)
    entryLugar.delete(0, tk.END)
    labelMensaje.config(text="¡Lugar insertado exitosamente!", fg="green")

def insertarLugarDonacion(ventanaPrincipal):
    ventana = tk.Toplevel(ventanaPrincipal)
    ventana.title("Insertar Lugar de Donación")
    ventana.geometry("400x220")

    opciones = []
    for codigo, nombre in nombresProvincias.items():
        opciones.append(f"{codigo} - {nombre}")

    tk.Label(ventana, text="Provincia:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    provinciaVar = tk.StringVar(value=opciones[0])
    tk.OptionMenu(ventana, provinciaVar, *opciones).grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tk.Label(ventana, text="Nuevo lugar:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entryLugar = tk.Entry(ventana, width=35)
    entryLugar.grid(row=1, column=1, padx=10, pady=10)

    labelMensaje = tk.Label(ventana, text="", font=("Arial", 9))
    labelMensaje.grid(row=2, column=0, columnspan=2, pady=5)

    tk.Button(ventana, text="Insertar", width=12,
        command=lambda: insertarLugar(provinciaVar, entryLugar, labelMensaje)
    ).grid(row=3, column=0, padx=10, pady=10)
    tk.Button(ventana, text="Salir", width=12, command=ventana.destroy).grid(row=3, column=1, padx=10, pady=10)


#Ventana Principal
def ventanaPrincipal():
    donadores = funciones.cargarDonadores()
    ventana = tk.Tk() #Crea la ventana principal
    ventana.title("Banco de Sangre - TEC") #Le ponemos titulo a la ventana
    ventana.geometry("300x400") #Definimos el tamaño de la ventana
    tk.Label(ventana, text="Sistema de Donación de Sangre", font=("Arial", 12, "bold")).pack(pady=10) #Título que ve el usuario, utilizamos "Label" solo para mostrar texto
    #Botones para que el usuario pueda interactuar
    tk.Button(ventana, text="1. Insertar donador",             width=30, command=lambda: insertarDonador(ventana, donadores)).pack(pady=5)
    tk.Button(ventana, text="2. Generar donadores",            width=30, command=lambda: generarDonadores(ventana, donadores)).pack(pady=5)
    tk.Button(ventana, text="3. Actualizar datos del donador", width=30, command=lambda: actualizarDonador(ventana, donadores)).pack(pady=5)
    tk.Button(ventana, text="4. Eliminar donador",             width=30, command=lambda: eliminarDonador(ventana, donadores)).pack(pady=5)
    tk.Button(ventana, text="5. Insertar lugar de donación",   width=30, command=lambda: insertarLugarDonacion(ventana)).pack(pady=5)
    tk.Button(ventana, text="6. Reportes",                     width=30).pack(pady=5)
    tk.Button(ventana, text="7. Salir",                        width=30, command=lambda: salir(ventana)).pack(pady=5)
    #Mantiene la ventana abierta
    ventana.mainloop()

ventanaPrincipal()