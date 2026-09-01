# TooManyFiles - Guía del Proyecto

## Descripción
`toomanyfiles` es una herramienta CLI y librería en Python para buscar y eliminar archivos y directorios obsoletos basándose en patrones de fecha y hora.

## Herramientas y Gestión de Dependencias
- **Gestor de paquetes**: Poetry (`poetry`)
- **Gestor de tareas**: Poe the Poet (`poe`)

### Tareas comunes con Poe:
- `poe translate`: Extrae cadenas con `xgettext`, actualiza los archivos `.po` (`es`, `fr`, `ro`, `ru`, `zh`, `hi`) con `msgmerge` y compila los archivos binarios `.mo` con `msgfmt`.
- `poe pytest`: Ejecuta la suite de pruebas unitarias.
- `poe coverage`: Genera el informe de cobertura de código.
- `poe video`: Genera demostraciones en vídeo/GIF utilizando `vhs`.
- `poe release`: Imprime la lista de pasos para publicar una nueva versión.

## Internacionalización (i18n / gettext)
- Todas las cadenas visibles para el usuario (mensajes de consola, ayuda de CLI, razones de exclusión, estados, logs) deben estar envueltas en `_()`.
- En caso de requerir formateo con `.format()`, siempre debe aplicarse **fuera** de la llamada a `_()`:
  - Correcto: `_("Texto con {}").format(variable)`
  - Incorrecto: `_("Texto con {}".format(variable))`
- Las tareas y catálogos de traducción se sincronizan ejecutando `poe translate`.
