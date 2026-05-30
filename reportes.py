from datetime import datetime
import funciones

def generarHTML(titulo, encabezados, filas, nombreArchivo):
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
    # Filtrar donadores activos de la provincia seleccionada
    resultado = []
    for donador in donadores:
        if donador[8] == 1 and donador[1][0] == provincia:
            resultado.append(donador)
    # Ordenar por nombre completo
    resultado.sort(key=lambda donador: donador[0][0] + donador[0][1] + donador[0][2])
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
    return generarHTML(titulo, encabezados, filas, f"reporte-provincia-{provincia}.html")
