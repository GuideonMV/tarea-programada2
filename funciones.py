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
    """Funcionamiento: Carga la lista de donadores desde el archivo binario .pkl usando pickle.
    Entradas:
        Ninguna
    Salidas:
        (list) donadores: lista con todos los donadores cargados, o lista vacía si el archivo no existe
    """
    try:
        with open(archivoDonadores, "rb") as archivo: # Abre el archivo en modo lectura binaria ("rb") para deserializar con pickle
            return pickle.load(archivo)
    except FileNotFoundError: # Si el archivo no existe aún, retorna lista vacía para iniciar sin datos
        return []
    except PermissionError:
        print("El archivo está abierto en estos momentos, ciérrelo e intente de nuevo")
        return []

def guardarDonadores(donadores):
    """Funcionamiento: Guarda la lista de donadores en el archivo binario .pkl usando pickle.
    Entradas:
        (list) donadores: lista con todos los donadores a guardar
    Salidas:
        Ninguna (escribe directamente en el archivo)
    """
    try:
        with open(archivoDonadores, "wb") as archivo: # Abre el archivo en modo escritura binaria ("wb"), sobreescribe el contenido anterior
            pickle.dump(donadores, archivo)
    except PermissionError:
        print("No se pudo guardar el archivo debido a que está abierto")

#Funciones para validar
def validarCedula(cedula):
    """Funcionamiento: Valida que la cédula tenga el formato costarricense #-####-####.
    Entradas:
        (str) cedula: número de cédula ingresado por el usuario
    Salidas:
        (bool) True si el formato es válido, False en caso contrario
    """
    patron = r'^[1-9]-\d{4}-\d{4}$' # Expresión regular: primer dígito del 1-9, guión, 4 dígitos, guión, 4 dígitos
    return bool(re.match(patron, cedula))

def validarFecha(fecha):
    """Funcionamiento: Valida que la fecha tenga el formato DD/MM/AAAA y que sea una fecha real.
    Entradas:
        (str) fecha: fecha ingresada por el usuario en formato DD/MM/AAAA
    Salidas:
        (bool) True si la fecha es válida, False en caso contrario
    """
    patron = r'^\d{2}/\d{2}/\d{4}$'  # Verifica primero el formato con expresión regular antes de intentar convertirla
    if not re.match(patron, fecha):
        return False
    try:
        dia, mes, anno = map(int, fecha.split("/"))  # Intenta construir un objeto date; si la fecha no existe (ej: 30/02/2000) lanza ValueError
        date(anno, mes, dia)
        return True
    except ValueError:
        return False

def validarCorreo(correo):
    """Funcionamiento: Valida que el correo pertenezca a un dominio costarricense o gmail permitido.
    Entradas:
        (str) correo: dirección de correo ingresada por el usuario
    Salidas:
        (bool) True si el correo es válido, False en caso contrario
    """
    patron = r'^[\w.-]+@(costarricense.cr|racsa.go.cr|ccss.sa.cr|gmail.com)$' # Solo se aceptan dominios específicos costarricenses y gmail
    return bool(re.match(patron, correo, re.IGNORECASE))  # re.IGNORECASE permite correos con mayúsculas en el dominio

def validarTelefono(telefono):
    """Funcionamiento: Valida que el teléfono tenga el formato costarricense ####-####.
    Entradas:
        (str) telefono: número de teléfono ingresado por el usuario
    Salidas:
        (bool) True si el teléfono es válido, False en caso contrario
    """
    patron = r'^[246789]\d{3}-\d{4}$' # El primer dígito debe ser 2, 4, 6, 7 u 8 según numeración costarricense
    return bool(re.match(patron, telefono))

def validarPeso(pesoTexto):
    """Funcionamiento: Valida que el peso sea un número entre 50 y 120 kg (rango permitido para donar).
    Entradas:
        (str) pesoTexto: peso ingresado por el usuario como texto
    Salidas:
        (bool) True si el peso es válido, False en caso contrario
    """
    try:
        peso = float(pesoTexto)
        return 50 < peso < 120
    except ValueError:
        return False

def cedulaExiste(cedula, donadores):
    """Funcionamiento: Verifica si una cédula ya está registrada en la lista de donadores.
    Entradas:
        (str) cedula: número de cédula a buscar
        (list) donadores: lista con todos los donadores registrados
    Salidas:
        (bool) True si la cédula ya existe, False en caso contrario
    """
    for donador in donadores: # La cédula está en la posición 1 de cada donador
        if donador[1] == cedula:
            return True
    return False

