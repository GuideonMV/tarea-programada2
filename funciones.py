import pickle

archivoDonadores = "datos/donadores.pkl"

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

