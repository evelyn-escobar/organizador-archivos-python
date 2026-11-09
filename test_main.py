import os
import tempfile
import unittest

from main import carpeta_para, destino_libre, organizar


class OrganizadorTest(unittest.TestCase):

    def test_carpeta_segun_extension(self):
        self.assertEqual(carpeta_para("foto.JPG"), "Imagenes")
        self.assertEqual(carpeta_para("tarea.pdf"), "PDFs")
        self.assertEqual(carpeta_para("programa.exe"), "Otros")

    def test_no_sobrescribe_archivos(self):
        with tempfile.TemporaryDirectory() as ruta:
            existente = os.path.join(ruta, "tarea.pdf")
            open(existente, "w").close()
            self.assertEqual(destino_libre(existente), os.path.join(ruta, "tarea (1).pdf"))

    def test_organizar_mueve_y_simular_no(self):
        with tempfile.TemporaryDirectory() as ruta:
            for nombre in ["foto.png", "notas.txt"]:
                open(os.path.join(ruta, nombre), "w").close()

            self.assertEqual(organizar(ruta, simular=True), 2)
            self.assertTrue(os.path.exists(os.path.join(ruta, "foto.png")))

            self.assertEqual(organizar(ruta), 2)
            self.assertTrue(os.path.exists(os.path.join(ruta, "Imagenes", "foto.png")))
            self.assertTrue(os.path.exists(os.path.join(ruta, "Documentos", "notas.txt")))


if __name__ == "__main__":
    unittest.main()
