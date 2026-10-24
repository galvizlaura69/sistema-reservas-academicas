# Sistema de Reservas Académicas

Aplicación web académica para gestionar reservas de laboratorios, auditorios y salas de cómputo. Desarrollada con Python, Flask, SQLite, HTML/CSS y pruebas con pytest.

## Requisitos

- Python 3.10+ (probado con Python 3.13)
- pip

## Instalación

1. Clonar o descargar el repositorio
2. Crear y activar entorno virtual (recomendado)

```powershell
# Windows PowerShell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

```bash
# Linux/macOS
python -m venv .venv
source .venv/bin/activate
```

3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecución

### Opción 1: run.py (recomendada)
```bash
py run.py
```
La aplicación estará disponible en `http://127.0.0.1:5000`

### Opción 2: Flask CLI
```powershell
# Windows PowerShell
$env:FLASK_APP = "app:create_app"
$env:FLASK_DEBUG = "1"
flask run --host=127.0.0.1 --port=5000
```

```bash
# Linux/macOS
export FLASK_APP=app:create_app
export FLASK_DEBUG=1
flask run --host=127.0.0.1 --port=5000
```

## Pruebas

Ejecutar pruebas unitarias:

```bash
py -m pytest tests/unit/ -v
```

Ejecutar todas las pruebas:

```bash
py -m pytest -v
```

## Estado del proyecto

- **Base implementada:** Estructura Flask modular, modelos, autenticación/roles, servicios básicos, interfaz web con plantillas
- **En desarrollo:** CRUD de espacios, lógica completa de reservas (conflictos, transacciones, aprobación/cancelación), historial y pruebas de integración
- **Pendiente:** Límite de máximo cuatro horas consecutivas (se gestionará como cambio independiente con OpenSpec)

## Documentación

- `PLAN_INGENIERIA.md` - Plan de ingeniería
- `openspec/` - Especificaciones con OpenSpec (SDD)
- `INFORME_FINAL.md` - Informe final con resultados reales
- `tasks.md` (en `openspec/changes/sistema-reservas-academicas/`) - Lista de tareas
