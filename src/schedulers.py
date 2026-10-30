"""Algoritmos de scheduling para asignar trabajos a maquinas virtuales (VM).

Modelo: todos los trabajos estan disponibles en t=0, cada VM ejecuta un solo
trabajo a la vez, sin costo de cambio de contexto y sin interrupciones.
Cada trabajo es una tupla (nombre, longitud). La duracion en una VM es
longitud / velocidad (velocidad = 1.0 para VM homogeneas).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from itertools import product
from typing import Dict, List, Sequence, Tuple

Job = Tuple[str, float]


@dataclass
class Result:
    name: str
    n_vms: int
    # asignacion: lista de (job, vm, inicio, fin) en orden de ejecucion
    schedule: List[Tuple[str, int, float, float]] = field(default_factory=list)

    def loads(self) -> List[float]:
        out = [0.0] * self.n_vms
        for _, vm, _, fin in self.schedule:
            out[vm] = max(out[vm], fin)
        return out

    def jobs_by_vm(self) -> Dict[int, List[str]]:
        d = {i: [] for i in range(self.n_vms)}
        for j, vm, _, _ in self.schedule:
            d[vm].append(j)
        return d

    @property
    def makespan(self) -> float:
        return max(self.loads())

    def avg_wait(self) -> float:
        # todos llegan en t=0 -> espera = instante de inicio
        return sum(s for _, _, s, _ in self.schedule) / len(self.schedule)

    def avg_completion(self) -> float:
        return sum(f for _, _, _, f in self.schedule) / len(self.schedule)

    def utilization(self) -> List[float]:
        ms = self.makespan
        busy = [0.0] * self.n_vms
        for _, vm, s, f in self.schedule:
            busy[vm] += f - s
        return [b / ms for b in busy]

    def avg_utilization(self) -> float:
        u = self.utilization()
        return sum(u) / len(u)

    def weighted_utilization(self, speeds) -> float:
        """Uso de la capacidad total: sum(capacidad_i * util_i) / sum(capacidad_i)."""
        u = self.utilization()
        return sum(c * x for c, x in zip(speeds, u)) / sum(speeds)

    def throughput(self) -> float:
        return len(self.schedule) / self.makespan


def _speeds(n_vms: int, speeds: Sequence[float] | None) -> List[float]:
    return list(speeds) if speeds is not None else [1.0] * n_vms


def round_robin(jobs: Sequence[Job], n_vms: int, speeds=None) -> Result:
    """Job i -> VM (i mod n). No mira duracion ni capacidad."""
    sp = _speeds(n_vms, speeds)
    free = [0.0] * n_vms
    r = Result("Round Robin", n_vms)
    for i, (name, length) in enumerate(jobs):
        vm = i % n_vms
        d = length / sp[vm]
        r.schedule.append((name, vm, free[vm], free[vm] + d))
        free[vm] += d
    return r


def fcfs(jobs: Sequence[Job], n_vms: int, speeds=None) -> Result:
    """Orden de llegada; cada trabajo va a la VM que se libera primero."""
    sp = _speeds(n_vms, speeds)
    free = [0.0] * n_vms
    r = Result("FCFS", n_vms)
    for name, length in jobs:
        vm = min(range(n_vms), key=lambda k: (free[k], k))
        d = length / sp[vm]
        r.schedule.append((name, vm, free[vm], free[vm] + d))
        free[vm] += d
    return r


def sjf(jobs: Sequence[Job], n_vms: int, speeds=None) -> Result:
    """Orden de menor a mayor duracion; cada trabajo va a la VM libre antes."""
    ordered = sorted(jobs, key=lambda j: j[1])
    r = fcfs(ordered, n_vms, speeds)
    r.name = "SJF"
    return r


def ljf(jobs: Sequence[Job], n_vms: int, speeds=None) -> Result:
    """Longest Job First (LPT): mayor a menor, a la VM libre antes."""
    ordered = sorted(jobs, key=lambda j: -j[1])
    r = fcfs(ordered, n_vms, speeds)
    r.name = "LJF (LPT)"
    return r


def _minmax(jobs: Sequence[Job], n_vms: int, speeds, pick_max: bool) -> Result:
    sp = _speeds(n_vms, speeds)
    ready = [0.0] * n_vms
    pending = list(jobs)
    r = Result("Max-Min" if pick_max else "Min-Min", n_vms)
    while pending:
        best = None  # (tiempo_fin_minimo, indice_tarea, vm)
        for idx, (name, length) in enumerate(pending):
            vm = min(range(n_vms), key=lambda k: (ready[k] + length / sp[k], k))
            ct = ready[vm] + length / sp[vm]
            cand = (ct, idx, vm)
            if best is None or (cand[0] > best[0] if pick_max else cand[0] < best[0]):
                best = cand
        ct, idx, vm = best
        name, length = pending.pop(idx)
        r.schedule.append((name, vm, ready[vm], ct))
        ready[vm] = ct
    return r


def min_min(jobs, n_vms, speeds=None) -> Result:
    return _minmax(jobs, n_vms, speeds, pick_max=False)


def max_min(jobs, n_vms, speeds=None) -> Result:
    return _minmax(jobs, n_vms, speeds, pick_max=True)


def from_assignment(name: str, jobs: Sequence[Job], assignment: Dict[int, List[str]], speeds=None) -> Result:
    """Construye un Result a partir de una asignacion manual {vm: [jobs]}."""
    length = dict(jobs)
    n = len(assignment)
    sp = _speeds(n, speeds)
    r = Result(name, n)
    for vm, names in assignment.items():
        t = 0.0
        for j in names:
            d = length[j] / sp[vm]
            r.schedule.append((j, vm, t, t + d))
            t += d
    return r


def optimal_bruteforce(jobs: Sequence[Job], n_vms: int) -> Tuple[float, Dict[int, List[str]], int]:
    """Busca el makespan minimo probando n_vms**n_jobs asignaciones (VM homogeneas)."""
    best, best_asg = float("inf"), None
    for combo in product(range(n_vms), repeat=len(jobs)):
        loads = [0.0] * n_vms
        for (_, l), vm in zip(jobs, combo):
            loads[vm] += l
        m = max(loads)
        if m < best:
            best, best_asg = m, combo
    asg = {i: [] for i in range(n_vms)}
    for (n, _), vm in zip(jobs, best_asg):
        asg[vm].append(n)
    return best, asg, n_vms ** len(jobs)
