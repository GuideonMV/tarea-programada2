import pickle
import re
from datetime import date
import random
from faker import Faker
from datetime import date, timedelta

#Datos aleatorios
fake = Faker('es_MX')
archivoDonadores = "datos/donadores.pkl"

#Variables Globales
nombresProvincias = {
    "1": "San José", "2": "Alajuela", "3": "Cartago",
    "4": "Heredia", "5": "Guanacaste", "6": "Puntarenas", "7": "Limón"
}

compatibilidadDonacion = {
    "O+":  ["O+", "A+", "B+", "AB+"],
    "O-":  ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"],
    "A+":  ["A+", "AB+"],
    "A-":  ["A+", "A-", "AB+", "AB-"],
    "B+":  ["B+", "AB+"],
    "B-":  ["B+", "B-", "AB+", "AB-"],
    "AB+": ["AB+"],
    "AB-": ["AB+", "AB-"],
}

compatibilidadRecepcion = {
    "O+":  ["O+", "O-"],
    "O-":  ["O-"],
    "A+":  ["A+", "A-", "O+", "O-"],
    "A-":  ["A-", "O-"],
    "B+":  ["B+", "B-", "O+", "O-"],
    "B-":  ["B-", "O-"],
    "AB+": ["AB+", "AB-", "A+", "A-", "B+", "B-", "O+", "O-"],
    "AB-": ["AB-", "A-", "B-", "O-"],
}

tiposSangre = ("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-")

justificaciones = {
    1: "Enfermedades Infecciosas/Crónicas: Portadores de VIH, Hepatitis B o C, sífilis, tuberculosis, o pacientes diabéticos insulinodependientes.",
    2: "Conductas de Riesgo: Nuevas parejas sexuales o más de una pareja sexual en los últimos 3 meses.",
    3: "Factores de Salud Física: Hemoglobina/hematocrito bajo o alto, presión arterial inestable, fiebre, o infecciones recientes.",
    4: "Procedimientos Médicos: Haber recibido transfusiones, trasplantes, cirugías mayores, tatuajes, piercing o endoscopias recientes.",
    5: "Uso de Medicamentos: Consumo de fármacos inyectables sin receta o ciertos medicamentos.",
    6: "Estilo de Vida y Viajes: Uso de drogas recreativas, consumo de alcohol en las últimas 24 horas, o viajes a zonas endémicas.",
    7: "Situaciones Específicas: Embarazo, lactancia o menstruación."
}

#Funciones para la base de datos
def cargarDonadores():
    try:
        with open(archivoDonadores, "rb") as archivo:
            return pickle.load(archivo)
    except FileNotFoundError:
        return []
    except PermissionError:
        print("El archivo está abierto en estos momentos, ciérrelo e intente de nuevo")
        return []

def guardarDonadores(donadores):
    try:
        with open(archivoDonadores, "wb") as archivo:
            pickle.dump(donadores, archivo)
    except PermissionError:
        print("No se pudo guardar el archivo debido a que está abierto")

#Funciones para validar
def validarCedula(cedula):
    patron = r'^[1-9]-\d{4}-\d{4}$'
    return bool(re.match(patron, cedula))

def validarFecha(fecha):
    patron = r'^\d{2}/\d{2}/\d{4}$'
    if not re.match(patron, fecha):
        return False
    try:
        dia, mes, anno = map(int, fecha.split("/"))
        date(anno, mes, dia)
        return True
    except ValueError:
        return False

def validarCorreo(correo):
    patron = r'^[\w.-]+@(costarricense.cr|racsa.go.cr|ccss.sa.cr|gmail.com)$'
    return bool(re.match(patron, correo, re.IGNORECASE))

def validarTelefono(telefono):
    patron = r'^[246789]\d{3}-\d{4}$'
    return bool(re.match(patron, telefono))

def validarPeso(pesoTexto):
    try:
        peso = float(pesoTexto)
        return 50 < peso < 120
    except ValueError:
        return False

