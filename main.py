import argparse
import json
import os
import shutil

# Tipos de archivos
extensiones = {
    "Imagenes": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"],
    "PDFs": [".pdf"],
    "Documentos": [".docx", ".doc", ".txt", ".pptx", ".ppt", ".xlsx", ".xls", ".csv", ".odt"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Musica": [".mp3", ".wav", ".m4a", ".flac"],
    "Archivos ZIP": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Programas": [".exe", ".msi"]
}

CARPETA_OTROS = "Otros"

# Registro de la última organización, para poder deshacerla
ARCHIVO_REGISTRO = ".organizador_registro.json"


def carpeta_para(archivo):
    """Devuelve la carpeta que corresponde a un archivo según su extensión."""
    _, extension = os.path.splitext(archivo)

    for carpeta, extensiones_lista in extensiones.items():
        if extension.lower() in extensiones_lista:
            return carpeta

    return CARPETA_OTROS


def destino_libre(destino, reservados=()):
    """Si ya existe un archivo con ese nombre, agrega (1), (2)... para no sobrescribirlo."""
    if not os.path.exists(destino) and destino not in reservados:
        return destino

    base, extension = os.path.splitext(destino)
    contador = 1

    while os.path.exists(f"{base} ({contador}){extension}") or f"{base} ({contador}){extension}" in reservados:
        contador += 1

    return f"{base} ({contador}){extension}"


def planificar(ruta):
    """Calcula qué archivo va a qué carpeta, sin mover nada. Devuelve una lista de movimientos."""
    movimientos = []
    reservados = set()

    for archivo in sorted(os.listdir(ruta)):
        archivo_ruta = os.path.join(ruta, archivo)

        # Solo se mueven archivos; las carpetas y el registro se dejan como están
        if not os.path.isfile(archivo_ruta) or archivo == ARCHIVO_REGISTRO:
            continue

        carpeta = carpeta_para(archivo)
        destino = destino_libre(os.path.join(ruta, carpeta, archivo), reservados)
        reservados.add(destino)

        movimientos.append({"archivo": archivo, "carpeta": carpeta, "origen": archivo_ruta, "destino": destino})

    return movimientos


def organizar(ruta, simular=False):
    """Mueve cada archivo a la carpeta de su tipo. Devuelve la lista de movimientos realizados."""
    movimientos = planificar(ruta)

    if simular:
        return movimientos

    for mov in movimientos:
        os.makedirs(os.path.dirname(mov["destino"]), exist_ok=True)
        shutil.move(mov["origen"], mov["destino"])

    if movimientos:
        with open(os.path.join(ruta, ARCHIVO_REGISTRO), "w", encoding="utf-8") as f:
            json.dump(movimientos, f, ensure_ascii=False, indent=2)

    return movimientos


def deshacer(ruta):
    """Devuelve los archivos a su lugar original según el registro de la última organización."""
    registro = os.path.join(ruta, ARCHIVO_REGISTRO)

    if not os.path.exists(registro):
        return 0

    with open(registro, encoding="utf-8") as f:
        movimientos = json.load(f)

    restaurados = 0

    for mov in movimientos:
        if os.path.exists(mov["destino"]) and not os.path.exists(mov["origen"]):
            shutil.move(mov["destino"], mov["origen"])
            restaurados += 1

    # Borra las carpetas que quedaron vacías
    for carpeta in {os.path.dirname(mov["destino"]) for mov in movimientos}:
        if os.path.isdir(carpeta) and not os.listdir(carpeta):
            os.rmdir(carpeta)

    os.remove(registro)

    return restaurados


def resumen(movimientos):
    """Cuenta cuántos archivos van a cada carpeta, por ejemplo {'PDFs': 2, 'Imagenes': 5}."""
    conteo = {}

    for mov in movimientos:
        conteo[mov["carpeta"]] = conteo.get(mov["carpeta"], 0) + 1

    return conteo


def main():
    parser = argparse.ArgumentParser(description="Organiza los archivos de una carpeta según su tipo.")
    parser.add_argument("ruta", nargs="?", help="carpeta que deseas organizar")
    parser.add_argument("--simular", action="store_true", help="muestra qué se movería sin mover nada")
    parser.add_argument("--deshacer", action="store_true", help="devuelve los archivos a su lugar original")
    args = parser.parse_args()

    ruta = args.ruta or input("Ingresa la ruta de la carpeta que deseas organizar: ").strip()

    if not os.path.isdir(ruta):
        print(f"La carpeta no existe: {ruta}")
        return

    if args.deshacer:
        print(f"Se restauraron {deshacer(ruta)} archivo(s).")
        return

    movimientos = organizar(ruta, simular=args.simular)

    for mov in movimientos:
        prefijo = "[simulación] " if args.simular else ""
        print(f"{prefijo}{mov['archivo']} → {mov['carpeta']}")

    detalle = ", ".join(f"{carpeta}: {cantidad}" for carpeta, cantidad in resumen(movimientos).items())

    print(f"Total: {len(movimientos)} archivo(s). {detalle}")


if __name__ == "__main__":
    main()
