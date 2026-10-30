"""Genera la hoja de calculo (con formulas) de la evaluacion practica."""
import pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from evaluacion import JOBS

OUT = pathlib.Path(__file__).resolve().parent.parent / "results" / "evaluacion_scheduling.xlsx"
H = PatternFill("solid", fgColor="5A189A"); L = PatternFill("solid", fgColor="E0AAFF")
W = Font(bold=True, color="FFFFFF"); thin = Side(style="thin", color="9D4EDD"); B = Border(left=thin, right=thin, top=thin, bottom=thin)


def head(ws, row, vals):
    for c, v in enumerate(vals, 1):
        x = ws.cell(row=row, column=c, value=v); x.fill, x.font, x.border = H, W, B
        x.alignment = Alignment(horizontal="center")


wb = Workbook(); ws = wb.active; ws.title = "Datos"
head(ws, 1, ["Trabajo", "Duracion (min)", "VM Round Robin", "VM Optimizada"])
rr = ["VM1", "VM2", "VM3"]
opt = {"J1": "VM1", "J6": "VM1", "J5": "VM2", "J4": "VM2", "J2": "VM2", "J3": "VM3", "J8": "VM3", "J7": "VM3"}
for i, (j, d) in enumerate(JOBS, 2):
    ws.append([j, d, rr[(i - 2) % 3], opt[j]])
    for c in range(1, 5): ws.cell(row=i, column=c).border = B
ws["A11"] = "Total"; ws["B11"] = "=SUM(B2:B9)"; ws["A12"] = "Carga media teorica"; ws["B12"] = "=B11/3"
ws["A13"] = "Limite inferior entero"; ws["B13"] = "=ROUNDUP(B11/3,0)"
for c in ("A11", "A12", "A13"): ws[c].font = Font(bold=True)
ws["B12"].number_format = "0.00"

for name, col in (("Actividad1_RR", "C"), ("Actividad3_Optima", "D")):
    s = wb.create_sheet(name); head(s, 1, ["VM", "Carga total (min)"])
    for k in range(1, 4):
        s.cell(row=k + 1, column=1, value=f"VM{k}")
        s.cell(row=k + 1, column=2, value=f'=SUMIF(Datos!{col}$2:{col}$9,A{k+1},Datos!$B$2:$B$9)')
        for c in (1, 2): s.cell(row=k + 1, column=c).border = B
    s["A5"] = "Makespan (Cmax)"; s["B5"] = "=MAX(B2:B4)"; s["A5"].font = s["B5"].font = Font(bold=True)
    s["A5"].fill = s["B5"].fill = L
    s.column_dimensions["A"].width = 20; s.column_dimensions["B"].width = 20

s = wb.create_sheet("Actividad2_SJF"); head(s, 1, ["Posicion", "Trabajo", "Duracion"])
for i, (j, d) in enumerate(sorted(JOBS, key=lambda x: x[1]), 1):
    s.append([i, j, d])
    for c in (1, 2, 3): s.cell(row=i + 1, column=c).border = B
head(s, 11, ["Trabajo", "VM asignada", "Inicio", "Fin"])
free = [0, 0, 0]
for i, (j, d) in enumerate(sorted(JOBS, key=lambda x: x[1])):
    vm = free.index(min(free)); s.append([j, f"VM{vm+1}", free[vm], free[vm] + d]); free[vm] += d
for r in range(12, 20):
    for c in range(1, 5): s.cell(row=r, column=c).border = B
s["F11"] = "VM"; s["G11"] = "Carga"; s["F11"].fill = s["G11"].fill = H; s["F11"].font = s["G11"].font = W
for k in range(1, 4):
    s.cell(row=11 + k, column=6, value=f"VM{k}"); s.cell(row=11 + k, column=7, value=f"=SUMIF(B12:B19,F{11+k},D12:D19)-SUMIF(B12:B19,F{11+k},C12:C19)")
s["F15"] = "Makespan (Cmax)"; s["G15"] = "=MAX(G12:G14)"; s["F15"].font = s["G15"].font = Font(bold=True); s["F15"].fill = s["G15"].fill = L
for sh in (ws, s):
    for col in "ABCDEFG": sh.column_dimensions[col].width = 20
wb.save(OUT); print("xlsx ->", OUT)