def validarNombre(nombre):
    """Funcionamiento: Valida que el nombre contenga al menos nombre y dos apellidos.
    Entradas:
        (str) nombre: nombre completo ingresado por el usuario
    Salidas:
        (bool) True si tiene al menos 3 partes, False en caso contrario
    """
    partes = nombre.strip().split()
    return len(partes) >= 3

def validarEdad(fecha):
    """Funcionamiento: Verifica que el donador sea mayor de 18 años según su fecha de nacimiento.
    Entradas:
        (str) fecha: fecha de nacimiento en formato DD/MM/AAAA
    Salidas:
        (bool) True si es mayor de 18 años, False en caso contrario
    """
    dia, mes, anno = map(int, fecha.split("/"))
    hoy = date.today()
    edad = (hoy - date(anno, mes, dia)).days // 365  # Calcula la edad en años dividiendo los días de diferencia entre 365
    return edad >= 18

def validarProvincia(cedula, lugaresDonacion):
    """Funcionamiento: Obtiene los lugares de donación disponibles según la provincia de la cédula.
    Entradas:
        (str) cedula: número de cédula del donador
        (dict) lugaresDonacion: diccionario con los lugares disponibles por provincia
    Salidas:
        (str) mensaje: texto indicando la provincia y los lugares donde puede donar
    """
    provincia = cedula[0] if cedula[0] != "8" else "1" # El primer dígito de la cédula indica la provincia; si es 8 (extranjero) se asigna San José
    lugares = lugaresDonacion.get(provincia, [])
    nombreProvincia = nombresProvincias.get(provincia, "desconocida")
    return f"Dado que usted nació en la provincia de: {nombreProvincia}, usted podría donar en: {', '.join(lugares)}."

def validarPeso(peso):
    """Funcionamiento: Retorna un mensaje informativo según el peso del donador.
    Entradas:
        (float) peso: peso del donador en kilogramos
    Salidas:
        (str) mensaje: texto indicando si el peso es adecuado para donar
    """
    peso = float(peso)
    if peso <= 50:
        return "Usted debe pesar más de 50 kgms para poder ser donador"
    elif peso >= 120:
        return "Dado su sobre peso, no es posible donar sangre"
    return "Usted posee un peso adecuado, correcto para ser donador de sangre"

#Funciones para ingresar donadores (op #1)
def insertarDonador(donadores, tiposSangre, cedula, nombre, apellido1, apellido2, tipoSangre, sexo, dia, mes, anno, peso, correo, telefono):
    """Funcionamiento: Crea un nuevo donador y lo agrega a la lista de donadores.
    Entradas:
        (list) donadores: lista con todos los donadores registrados
        (tuple) tiposSangre: tupla con los tipos de sangre válidos
        (str) cedula: número de cédula del donador
        (str) nombre: primer nombre del donador
        (str) apellido1: primer apellido del donador
        (str) apellido2: segundo apellido del donador
        (str) tipoSangre: tipo de sangre del donador
        (bool) sexo: True si es masculino, False si es femenino
        (int) dia, mes, anno: fecha de nacimiento del donador
        (float) peso: peso del donador en kilogramos
        (str) correo: correo electrónico del donador
        (str) telefono: número de teléfono del donador
    Salidas:
        (list) donadores: lista actualizada con el nuevo donador agregado
    """
    indiceTipo = tiposSangre.index(tipoSangre) # Convierte el tipo de sangre a su índice en la tupla para almacenarlo de forma compacta
    nuevoDonador = [[nombre, apellido1, apellido2], cedula, indiceTipo, sexo, (dia, mes, anno), float(peso), correo, telefono, 1, 0, date.today()]
    donadores.append(nuevoDonador) # [9] Código de justificación (0 = ninguna)
    return donadores

def validarDonador(cedula, nombre, fecha, telefono, correo, peso, donadores):
    """Funcionamiento: Valida todos los campos del formulario antes de registrar un donador.
    Entradas:
        (str) cedula: número de cédula del donador
        (str) nombre: nombre completo del donador
        (str) fecha: fecha de nacimiento en formato DD/MM/AAAA
        (str) telefono: número de teléfono del donador
        (str) correo: correo electrónico del donador
        (str) peso: peso del donador como texto
        (list) donadores: lista con todos los donadores registrados
    Salidas:
        (str) mensaje de error si hay algún campo inválido, None si todos son válidos
    """
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
    """Funcionamiento: Retorna una recomendación de donación según el tipo de sangre del donador.
    Entradas:
        (str) tipoSangre: tipo de sangre del donador
    Salidas:
        (str) mensaje: recomendación personalizada según el tipo de sangre
    """
    infoSangre = {
        "A+": "Se recomienda donar sangre entera y plaquetas.",
        "A-": "Se recomienda donar sangre entera y glóbulos rojos dobles.",
        "B+": "Se recomienda donar sangre entera y glóbulos rojos dobles.",
        "B-": "Se recomienda donar sangre entera o plaquetas.",
        "O+": "Se recomienda donar glóbulos rojos dobles y sangre entera.",
        "O-": "Se recomienda donar glóbulos rojos dobles y sangre entera.",
        "AB+": "Se recomienda hacer donaciones de plaquetas y plasma.",
        "AB-": "Se recomienda donar plaquetas y plasma."
    }
    return f"Dado su tipo de sangre {tipoSangre}: {infoSangre[tipoSangre]}"