def cedulaExiste(cedula, donadores):
    for donador in donadores:
        if donador[1] == cedula:
            return True
    return False

def validarNombre(nombre):
    partes = nombre.strip().split()
    return len(partes) >= 3

def validarEdad(fecha):
    dia, mes, anno = map(int, fecha.split("/"))
    hoy = date.today()
    edad = (hoy - date(anno, mes, dia)).days // 365
    return edad >= 18

def validarProvincia(cedula, lugaresDonacion):
    provincia = cedula[0] if cedula[0] != "8" else "1"
    lugares = lugaresDonacion.get(provincia, [])
    nombreProvincia = nombresProvincias.get(provincia, "desconocida")
    return f"Dado que usted nació en la provincia de: {nombreProvincia}, usted podría donar en: {', '.join(lugares)}."

def validarPeso(peso):
    peso = float(peso)
    if peso <= 50:
        return "Usted debe pesar más de 50 kgms para poder ser donador"
    elif peso >= 120:
        return "Dado su sobre peso, no es posible donar sangre"
    return "Usted posee un peso adecuado, correcto para ser donador de sangre"

#Funciones para ingresar donadores (op #1)
def insertarDonador(donadores, tiposSangre, cedula, nombre, apellido1, apellido2, tipoSangre, sexo, dia, mes, anno, peso, correo, telefono):
    indiceTipo = tiposSangre.index(tipoSangre)
    nuevoDonador = [
        [nombre, apellido1, apellido2],
        cedula,
        indiceTipo,
        sexo,
        (dia, mes, anno),
        float(peso),
        correo,
        telefono,
        1,
        0,
        date.today()
    ]
    donadores.append(nuevoDonador)
    return donadores

def validarDonador(cedula, nombre, fecha, telefono, correo, peso, donadores):
    if not validarCedula(cedula):
        return "Cédula inválida. Formato: #-####-####"
    if not validarNombre(nombre):
        return "Ingrese nombre y dos apellidos"
    if not validarFecha(fecha):
        return "Fecha inválida o el donador debe ser mayor de 18 años. Formato: DD/MM/AAAA"
    if not validarTelefono(telefono):
        return "Teléfono inválido. Formato: ####-####"
    if not validarCorreo(correo):
        return "Correo inválido"
    if not validarPeso(peso):
        return "Peso inválido. Debe ser mayor a 50 y menor a 120"
    if cedulaExiste(cedula, donadores):
        return "Esta cédula ya está registrada"
    if not validarEdad(fecha):
        return "El donador debe ser mayor de 18 años"
    return None

def recomendarTipoSangre(tipoSangre):
    infoSangre = {
        "A+": "Se recomienda donar sangre entera y plaquetas",
        "A-": "Se recomienda donar sangre entera y glóbulos rojos dobles",
        "B+": "Se recomienda donar sangre entera y glóbulos rojos dobles",
        "B-": "Se recomienda donar sangre entera o plaquetas",
        "O+": "Se recomienda donar glóbulos rojos dobles y sangre entera",
        "O-": "Se recomienda donar glóbulos rojos dobles y sangre entera",
        "AB+": "Se recomienda hacer donaciones de plaquetas y plasma",
        "AB-": "Se recomienda donar plaquetas y plasma"
    }
    return f"Dado su tipo de sangre {tipoSangre}: {infoSangre[tipoSangre]}"

def recomendarVideoSangreA(tipoSangre):
    if tipoSangre in ("A+", "A-"):
        return "Recomendación: vea el video 'Particularidades de la sangre tipo A: Responde diferente al estrés según la ciencia'"
    return None

def obtenerRealimentacion(cedula, fecha, peso, tipoSangre, lugaresDonacion):
    mensajes = [
        validarEdad(fecha),
        validarProvincia(cedula, lugaresDonacion),
        validarPeso(peso),
        recomendarTipoSangre(tipoSangre),
    ]
    video = recomendarVideoSangreA(tipoSangre)
    if video:
        mensajes.append(video)
    return mensajes

