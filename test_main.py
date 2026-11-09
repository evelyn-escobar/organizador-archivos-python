import os
import tempfile
import unittest

from main import ARCHIVO_REGISTRO, carpeta_para, deshacer, destino_libre, organizar, planificar, resumen


def crear(ruta, *nombres):
    for nombre in nombres:
        open(os.path.join(ruta, nombre), "w").close()


class OrganizadorTest(unittest.TestCase):

    def test_carpeta_segun_extension(self):
        self.assertEqual(carpeta_para("foto.JPG"), "Imagenes")
        self.assertEqual(carpeta_para("tarea.pdf"), "PDFs")
        self.assertEqual(carpeta_para("archivo.xyz"), "Otros")

    def test_no_sobrescribe_archivos(self):
        with tempfile.TemporaryDirectory() as ruta:
            crear(ruta, "tarea.pdf")
            existente = os.path.join(ruta, "tarea.pdf")
            self.assertEqual(destino_libre(existente), os.path.join(ruta, "tarea (1).pdf"))

    def test_simular_no_mueve_nada(self):
        with tempfile.TemporaryDirectory() as ruta:
            crear(ruta, "foto.png", "notas.txt")
            movimientos = organizar(ruta, simular=True)
            self.assertEqual(len(movimientos), 2)
            self.assertTrue(os.path.exists(os.path.join(ruta, "foto.png")))
            self.assertFalse(os.path.exists(os.path.join(ruta, "Imagenes")))

    def test_organizar_y_deshacer(self):
        with tempfile.TemporaryDirectory() as ruta:
            crear(ruta, "foto.png", "notas.txt", "cancion.mp3")
            os.makedirs(os.path.join(ruta, "Mis cosas"))

            movimientos = organizar(ruta)
            self.assertEqual(resumen(movimientos), {"Imagenes": 1, "Documentos": 1, "Musica": 1})
            self.assertTrue(os.path.exists(os.path.join(ruta, "Imagenes", "foto.png")))
            self.assertTrue(os.path.isdir(os.path.join(ruta, "Mis cosas")))
            self.assertTrue(os.path.exists(os.path.join(ruta, ARCHIVO_REGISTRO)))

            self.assertEqual(deshacer(ruta), 3)
            self.assertTrue(os.path.exists(os.path.join(ruta, "foto.png")))
            self.assertFalse(os.path.exists(os.path.join(ruta, "Imagenes")))
            self.assertFalse(os.path.exists(os.path.join(ruta, ARCHIVO_REGISTRO)))

    def test_nombres_repetidos_en_la_misma_tanda(self):
        with tempfile.TemporaryDirectory() as ruta:
            os.makedirs(os.path.join(ruta, "PDFs"))
            crear(os.path.join(ruta, "PDFs"), "informe.pdf")
            crear(ruta, "informe.pdf")
            destinos = [m["destino"] for m in planificar(ruta)]
            self.assertEqual(destinos, [os.path.join(ruta, "PDFs", "informe (1).pdf")])


if __name__ == "__main__":
    unittest.main()