def recomendarVideoSangreA(tipoSangre):
    """Funcionamiento: Si el tipo de sangre es A+ o A-, retorna una recomendación de video informativo.
    Entradas:
        (str) tipoSangre: tipo de sangre del donador
    Salidas:
        (str) mensaje con recomendación del video, o None si no aplica
    """
    if tipoSangre in ("A+", "A-"):
        return "Recomendación: vea el video 'Particularidades de la sangre tipo A: Responde diferente al estrés según la ciencia'."
    return None

def obtenerRealimentacion(cedula, fecha, peso, tipoSangre, lugaresDonacion):
    """Funcionamiento: Genera una lista de mensajes de retroalimentación para mostrar al donador recién registrado.
    Entradas:
        (str) cedula: número de cédula del donador
        (str) fecha: fecha de nacimiento en formato DD/MM/AAAA
        (float) peso: peso del donador en kilogramos
        (str) tipoSangre: tipo de sangre del donador
        (dict) lugaresDonacion: diccionario con los lugares disponibles por provincia
    Salidas:
        (list) mensajes: lista de strings con la retroalimentación personalizada
    """
    mensajes = [validarEdad(fecha), validarProvincia(cedula, lugaresDonacion), validarPeso(peso), recomendarTipoSangre(tipoSangre)]
    video = recomendarVideoSangreA(tipoSangre)
    if video:
        mensajes.append(video)  
    return mensajes

#Funciones para generar de forma aleatoria
def generarCedula():
    """Funcionamiento: Genera un número de cédula aleatorio con formato costarricense.
    Entradas:
        Ninguna
    Salidas:
        (str) cedula: cédula generada en formato #-####-####
    """
    provincia = str(random.randint(1, 8))
    tomo = str(random.randint(1000, 9999))
    asiento = str(random.randint(1000, 9999))
    return f"{provincia}-{tomo}-{asiento}"

def generarCorreo(nombre):
    """Funcionamiento: Genera un correo electrónico aleatorio basado en el nombre del donador.
    Entradas:
        (str) nombre: nombre del donador para construir el usuario del correo
    Salidas:
        (str) correo: dirección de correo generada con dominio costarricense o gmail
    """
    usuario = f"{nombre.lower().replace(' ', '')}{random.randint(1,99)}" # Elimina espacios y convierte a minúsculas para formar el usuario, agrega número aleatorio
    dominio = random.choice(["costarricense.cr", "racsa.go.cr", "ccss.sa.cr", "gmail.com"])
    return f"{usuario}@{dominio}"

def generarTelefono():
    """Funcionamiento: Genera un número de teléfono aleatorio con formato costarricense.
    Entradas:
        Ninguna
    Salidas:
        (str) telefono: número de teléfono en formato ####-####
    """
    # El primer dígito debe ser uno de los válidos según numeración costarricense
    return f"{random.choice([2,4,6,7,8])}{random.randint(100,999)}-{random.randint(1000,9999)}"

def determinarEstado(peso, anno):
    """Funcionamiento: Determina si un donador generado aleatoriamente debe ser activo o inactivo.
    Entradas:
        (float) peso: peso del donador en kilogramos
        (int) anno: año de nacimiento del donador
    Salidas:
        (int) estado: 1 si es activo, 0 si es inactivo
        (int) justificacion: código de justificación si es inactivo, 0 si es activo
    """
    if peso <= 50 or peso >= 120:
        return 0, 3
    elif anno > 2007:
        return 0, 1
    else:
        return 1, 0

