# Scheduling y asignacion eficiente de recursos en la nube

Curso **Servicios Cloud** - UTP (Semana 12) · Autora: **Karen Meylin Quispe Saavedra**

Repositorio con la **Evaluacion practica individual** y la **Guia de laboratorio** sobre scheduling en la nube.

| Archivo | Contenido |
|---|---|
| `src/schedulers.py` | Round Robin, FCFS, SJF, LJF, Min-Min, Max-Min y busqueda del optimo por fuerza bruta |
| `src/evaluacion.py` | Caso de 8 trabajos / 3 VM homogeneas (Actividades 1-3) |
| `src/pregunta3.py` | Pregunta 3: VM heterogeneas (8, 2 y 2 vCPU) |
| `src/laboratorio.py` | Laboratorio: 50 tareas, 5 VM heterogeneas, FCFS vs Min-Min (+ RR y Max-Min) |
| `src/graficos.py` | Gantt, comparativos y utilizacion |
| `src/excel_evaluacion.py` | Hoja de calculo con formulas del caso evaluado |
| `tests/` | Pruebas automaticas (pytest) |
| `results/` | Salidas JSON/CSV (dataset de 50 tareas, calendario de asignacion) |
| `docs/capturas/` | Capturas y graficos usados en el informe |

## Ejecucion
```bash
pip install -r requirements.txt
pytest -q
python src/evaluacion.py
python src/pregunta3.py
python src/laboratorio.py
python src/graficos.py
```

## Resultados clave
- Evaluacion: Round Robin = **21 min**, SJF (VM libre primero) = **22 min**, asignacion optimizada = **18 min** (optimo comprobado con 6 561 combinaciones).
- Laboratorio (semilla 42): FCFS = 146.2 s, Min-Min = 123.0 s (15.9 % menos) y espera media 45 % menor.

## Supuestos
Trabajos disponibles en t=0, una tarea por VM a la vez, sin interrupciones ni costo de cambio de contexto. En el laboratorio la duracion es `longitud (MI) / MIPS de la VM`.
