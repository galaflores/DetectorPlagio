# App

Este es el directorio principal de la aplicación. Contiene todo el código fuente necesario para ejecutar el programa de detección de plagio.

## Descripción de las Clases

- **Resultados:** Esta carpeta contiene los archivos PDF generados por el programa, que muestran los resultados de la detección de plagio.
  
- **Tests:** Aquí se encuentran los tests unitarios para algunos métodos de las clases implementadas en la aplicación.

- **App.py:** Este archivo contiene la lógica principal de la aplicación, incluyendo la interfaz de usuario y la integración de los diferentes módulos.

- **DetectorDePlagio.py:** Clase que implementa el algoritmo de detección de plagio.

- **Preprocesamiento.py:** Clase que se encarga de realizar el preprocesamiento de los textos antes de aplicar el algoritmo de detección de plagio.

- **Procesamiento.py:** Clase que proporciona funciones para el procesamiento de texto y cálculo de similitud entre documentos.

## Dependencias

Para ejecutar la aplicación, es necesario tener instaladas las siguientes dependencias:

- Python 3.x
- NLTK (Natural Language Toolkit): Puedes instalarlo ejecutando `pip install nltk`
- PyPDF2: Puedes instalarlo ejecutando `pip install PyPDF2`
- pytest (solo para ejecutar tests): Puedes instalarlo ejecutando `pip install pytest`

## Ejecutar Pruebas

Para ejecutar todas las pruebas, utiliza el siguiente comando en la terminal desde la raíz del proyecto:

`python -m pytest`


Para ejecutar pruebas específicas, puedes especificar la ruta del archivo de prueba:

`python -m pytest Tests/test_nombre_del_archivo.py`


## Ejecutar la Aplicación

Sigue estos pasos para ejecutar la aplicación:

1. Descarga o clona el repositorio desde GitHub.
2. Instala las dependencias mencionadas anteriormente.
3. Asegúrate de corregir las rutas de archivos dentro del código según sea necesario.
4. Desde la terminal, navega hasta la carpeta "app" del proyecto.
5. Ejecuta el programa utilizando el siguiente comando:


`python -m App.py`
