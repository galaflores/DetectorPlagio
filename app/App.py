import tkinter as tk
from tkinter import filedialog
import os
from typing import List, Any
from sklearn.metrics.pairwise import cosine_similarity
import customtkinter
import DetectorDePlagio
import sys


class App(customtkinter.CTk, tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("550x600")
        self.title("Detector de plagio")
        self.path_plagiados = "/Users/sergiogonzalez/Documents/GitHub/DetectorPlagio/textos_plagiados" # Cambiar la ruta.

        # TODO: Boton para seleccionar archivo en solitairo de texto

        # Botón para seleccionar la carpeta y mostrar la ruta.
        self.select_folder_button = customtkinter.CTkButton(self, text="Seleccionar Carpeta",
                                                            command=self.select_folder)
        self.select_folder_button.grid(row=0, column=0, padx=20, pady=10)

        # Botón Start
        self.start_button = customtkinter.CTkButton(self, text="Start", command=self.start_functionality,
                                                    state=tk.DISABLED)
        self.start_button.grid(row=0, column=1, padx=20, pady=10)

        # Botón para limpiar los resultados
        self.clear_results_button = customtkinter.CTkButton(self, text="Limpiar Resultados", command=self.clear_results)
        self.clear_results_button.grid(row=0, column=2, padx=20, pady=10)

        # Label para mostrar la ruta seleccionada
        self.folder_path_label = tk.Label(self, text="", font=("Arial", 8))  # Texto más pequeño
        self.folder_path_label.grid(row=1, column=0, columnspan=3, padx=20, pady=5, sticky="we")

        # TODO: Agregar parametrizacion para el preprocesamiento de los textos

        # Widget de texto para mostrar los resultados
        self.result_text = tk.Text(self, height=20, width=60)
        self.result_text.grid(row=2, column=0, columnspan=3, padx=20, pady=10)

        # Redirigir la salida estándar a result_text
        sys.stdout = self.result_text

    def select_folder(self):
        folder_path = filedialog.askdirectory(title="Seleccionar carpeta")
        if folder_path:
            self.folder_path_label.configure(text=folder_path)
            self.start_button.configure(state=tk.NORMAL)
            self.start_button.configure(fg_color="green")  # Botón en verde cuando hay una ruta seleccionada

    def start_functionality(self):
        self.result_text.insert(tk.END,"Iniciando análisis de similitud...\n")
        # Obtener la ruta de la carpeta
        folder_path = self.folder_path_label.cget("text")

        # Llamar a la función de detección de plagio con la ruta seleccionada
        self.detect_plagiarism(folder_path)

    def detect_plagiarism(self, selected_path: str):
        # TODO: Finalizar la implementación de la función detect_plagiarism para archivo en solitario
        if os.path.isfile(selected_path):
            preprocess_originales = DetectorDePlagio.DetectorDePlagio().preprocesar_texto(selected_path, True)
            print("Es un archivo")

        elif os.path.isdir(selected_path):
            similitud = DetectorDePlagio.DetectorDePlagio().analizar_similitud(
                self.path_plagiados,
                selected_path)
            pdf = DetectorDePlagio.DetectorDePlagio().generar_documentos_pdf(
                self.path_plagiados,
                selected_path,
                similitud
            )

            for res in similitud:
                self.result_text.insert(tk.END, res)
                self.result_text.insert(tk.END, "\n")
            self.result_text.insert(tk.END, "------------------------------------------------------------\n")
            for res in pdf:
                self.result_text.insert(tk.END, res[0])
                self.result_text.insert(tk.END, "\n")
                self.result_text.insert(tk.END, "\n")
                self.result_text.insert(tk.END, "\n")
                self.result_text.insert(tk.END, res[1])
                self.result_text.insert(tk.END, "\n")
                self.result_text.insert(tk.END, "\n")
                self.result_text.insert(tk.END, "\n")
                self.result_text.insert(tk.END, res[2])
                self.result_text.insert(tk.END, "\n")
                self.result_text.insert(tk.END, "\n")
                self.result_text.insert(tk.END, "\n")
                self.result_text.insert(tk.END, "------------------------------------------------------------\n")
                self.result_text.insert(tk.END, "\n")
                self.result_text.insert(tk.END, "\n")
            self.result_text.insert(tk.END, "El analisis finalizo\n")

        else:
            print("Error: La ruta seleccionada no es válida.")

    def clear_results(self):
        # Función para limpiar los resultados en la sección 4
        self.result_text.delete(1.0, tk.END)



app = App()
app.mainloop()
