# Detector Plagio

 Esta es una herramienta de detección de plagio externo la cual usa técnicas de procesamiento de lenguaje natural donde muestra el nivel de similitud entre documentos y las coincidencias detectadas de los documentos originales. 

 ## Arquitectura:
 - Preprocesamiento - Tokenización, Lematización, N-grams 
 - Procesamiento - Word embedding, Similitud de cosenos
 - Decisión - Keras accuracy


 Este propuesta busca garantizar no solo el diseño pero también un desarrollo y funcionamiento efectivo para una interacción coherente, clara y precisa de los resultados de cada etapa y la detección en conjunto gracias al uso de interfaz gráfica para optimizar la busqueda de archivos y resultados al usuario.

## Estructura del Proyecto

El proyecto se divide en dos carpetas principales:

- **App:** Contiene la aplicación principal de detección de plagio, donde se encuentran los módulos y scripts necesarios para ejecutar el programa.
- **Sandbox:** Esta carpeta contiene archivos de pruebas y scripts utilizados durante el desarrollo de la aplicación principal. Es un entorno de prueba donde se experimenta con diferentes técnicas y algoritmos.

## Carpeta Sandbox

La carpeta "sandbox" es un espacio dedicado a pruebas y experimentación durante el desarrollo de la aplicación. Aquí se encuentran notebooks de Jupyter, scripts de prueba y otros archivos que ayudaron en el proceso de desarrollo.

Puedes explorar la carpeta "sandbox" para ver ejemplos de código, pruebas de concepto y experimentos que se realizaron antes de integrar la funcionalidad en la aplicación principal.

## Carpeta de Aplicación Principal (App)

La carpeta "App" contiene todo el código fuente necesario para ejecutar la aplicación principal de detección de plagio. Aquí encontrarás los siguientes archivos y carpetas:

- **Resultados:** Esta carpeta contiene los archivos PDF generados por el programa, que muestran los resultados de la detección de plagio.
- **Tests:** Aquí se encuentran los tests unitarios para algunos métodos de las clases implementadas en la aplicación.
- **App.py:** Este archivo contiene la lógica principal de la aplicación, incluyendo la interfaz de usuario y la integración de los diferentes módulos.
- **DetectorDePlagio.py:** Clase que implementa el algoritmo de detección de plagio.
- **Preprocesamiento.py:** Clase que se encarga de realizar el preprocesamiento de los textos antes de aplicar el algoritmo de detección de plagio.
- **Procesamiento.py:** Clase que proporciona funciones para el procesamiento de texto y cálculo de similitud entre documentos.

## Instalación

Para instalar y ejecutar el proyecto, sigue estos pasos:

1. **Descarga el repositorio:** Clona o descarga el repositorio del proyecto desde GitHub a tu máquina local.

2. **Instala las dependencias:** Abre una terminal, navega hasta la carpeta raíz del proyecto y ejecuta el siguiente comando para instalar las dependencias necesarias:

   ```bash
   pip install -r requirements.txt
    ```
3. **Corrige las rutas (opcional):** Si es necesario, corrige las rutas de los archivos en el código según la estructura de tu sistema de archivos.
4. **Accede a la carpeta de la aplicación:** Desde la terminal, entra al directorio "App" del proyecto:

    ```bash
    cd App
    ```
5. **Ejecuta la aplicación:** Finalmente, ejecuta la aplicación utilizando el siguiente comando:

    ```bash
    python -m App.py
    ```
6. **Explora la aplicación:** Una vez que la aplicación esté en funcionamiento, puedes explorar las diferentes funcionalidades, cargar archivos de texto y ver los resultados de la detección de plagio.

## Video de la App

![GIF Demostrativo](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZGN0NHJnMHRnZWltN3FrenY4OG01d2NzMXQ0d3p4MG9yZGQ4ZWkybSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/S8Mw6A5rCWZxcuizdH/giphy.gif)
