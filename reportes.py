#Importación de librerías
from datetime import datetime
from datetime import date
from datetime import date, timedelta
import funciones

#Funciones
def generarHTML(titulo, encabezados, filas, nombreArchivo):
    """
    Funcionamiento: construye un archivo HTML con una tabla a partir de los datos proporcionados
    y lo guarda en la carpeta 'reportes/'.
    Entradas:
        titulo (str): Título del reporte que aparece como <h1> en el HTML.
        encabezados (list[str]): Lista con los nombres de las columnas de la tabla.
        filas (list[list]): Lista de filas; cada fila es una lista de valores para cada columna.
        nombreArchivo (str): Nombre del archivo HTML a crear (ej: "reporte_provincia_1.html").
    Salidas:
        Retorna True si el archivo se creó correctamente, False si ocurrió algún error.
    """
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    filasHTML = ""
    for fila in filas:
        filasHTML += "<tr>"
        for dato in fila:
            filasHTML += f"<td>{dato}</td>"
        filasHTML += "</tr>"
    encabezadosHTML = ""
    for encabezado in encabezados:
        encabezadosHTML += f"<th>{encabezado}</th>"
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{titulo}</title>
</head>
<body>
    <h1>{titulo}</h1>
    <p>Fecha y hora: {ahora}</p>
    <table border="1">
        <tr>{encabezadosHTML}</tr>
        {filasHTML}
    </table>