#Funciones para generar donadores de manera masiva (op#2)
def crearDonador(tiposSangre):
    """Funcionamiento: Crea un donador con datos generados aleatoriamente usando la librería Faker.
    Entradas:
        (tuple) tiposSangre: tupla con los tipos de sangre válidos
    Salidas:
        (list) donador: lista con todos los datos del donador generado
        (str) cedula: cédula del donador generado (para verificar duplicados)
    """
    nombre   = fake.first_name()
    apellido1 = fake.last_name()
    apellido2 = fake.last_name()
    cedula   = generarCedula()
    tipoSangre = random.choice(tiposSangre)
    sexo     = random.choice([True, False])
    dia      = random.randint(1, 28) # Máximo 28 para evitar días inválidos en todos los meses
    mes      = random.randint(1, 12)
    anno     = random.randint(1950, 2010)
    peso     = round(random.uniform(40, 130), 1)
    correo   = generarCorreo(nombre)
    telefono = generarTelefono()
    estado, justificacion = determinarEstado(peso, anno)
    fechaUltimaDonacion = date.today() - timedelta(days=random.randint(0, 180))  # Genera una fecha de última donación aleatoria entre hoy y 180 días atrás (~6 meses)
    return [[nombre, apellido1, apellido2], cedula, tiposSangre.index(tipoSangre), sexo, (dia, mes, anno), float(peso), correo, telefono, estado, justificacion, fechaUltimaDonacion], cedula

def generarDonadores(donadores, tiposSangre, cantidad):
    """Funcionamiento: Genera e inserta una cantidad dada de donadores aleatorios en la lista.
    Entradas:
        (list) donadores: lista con todos los donadores registrados
        (tuple) tiposSangre: tupla con los tipos de sangre válidos
        (int) cantidad: número de donadores a generar
    Salidas:
        (list) donadores: lista actualizada con los nuevos donadores agregados
    """
    for x in range(cantidad):
        donador, cedula = crearDonador(tiposSangre)
        if not cedulaExiste(cedula, donadores): # Verifica que la cédula generada no exista ya en la base de datos
            donadores.append(donador)
    return donadores

#Funiones para actualizar donadores (op#3)
def buscarDonador(cedula, donadores):
    """Funcionamiento: Busca un donador en la lista por su número de cédula.
    Entradas:
        (str) cedula: número de cédula a buscar
        (list) donadores: lista con todos los donadores registrados
    Salidas:
        (int) índice del donador en la lista, o -1 si no se encuentra
    """
    for i, donador in enumerate(donadores): # Verifica que la cédula generada no exista ya en la base de datos
        if donador[1] == cedula:
            return i
    return -1

def validarDonadorActualizar(cedula, nombre, fecha, telefono, correo, peso):
    """Funcionamiento: Valida los campos del formulario al actualizar los datos de un donador.
    Entradas:
        (str) cedula: número de cédula del donador (solo para referencia, no se modifica)
        (str) nombre: nombre completo del donador
        (str) fecha: fecha de nacimiento en formato DD/MM/AAAA
        (str) telefono: número de teléfono del donador
        (str) correo: correo electrónico del donador
        (str) peso: peso del donador como texto
    Salidas:
        (str) mensaje de error si hay algún campo inválido, None si todos son válidos
    """
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
    """Funcionamiento: Actualiza los datos de un donador existente en la lista.
    Entradas:
        (list) donadores: lista con todos los donadores registrados
        (tuple) tiposSangre: tupla con los tipos de sangre válidos
        (int) indice: posición del donador en la lista
        (str) nombre: nuevo primer nombre del donador
        (str) apellido1: nuevo primer apellido del donador
        (str) apellido2: nuevo segundo apellido del donador
        (str) tipoSangre: nuevo tipo de sangre del donador
        (bool) sexo: True si es masculino, False si es femenino
        (int) dia, mes, anno: nueva fecha de nacimiento del donador
        (float) peso: nuevo peso del donador en kilogramos
        (str) correo: nuevo correo electrónico del donador
        (str) telefono: nuevo número de teléfono del donador
    Salidas:
        (list) donadores: lista actualizada con los datos del donador modificados
    """ 
    indiceTipo = tiposSangre.index(tipoSangre) # Convierte el tipo de sangre a índice para mantener consistencia con la estructura
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
    """Funcionamiento: Marca un donador como inactivo en la lista (eliminación lógica, no física).
    Entradas:
        (str) cedula: número de cédula del donador a eliminar
        (list) donadores: lista con todos los donadores registrados
        (int) justificacion: código de justificación para la inactivación
    Salidas:
        (bool) True si el donador fue encontrado e inactivado, False si no se encontró
    """
    for donador in donadores:
        if donador[1] == cedula: 
            donador[8] = 0 # Cambia estado a inactivo
            donador[9] = justificacion # Guarda el código de justificación
            return True
    return False

