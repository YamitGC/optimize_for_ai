# Conversor DOCX → Markdown/Texto optimizado para IA

> 🌐 **Idioma:** [English](README.md) | [Español](README.es.md)

Una pequeña utilidad en Python que toma un archivo `.docx`, elimina los encabezados y pies de página repetitivos (que consumen tokens innecesarios cuando se le pasan documentos a una IA) y lo convierte en dos formatos optimizados:

- **`.md`** — Markdown, conservando la jerarquía de títulos y las tablas.
- **`.txt`** — Texto plano, con el mínimo consumo de tokens posible.

---

## Tabla de contenidos

- [¿Cómo funciona?](#cómo-funciona)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
  - [🪟 Windows](#-windows)
  - [🐧 Linux](#-linux)
    - [Ubuntu / Debian / Pop!_OS](#ubuntu--debian--pop_os)
    - [Linux Mint](#linux-mint)
    - [Fedora](#fedora)
    - [Arch Linux / Manjaro](#arch-linux--manjaro)
- [Uso](#uso)
- [Ejemplo de salida](#ejemplo-de-salida)
- [Solución de problemas](#solución-de-problemas)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Licencia](#licencia)

---

## ¿Cómo funciona?

El script (`optimize_for_ai.py`) hace lo siguiente:

1. Resuelve la ruta del archivo de entrada (expande `~` y la convierte en una ruta absoluta). Si el nombre indicado no existe en la carpeta actual, también lo busca automáticamente en `~/Documents` y `~/Downloads` — así puedes ejecutar el script desde cualquier lugar y pasar solo el nombre del archivo, sin escribir la ruta completa, siempre que el archivo esté en alguna de esas dos carpetas.
2. Abre el `.docx` ya resuelto con `python-docx`.
3. Borra el texto de todos los encabezados y pies de página de cada sección (normalmente contienen números de página, logos u otro texto repetido que no aporta valor a una IA).
4. Guarda una copia temporal ya "limpia".
5. Convierte esa copia con `markitdown` a texto Markdown estructurado.
6. Escribe el resultado en dos archivos junto al original: `<nombre>.md` y `<nombre>.txt`.
7. Elimina el archivo temporal.

> 💡 **Consejo:** Si tu archivo no está en la carpeta actual, en `Documents` ni en `Downloads`, simplemente pasa la ruta completa en lugar de solo el nombre, por ejemplo: `python optimize_for_ai.py C:\Users\yo\Desktop\informe.docx` (Windows) o `python3 optimize_for_ai.py ~/Desktop/informe.docx` (Linux).

---

## Requisitos

- **Python 3.9 o superior** (se recomienda 3.10+).
- **pip** (gestor de paquetes de Python).
- Conexión a internet la primera vez que instales las dependencias.
- Los dos paquetes de Python listados en [`requirements.txt`](requirements.txt):
  - [`python-docx`](https://pypi.org/project/python-docx/)
  - [`markitdown`](https://pypi.org/project/markitdown/)

> 💡 `markitdown` puede manejar opcionalmente más tipos de archivo (PDF, PPTX, imágenes con OCR, transcripción de audio, etc.) si lo instalas con extras: `pip install "markitdown[all]"`. Para este script, la instalación básica es suficiente, ya que solo necesitamos soporte para `.docx`.

---

## Instalación

Primero clona o descarga este repositorio:

```bash
git clone https://github.com/YamitGC/optimize_for_ai.git
cd optimize_for_ai
```

### 🪟 Windows

1. **Instalar Python**
   - Descarga el instalador desde [python.org/downloads](https://www.python.org/downloads/).
   - Ejecútalo y **marca la casilla "Add python.exe to PATH"** antes de darle a *Install Now*. Este es el motivo número 1 de errores tipo "python no se reconoce".

2. **Verificar la instalación** (abre *PowerShell* o *CMD*):
   ```powershell
   python --version
   pip --version
   ```
   Si `python` no se reconoce, cierra y vuelve a abrir la terminal, o reinstala Python asegurándote de marcar la casilla de PATH.

3. **(Recomendado) Crear un entorno virtual**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```
   Deberías ver `(venv)` al inicio de tu línea de comandos.

   > Si PowerShell bloquea el script de activación con un error de "política de ejecución", abre PowerShell **como Administrador** una vez y ejecuta:
   > ```powershell
   > Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   > ```
   > Luego intenta activarlo de nuevo.

4. **Instalar dependencias**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Ejecutar el script**
   ```powershell
   python optimize_for_ai.py mi_documento.docx
   ```

6. **(Opcional) Desactivar el entorno virtual al terminar**
   ```powershell
   deactivate
   ```

---

### 🐧 Linux

Notas generales para todas las distribuciones:
- Usa explícitamente `python3` y `pip3` (algunas distros no crean el alias `python`/`pip` apuntando a Python 3).
- Se recomienda encarecidamente usar un **entorno virtual** para evitar conflictos con los paquetes de Python gestionados por el sistema (especialmente en Debian/Ubuntu modernos, que bloquean por defecto el `pip install` global — ver [Solución de problemas](#solución-de-problemas)).

#### Ubuntu / Debian / Pop!_OS

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python3 optimize_for_ai.py mi_documento.docx
```

#### Linux Mint

Mint está basado en Ubuntu/Debian, así que se usan los mismos comandos:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python3 optimize_for_ai.py mi_documento.docx
```

#### Fedora

Fedora usa `dnf` y normalmente ya trae `python3`/`pip3`, pero el soporte de `venv` puede necesitar un paquete adicional:

```bash
sudo dnf install -y python3 python3-pip python3-virtualenv

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python3 optimize_for_ai.py mi_documento.docx
```

#### Arch Linux / Manjaro

Arch trae una versión muy reciente de Python vía `pacman`, y `python-pip` ya incluye soporte para `venv`:

```bash
sudo pacman -Syu --needed python python-pip

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python optimize_for_ai.py mi_documento.docx
```

> ⚠️ Arch es una distro de "rolling release" con versiones de Python muy nuevas. Si `markitdown` o `python-docx` da un error de compatibilidad, revisa la sección de [Solución de problemas](#solución-de-problemas) sobre `--break-system-packages` o fija versiones específicas en `requirements.txt`.

---

## Uso

Una vez instaladas las dependencias (y con el entorno virtual activado, si creaste uno):

```bash
python optimize_for_ai.py ruta/al/documento.docx
```

También puedes pasar solo el nombre del archivo (sin ruta) si está en tu carpeta actual, en `Documents` o en `Downloads` — el script lo encontrará automáticamente:

```bash
python optimize_for_ai.py mi_informe.docx
```

Esto genera, en la carpeta donde se encontró el archivo de entrada:

- `documento.md`
- `documento.txt`

---

## Ejemplo de salida

```
Procesando: /home/usuario/Documents/documento.docx
Limpiando el documento...
Convirtiendo a formatos para IA...

¡Listo! Archivos generados en /home/usuario/Documents:
 - documento.md
 - documento.txt
```

---

## Solución de problemas

| Problema | Causa | Solución |
|---|---|---|
| `python: command not found` (Linux) o `'python' no se reconoce` (Windows) | Python no está instalado o no está en el PATH | Reinstala Python asegurándote de configurar el PATH (ver pasos por sistema operativo arriba), o usa `python3` en Linux |
| `error: externally-managed-environment` al hacer `pip install` | Debian/Ubuntu/Mint modernos (PEP 668) bloquean la instalación global con pip | Usa un entorno virtual (`python3 -m venv venv && source venv/bin/activate`) — **no** uses `--break-system-packages` a menos que entiendas bien el riesgo |
| `ModuleNotFoundError: No module named 'docx'` | `python-docx` no está instalado, o está instalado en un entorno distinto al que ejecuta el script | Activa tu entorno virtual antes de instalar/ejecutar, o reinstala con `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'markitdown'` | Igual que el caso anterior, pero con `markitdown` | Misma solución |
| El script corre pero genera un `.md` vacío o corrupto | Archivo `.docx` corrupto o protegido con contraseña | Abre y vuelve a guardar el archivo en Word/LibreOffice, y quita cualquier protección con contraseña |
| `PermissionError` al guardar los archivos de salida | El `.docx` (o la carpeta de salida) está abierto en Word o es de solo lectura | Cierra el archivo en cualquier otro programa y revisa los permisos de escritura de la carpeta |
| PowerShell no ejecuta `venv\Scripts\activate` | Restricción de política de ejecución | Ejecuta `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` en una PowerShell elevada |
| `pip install` funciona pero el script sigue fallando en Fedora/Arch tras una actualización del sistema | El Python del sistema se actualizó y rompió el venv | Borra la carpeta `venv` y créala de nuevo (`rm -rf venv && python3 -m venv venv`) |
| `Error: No se encontró '<archivo>' en el directorio actual, ni en Documents ni en Downloads` | Escribiste un nombre de archivo que no está en la carpeta actual, en `~/Documents` ni en `~/Downloads` | Revisa la ortografía/extensión, mueve el archivo a alguna de esas carpetas, o pasa la ruta completa (ej. `~/Desktop/archivo.docx`) |

---

## Estructura del proyecto

```
.
├── optimize_for_ai.py     # Script principal de conversión
├── requirements.txt       # Dependencias de Python
├── README.md               # Este archivo (inglés)
├── README.es.md            # Versión en español
├── LICENSE.md               # Licencia (inglés)
└── LICENSE.es.md            # Licencia (español, informativa)
```

---

## Licencia

Este proyecto se distribuye bajo la [Licencia MIT](LICENSE.md). Consulta [`LICENSE.md`](LICENSE.md) para el texto completo (o [`LICENSE.es.md`](LICENSE.es.md) para una traducción informativa al español).
