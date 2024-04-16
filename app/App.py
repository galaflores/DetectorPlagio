import customtkinter
import DetectorDePlagio
from tkinter import filedialog


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("Detector de plagio")

        # add widgets to app
        self.button = customtkinter.CTkButton(self, text="Seleccionar Archivo", command=self.select_file)
        self.button.grid(row=0, column=0, padx=20, pady=10)

    # add methods to app
    def select_file(self):
        file_path = filedialog.askopenfilename(title="Seleccionar archivo de texto",
                                               filetypes=[("Archivos de texto", "*.txt")])
        if file_path:
            self.detect_plagiarism(file_path)

    def detect_plagiarism(self, file_path):
        # Aquí puedes llamar a tu función de detección de plagio pasando el archivo seleccionado
        # Por ejemplo:
        # Detector_de_plagio.detectar_plagio_en_archivo(file_path)
        archivo_preprocesado = DetectorDePlagio.DetectorDePlagio().preprocesar_texto(file_path)

        print("Detección de plagio en el archivo:", archivo_preprocesado)


app = App()
app.mainloop()
