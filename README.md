# NN Implementation Example (Flask + Keras)

Pequeño proyecto de ejemplo que expone una página web (Flask) e integra un modelo de red neuronal (Keras/TensorFlow). 
La app sirve una interfaz HTML desde `templates/`, archivos estáticos desde `static/`, y carga/guarda artefactos del modelo en `model/`. 
Los datos (si aplica) viven en `data/`.

## Estructura del proyecto

```
.
├── app.py               # Punto de entrada de Flask
├── templates/           # Vistas Jinja2 (HTML)
├── static/              # CSS/JS/imagenes
├── model/               # Artefactos del modelo (.h5, .keras, scaler.pkl, etc.)
└── data/                # Datos de ejemplo/entrada
```

## Requisitos

- Python 3.9 – 3.12
- Pip actualizado (`pip>=23`)
- Dependencias Python:
  - Flask (servidor web)
  - TensorFlow 2.x (incluye Keras) **o** `keras` independiente
  - NumPy, (opcional) pandas / scikit-learn si tu pipeline los usa

> Si el repo incluye `requirements.txt`, usa ese archivo y omite la instalación manual.

## Instalación

### 1) Clonar el repo

```bash
git clone https://github.com/vareladev/nn-implementation-example.git
cd nn-implementation-example
```

### 2) Crear entorno virtual

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux (bash/zsh):**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Instalar dependencias

**Con requirements.txt (recomendado si existe):**
```bash
pip install -U pip
pip install -r requirements.txt
```

**Instalación mínima (si no hay requirements.txt):**
```bash
pip install -U pip
pip install flask tensorflow  # o: pip install flask keras tensorflow
pip install numpy             # + cualquier otra lib que uses (pandas, scikit-learn, etc.)
```

## Configuración

Opcionalmente puedes usar variables de entorno de Flask:

```bash
# macOS/Linux
export FLASK_APP=app.py
export FLASK_ENV=development

# Windows (PowerShell)
$env:FLASK_APP="app.py"
$env:FLASK_ENV="development"
```

## Ejecutar la aplicación

### Opción A: con Python directamente
```bash
python app.py
```

### Opción B: con Flask
```bash
flask run --host=0.0.0.0 --port=5000
```

Luego abre en el navegador: http://localhost:5000

## Modelo de Keras

Coloca tu modelo en `model/`, por ejemplo:

- `model/model.h5` o `model/model.keras`
- Preprocesadores: `model/scaler.pkl`, `model/label_encoder.pkl`, etc.

En `app.py` se suele cargar así (ejemplo genérico):

```python
from tensorflow.keras.models import load_model
model = load_model("model/model.h5")  # o "model/model.keras"
```

> Si el proyecto trae ya un modelo pre-entrenado en `model/`, no necesitas reentrenar.  
> Si **no** existe el archivo del modelo, crea/entrena uno (ver siguiente sección).

## Entrenamiento (opcional)

Si el proyecto incluye un script de entrenamiento (por ejemplo `train.py` dentro de `model/`), ejecútalo:

```bash
python model/train.py   --data data/dataset.csv   --out model/model.h5
```

Ajusta nombres/rutas según tu script. Asegúrate de guardar el modelo en `model/` y que `app.py` lo ubique ahí.

## Endpoints (ejemplo)

> Estos endpoints dependen del contenido de `app.py`. Si tu app sigue el patrón típico:

- `GET /` — página principal (render de `templates/index.html`)
- `POST /predict` — recibe datos (JSON o form), ejecuta el modelo y retorna la predicción

Ejemplo de petición `curl` (JSON):

```bash
curl -X POST http://localhost:5000/predict   -H "Content-Type: application/json"   -d '{"features":[0.25, 0.10, 0.75, 0.40]}'
```

## Despliegue rápido (Gunicorn)

Para producción Linux:

```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:8000 app:app
```

Detrás de Nginx o similar.

## Problemas comunes

- **TensorFlow/oneDNN aviso**: mensajes de precisión numérica ligeramente distinta son normales.
- **Falta el archivo del modelo**: asegúrate de tener `model/model.h5` (o `.keras`). Si no existe, entrena o copia el artefacto.
- **Error al importar TensorFlow en Windows**: instala el Visual C++ Redistributable actualizado. Ejecutar en Python 64-bit recomendado.
- **Puertos ocupados**: cambia el puerto (`--port 5001`, por ejemplo).

## Licencia

MIT (o la que corresponda).
