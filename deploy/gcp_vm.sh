#!/usr/bin/env bash
# Ejecuta el laboratorio en una VM de Compute Engine (GCP). Requiere `gcloud auth login`
# y un proyecto con facturacion/free tier. NO se ejecuto en la entrega: ver docs/GCP.md
set -euo pipefail
PROJECT="${1:?uso: $0 <PROJECT_ID> [ZONA]}"; ZONE="${2:-us-central1-a}"
gcloud config set project "$PROJECT"
gcloud compute instances create scheduling-lab --zone "$ZONE" --machine-type e2-micro \
  --image-family debian-12 --image-project debian-cloud
gcloud compute ssh scheduling-lab --zone "$ZONE" --command \
  "sudo apt-get update -qq && sudo apt-get install -y -qq git python3-pip python3-venv && \
   git clone https://github.com/<TU_USUARIO>/scheduling-cloud-utp.git && cd scheduling-cloud-utp && \
   python3 -m venv .venv && . .venv/bin/activate && pip install -q -r requirements.txt && \
   pytest -q && python src/evaluacion.py && python src/laboratorio.py"
# Para no generar costo: gcloud compute instances delete scheduling-lab --zone "$ZONE" --quiet
