# Viva Flight Updater - Documentación Oficial

## 1. Resumen Ejecutivo
* **Descripción**: Aplicación de consola en Python diseñada para automatizar la actualización masiva de estados de vuelos en sistemas DCS (Navitaire).
* **Problema Identificado**: La reactivación manual de vuelos suspendidos es ineficiente, consume tiempo excesivo y es propensa a errores humanos de captura.
* **Solución**: Script automatizado que procesa archivos CSV, valida identificadores y ejecuta peticiones seguras de tipo PATCH a la API.
* **Arquitectura**: 
    * **Entrada**: Archivo `suspended_flights.csv`.
    * **Lógica**: Cliente Python con manejo de sesiones y tokens.
    * **CI/CD**: Validación automatizada mediante GitHub Actions.
    * **Salida**: Actualización directa en API y reporte `resultado_vuelos.csv`.

## 2. Tabla de Contenidos (ToC)
1. [Requerimientos](#requerimientos)
2. [Instalación](#instalación)
3. [Configuración](#configuración)
4. [Uso](#uso)
5. [Contribución](#contribución)
6. [Roadmap](#roadmap)

<a name="requerimientos"></a>
## 3. Requerimientos
* **Servidor**: Entorno compatible con Python 3.9+ (Local o Nube).
* **Paquetes**: Librería `requests` para comunicación HTTP.
* **Lenguaje**: Python 3.9.

<a name="instalación"></a>
## 4. Instalación
* **Ambiente de Desarrollo**: Clonar repositorio y asegurar instalación de Python.
* **Pruebas Manuales**: Ejecutar el comando `python test_vuelos.py`.
* **Implementación**: Ejecución directa en servidor local o carga de variables de entorno en proveedores como Heroku.

<a name="configuración"></a>
## 5. Configuración
* **Configuración del Producto**: Requiere un archivo `.env` con las variables `NAVITAIRE_BASE_URL`, `NAVITAIRE_USERNAME` y `NAVITAIRE_PASSWORD`.
* **Requerimientos de Datos**: El archivo CSV debe contener las columnas: FlightNumber, DepartureStation, ArrivalStation, DepartureDate.

<a name="uso"></a>
## 6. Uso
* **Referencia Usuario Final**: Colocar el archivo CSV en la raíz y ejecutar `python main.py`. Revisar los resultados en `resultado_vuelos.csv`.
* **Referencia Administrador**: Monitorear logs de auditoría en `procesamiento_nocturno.log` para traza de errores de red o API.

<a name="contribución"></a>
## 7. Contribución
1. Clonar repositorio.
2. Crear nueva rama: `git checkout -b feat/nombre-mejora`.
3. Enviar Pull Request (PR) hacia la rama `develop`.
4. Validar el paso de pruebas en GitHub Actions antes del Merge.

<a name="roadmap"></a>
## 8. Roadmap
* Implementación de Interfaz Gráfica de Usuario (GUI).
* Soporte para base de datos SQL centralizada.
* Sistema de alertas automáticas vía correo electrónico.
