# Hosts Editor

**Hosts Editor** es una herramienta de escritorio para Windows que simplifica la gestión del archivo `hosts`. Con una interfaz gráfica intuitiva, permite añadir, modificar y eliminar entradas de forma segura. La aplicación crea automáticamente una copia de seguridad antes de cada cambio y está diseñada para funcionar como un único archivo `.exe` sin dependencias externas.

 ---

## Características Principales

  * **Interfaz Gráfica Sencilla**: Utiliza Tkinter para una experiencia de usuario directa.
  * **Gestión Completa**: Añade, edita y elimina entradas del archivo `hosts`.
  * **Multilingüe**: Detección automática del idioma del sistema (soporta español e inglés por defecto). Las traducciones están empaquetadas en el ejecutable.
  * **Seguridad**: Realiza una copia de seguridad automática de tu archivo `hosts` antes de guardar cualquier cambio.
  * **Portabilidad**: Distribuido como un único ejecutable `.exe` que no requiere instalación de Python.
  * **Verificación de Permisos**: Muestra mensajes claros si no se ejecuta con permisos de administrador.

-----

## Guía de Uso

### Instalación

1.  Descarga el ejecutable `hosts_editor` desde la [página de lanzamientos](https://github.com/aledotsoftware/Hosts-Editor/releases). 
2.  Haz clic derecho sobre el archivo y selecciona **"Ejecutar como administrador"** para tener los permisos necesarios para modificar el archivo `hosts`.

### Uso Básico

1.  Abre la aplicación. Verás una lista con todas las entradas actuales de tu archivo `hosts`.
2.  Utiliza los botones de la interfaz para **Agregar**, **Editar** o **Eliminar** entradas.
3.  Cuando estés listo, haz clic en **Guardar** para aplicar los cambios y sobrescribir el archivo `hosts`. La aplicación creará una copia de seguridad automáticamente.

-----

## Para Desarrolladores

### Requisitos

  * [Python 3.10+](https://www.python.org/downloads/)
  * [PyInstaller](https://pyinstaller.org/en/stable/)

### Configuración del Entorno

1.  Clona el repositorio:
    ```bash
    git clone https://github.com/aledotsoftware/Hosts-Editor.git
    cd Hosts-Editor
    ```
2.  Instala PyInstaller:
    ```bash
    pip install pyinstaller
    ```

### Compilación del Ejecutable

Para generar el archivo `.exe` en la carpeta `dist/`, ejecuta el siguiente comando desde la raíz del proyecto:

```bash
python -m PyInstaller --onefile --windowed --add-data "locales;locales" hosts_editor.py

```

El `exe` generado no requiere que el usuario final tenga Python instalado.

-----

## Estructura del Proyecto

```
hosts-editor/
│
├─ hosts_editor.py        # Código fuente principal
├─ locales/
│   ├─ en.json            # Traducciones en inglés
│   └─ es.json            # Traducciones en español
└─ README.md
```

-----

## Licencia

Este proyecto está bajo la **Licencia Pública General GNU, versión 3 o superior (GPLv3+)**.

Esto significa que el código es completamente libre. Puedes usarlo, estudiarlo, compartirlo y modificarlo. Si distribuyes una versión modificada del software, debes hacerlo bajo los mismos términos de la licencia, asegurando que tu versión también sea software libre.

Para más detalles, consulta el [texto completo de la licencia](https://www.gnu.org/licenses/gpl-3.0.html).