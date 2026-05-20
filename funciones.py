import pickle
import re
from datetime import date
import random

#Datos aleatorios
archivoDonadores = "datos/donadores.pkl"
nombresAleatorios = ["Carlos", "Juan", "María", "Ana", "Luis", "Laura", "Pedro", "Sofía", "Diego", "Valeria"]
apellidosAleatorios = ["González", "Rodríguez", "López", "Martínez", "Pérez", "Sánchez", "Ramírez", "Torres", "Flores", "Rivera"]
correosAleatorios = ["gmail.com", "costarricense.cr", "racsa.go.cr", "ccss.sa.cr"]

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
        0                                
    ]
    
    donadores.append(nuevoDonador)
    return donadores
