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

