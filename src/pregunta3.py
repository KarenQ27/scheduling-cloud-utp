"""Pregunta 3: VM1 con 8 vCPU y VM2/VM3 con 2 vCPU (VM heterogeneas).

Supuesto explicito (ilustrativo): la velocidad de ejecucion es proporcional a las
vCPU, tomando 4 vCPU como referencia (los tiempos del enunciado) -> velocidades 2.0, 0.5, 0.5.
"""
from schedulers import round_robin, fcfs, min_min, sjf
from evaluacion import JOBS
from itertools import product

SPEEDS = [8 / 4, 2 / 4, 2 / 4]


def main():
    print("PREGUNTA 3 - VM heterogeneas (velocidades relativas 2.0, 0.5, 0.5)")
    print(f"  {'Estrategia':<12}{'Makespan':>9}   Cargas por VM")
    for fn in (round_robin, fcfs, sjf, min_min):
        r = fn(JOBS, 3, SPEEDS)
        print(f"  {r.name:<12}{r.makespan:>9.1f}   " + "  ".join(f"VM{i+1}={c:.1f}" for i, c in enumerate(r.loads())))

    # optimo por fuerza bruta (3^8 asignaciones; el orden dentro de una VM no cambia su carga)
    best = float("inf")
    for c in product(range(3), repeat=len(JOBS)):
        loads = [0.0] * 3
        for (_, l), vm in zip(JOBS, c):
            loads[vm] += l / SPEEDS[vm]
        best = min(best, max(loads))
    print(f"  Optimo (fuerza bruta, 6561 asignaciones) = {best:.1f} min | cota inferior 52/3.0 = {52/3:.2f} min")


if __name__ == "__main__":
    main()
