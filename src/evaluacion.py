"""Evaluacion practica: scheduling de 8 trabajos sobre 3 VM homogeneas."""
import json, math, pathlib
from schedulers import round_robin, sjf, fcfs, ljf, from_assignment, optimal_bruteforce

JOBS = [("J1", 12), ("J2", 4), ("J3", 8), ("J4", 3), ("J5", 10), ("J6", 6), ("J7", 2), ("J8", 7)]
N_VMS = 3
OUT = pathlib.Path(__file__).resolve().parent.parent / "results"


def fmt(r):
    rows = []
    for vm, js in r.jobs_by_vm().items():
        d = dict(JOBS)
        rows.append((f"VM{vm+1}", "+".join(js), " + ".join(str(d[j]) for j in js), r.loads()[vm]))
    return rows


def main():
    total = sum(l for _, l in JOBS)
    print("=" * 64)
    print("EVALUACION PRACTICA - SCHEDULING EN LA NUBE")
    print("=" * 64)
    print(f"Tiempo total = {total} min | carga media teorica = {total/N_VMS:.2f} min "
          f"| limite inferior entero = {math.ceil(total/N_VMS)} min\n")

    rr = round_robin(JOBS, N_VMS)
    print("ACTIVIDAD 1 - Round Robin")
    for vm, js, calc, c in fmt(rr):
        print(f"  {vm}: {js:<10} {calc:<12} = {c:g}")
    print(f"  Makespan Cmax = max({', '.join(f'{c:g}' for c in rr.loads())}) = {rr.makespan:g} min\n")

    print("ACTIVIDAD 2 - SJF (orden menor a mayor)")
    order = sorted(JOBS, key=lambda j: j[1])
    print("  Pos  Trabajo  Duracion")
    for i, (n, l) in enumerate(order, 1):
        print(f"  {i:<4} {n:<8} {l}")
    sj = sjf(JOBS, N_VMS)
    print("  Criterio de seleccion de VM: la que quede libre primero (menor carga acumulada)")
    for n, vm, s, f in sj.schedule:
        print(f"    {n}: VM{vm+1}  inicio={s:g}  fin={f:g}")
    for vm, js, calc, c in fmt(sj):
        print(f"  {vm}: {js:<10} {calc:<12} = {c:g}")
    print(f"  Makespan Cmax = {sj.makespan:g} min\n")

    print("ACTIVIDAD 3 - Asignacion optimizada")
    asg = {0: ["J1", "J6"], 1: ["J5", "J4", "J2"], 2: ["J3", "J8", "J7"]}
    op = from_assignment("Optimizada", JOBS, asg)
    for vm, js, calc, c in fmt(op):
        print(f"  {vm}: {js:<10} {calc:<12} = {c:g}")
    print(f"  Makespan Cmax = {op.makespan:g} min")
    best, _, n = optimal_bruteforce(JOBS, N_VMS)
    print(f"  Verificacion por fuerza bruta ({n} asignaciones): minimo posible = {best:g} min\n")

    print("COMPARATIVO DE INDICADORES")
    print(f"  {'Estrategia':<14}{'Makespan':>9}{'Espera media':>14}{'Util. media':>13}{'Throughput':>12}")
    allr = [rr, sj, ljf(JOBS, N_VMS), op]
    for r in allr:
        print(f"  {r.name:<14}{r.makespan:>9g}{r.avg_wait():>14.2f}{r.avg_utilization()*100:>12.1f}%{r.throughput():>12.3f}")

    OUT.mkdir(exist_ok=True)
    data = {r.name: {"makespan": r.makespan, "loads": r.loads(), "avg_wait": r.avg_wait(),
                     "avg_util": r.avg_utilization(), "throughput": r.throughput(),
                     "assignment": {f"VM{k+1}": v for k, v in r.jobs_by_vm().items()}} for r in allr}
    data["optimo_bruteforce"] = best
    (OUT / "evaluacion.json").write_text(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
