"""Ventana del Organizador de Archivos (tkinter, incluido en Python)."""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from main import ARCHIVO_REGISTRO, deshacer, organizar, planificar, resumen

COLOR = "#2563eb"


class OrganizadorApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Organizador de Archivos")
        self.geometry("760x520")
        self.minsize(600, 420)
        self.ruta = tk.StringVar()
        self.estado = tk.StringVar(value="Elige una carpeta para empezar.")
        self._construir()

    def _construir(self):
        estilo = ttk.Style(self)
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 16, "bold"), foreground=COLOR)
        estilo.configure("Accion.TButton", font=("Segoe UI", 10, "bold"))

        marco = ttk.Frame(self, padding=16)
        marco.pack(fill="both", expand=True)

        ttk.Label(marco, text="📂 Organizador de Archivos", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(marco, text="Ordena una carpeta en subcarpetas según el tipo de archivo: imágenes, PDFs, documentos, música...").pack(anchor="w", pady=(2, 12))

        fila = ttk.Frame(marco)
        fila.pack(fill="x")
        ttk.Entry(fila, textvariable=self.ruta).pack(side="left", fill="x", expand=True)
        ttk.Button(fila, text="Elegir carpeta...", command=self.elegir).pack(side="left", padx=(8, 0))

        botones = ttk.Frame(marco)
        botones.pack(fill="x", pady=12)
        ttk.Button(botones, text="👀 Vista previa", command=self.vista_previa).pack(side="left")
        ttk.Button(botones, text="✅ Organizar", style="Accion.TButton", command=self.organizar).pack(side="left", padx=8)
        ttk.Button(botones, text="↩ Deshacer", command=self.deshacer).pack(side="left")

        columnas = ("archivo", "carpeta")
        self.tabla = ttk.Treeview(marco, columns=columnas, show="headings")
        self.tabla.heading("archivo", text="Archivo")
        self.tabla.heading("carpeta", text="Irá a la carpeta")
        self.tabla.column("archivo", width=440)
        self.tabla.column("carpeta", width=200)

        barra = ttk.Scrollbar(marco, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="left", fill="y")

        ttk.Label(self, textvariable=self.estado, padding=(16, 8), relief="sunken").pack(fill="x", side="bottom")

    def _carpeta_valida(self):
        ruta = self.ruta.get().strip()

        if not os.path.isdir(ruta):
            messagebox.showwarning("Carpeta no válida", "Elige una carpeta que exista.")
            return None

        return ruta

    def _mostrar(self, movimientos):
        self.tabla.delete(*self.tabla.get_children())

        for mov in movimientos:
            self.tabla.insert("", "end", values=(mov["archivo"], mov["carpeta"]))

    def elegir(self):
        ruta = filedialog.askdirectory(title="Elige la carpeta que quieres organizar")

        if ruta:
            self.ruta.set(ruta)
            self.vista_previa()

    def vista_previa(self):
        ruta = self._carpeta_valida()

        if not ruta:
            return

        movimientos = planificar(ruta)
        self._mostrar(movimientos)

        if movimientos:
            detalle = ", ".join(f"{c}: {n}" for c, n in resumen(movimientos).items())
            self.estado.set(f"Vista previa: se moverán {len(movimientos)} archivo(s). {detalle}")
        else:
            self.estado.set("No hay archivos sueltos para organizar en esta carpeta.")

    def organizar(self):
        ruta = self._carpeta_valida()

        if not ruta:
            return

        cantidad = len(planificar(ruta))

        if cantidad == 0:
            self.estado.set("No hay archivos sueltos para organizar en esta carpeta.")
            return

        if not messagebox.askyesno("Confirmar", f"¿Mover {cantidad} archivo(s) a sus carpetas?"):
            return

        movimientos = organizar(ruta)
        self._mostrar(movimientos)
        self.estado.set(f"Listo: se organizaron {len(movimientos)} archivo(s). Puedes deshacerlo con «Deshacer».")

    def deshacer(self):
        ruta = self._carpeta_valida()

        if not ruta:
            return

        if not os.path.exists(os.path.join(ruta, ARCHIVO_REGISTRO)):
            messagebox.showinfo("Nada que deshacer", "No hay una organización reciente en esta carpeta.")
            return

        restaurados = deshacer(ruta)
        self._mostrar([])
        self.estado.set(f"Se devolvieron {restaurados} archivo(s) a su lugar original.")


if __name__ == "__main__":
    OrganizadorApp().mainloop()