#Funciones para generar de forma aleatoria
def generarCedula():
    provincia = str(random.randint(1, 8))
    tomo = str(random.randint(1000, 9999))
    asiento = str(random.randint(1000, 9999))
    return f"{provincia}-{tomo}-{asiento}"

def generarCorreo(nombre):
    usuario = f"{nombre.lower().replace(' ', '')}{random.randint(1,99)}"
    dominio = random.choice(["costarricense.cr", "racsa.go.cr", "ccss.sa.cr", "gmail.com"])
    return f"{usuario}@{dominio}"

def generarTelefono():
    return f"{random.choice([2,4,6,7,8])}{random.randint(100,999)}-{random.randint(1000,9999)}"

def determinarEstado(peso, anno):
    if peso <= 50 or peso >= 120:
        return 0, 3
    elif anno > 2007:
        return 0, 1
    else:
        return 1, 0

#Funciones para generar donadores de manera masiva (op#2)
def crearDonador(tiposSangre):
    nombre   = fake.first_name()
    apellido1 = fake.last_name()
    apellido2 = fake.last_name()
    cedula   = generarCedula()
    tipoSangre = random.choice(tiposSangre)
    sexo     = random.choice([True, False])
    dia      = random.randint(1, 28)
    mes      = random.randint(1, 12)
    anno     = random.randint(1950, 2010)
    peso     = round(random.uniform(40, 130), 1)
    correo   = generarCorreo(nombre)
    telefono = generarTelefono()
    estado, justificacion = determinarEstado(peso, anno)
    fechaUltimaDonacion = date.today() - timedelta(days=random.randint(0, 180))
    return [
        [nombre, apellido1, apellido2], cedula, tiposSangre.index(tipoSangre),
        sexo,
        (dia, mes, anno),
        float(peso),
        correo,
        telefono,
        estado,
        justificacion,
        fechaUltimaDonacion], cedula

def generarDonadores(donadores, tiposSangre, cantidad):
    for x in range(cantidad):
        donador, cedula = crearDonador(tiposSangre)
        if not cedulaExiste(cedula, donadores):
            donadores.append(donador)
    return donadores

#Funiones para actualizar donadores (op#3)
def buscarDonador(cedula, donadores):
    for i, donador in enumerate(donadores):
        if donador[1] == cedula:
            return i
    return -1

def validarDonadorActualizar(cedula, nombre, fecha, telefono, correo, peso):
    if not validarNombre(nombre):
        return "Ingrese nombre y dos apellidos"
    if not validarFecha(fecha):
        return "Fecha inválida. Formato: DD/MM/AAAA"
    if not validarEdad(fecha):
        return "El donador debe ser mayor de 18 años"
    if not validarTelefono(telefono):
        return "Teléfono inválido. Formato: ####-####"
    if not validarCorreo(correo):
        return "Correo inválido"
    if not validarPeso(peso):
        return "Peso inválido. Debe ser mayor a 50 y menor a 120"
    return None

def actualizarDonador(donadores, tiposSangre, indice, nombre, apellido1, apellido2, tipoSangre, sexo, dia, mes, anno, peso, correo, telefono):
    indiceTipo = tiposSangre.index(tipoSangre)
    donadores[indice][0] = [nombre, apellido1, apellido2]
    donadores[indice][2] = indiceTipo
    donadores[indice][3] = sexo
    donadores[indice][4] = (dia, mes, anno)
    donadores[indice][5] = float(peso)
    donadores[indice][6] = correo
    donadores[indice][7] = telefono
    return donadores

#Funciones para eliminar donador (op#4)
def eliminarDonador(cedula, donadores, justificacion):
    for donador in donadores:
        if donador[1] == cedula:
            donador[8] = 0
            donador[9] = justificacion
            return True
    return False