import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from schedulers import round_robin, sjf, from_assignment, optimal_bruteforce, min_min, fcfs
from evaluacion import JOBS


def test_round_robin_makespan_21():
    r = round_robin(JOBS, 3)
    assert r.loads() == [17, 21, 14] and r.makespan == 21


def test_sjf_order_and_makespan():
    r = sjf(JOBS, 3)
    assert [j for j, *_ in r.schedule] == ["J7", "J4", "J2", "J6", "J8", "J3", "J5", "J1"]
    assert r.makespan == 22


def test_optimized_is_18_and_optimal():
    r = from_assignment("opt", JOBS, {0: ["J1", "J6"], 1: ["J5", "J4", "J2"], 2: ["J3", "J8", "J7"]})
    assert r.makespan == 18
    assert optimal_bruteforce(JOBS, 3)[0] == 18


def test_min_min_beats_fcfs_on_lab_dataset():
    from laboratorio import dataset, VMS
    sp = [m for *_, m in VMS]
    t = dataset()
    assert min_min(t, 5, sp).makespan < fcfs(t, 5, sp).makespan
