# 📂 Organizador Inteligente de Archivos

Herramienta en **Python** que ordena automáticamente una carpeta desordenada, moviendo cada archivo a una subcarpeta según su tipo: imágenes, PDFs, documentos, música, videos y más.

Se puede usar con una **ventana gráfica** sencilla o desde la **línea de comandos**, y permite **deshacer** la última organización.

---

## Funcionalidades

- **Ventana gráfica (tkinter):** eliges la carpeta, ves la vista previa en una tabla y organizas con un clic.
- **Vista previa:** muestra qué archivo irá a cada carpeta antes de mover nada.
- **Deshacer:** devuelve los archivos a su lugar original y borra las carpetas que quedaron vacías.
- **No sobrescribe archivos:** si el nombre ya existe, agrega (1), (2)...
- **Carpeta "Otros":** para los tipos de archivo no reconocidos.
- **Respeta las subcarpetas existentes:** solo mueve archivos sueltos.
- **Resumen:** al terminar indica cuántos archivos fueron a cada carpeta.

| Carpeta | Extensiones |
|---|---|
| Imagenes | jpg, jpeg, png, gif, webp, bmp, svg |
| PDFs | pdf |
| Documentos | docx, doc, txt, pptx, ppt, xlsx, xls, csv, odt |
| Videos | mp4, mkv, mov, avi |
| Musica | mp3, wav, m4a, flac |
| Archivos ZIP | zip, rar, 7z, tar, gz |
| Programas | exe, msi |
| Otros | cualquier otra |

## Tecnologías

- Python 3, solo con la librería estándar: `os`, `shutil`, `json`, `argparse`, `tkinter`
- `unittest` para las pruebas automáticas

## Cómo usarlo

```bash
git clone https://github.com/evelyn-escobar/organizador-archivos-python.git
cd organizador-archivos-python
```

### Con la ventana gráfica

```bash
python gui.py
```

1. Haz clic en **Elegir carpeta...**
2. Revisa la **vista previa**.
3. Haz clic en **Organizar** y confirma.
4. Si te arrepientes, usa **Deshacer**.

### Desde la línea de comandos

```bash
# Te pide la ruta de la carpeta
python main.py

# O pásala directamente
python main.py carpeta_prueba

# Ver qué se movería, sin mover nada
python main.py carpeta_prueba --simular

# Devolver los archivos a su lugar
python main.py carpeta_prueba --deshacer
```

## Ejemplo

```plaintext
Antes                     Después
carpeta_prueba/           carpeta_prueba/
├── foto.jpg              ├── Imagenes/
├── tarea.pdf             │   └── foto.jpg
├── musica.mp3            ├── PDFs/
└── video.mp4             │   └── tarea.pdf
                          ├── Musica/
                          │   └── musica.mp3
                          └── Videos/
                              └── video.mp4
```

## Pruebas

```bash
python -m unittest
```

Las pruebas crean carpetas temporales y verifican la clasificación por extensión, que no se sobrescriban archivos, la vista previa, la organización y el deshacer.

## Estructura

```plaintext
organizador-archivos-python/
├── main.py          # Lógica de organización y línea de comandos
├── gui.py           # Ventana gráfica
├── test_main.py     # Pruebas automáticas
└── carpeta_prueba/  # Archivos de ejemplo
```

## Autora

**Evelyn Daniela Escobar** – Estudiante de Tecnología en Desarrollo de Software (UNAD).
