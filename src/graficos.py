"""Graficos del laboratorio y de la evaluacion (paleta morada)."""
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from laboratorio import dataset, VMS, N_VMS
from schedulers import fcfs, min_min, round_robin, max_min, sjf, from_assignment
import evaluacion as ev

IMG = pathlib.Path(__file__).resolve().parent.parent / "docs" / "capturas"
P = {"fcfs": "#7B2CBF", "minmin": "#C77DFF", "rr": "#5A189A", "maxmin": "#E0AAFF", "dark": "#240046"}
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#7a6a8a", "axes.titleweight": "bold", "axes.titlecolor": P["dark"]})


def gantt(ax, r, title, names):
    cm = plt.get_cmap("Purples")
    for t, vm, s, e in r.schedule:
        k = int(t[1:]) if t.startswith("T") else int(t[1:])
        ax.barh(vm, e - s, left=s, color=cm(0.35 + 0.55 * ((k * 7) % 10) / 10), edgecolor="white", linewidth=.6)
    ax.set_yticks(range(len(names))); ax.set_yticklabels(names); ax.invert_yaxis()
    ax.set_xlabel("Tiempo"); ax.set_title(title)


def lab():
    tasks = dataset(); sp = [m for *_, m in VMS]; names = [v[0] for v in VMS]
    algs = [fcfs(tasks, N_VMS, sp), min_min(tasks, N_VMS, sp), round_robin(tasks, N_VMS, sp), max_min(tasks, N_VMS, sp)]
    cols = [P["fcfs"], P["minmin"], P["rr"], P["maxmin"]]
    fig, ax = plt.subplots(1, 3, figsize=(14, 4.2))
    for a, key, ttl, unit in zip(ax, [lambda r: r.makespan, lambda r: r.avg_wait(), lambda r: r.avg_utilization() * 100],
                                 ["Makespan", "Tiempo medio de espera", "Utilizacion media de CPU"], ["s", "s", "%"]):
        v = [key(r) for r in algs]
        b = a.bar([r.name for r in algs], v, color=cols)
        a.bar_label(b, fmt="%.1f", padding=2); a.set_title(ttl); a.set_ylabel(unit)
    fig.tight_layout(); fig.savefig(IMG / "lab_comparacion.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(2, 1, figsize=(12, 6.5), sharex=True)
    gantt(ax[0], algs[0], f"FCFS - makespan {algs[0].makespan:.1f} s", names)
    gantt(ax[1], algs[1], f"Min-Min - makespan {algs[1].makespan:.1f} s", names)
    ax[0].set_xlabel("")
    fig.tight_layout(); fig.savefig(IMG / "lab_gantt.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 4.2)); x = np.arange(N_VMS); w = .38
    for i, r in enumerate(algs[:2]):
        b = ax.bar(x + (i - .5) * w, [u * 100 for u in r.utilization()], w, label=r.name, color=cols[i])
        ax.bar_label(b, fmt="%.0f%%", padding=2, fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(names); ax.set_ylabel("Utilizacion (%)"); ax.set_ylim(0, 115)
    ax.set_title("Utilizacion por VM: FCFS vs Min-Min"); ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(IMG / "lab_utilizacion.png", dpi=160); plt.close(fig)


def evaluacion():
    J = ev.JOBS
    asg = {0: ["J1", "J6"], 1: ["J5", "J4", "J2"], 2: ["J3", "J8", "J7"]}
    rs = [round_robin(J, 3), sjf(J, 3), from_assignment("Optimizada", J, asg)]
    fig, ax = plt.subplots(3, 1, figsize=(11, 6.2), sharex=True)
    cm = plt.get_cmap("Purples")
    for a, r in zip(ax, rs):
        for j, vm, s, e in r.schedule:
            a.barh(vm, e - s, left=s, color=cm(.3 + .6 * (int(j[1:]) / 8)), edgecolor="white")
            a.text((s + e) / 2, vm, j, ha="center", va="center", color="white" if int(j[1:]) > 3 else P["dark"], fontsize=9, fontweight="bold")
        a.axvline(r.makespan, color=P["dark"], ls="--", lw=1)
        a.set_yticks(range(3)); a.set_yticklabels(["VM1", "VM2", "VM3"]); a.invert_yaxis()
        a.set_title(f"{r.name} - Cmax = {r.makespan:g} min", loc="left")
        a.set_xlim(0, 24)
    ax[-1].set_xlabel("Tiempo (min)")
    fig.tight_layout(); fig.savefig(IMG / "eval_gantt.png", dpi=160); plt.close(fig)


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    lab(); evaluacion(); print("graficos generados en", IMG)