</body>
</html>"""
    try:
        with open(f"reportes/{nombreArchivo}", "w", encoding="utf-8") as archivo:
            archivo.write(html)
        return True
    except:
        return False

#Reporte 1

def reporteDonantesporProvincia(donadores, tiposSangre, provincia, nombresProvincias):
    """
    Funcionamiento: genera un reporte HTML con los donadores activos de una provincia específica,
    ordenados alfabéticamente por nombre completo.
    Entradas:
        donadores (list): Lista de donadores en memoria.
        tiposSangre (tuple): Tupla con los tipos de sangre (no se usa directamente aquí).
        provincia (str): Código de la provincia a filtrar (ej: "1" para San José).
        nombresProvincias(dict): Diccionario de código → nombre de provincia.
    Salidas:
        Retorna True si el archivo HTML fue creado correctamente, False si ocurrió un error.
        Genera el archivo: reportes/reporte_provincia_{provincia}.html
    """
    # Filtrar donadores activos de la provincia seleccionada
    resultado = []
    for donador in donadores:
        if donador[8] == 1 and donador[1][0] == provincia:
            resultado.append(donador)
    # Ordenar por nombre completo
    resultado.sort(key=lambda d: d[0][0] + d[0][1] + d[0][2])
    # Construir filas
    filas = []
    for donador in resultado:
        nombreCompleto = " ".join(donador[0])
        dia, mes, anno = donador[4]
        fechaNac = f"{dia:02d}/{mes:02d}/{anno}"
        filas.append([donador[1], nombreCompleto, fechaNac, donador[7], donador[6]])
    nombreProvincia = nombresProvincias.get(provincia, "desconocida")
    titulo = f"Donantes por Provincia: {nombreProvincia}"
    encabezados = ["Cédula", "Nombre Completo", "Fecha de Nacimiento", "Teléfono", "Correo"]
    return generarHTML(titulo, encabezados, filas, f"reporte_provincia_{provincia}.html")

#Reporte 2
def reportePorRangoEdad(donadores, edadInicial, edadFinal):
    """
    Funcionamiento: genera un reporte HTML con los donadores activos cuya edad se encuentre
    dentro del rango especificado.
    Entradas:
        donadores (list): Lista de donadores en memoria.
        edadInicial (int): Edad mínima del rango.
        edadFinal (int | None): Edad máxima del rango. Si es None, no hay límite superior.
    Salidas:
        Retorna True si el archivo HTML fue creado correctamente, False si ocurrió un error.
        Genera el archivo: reportes/reporte_rango_edad.html
    """
    hoy = date.today()
    resultado = []
    for donador in donadores:
        if donador[8] == 1: # Solo donadores activos
            dia, mes, anno = donador[4]
            edad = (hoy - date(anno, mes, dia)).days // 365 # Calcula la edad en años a partir de la fecha de nacimiento
            if edadFinal is None:  # Sin límite superior: incluye desde edadInicial en adelante
                if edad >= edadInicial:
                    resultado.append(donador)
            else:
                if edadInicial <= edad <= edadFinal:
                    resultado.append(donador)
    filas = []
    for donador in resultado:
        nombreCompleto = " ".join(donador[0])
        dia, mes, anno = donador[4]
        fechaNac = f"{dia:02d}/{mes:02d}/{anno}"
        filas.append([donador[1], nombreCompleto, fechaNac, donador[7], donador[6]])
    titulo = "Donantes por Rango de Edad"
    encabezados = ["Cédula", "Nombre Completo", "Fecha de Nacimiento", "Teléfono", "Correo"]
    return generarHTML(titulo, encabezados, filas, "reporte_rango_edad.html")

def validarEdadReporte(edadInicial, edadFinal):
    """
    Funcionamiento: valida que los valores de edad ingresados para el reporte sean correctos.
    Entradas:
        edadInicial (str): Texto con la edad inicial ingresada por el usuario.
        edadFinal (str): Texto con la edad final ingresada (puede ser cadena vacía si no aplica).
    Salidas:
        Retorna None si los datos son válidos.
        Retorna un string con el mensaje de error si alguna validación falla.
    """
    if not edadInicial.isdigit():
        return "La edad inicial debe ser un número"
    if not (18 <= int(edadInicial) <= 65):
        return "La edad inicial debe ser entre 18 y 65 años"
    if edadFinal != "":  # La edad final es opcional; solo se valida si fue ingresada
        if not edadFinal.isdigit():
            return "La edad final debe ser un número"
        if not (18 <= int(edadFinal) <= 65):
            return "La edad final debe ser entre 18 y 65 años"
        if int(edadFinal) < int(edadInicial):
            return "La edad final no puede ser menor a la inicial"
    return None

#Reportes 3
def reporteEmergenciaTipoSangre(donadores, tipoSangreBuscado, provincia):
    """
    Funcionamiento: genera un reporte de emergencia con donadores activos de un tipo de sangre específico
    en una provincia, excluyendo quienes donaron hace menos de 8 semanas.
    Entradas:
        donadores (list): Lista de donadores en memoria.
        tipoSangreBuscado (str): Tipo de sangre requerido (ej: "O+", "AB-").
        provincia (str): Código de la provincia a filtrar.
    Salidas:
        Retorna True si el archivo HTML fue creado correctamente, False si ocurrió un error.
        Genera el archivo: reportes/reporte_emergencia_{tipo}_{provincia}.html
    """
    hoy = date.today()
    indiceTipo = funciones.tiposSangre.index(tipoSangreBuscado) # Convierte el tipo de sangre en su índice numérico para comparar con donador[2]
    resultado = []
    for donador in donadores:
        if donador[8] != 1:  # Excluye donadores inactivos
            continue
        if donador[2] != indiceTipo: # Excluye tipos de sangre diferentes
            continue
        if donador[1][0] != provincia: # Excluye provincias diferentes
            continue
        # Verifica que hayan pasado al menos 8 semanas desde la última donación
        ultimaDonacion = donador[10] if len(donador) > 10 else None
        if ultimaDonacion and (hoy - ultimaDonacion).days < 56:  # 8 semanas = 56 días
            continue # Aún no puede donar de nuevo
        resultado.append(donador)
    resultado.sort(key=lambda d: d[0][0] + d[0][1] + d[0][2]) # Ordena alfabéticamente por apellidos y nombre
    filas = []
    for donador in resultado:
        nombreCompleto = " ".join(donador[0])
        dia, mes, anno = donador[4]
        fechaNac = f"{dia:02d}/{mes:02d}/{anno}"
        filas.append([donador[1], nombreCompleto, fechaNac, donador[7], donador[6]])
    nombreProvincia = funciones.nombresProvincias.get(provincia, "desconocida")
    titulo = f"Donantes en Emergencia — Tipo {tipoSangreBuscado} — {nombreProvincia}"
    encabezados = ["Cédula", "Nombre Completo", "Fecha de Nacimiento", "Teléfono", "Correo"]
    nombreArchivo = f"reporte_emergencia_{tipoSangreBuscado.replace('+','pos').replace('-','neg')}_{provincia}.html"
    return generarHTML(titulo, encabezados, filas, nombreArchivo)

#Reporte 4
def reporteListaCompletaDonadores(donadores):
    """
    Funcionamiento: genera un reporte HTML con todos los donadores activos del sistema,
    ordenados por provincia (primer dígito de la cédula) de forma ascendente.
    Entradas:
        donadores (list): Lista de donadores en memoria.
    Salidas:
        Retorna True si el archivo HTML fue creado correctamente, False si ocurrió un error.
        Genera el archivo: reportes/reporte_lista_completa.html
    """
    resultado = [d for d in donadores if d[8] == 1] # Filtra solo donadores activos y ordena por el primer dígito de la cédula (código de provincia)
    resultado.sort(key=lambda d: d[1][0])  # ordena por provincia (primer dígito de cédula)
    filas = []
    for donador in resultado:
        nombreCompleto = " ".join(donador[0])
        dia, mes, anno = donador[4]
        fechaNac = f"{dia:02d}/{mes:02d}/{anno}"
        tipoSangre = funciones.tiposSangre[donador[2]]
        sexo = "Masculino" if donador[3] else "Femenino"
        filas.append([donador[1], nombreCompleto, tipoSangre, fechaNac, donador[5], sexo, donador[7], donador[6]])
    titulo = "Lista Completa de Donadores — Día Mundial del Donante de Sangre (14 de junio)"
    encabezados = ["Cédula", "Nombre Completo", "Tipo de Sangre", "Fecha de Nacimiento", "Peso (kg)", "Sexo", "Teléfono", "Correo"]
    return generarHTML(titulo, encabezados, filas, "reporte_lista_completa.html")

#Reporte 5
def reporteMujeresONegativo(donadores):
    """
    Funcionamiento: genera un reporte HTML con las mujeres donantes activas de tipo O negativo
    menores de 45 años, ordenadas de menor a mayor edad.
    Entradas:
        donadores (list): Lista de donadores en memoria.
    Salidas:
        Retorna True si el archivo HTML fue creado correctamente, False si ocurrió un error.
        Genera el archivo: reportes/reporte_mujeres_onegativo.html
    """
    hoy = date.today()
    indiceONeg = funciones.tiposSangre.index("O-")
    resultado = []
    for donador in donadores:
        if donador[8] != 1: # Solo activos
            continue
        if donador[3] != False: # Solo mujeres (False = Femenino)
            continue
        if donador[2] != indiceONeg: # Solo tipo O-
            continue
        dia, mes, anno = donador[4]
        edad = (hoy - date(anno, mes, dia)).days // 365
        if edad >= 45: # Excluye mayores o iguales a 45 años
            continue
        resultado.append((donador, edad))
    resultado.sort(key=lambda x: x[1]) # Ordena de menor a mayor edad
    filas = []
    for donador, edad in resultado:
        nombreCompleto = " ".join(donador[0])
        dia, mes, anno = donador[4]
        fechaNac = f"{dia:02d}/{mes:02d}/{anno}"
        filas.append([donador[1], nombreCompleto, fechaNac, donador[7], donador[6]])
    titulo = "Mujeres Donantes O- Menores de 45 Años"
    encabezados = ["Cédula", "Nombre Completo", "Fecha de Nacimiento", "Teléfono", "Correo"]
    return generarHTML(titulo, encabezados, filas, "reporte_mujeres_onegativo.html")

#Reporte 6

def reporteAQuienPuedeDonor(donadores, tipoSangreBuscado):
    """
    Funcionamiento: genera un reporte HTML con los donadores activos cuyo tipo de sangre es
    compatible para donar al tipo de sangre indicado, ordenados por provincia ascendente.
    Entradas:
        donadores (list): Lista de donadores en memoria.
        tipoSangreBuscado (str):  Tipo de sangre receptor (ej: "A+").
    Salidas:
        Retorna True si el archivo HTML fue creado correctamente, False si ocurrió un error.
        Genera el archivo: reportes/reporte_puede_donar_a_{tipo}.html
    """
    puedeDonarA = funciones.compatibilidadDonacion[tipoSangreBuscado] # Obtiene los tipos de sangre que pueden donar al tipo buscado
    indicesCompatibles = [funciones.tiposSangre.index(t) for t in puedeDonarA]
    resultado = []
    for donador in donadores:
        if donador[8] != 1: # Solo activos
            continue
        if donador[2] not in indicesCompatibles: # Solo tipos compatibles
            continue
        resultado.append(donador)
    resultado.sort(key=lambda d: d[1][0])  # Ordena por el primer dígito de la cédula (código de provincia) ascendente
    filas = []
    for donador in resultado:
        nombreCompleto = " ".join(donador[0])
        tipoSangre = funciones.tiposSangre[donador[2]]
        filas.append([donador[1], nombreCompleto, tipoSangre, donador[7], donador[6]])
    titulo = f"¿A quién puede donar? — Tipo de sangre {tipoSangreBuscado}"
    encabezados = ["Cédula", "Nombre Completo", "Tipo de Sangre", "Teléfono", "Correo"]
    nombreArchivo = f"reporte_puede_donar_a_{tipoSangreBuscado.replace('+','pos').replace('-','neg')}.html"
    return generarHTML(titulo, encabezados, filas, nombreArchivo)

#Reporte 7
def reporteDeQuienPuedeRecibir(donadores, tipoSangreBuscado):
    """
    Funcionamiento: genera un reporte HTML con los donadores activos cuyo tipo de sangre es compatible
    para ser recibido por el tipo de sangre indicado, ordenados por provincia descendente. 
    Entradas:
        donadores (list): Lista de donadores en memoria.
        tipoSangreBuscado (str): Tipo de sangre receptor (ej: "B-").
    Salidas:
        Retorna True si el archivo HTML fue creado correctamente, False si ocurrió un error.
        Genera el archivo: reportes/reporte_puede_recibir_de_{tipo}.html
    """
    puedeRecibirDe = funciones.compatibilidadRecepcion[tipoSangreBuscado] # Obtiene los tipos de sangre de los que puede recibir el tipo buscado
    indicesCompatibles = [funciones.tiposSangre.index(t) for t in puedeRecibirDe]
    resultado = []
    for donador in donadores:
        if donador[8] != 1: # Solo activos
            continue
        if donador[2] not in indicesCompatibles: # Solo tipos compatibles
            continue
        resultado.append(donador)
    resultado.sort(key=lambda d: d[1][0], reverse=True)  # Ordena por provincia de forma descendente (reverse=True)
    filas = []
    for donador in resultado:
        nombreCompleto = " ".join(donador[0])
        tipoSangre = funciones.tiposSangre[donador[2]]
        filas.append([donador[1], nombreCompleto, tipoSangre, donador[7], donador[6]])
    titulo = f"¿De quién puede recibir? — Tipo de sangre {tipoSangreBuscado}"
    encabezados = ["Cédula", "Nombre Completo", "Tipo de Sangre", "Teléfono", "Correo"]
    nombreArchivo = f"reporte_puede_recibir_de_{tipoSangreBuscado.replace('+','pos').replace('-','neg')}.html"
    return generarHTML(titulo, encabezados, filas, nombreArchivo)

#Reporte 8
def reporteDonantesNoActivos(donadores):
    """
    Funcionamiento: genera un reporte HTML con todos los donadores que han sido desactivados del sistema,
    ordenados por código de justificación de forma ascendente.
    Entradas:
        donadores (list): Lista de donadores en memoria.
    Salidas:
        Retorna True si el archivo HTML fue creado correctamente, False si ocurrió un error.
        Genera el archivo: reportes/reporte_donantes_no_activos.html
    """
    resultado = [d for d in donadores if d[8] == 0] # Filtra solo los donadores inactivos (estado == 0)
    resultado.sort(key=lambda d: d[9])  # Ordena por el código numérico de justificación (donador[9])
    filas = []
    for donador in resultado:
        nombreCompleto = " ".join(donador[0])
        dia, mes, anno = donador[4]
        fechaNac = f"{dia:02d}/{mes:02d}/{anno}"
        tipoSangre = funciones.tiposSangre[donador[2]]
        sexo = "Masculino" if donador[3] else "Femenino" 
        justificacion = funciones.justificaciones.get(donador[9], "Sin justificación")  # Obtiene el texto de la justificación a partir del código almacenado en donador[9]
        filas.append([justificacion, donador[1], nombreCompleto, tipoSangre, fechaNac, donador[5], sexo, donador[7], donador[6]])
    titulo = "Donantes No Activos"
    encabezados = ["Justificación", "Cédula", "Nombre Completo", "Tipo de Sangre", "Fecha de Nacimiento", "Peso (kg)", "Sexo", "Teléfono", "Correo"]
    return generarHTML(titulo, encabezados, filas, "reporte_donantes_no_activos.html")

#Reporte 9
def reporteLugaresDonacion(donadores, lugaresDonacion):
    """
    Funcionamiento: genera un reporte HTML con la cantidad de donadores y los centros de donación
    disponibles en cada provincia, ordenadas por código ascendente.
    Entradas:
        donadores (list): Lista de donadores en memoria.
        lugaresDonacion(dict): Diccionario de código de provincia → lista de centros de donación.
    Salidas:
        Retorna True si el archivo HTML fue creado correctamente, False si ocurrió un error.
        Genera el archivo: reportes/reporte_lugares_donacion.html
    """
    filas = []
    for codigo, nombre in sorted(funciones.nombresProvincias.items()):  # Recorre las provincias en orden ascendente por su código
        cantidad = sum(1 for d in donadores if d[1][0] == codigo) # Cuenta cuántos donadores (activos e inactivos) pertenecen a esta provincia
        lugares = lugaresDonacion.get(codigo, [])
        lugaresStr = ", ".join(lugares) if lugares else "Sin recintos registrados" # Si no hay lugares registrados, muestra un mensaje indicativo
        filas.append([nombre, cantidad, lugaresStr])
    titulo = "Lugares de Donación por Provincia"
    encabezados = ["Provincia", "Cantidad de Donadores", "Recintos de Donación"]
    return generarHTML(titulo, encabezados, filas, "reporte_lugares_donacion.html")