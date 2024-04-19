import tkinter

import customtkinter
import DetectorDePlagio
import tkinter as tk
from tkinter import filedialog


class App(customtkinter.CTk, tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("Detector de plagio")

        # TODO: Variables de control para las opciones
        # self.usar_lematizacion = tk.BooleanVar(value=False)
        # self.usar_stemming = tk.BooleanVar(value=True)

        # TODO: Crear widgets para seleccionar opciones
        # self.checkbox_lematizacion = tk.Checkbutton(self, text="Usar lematización", variable=self.usar_lematizacion)
        # self.checkbox_lematizacion.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        # self.checkbox_stemming = tk.Checkbutton(self, text="Usar stemming", variable=self.usar_stemming)
        # self.checkbox_stemming.grid(row=2, column=0, padx=20, pady=5, sticky="w")

        # Boton para la seleccion de archivo
        self.button = customtkinter.CTkButton(self, text="Seleccionar Archivo", command=self.select_file)
        self.button.grid(row=0, column=0, padx=20, pady=10)

    # add methods to app
    def select_file(self):
        # TODO: Obtener los valores seleccionados
        # usar_lematizacion = self.usar_lematizacion.get()
        # usar_stemming = self.usar_stemming.get()

        file_path = filedialog.askopenfilename(title="Seleccionar archivo de texto",
                                               filetypes=[("Archivos de texto", "*.txt")])
        if file_path:
            self.detect_plagiarism(file_path)

    def detect_plagiarism(self, file_path):
        """
        Esta funcion es el trigger para detectar plagio en un archivo comparado con los archivos de la base de datos

        """
        ruta_de_archivos = "/Users/sergiogonzalez/Documents/GitHub/DetectorPlagio/app/Resumenes_texto/"
        archivo_preprocesado = DetectorDePlagio.DetectorDePlagio().preprocesar_texto(file_path, ruta_de_archivos)
        # TODO: Habilitar la deteccion de plagio
        # detecccion_de_plagio = DetectorDePlagio.DetectorDePlagio().deteccion_de_plagio(archivo_preprocesado, 1)
        print("Detección de plagio en el archivo:", archivo_preprocesado)


app = App()
app.mainloop()
