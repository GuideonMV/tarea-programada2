#Elaborado por: Jimena Acuña Parra y Guideon Montero Vargas
#Fecha de elaboración: 217/05/2026 
#Última fecha de modificación: 30/05/2026 
#Versión: 3.14.3

#Librerías
import tkinter as tk
from tkinter import messagebox
import funciones
import pickle
import reportes

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
    """
    Funcionamiento: muestra un mensaje de despedida y cierra la ventana principal.
    Entradas:
        ventana (tk.Tk): Ventana principal de la aplicación.
    Salidas:
        No retorna valor. Cierra la aplicación.
    """
    messagebox.showinfo("Salir", "Donar sangre, es donar vida") #Muestra este mensaje cuando se selecciona salir. El primer parámetro es el nombre de la mini ventana
    ventana.destroy() #Se cierra la ventana

def limpiarCampos(entryCedula, entryNombre, entryFecha, entryPeso, entryTelefono, entryCorreo):
    """
    Funcionamiento: borra el contenido de todos los campos Entry del formulario de donador.
    Entradas:
        entryCedula (tk.Entry): Campo de texto para la cédula.
        entryNombre (tk.Entry): Campo de texto para el nombre.
        entryFecha (tk.Entry): Campo de texto para la fecha de nacimiento.
        entryPeso (tk.Entry): Campo de texto para el peso.
        entryTelefono (tk.Entry): Campo de texto para el teléfono.
        entryCorreo (tk.Entry): Campo de texto para el correo.
    Salidas:
        No retorna valor. Modifica los widgets directamente.
    """
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
    """
    Funcionamiento: crea y coloca todos los campos del formulario de donador en una ventana.
    Es reutilizado tanto para insertar como para actualizar donadores.
    Entradas:
        ventana (tk.Toplevel): Ventana donde se colocarán los campos.
        tiposSangre (tuple): Tupla con los tipos de sangre disponibles.
    Salidas:
        Retorna una tupla con todos los widgets del formulario
    """
    #Crea los campos del formulario y los retorna para usarlos en insertar y actualizar
    tk.Label(ventana, text="Cédula (#-####-####):").grid(row=0, column=0, padx=10, pady=5, sticky="w")   # tk.Label muestra texto estático; sticky="w" alinea el texto a la izquierda (west)
    entryCedula = tk.Entry(ventana, width=30) # tk.Entry es un campo de texto editable de una sola línea
    entryCedula.grid(row=0, column=1, padx=10, pady=5)
    tk.Label(ventana, text="Nombre Completo:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entryNombre = tk.Entry(ventana, width=30)
    entryNombre.grid(row=1, column=1, padx=10, pady=5)
    tk.Label(ventana, text="Fecha de nacimiento (DD/MM/AAAA):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entryFecha = tk.Entry(ventana, width=30)
    entryFecha.grid(row=2, column=1, padx=10, pady=5)
    tk.Label(ventana, text="Tipo de sangre:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    tipoSangreVar = tk.StringVar(value=tiposSangre[0]) #Guarda lo que está seleccionado en el optionMenu
    tk.OptionMenu(ventana, tipoSangreVar, *tiposSangre).grid(row=3, column=1, padx=10, pady=5) #Le ponemos "*" a tiposSangre para desempacar todo lo que hay en la tupla. tk.StringVar almacena un valor de texto asociado a un widget; se actualiza automáticamente
    tk.Label(ventana, text="Sexo:").grid(row=4, column=0, padx=10, pady=5, sticky="w") # tk.BooleanVar almacena un valor booleano; True = Masculino (valor por defecto)
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
    """
    Funcionamiento: lee los datos del formulario, los valida e inserta el donador si son correctos.
    Luego muestra una ventana de realimentación con información útil para el donador.
    Entradas:
        ventana (tk.Toplevel): Ventana padre del formulario.
        entryCedula (tk.Entry): Campo con la cédula ingresada.
        entryNombre (tk.Entry): Campo con el nombre ingresado.
        entryFecha (tk.Entry): Campo con la fecha de nacimiento.
        tipoSangreVar (tk.StringVar): Variable con el tipo de sangre seleccionado.
        sexoVar (tk.BooleanVar): Variable con el sexo seleccionado (True=Masculino).
        entryPeso (tk.Entry): Campo con el peso ingresado.
        entryTelefono (tk.Entry): Campo con el teléfono ingresado.
        entryCorreo (tk.Entry): Campo con el correo ingresado.
        donadores (list): Lista de donadores registrados en memoria.
    Salidas:
        No retorna valor. Inserta en la lista, guarda en archivo y abre ventana de realimentación.
    """
    #Guarda lo que se digitó en los entrys en variables
    cedula     = entryCedula.get().strip() # .get() obtiene el texto actual del Entry; .strip() elimina espacios al inicio/final
    nombre     = entryNombre.get().strip()
    fecha      = entryFecha.get().strip()
    tipoSangre = tipoSangreVar.get()
    sexo       = sexoVar.get()
    peso       = entryPeso.get().strip()
    telefono   = entryTelefono.get().strip()
    correo     = entryCorreo.get().strip()
    error      = funciones.validarDonador(cedula, nombre, fecha, telefono, correo, peso, donadores)
    if error:
        messagebox.showerror("Error", error)
        return
    partes = nombre.split()
    dia, mes, anno = fecha.split("/")
    funciones.insertarDonador(donadores, tiposSangre, cedula, partes[0], partes[1], partes[2], tipoSangre, sexo, int(dia), int(mes), int(anno), peso, correo, telefono)
    funciones.guardarDonadores(donadores)
    #Ventana de realimentación con información del donador
    mensajes = funciones.obtenerRealimentacion(cedula, fecha, peso, tipoSangre, lugaresDonacion)
    ventanaRealimentacion = tk.Toplevel(ventana) # tk.Toplevel crea una ventana secundaria que se superpone a la ventana padre
    ventanaRealimentacion.title("Información del Donador")
    ventanaRealimentacion.geometry("500x300")
    tk.Label(ventanaRealimentacion, text="¡Donador registrado exitosamente!", font=("Arial", 10, "bold"), fg="green").pack(padx=10, pady=10, anchor="w")
    for mensaje in mensajes:
        tk.Label(ventanaRealimentacion, text=mensaje, wraplength=450, justify="left").pack(padx=10, pady=5, anchor="w")# wraplength limita el ancho del texto en píxeles (hace salto de línea automático)
        # justify="left" alinea el texto a la izquierda dentro del Label
    tk.Button(ventanaRealimentacion, text="Regresar", command=ventanaRealimentacion.destroy).pack(pady=10)

#Opcion 1 del menu
def insertarDonador(ventanaPrincipal, donadores):
    """
    Funcionamiento: Abre la ventana con el formulario para registrar un nuevo donador.
    Entradas:
        ventanaPrincipal (tk.Tk): Ventana principal de la aplicación.
        donadores (list): Lista de donadores en memoria.
    Salidas:
        No retorna valor. Abre una ventana Toplevel con el formulario.
    """
    ventana = tk.Toplevel(ventanaPrincipal) #Crea una ventana encima de la principal
    ventana.title("Insertar Donador")
    ventana.geometry("400x500")
    #Utilizamos "grid" para visualizar todo en forma de tabla, crearFormulario retorna los campos
    entryCedula, entryNombre, entryFecha, tipoSangreVar, sexoVar, entryPeso, entryTelefono, entryCorreo = crearFormulario(ventana, tiposSangre)
    #Botones
    # lambda: permite pasar argumentos a la función cuando el botón es presionado
    tk.Button(ventana, text="Registrar", width=12, command=lambda: registrar(ventana, entryCedula, entryNombre, entryFecha, tipoSangreVar, sexoVar, entryPeso, entryTelefono, entryCorreo, donadores)).grid(row=9, column=0, padx=10, pady=15)
    tk.Button(ventana, text="Limpiar", width=12, command=lambda: limpiarCampos(entryCedula, entryNombre, entryFecha, entryPeso, entryTelefono, entryCorreo)).grid(row=9, column=1, padx=10, pady=15)
    tk.Button(ventana, text="Regresar", width=12, command=ventana.destroy).grid(row=9, column=2, padx=10, pady=15)

#Opcio 2 del menu
def generarMensaje(ventana, entryCantidad, donadores):
    """
    Funcionamiento: valida la cantidad ingresada y genera donadores aleatorios en la base de datos.
    Entradas:
        ventana (tk.Toplevel): Ventana donde está el campo de cantidad.
        entryCantidad (tk.Entry): Campo con la cantidad de donadores a generar.
        donadores (list): Lista de donadores en memoria.
    Salidas:
        No retorna valor. Genera donadores, guarda y cierra la ventana.
    """
    cantidad = entryCantidad.get().strip()
    if not cantidad.isdigit() or int(cantidad) <= 0:
        messagebox.showerror("Error", "Ingrese un número mayor a 0")
        return
    funciones.generarDonadores(donadores, tiposSangre, int(cantidad))
    funciones.guardarDonadores(donadores)
    messagebox.showinfo("Éxito", f"¡{cantidad} donadores generados exitosamente!")
    ventana.destroy()

def generarDonadores(ventanaPrincipal, donadores):
    """
    Funcionamiento: abre una ventana para que el usuario indique cuántos donadores generar.
    Entradas:
        ventanaPrincipal (tk.Tk): Ventana principal de la aplicación.
        donadores        (list):  Lista de donadores en memoria.
    Salidas:
        No retorna valor. Abre ventana Toplevel con campo de cantidad.
    """
    ventana = tk.Toplevel(ventanaPrincipal) #Crea una ventana encima de la principal
    ventana.title("Generar Donadores")
    ventana.geometry("300x150")
    tk.Label(ventana, text="Cantidad de donadores a generar:").pack(padx=10, pady=10) # pack() posiciona los widgets de forma apilada (uno debajo del otro)
    entryCantidad = tk.Entry(ventana, width=20)
    entryCantidad.pack(padx=10, pady=5)
    tk.Button(ventana, text="Generar", width=12, command=lambda: generarMensaje(ventana, entryCantidad, donadores)).pack(pady=10)

#Opcion 3 del menu
def confirmarActualizar(ventana, donadores, indice, entryCedula, entryNombre, entryFecha, tipoSangreVar, sexoVar, entryPeso, entryTelefono, entryCorreo):
    """
    Funcionamiento: lee los datos modificados del formulario, los valida y actualiza el donador.
    Entradas:
        ventana (tk.Toplevel): Ventana del formulario de actualización.
        donadores (list): Lista de donadores en memoria.
        indice (int): Posición del donador en la lista.
        entryCedula (tk.Entry): Campo de cédula (solo lectura, no se modifica).
        entryNombre (tk.Entry): Campo con el nombre actualizado.
        entryFecha (tk.Entry): Campo con la fecha actualizada.
        tipoSangreVar (tk.StringVar): Variable con el tipo de sangre actualizado.
        sexoVar (tk.BooleanVar): Variable con el sexo actualizado.
        entryPeso (tk.Entry): Campo con el peso actualizado.
        entryTelefono (tk.Entry): Campo con el teléfono actualizado.
        entryCorreo (tk.Entry): Campo con el correo actualizado.
    Salidas:
        No retorna valor. Actualiza la lista y el archivo, luego cierra la ventana.
    """
    #Guarda lo que se digitó en los entrys en variables
    nombre     = entryNombre.get().strip()
    fecha      = entryFecha.get().strip()
    tipoSangre = tipoSangreVar.get()
    sexo       = sexoVar.get()
    peso       = entryPeso.get().strip()
    telefono   = entryTelefono.get().strip()
    correo     = entryCorreo.get().strip()
    cedula     = donadores[indice][1] # La cédula no cambia, se toma del registro existente
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
    """
    Funcionamiento: abre el formulario de actualización precargado con los datos actuales del donador.
    Entradas:
        donadores (list): Lista de donadores en memoria.
        indice (int): Posición del donador a actualizar.
    Salidas:
        No retorna valor. Abre ventana Toplevel con el formulario precargado.
    """
    donador = donadores[indice]
    ventana = tk.Toplevel() #Crea una ventana encima de la principal
    ventana.title("Actualizar Donador")
    ventana.geometry("400x500")
    #Utilizamos crearFormulario para reutilizar los campos
    entryCedula, entryNombre, entryFecha, tipoSangreVar, sexoVar, entryPeso, entryTelefono, entryCorreo = crearFormulario(ventana, tiposSangre)
    #Precargamos los datos del donador en los campos
    entryCedula.insert(0, donador[1]) # insert(0, valor) inserta texto al inicio del Entry
    entryCedula.config(state="readonly") # config(state="readonly") evita que el usuario edite ese campo
    entryNombre.insert(0, " ".join(donador[0]))
    dia, mes, anno = donador[4]
    entryFecha.insert(0, f"{dia:02d}/{mes:02d}/{anno}")
    tipoSangreVar.set(tiposSangre[donador[2]]) # .set() actualiza el valor del StringVar/BooleanVar
    sexoVar.set(donador[3])
    entryPeso.insert(0, str(donador[5]))
    entryTelefono.insert(0, donador[7])
    entryCorreo.insert(0, donador[6])
    #Botones
    tk.Button(ventana, text="Confirmar", width=12, command=lambda: confirmarActualizar(ventana, donadores, indice, entryCedula, entryNombre, entryFecha, tipoSangreVar, sexoVar, entryPeso, entryTelefono, entryCorreo)).grid(row=9, column=0, padx=10, pady=15)
    tk.Button(ventana, text="Regresar", width=12, command=ventana.destroy).grid(row=9, column=1, padx=10, pady=15)

def buscarParaActualizar(entryCedula, donadores, ventana):
    """
    Funcionamiento: busca un donador por cédula y abre el formulario de actualización si existe.
    Entradas:
        entryCedula (tk.Entry): Campo con la cédula a buscar.
        donadores (list): Lista de donadores en memoria.
        ventana (tk.Toplevel): Ventana de búsqueda (se cierra al encontrar).
    Salidas:
        No retorna valor. Cierra la ventana de búsqueda y abre el formulario de actualización.
    """
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
    """
    Funcionamiento: abre la ventana para buscar por cédula al donador que se desea actualizar.
    Entradas:
        ventanaPrincipal (tk.Tk): Ventana principal de la aplicación.
        donadores (list): Lista de donadores en memoria.
    Salidas:
        No retorna valor. Abre ventana Toplevel con campo de búsqueda por cédula.
    """
    ventana = tk.Toplevel(ventanaPrincipal) #Crea una ventana encima de la principal
    ventana.title("Actualizar Donador")
    ventana.geometry("300x150")
    tk.Label(ventana, text="Ingrese el número de cédula:").pack(padx=10, pady=10)
    entryCedula = tk.Entry(ventana, width=30)
    entryCedula.pack(padx=10, pady=5)
    tk.Button(ventana, text="Buscar", width=12, command=lambda: buscarParaActualizar(entryCedula, donadores, ventana)).pack(pady=10)

#Opcion 4
def confirmarEliminacion(ventanaConfirm, cedula, donadores, justificacionVar):
    """
    Funcionamiento: confirma la eliminación (desactivación) del donador con la justificación seleccionada.
    Entradas:
        ventanaConfirm (tk.Toplevel): Ventana de confirmación de eliminación.
        cedula (str): Cédula del donador a eliminar.
        donadores (list): Lista de donadores en memoria.
        justificacionVar(tk.StringVar): Variable con la justificación seleccionada.
    Salidas:
        No retorna valor. Elimina el donador, guarda y cierra la ventana.
    """
    justificacion = int(justificacionVar.get().split(" - ")[0]) # El valor del OptionMenu tiene formato "código - descripción"; se extrae solo el código
    indice = funciones.buscarDonador(cedula, donadores)
    esMasculino = donadores[indice][3]
    if esMasculino and justificacion == 7:
        messagebox.showerror("Error", "La justificación de embarazo no aplica para donadores masculinos")
        return
    funciones.eliminarDonador(cedula, donadores, justificacion)
    funciones.guardarDonadores(donadores)
    messagebox.showinfo("Éxito", "¡Donador eliminado exitosamente!")
    ventanaConfirm.destroy()

def buscarParaEliminar(entryCedula, donadores, ventana):
    """
    Funcionamiento: busca un donador por cédula y muestra la ventana de confirmación de eliminación.
    Entradas:
        entryCedula (tk.Entry): Campo con la cédula a buscar.
        donadores (list): Lista de donadores en memoria.
        ventana (tk.Toplevel): Ventana de búsqueda (permanece abierta).
    Salidas:
        No retorna valor. Abre ventana de confirmación si el donador existe y está activo.
    """
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
    ventanaConfirm = tk.Toplevel(ventana) # Ventana secundaria para confirmar la acción antes de eliminar
    ventanaConfirm.title("Confirmar eliminación")
    ventanaConfirm.geometry("450x250")
    nombre = " ".join(donador[0])
    tk.Label(ventanaConfirm, text=f"Donador encontrado: {nombre}", font=("Arial", 10, "bold")).pack(pady=10) # font=("Arial", 10, "bold") pone el texto en negrita
    tk.Label(ventanaConfirm, text="Seleccione la justificación:").pack()
    opcionesJustificacion = [f"{codigo} - {justificacion}" for codigo, justificacion in funciones.justificaciones.items()] # Construye las opciones del menú con formato "código - descripción"
    justificacionVar = tk.StringVar(value=opcionesJustificacion[0]) 
    tk.OptionMenu(ventanaConfirm, justificacionVar, *opcionesJustificacion).pack(padx=10, pady=5)
    tk.Label(ventanaConfirm, text="¿Está seguro de que desea eliminarlo?").pack(pady=8)
    frameBotones = tk.Frame(ventanaConfirm) # tk.Frame agrupa widgets en un contenedor para organizarlos juntos
    frameBotones.pack(pady=5) 
    tk.Button(frameBotones, text="Confirmar", width=12, command=lambda: confirmarEliminacion(ventanaConfirm, cedula, donadores, justificacionVar)).grid(row=0, column=0, padx=10)
    tk.Button(frameBotones, text="Cancelar", width=12, command=ventanaConfirm.destroy).grid(row=0, column=1, padx=10)

def eliminarDonador(ventanaPrincipal, donadores):
    """
    Funcionamiento: abre la ventana para buscar por cédula al donador que se desea eliminar.
    Entradas:
        ventanaPrincipal (tk.Tk): Ventana principal de la aplicación.
        donadores (list): Lista de donadores en memoria.
    Salidas:
        No retorna valor. Abre ventana Toplevel con campo de búsqueda.
    """
    ventana = tk.Toplevel(ventanaPrincipal)
    ventana.title("Eliminar Donador")
    ventana.geometry("350x150")
    tk.Label(ventana, text="Cédula del donador a eliminar:").grid(row=0, column=0, padx=10, pady=15, sticky="w")
    entryCedula = tk.Entry(ventana, width=25)
    entryCedula.grid(row=0, column=1, padx=10, pady=15)
    tk.Button(ventana, text="Buscar", width=12, command=lambda: buscarParaEliminar(entryCedula, donadores, ventana)).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(ventana, text="Regresar", width=12, command=ventana.destroy).grid(row=1, column=1, padx=10, pady=10)

#Opcion 5
def insertarLugar(provinciaVar, entryLugar, labelMensaje):
    """
    Funcionamiento: agrega un nuevo lugar de donación a la provincia seleccionada.
    Entradas:
        provinciaVar (tk.StringVar): Variable con la provincia seleccionada ("código - nombre").
        entryLugar (tk.Entry): Campo con el nombre del nuevo lugar.
        labelMensaje (tk.Label): Etiqueta donde se muestra el resultado de la operación.
    Salidas:
        No retorna valor. Modifica lugares. Donacion y actualiza el labelMensaje.
    """
    codigo    = provinciaVar.get().split(" - ")[0]  # obtiene el "1", "2", etc.
    nuevoLugar = entryLugar.get().strip()
    if not nuevoLugar: # .config() modifica propiedades de un widget ya existente (texto, color, etc.)
        labelMensaje.config(text="Debe ingresar un lugar", fg="red")
        return
    if nuevoLugar in lugaresDonacion[codigo]:
        labelMensaje.config(text="Ese lugar ya está registrado en esa provincia", fg="red")
        return
    lugaresDonacion[codigo].append(nuevoLugar)
    entryLugar.delete(0, tk.END)
    labelMensaje.config(text="¡Lugar insertado exitosamente!", fg="green")

def insertarLugarDonacion(ventanaPrincipal):
    """
    Funcionamiento: abre la ventana para agregar un nuevo centro de donación a una provincia.
    Entradas:
        ventanaPrincipal (tk.Tk): Ventana principal de la aplicación.
    Salidas:
        No retorna valor. Abre ventana Toplevel con selección de provincia y campo de lugar.
    """
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
    labelMensaje = tk.Label(ventana, text="", font=("Arial", 9)) # Label vacío que se usará para mostrar mensajes de éxito o error
    labelMensaje.grid(row=2, column=0, columnspan=2, pady=5)
    tk.Button(ventana, text="Insertar", width=12, command=lambda: insertarLugar(provinciaVar, entryLugar, labelMensaje)).grid(row=3, column=0, padx=10, pady=10)
    tk.Button(ventana, text="Salir", width=12, command=ventana.destroy).grid(row=3, column=1, padx=10, pady=10)
    
#Opcion 6
#Reporte 1
def generarReporteProvincia(provinciaVar, ventana, donadores, nombresProvincias):
    """
    Funcionamiento: genera el reporte de donantes filtrado por la provincia seleccionada.
    Entradas:
        provinciaVar (tk.StringVar): Variable con la provincia seleccionada.
        ventana (tk.Toplevel): Ventana del reporte (no se cierra automáticamente).
        donadores (list): Lista de donadores en memoria.
        nombresProvincias(dict): Diccionario de códigos y nombres de provincias.
    Salidas:
        No retorna valor. Genera el archivo de reporte y muestra mensaje de resultado.
    """
    provincia = provinciaVar.get().split(" - ")[0]
    resultado = reportes.reporteDonantesporProvincia(donadores, tiposSangre, provincia, nombresProvincias)
    if resultado:
        messagebox.showinfo("Éxito", "Reporte creado satisfactoriamente.")
    else:
        messagebox.showerror("Error", "Reporte no creado.")

def ventanaReporteProvincia(ventanaPadre, donadores, nombresProvincias):
    """
    Funcionamiento: abre la ventana para seleccionar la provincia del reporte de donantes.
    Entradas:
        ventanaPadre (tk.Toplevel): Ventana padre (menú de reportes).
        donadores (list): Lista de donadores en memoria.
        nombresProvincias(dict): Diccionario de códigos y nombres de provincias.
    Salidas:
        No retorna valor. Abre ventana Toplevel con selector de provincia.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Reporte - Donantes por Provincia")
    ventana.geometry("350x150")
    tk.Label(ventana, text="Seleccione la provincia:").pack(padx=10, pady=10)
    opciones = []
    for codigo, nombre in nombresProvincias.items():
        opciones.append(f"{codigo} - {nombre}")
    provinciaVar = tk.StringVar(value=opciones[0])
    tk.OptionMenu(ventana, provinciaVar, *opciones).pack(padx=10, pady=5)
    tk.Button(ventana, text="Generar reporte", width=15, command=lambda: generarReporteProvincia(provinciaVar, ventana, donadores, nombresProvincias)).pack(pady=5)
    tk.Button(ventana, text="Regresar", width=15, command=ventana.destroy).pack(pady=5)

#Reportes 2
def generarReporteRangoEdad(entryInicial, entryFinal, listaDonadores):
    """
    Funcionamiento: valida el rango de edades ingresado y genera el reporte correspondiente.
    Entradas:
        entryInicial  (tk.Entry): Campo con la edad inicial del rango.
        entryFinal (tk.Entry): Campo con la edad final del rango (puede quedar vacío).
        listaDonadores (list): Lista de donadores en memoria.
    Salidas:
        No retorna valor. Genera el archivo de reporte y muestra mensaje de resultado.
    """
    txtInicial = entryInicial.get().strip()
    txtFinal = entryFinal.get().strip()
    mensajeError = reportes.validarEdadReporte(txtInicial, txtFinal)
    if mensajeError is not None:
        messagebox.showerror("Error de validación", mensajeError)
        return
    edadInicialInt = int(txtInicial)
    edadFinalInt = int(txtFinal) if txtFinal != "" else None
    exito = reportes.reportePorRangoEdad(listaDonadores, edadInicialInt, edadFinalInt)
    if exito:
        messagebox.showinfo("Éxito", "¡Reporte generado correctamente!")
    else:
        messagebox.showerror("Error", "No se pudo crear el archivo. Verifica que exista la carpeta llamada 'reportes'.")

def ventanaReporteRangoEdad(ventanaPadre, listaDonadores):
    """
    Funcionamiento: abre la ventana para ingresar el rango de edades del reporte.
    Entradas:
        ventanaPadre (tk.Toplevel): Ventana padre (menú de reportes).
        listaDonadores (list): Lista de donadores en memoria.
    Salidas:
        No retorna valor. Abre ventana Toplevel con campos de edad inicial y final.
    """
    ventanaSecundaria = tk.Toplevel(ventanaPadre)
    ventanaSecundaria.title("Reporte - Por Rango de Edad")
    ventanaSecundaria.geometry("300x200")
    tk.Label(ventanaSecundaria, text="Edad inicial:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entryInicial = tk.Entry(ventanaSecundaria, width=10)
    entryInicial.grid(row=0, column=1, padx=10, pady=10)
    tk.Label(ventanaSecundaria, text="Edad final:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entryFinal = tk.Entry(ventanaSecundaria, width=10) 
    entryFinal.grid(row=1, column=1, padx=10, pady=10)
    tk.Button(ventanaSecundaria, text="Generar reporte", width=15, command=lambda: generarReporteRangoEdad(entryInicial, entryFinal, listaDonadores)).grid(row=2, column=0, padx=10, pady=10)
    tk.Button(ventanaSecundaria, text="Regresar", width=15, command=ventanaSecundaria.destroy).grid(row=2, column=1, padx=10, pady=10)

#Reporte 3
def generarReporteEmergencia(tipoSangreVar, provinciaVar, donadores):
    """
    Funcionamiento: genera un reporte de emergencia filtrando por tipo de sangre y provincia.
    Entradas:
        tipoSangreVar (tk.StringVar): Variable con el tipo de sangre seleccionado.
        provinciaVar (tk.StringVar): Variable con la provincia seleccionada.
        donadores (list): Lista de donadores en memoria.
    Salidas:
        No retorna valor. Genera el archivo de reporte y muestra mensaje de resultado.
    """
    tipoSangre = tipoSangreVar.get()
    provincia  = provinciaVar.get().split(" - ")[0]
    resultado = reportes.reporteEmergenciaTipoSangre(donadores, tipoSangre, provincia)
    if resultado:
        messagebox.showinfo("Éxito", "Reporte creado satisfactoriamente.")
    else:
        messagebox.showerror("Error", "Reporte no creado.")

def ventanaReporteEmergencia(ventanaPadre, donadores):
    """
    Funcionamiento: abre la ventana para seleccionar tipo de sangre y provincia del reporte de emergencia.
    Entradas:
        ventanaPadre (tk.Toplevel): Ventana padre (menú de reportes).
        donadores (list): Lista de donadores en memoria.
    Salidas:
        No retorna valor. Abre ventana Toplevel con selectores de tipo de sangre y provincia.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Reporte - Emergencia por Tipo de Sangre")
    ventana.geometry("380x220")
    tk.Label(ventana, text="Tipo de sangre:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    tipoSangreVar = tk.StringVar(value=tiposSangre[0])
    tk.OptionMenu(ventana, tipoSangreVar, *tiposSangre).grid(row=0, column=1, padx=10, pady=10, sticky="w")
    tk.Label(ventana, text="Provincia:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    opcionesProv = [f"{cod} - {nom}" for cod, nom in nombresProvincias.items()]
    provinciaVar = tk.StringVar(value=opcionesProv[0])
    tk.OptionMenu(ventana, provinciaVar, *opcionesProv).grid(row=1, column=1, padx=10, pady=10, sticky="w")
    frameBotones = tk.Frame(ventana)
    frameBotones.grid(row=2, column=0, columnspan=2, pady=15)
    tk.Button(frameBotones, text="Generar reporte", width=15,
        command=lambda: generarReporteEmergencia(tipoSangreVar, provinciaVar, donadores)
    ).grid(row=0, column=0, padx=10)
    tk.Button(frameBotones, text="Regresar", width=15,
        command=ventana.destroy
    ).grid(row=0, column=1, padx=10)

# Reporte 4
def generarReporteListaCompleta(donadores):
    """
    Funcionamiento: genera el reporte con la lista completa de todos los donadores registrados.
    Entradas:
        donadores (list): Lista de donadores en memoria.
    Salidas:
        No retorna valor. Genera el archivo de reporte y muestra mensaje de resultado.
    """
    resultado = reportes.reporteListaCompletaDonadores(donadores)
    if resultado:
        messagebox.showinfo("Éxito", "Reporte creado satisfactoriamente.")
    else:
        messagebox.showerror("Error", "Reporte no creado.")

# Reporte 5
def generarReporteMujeresONegativo(donadores):
    """
    Funcionamiento: genera el reporte de mujeres donantes con tipo de sangre O negativo.
    Entradas:
        donadores (list): Lista de donadores en memoria.
    Salidas:
        No retorna valor. Genera el archivo de reporte y muestra mensaje de resultado.
    """
    resultado = reportes.reporteMujeresONegativo(donadores)
    if resultado:
        messagebox.showinfo("Éxito", "Reporte creado satisfactoriamente.")
    else:
        messagebox.showerror("Error", "Reporte no creado.")
        
#Reporte 6
def generarReporteAQuienPuedeDonor(tipoSangreVar, donadores):
    """
    Funcionamiento: genera el reporte de compatibilidad mostrando a qué tipos de sangre puede donar.
    Entradas:
        tipoSangreVar (tk.StringVar): Variable con el tipo de sangre del donador.
        donadores (list): Lista de donadores en memoria.
    Salidas:
        No retorna valor. Genera el archivo de reporte y muestra mensaje de resultado.
    """
    tipoSangre = tipoSangreVar.get()
    resultado = reportes.reporteAQuienPuedeDonor(donadores, tipoSangre)
    if resultado:
        messagebox.showinfo("Éxito", "Reporte creado satisfactoriamente.")
    else:
        messagebox.showerror("Error", "Reporte no creado.")

def ventanaReporteAQuienPuedeDonor(ventanaPadre, donadores):
    """
    Funcionameinto: abre la ventana para seleccionar el tipo de sangre del reporte de compatibilidad (donación).
    Entradas:
        ventanaPadre (tk.Toplevel): Ventana padre (menú de reportes).
        donadores (list): Lista de donadores en memoria.
    Salidas:
        No retorna valor. Abre ventana Toplevel con selector de tipo de sangre.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Reporte - ¿A quién puede donar?")
    ventana.geometry("350x150")
    tk.Label(ventana, text="Tipo de sangre:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    tipoSangreVar = tk.StringVar(value=funciones.tiposSangre[0])
    tk.OptionMenu(ventana, tipoSangreVar, *funciones.tiposSangre).grid(row=0, column=1, padx=10, pady=10, sticky="w")
    frameBotones = tk.Frame(ventana)
    frameBotones.grid(row=1, column=0, columnspan=2, pady=15)
    tk.Button(frameBotones, text="Generar reporte", width=15,
        command=lambda: generarReporteAQuienPuedeDonor(tipoSangreVar, donadores)
    ).grid(row=0, column=0, padx=10)
    tk.Button(frameBotones, text="Regresar", width=15,
        command=ventana.destroy
    ).grid(row=0, column=1, padx=10)

#Reportes 7
def generarReporteDeQuienPuedeRecibir(tipoSangreVar, donadores):
    """
    Funcionamiento: genera el reporte mostrando de qué tipos de sangre puede recibir el tipo seleccionado.
    Entradas:
        tipoSangreVar (tk.StringVar): Variable con el tipo de sangre receptor.
        donadores (list): Lista de donadores en memoria.
    Salidas:
        No retorna valor. Genera el archivo de reporte y muestra mensaje de resultado.
    """
    tipoSangre = tipoSangreVar.get()
    resultado = reportes.reporteDeQuienPuedeRecibir(donadores, tipoSangre)
    if resultado:
        messagebox.showinfo("Éxito", "Reporte creado satisfactoriamente.")
    else:
        messagebox.showerror("Error", "Reporte no creado.")

def ventanaReporteDeQuienPuedeRecibir(ventanaPadre, donadores):
    """
    Funcionamiento: abre la ventana para seleccionar el tipo de sangre del reporte de recepción de sangre.
    Entradas:
        ventanaPadre (tk.Toplevel): Ventana padre (menú de reportes).
        donadores (list): Lista de donadores en memoria.
    Salidas:
        No retorna valor. Abre ventana Toplevel con selector de tipo de sangre.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Reporte - ¿De quién puede recibir?")
    ventana.geometry("350x150")
    tk.Label(ventana, text="Tipo de sangre:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    tipoSangreVar = tk.StringVar(value=funciones.tiposSangre[0])
    tk.OptionMenu(ventana, tipoSangreVar, *funciones.tiposSangre).grid(row=0, column=1, padx=10, pady=10, sticky="w")
    frameBotones = tk.Frame(ventana)
    frameBotones.grid(row=1, column=0, columnspan=2, pady=15)
    tk.Button(frameBotones, text="Generar reporte", width=15,
        command=lambda: generarReporteDeQuienPuedeRecibir(tipoSangreVar, donadores)
    ).grid(row=0, column=0, padx=10)
    tk.Button(frameBotones, text="Regresar", width=15,
        command=ventana.destroy
    ).grid(row=0, column=1, padx=10)

#Reporte 8
def generarReporteDonantesNoActivos(donadores):
    """
    Funcionamiento: genera el reporte de donantes que han sido marcados como inactivos en el sistema.
    Entradas:
        donadores (list): Lista de donadores en memoria.
    Salidas:
        No retorna valor. Genera el archivo de reporte y muestra mensaje de resultado.
    """
    resultado = reportes.reporteDonantesNoActivos(donadores)
    if resultado:
        messagebox.showinfo("Éxito", "Reporte creado satisfactoriamente.")
    else:
        messagebox.showerror("Error", "Reporte no creado.")

#Reportes 9
def generarReporteLugaresDonacion(donadores):
    """
    Funcionamiento: genera el reporte con todos los lugares de donación disponibles por provincia.
    Entradas:
        donadores (list): Lista de donadores en memoria.
    Salidas:
        No retorna valor. Genera el archivo de reporte y muestra mensaje de resultado.
    """
    resultado = reportes.reporteLugaresDonacion(donadores, lugaresDonacion)
    if resultado:
        messagebox.showinfo("Éxito", "Reporte creado satisfactoriamente.")
    else:
        messagebox.showerror("Error", "Reporte no creado.")

#Ventana de opciones 
def ventanaReportes(ventanaPadre, donadores):
    """
    Funcionamiento: muestra el menú principal de reportes con acceso a todos los tipos disponibles.
    Entradas:
        ventanaPadre (tk.Tk o tk.Toplevel): Ventana principal o padre.
        donadores (list): Lista de donadores en memoria.
    Salidas:
        No retorna valor. Abre ventana Toplevel con botones para cada reporte.
    """
    ventana = tk.Toplevel(ventanaPadre)
    ventana.title("Reportes")
    ventana.geometry("300x450")
    tk.Label(ventana, text="Reportes", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Button(ventana, text="1. Donantes por provincia",      width=30, command=lambda: ventanaReporteProvincia(ventana, donadores, nombresProvincias)).pack(pady=5)
    tk.Button(ventana, text="2. Por rango de edad",           width=30, command=lambda: ventanaReporteRangoEdad(ventana, donadores)).pack(pady=5)
    tk.Button(ventana, text="3. Por tipo de sangre",          width=30, command=lambda: ventanaReporteEmergencia(ventana, donadores)).pack(pady=5)
    tk.Button(ventana, text="4. Lista completa de donadores", width=30, command=lambda: generarReporteListaCompleta(donadores)).pack(pady=5)
    tk.Button(ventana, text="5. Mujeres donantes O-",         width=30, command=lambda: generarReporteMujeresONegativo(donadores)).pack(pady=5)
    tk.Button(ventana, text="6. ¿A quién puede donar?",       width=30, command=lambda: ventanaReporteAQuienPuedeDonor(ventana, donadores)).pack(pady=5)
    tk.Button(ventana, text="7. ¿De quién puede recibir?",    width=30, command=lambda: ventanaReporteDeQuienPuedeRecibir(ventana, donadores)).pack(pady=5)
    tk.Button(ventana, text="8. Donantes no activos",         width=30, command=lambda: generarReporteDonantesNoActivos(donadores)).pack(pady=5)
    tk.Button(ventana, text="9. Lugares de donación",         width=30, command=lambda: generarReporteLugaresDonacion(donadores)).pack(pady=5)
    tk.Button(ventana, text="Regresar",                       width=30, command=ventana.destroy).pack(pady=5)

#Ventana Principal
def ventanaPrincipal():
    """
    Funcionamiento: crea y muestra la ventana principal del sistema con el menú de opciones.
    Los botones 3, 4 y 6 se deshabilitan si no hay donadores cargados.
    Entradas:
        No recibe parámetros. Carga los donadores desde archivo al iniciar.
    Salidas:
        No retorna valor. Inicia el loop principal de tkinter (mainloop).
    """
    donadores = funciones.cargarDonadores()
    ventana = tk.Tk() #Crea la ventana principal
    ventana.title("Banco de Sangre - TEC") #Le ponemos titulo a la ventana
    ventana.geometry("300x400") #Definimos el tamaño de la ventana
    tk.Label(ventana, text="Sistema de Donación de Sangre", font=("Arial", 12, "bold")).pack(pady=10) #Título que ve el usuario, utilizamos "Label" solo para mostrar texto
    # Si hay donadores activa todos, si no solo 1, 2, 5 y 7
    estado = "normal" if len(donadores) > 0 else "disabled" # state="disabled" desactiva el botón; state="normal" lo habilita
    #Botones para que el usuario pueda interactuar
    tk.Button(ventana, text="1. Insertar donador",             width=30, command=lambda: insertarDonador(ventana, donadores)).pack(pady=5)
    tk.Button(ventana, text="2. Generar donadores",            width=30, command=lambda: generarDonadores(ventana, donadores)).pack(pady=5)
    tk.Button(ventana, text="3. Actualizar datos del donador", width=30, state=estado, command=lambda: actualizarDonador(ventana, donadores)).pack(pady=5)
    tk.Button(ventana, text="4. Eliminar donador",             width=30, state=estado, command=lambda: eliminarDonador(ventana, donadores)).pack(pady=5)
    tk.Button(ventana, text="5. Insertar lugar de donación",   width=30, command=lambda: insertarLugarDonacion(ventana)).pack(pady=5)
    tk.Button(ventana, text="6. Reportes",                     width=30, state=estado, command=lambda: ventanaReportes(ventana, donadores)).pack(pady=5)
    tk.Button(ventana, text="7. Salir",                        width=30, command=lambda: salir(ventana)).pack(pady=5)
    #Mantiene la ventana abierta
    ventana.mainloop() # mainloop() mantiene la ventana abierta y procesa eventos (clics, teclas, etc.)

ventanaPrincipal()