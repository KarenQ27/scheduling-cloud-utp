# Uso opcional de GCP

La guia indica que GCP se use *si es necesario*. El laboratorio es una simulacion en Python
y corre en cualquier maquina, por lo que GCP no es obligatorio. Para correrlo en la nube:

1. `gcloud auth login`
2. `./deploy/gcp_vm.sh <PROJECT_ID>` (crea una VM e2-micro, clona el repo y ejecuta pruebas y simulaciones)
3. Eliminar la VM al terminar para no generar costos.

Alternativa sin costo: Google Colab (`!git clone ...` y `!python src/laboratorio.py`).
