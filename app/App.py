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
        self.geometry("1500x600")
        self.title("Detector de plagio")
        self.path_originales = "/Users/sergiogonzalez/Documents/GitHub/DetectorPlagio/Documentos de Prueba/docs_originales"  # Cambiar la ruta.

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

        # Frame para contener el widget de texto y habilitar el desplazamiento lateral
        self.text_frame = tk.Frame(self)
        self.text_frame.grid(row=2, column=0, columnspan=3, padx=20, pady=10)
        self.text_frame.grid_rowconfigure(0, weight=1)
        self.text_frame.grid_columnconfigure(0, weight=1)

        # Widget de texto para mostrar los resultados dentro del Frame
        self.result_text = tk.Text(self.text_frame, height=30, width=200)
        self.result_text.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)


        # Redirigir la salida estándar a result_text
        sys.stdout = self.result_text

    def select_folder(self):
        """
        Esta función se encarga de abrir un cuadro de diálogo para seleccionar una carpeta.
        """
        folder_path = filedialog.askdirectory(title="Seleccionar carpeta")
        if folder_path:
            self.folder_path_label.configure(text=folder_path)
            self.start_button.configure(state=tk.NORMAL)
            self.start_button.configure(fg_color="green")  # Botón en verde cuando hay una ruta seleccionada

    def start_functionality(self):
        self.result_text.insert(tk.END, "Iniciando análisis de similitud...\n")
        # Obtener la ruta de la carpeta
        folder_path = self.folder_path_label.cget("text")

        # Llamar a la función de detección de plagio con la ruta seleccionada
        self.detect_plagiarism(folder_path)

    def detect_plagiarism(self, selected_path: str):
        """
        Esta función se encarga de detectar el plagio en los textos seleccionados.
        Args: selected_path: str
        
        """
        similitud = DetectorDePlagio.DetectorDePlagio().analizar_similitud(selected_path, self.path_originales, "lemmatize")
        tipos_plagio = DetectorDePlagio.DetectorDePlagio().encontrar_tipos_de_plagio(similitud, selected_path, self.path_originales)
        # pdf = DetectorDePlagio.DetectorDePlagio().generar_documentos_pdf(
        # self.path_originales,
        # selected_path,
        # similitud
        # )

        # Printing results similitud
        for res in similitud:
            plagio_title, original_title, similarity_score, original_doc = res
            result_text = f"Similarity between '{plagio_title}' and '{original_title}': {similarity_score * 100:.2f}%"
            self.result_text.insert(tk.END, result_text)
            self.result_text.insert(tk.END, "\n")
        self.result_text.insert(tk.END, "------------------------------------------------------------\n")
        self.result_text.insert(tk.END, "\n")

        resultado = DetectorDePlagio.DetectorDePlagio().imprimir_resultados(tipos_plagio[0])
        self.result_text.insert(tk.END, resultado)
        self.result_text.insert(tk.END, "------------------------------------------------------------\n")
        self.result_text.insert(tk.END, "\n")

        auc_text = f'''
        AUC Calculado 
        TPR(Tasa de Verdaderos Positivos): {tipos_plagio[1][0]} \n
        FPR(Tasa de Falsos Positivos): {tipos_plagio[1][1]} \n
        AUC(AREA BAJO LA CURVA ROC): {tipos_plagio[1][2]} \n
        '''
        self.result_text.insert(tk.END, auc_text)
        self.result_text.insert(tk.END, "------------------------------------------------------------\n")
        self.result_text.insert(tk.END, "************************************************************\n")
        self.result_text.insert(tk.END, "*                                                          *\n")
        self.result_text.insert(tk.END, "*               El analisis finalizo                       *\n")
        self.result_text.insert(tk.END, "*                                                          *\n")
        self.result_text.insert(tk.END, "************************************************************\n")

    def clear_results(self):
        # Función para limpiar los resultados en la sección 4
        self.result_text.delete(1.0, tk.END)


app = App()
app.mainloop()
