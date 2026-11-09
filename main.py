import argparse
import os
import shutil

# Tipos de archivos
extensiones = {
    "Imagenes": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "PDFs": [".pdf"],
    "Documentos": [".docx", ".doc", ".txt", ".pptx", ".xlsx", ".csv"],
    "Videos": [".mp4", ".mkv", ".mov"],
    "Musica": [".mp3", ".wav"],
    "Archivos ZIP": [".zip", ".rar", ".7z"]
}

CARPETA_OTROS = "Otros"


def carpeta_para(archivo):
    """Devuelve la carpeta que corresponde a un archivo según su extensión."""
    _, extension = os.path.splitext(archivo)

    for carpeta, extensiones_lista in extensiones.items():
        if extension.lower() in extensiones_lista:
            return carpeta

    return CARPETA_OTROS


def destino_libre(destino):
    """Si ya existe un archivo con ese nombre, agrega (1), (2)... para no sobrescribirlo."""
    if not os.path.exists(destino):
        return destino

    base, extension = os.path.splitext(destino)
    contador = 1

    while os.path.exists(f"{base} ({contador}){extension}"):
        contador += 1

    return f"{base} ({contador}){extension}"


def organizar(ruta, simular=False):
    """Mueve cada archivo de la carpeta a la subcarpeta de su tipo y devuelve cuántos movió."""
    movidos = 0

    for archivo in os.listdir(ruta):
        archivo_ruta = os.path.join(ruta, archivo)

        # Solo se mueven archivos; las carpetas se dejan como están
        if not os.path.isfile(archivo_ruta):
            continue

        carpeta = carpeta_para(archivo)
        destino = destino_libre(os.path.join(ruta, carpeta, archivo))

        if simular:
            print(f"[simulación] {archivo} → {carpeta}")
        else:
            os.makedirs(os.path.join(ruta, carpeta), exist_ok=True)
            shutil.move(archivo_ruta, destino)
            print(f"Movido: {archivo} → {carpeta}")

        movidos += 1

    return movidos


def main():
    parser = argparse.ArgumentParser(description="Organiza los archivos de una carpeta según su tipo.")
    parser.add_argument("ruta", nargs="?", help="carpeta que deseas organizar")
    parser.add_argument("--simular", action="store_true", help="muestra qué se movería sin mover nada")
    args = parser.parse_args()

    ruta = args.ruta or input("Ingresa la ruta de la carpeta que deseas organizar: ").strip()

    if not os.path.isdir(ruta):
        print(f"La carpeta no existe: {ruta}")
        return

    movidos = organizar(ruta, simular=args.simular)

    print(f"Organización completada: {movidos} archivo(s).")


if __name__ == "__main__":
    main()
