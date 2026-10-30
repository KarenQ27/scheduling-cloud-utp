"""Laboratorio: FCFS vs Min-Min con 50 tareas y 5 VM heterogeneas (+ RR y Max-Min de referencia)."""
import csv, json, pathlib, random
from schedulers import fcfs, min_min, round_robin, max_min

SEED = 42
N_TASKS, N_VMS = 50, 5
# VM heterogeneas (MIPS ~ capacidad de calculo) y su costo referencial por hora
VMS = [("VM1", 1, 500), ("VM2", 2, 1000), ("VM3", 4, 1500), ("VM4", 4, 2000), ("VM5", 8, 3000)]  # (nombre, vCPU, MIPS)
OUT = pathlib.Path(__file__).resolve().parent.parent / "results"


def dataset(seed=SEED):
    rnd = random.Random(seed)
    # longitud en millones de instrucciones (MI): 20% grandes, 50% medianas, 30% pequenas
    tasks = []
    for i in range(1, N_TASKS + 1):
        u = rnd.random()
        mi = rnd.randint(20000, 60000) if u < .2 else rnd.randint(8000, 20000) if u < .7 else rnd.randint(1000, 8000)
        tasks.append((f"T{i:02d}", float(mi)))
    return tasks


def main():
    tasks = dataset()
    speeds = [m for _, _, m in VMS]  # tiempo(s) = MI / MIPS
    OUT.mkdir(exist_ok=True)
    with open(OUT / "dataset_tareas.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["tarea", "longitud_MI"]); w.writerows(tasks)

    print("=" * 72)
    print(f"LABORATORIO - {N_TASKS} tareas y {N_VMS} VM heterogeneas (semilla {SEED})")
    print("=" * 72)
    print("VM    vCPU   MIPS")
    for n, c, m in VMS:
        print(f"{n:<6}{c:<7}{m}")
    print(f"Longitud total = {sum(l for _, l in tasks):,.0f} MI | Capacidad total = {sum(speeds)} MIPS | "
          f"limite inferior = {sum(l for _, l in tasks)/sum(speeds):.2f} s\n")

    res = [fcfs(tasks, N_VMS, speeds), min_min(tasks, N_VMS, speeds),
           round_robin(tasks, N_VMS, speeds), max_min(tasks, N_VMS, speeds)]
    print(f"{'Algoritmo':<13}{'Makespan(s)':>12}{'Espera med.(s)':>16}{'Retorno med.(s)':>17}{'Util. media':>13}{'Util.pond.':>11}{'Throughput(t/s)':>17}")
    for r in res:
        print(f"{r.name:<13}{r.makespan:>12.2f}{r.avg_wait():>16.2f}{r.avg_completion():>17.2f}"
              f"{r.avg_utilization()*100:>12.1f}%{r.weighted_utilization(speeds)*100:>10.1f}%{r.throughput():>17.4f}")
    a, b = res[0], res[1]
    print(f"\nMin-Min vs FCFS: makespan {100*(a.makespan-b.makespan)/a.makespan:+.1f}% menor, "
          f"espera media {100*(a.avg_wait()-b.avg_wait())/a.avg_wait():+.1f}% menor")
    print("  (Util. media = promedio simple por VM; Util.pond. = ponderada por capacidad MIPS de cada VM)")
    print("\nUtilizacion por VM (%)")
    print(f"{'Algoritmo':<13}" + "".join(f"{v[0]:>9}" for v in VMS))
    for r in res:
        print(f"{r.name:<13}" + "".join(f"{u*100:>8.1f}%" for u in r.utilization()))
    print("\nTareas por VM")
    for r in res[:2]:
        print(f"{r.name:<13}" + "".join(f"{len(v):>9}" for v in r.jobs_by_vm().values()))
    ju = {r.name: {"makespan": r.makespan, "avg_wait": r.avg_wait(), "avg_completion": r.avg_completion(),
                   "avg_util": r.avg_utilization(), "weighted_util": r.weighted_utilization(speeds), "util": r.utilization(), "throughput": r.throughput(),
                   "tasks_per_vm": [len(v) for v in r.jobs_by_vm().values()]} for r in res}
    (OUT / "laboratorio.json").write_text(json.dumps(ju, indent=2))
    with open(OUT / "schedule_fcfs_minmin.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["algoritmo", "tarea", "vm", "inicio_s", "fin_s"])
        for r in res[:2]:
            for t, vm, s, e in r.schedule:
                w.writerow([r.name, t, f"VM{vm+1}", f"{s:.3f}", f"{e:.3f}"])
    return tasks, res


if __name__ == "__main__":
    main()
