# Sessione 24 - SOLA LETTURA. Allineamento fasi completate T09 (file 26-19008_EG.xlsx del 06/10/2026).
# Per ogni fase/set: trova la Job Card, calcola le date stimate e verifica i vincoli. NON scrive nulla sul database.
# Uso (console): exec(open("/home/frappe-user/script_progetto/allineamento_fasi_prova.py").read(), {"frappe": frappe})
import datetime
from frappe.utils import get_datetime, getdate, add_days

PROJECT = "PROJ-0002"
FG = "T09-0100-A0001"
BUFFER = 5
ANCORA = datetime.datetime(2026, 10, 6, 17, 0, 0)   # data del file di avanzamento
OUT = "/home/frappe-user/script_progetto/allineamento_fasi_prova.txt"

# lotti da 10 liner del file -> nostri set: set1=[1], set2=[2,3], set3=[4,5], set4=[6,7], set5=[8,9], set6=[10]
LOTTI_SET = {1: [1], 2: [2, 3], 3: [4, 5], 4: [6, 7], 5: [8, 9], 6: [10]}
TUTTI = list(range(1, 11))
FATTE = [  # articolo, codice fase, lotti completati
    ("T09-0100-P1800", "T09-0100-P1800-10LT", TUTTI),
    ("T08-0100-P1400", "T08-0100-P1400-10LT", [1, 2, 3, 4, 5]),
    ("T08-0100-P1400", "T08-0100-P1400-10QC", [1, 2, 3, 4, 5]),
    ("T09-0100-P3104", "T09-0100-P3104-10LT", TUTTI),
    ("T09-0100-P3104", "T09-0100-P3104-10QC", TUTTI),
    ("T08-0200-P3203", "T08-0200-P3203-10LT", TUTTI),
    ("T08-0200-P3203", "T08-0200-P3203-10QC", TUTTI),
    ("T08-0200-P3302", "T08-0200-P3302-10LT", [1, 2, 3, 4, 5, 6, 7, 8]),
    ("T08-0200-P3302", "T08-0200-P3302-10QC", [1, 2, 3, 4, 5, 6, 7, 8]),
    ("T08-0100-P2108", "T08-0100-P2108-10LA", TUTTI),
]

righe = []
def p(*a):
    righe.append(" ".join([str(x) for x in a]))

def giorni_lav_indietro(dt, n):
    while n > 0:
        dt = dt - datetime.timedelta(days=1)
        if dt.weekday() < 5:
            n -= 1
    return dt

# ---- set: date di consegna e ritardo attuale
consegne = [r[0] for r in frappe.db.sql("""SELECT DISTINCT jc.custom_consegna_set FROM `tabJob Card` jc
    JOIN `tabWork Order` wo ON wo.name = jc.work_order
    WHERE wo.project=%s AND wo.docstatus=1 AND jc.docstatus<2 AND jc.custom_consegna_set IS NOT NULL
    ORDER BY jc.custom_consegna_set""", PROJECT)]
p("=== SET ===")
SET = {}
for i, c in enumerate(consegne, 1):
    fine = frappe.db.sql("""SELECT MAX(planned_end_date) FROM `tabWork Order` WHERE project=%s AND docstatus=1
        AND production_item=%s AND expected_delivery_date=%s""", (PROJECT, FG, c))[0][0]
    obiettivo = add_days(getdate(c), -BUFFER)
    ritardo = max(0, (getdate(fine) - obiettivo).days) if fine else 0
    ancora = giorni_lav_indietro(ANCORA, 6 - i)   # set scaglionati: set 6 = 06/10, set 5 = giorno lavorativo prima, ...
    SET[i] = {"consegna": c, "ritardo": ritardo, "ancora": ancora}
    p("set", i, "| consegna", c, "| fine A0001", fine, "| obiettivo", obiettivo, "| ritardo gg", ritardo, "| ancora fallback", ancora)
if len(consegne) != 6:
    p("!!! ATTESI 6 SET, TROVATI", len(consegne))

# ---- controlli generali
p("=== CONTROLLI ===")
for art in sorted(set(x[0] for x in FATTE)):
    p("Item", art, "esiste:", bool(frappe.db.exists("Item", art)))
meta_tl = frappe.get_meta("Job Card Time Log")
p("Job Card Time Log.employee obbligatorio:", meta_tl.get_field("employee").reqd if meta_tl.get_field("employee") else "campo assente")
ms = frappe.get_single("Manufacturing Settings")
for f in ["disable_capacity_planning", "allow_overtime", "job_card_excess_transfer", "backflush_raw_materials_based_on"]:
    if ms.meta.get_field(f):
        p("Manufacturing Settings", f, "=", ms.get(f))

# ---- ricerca Job Card e calcolo date
p("=== FASI ===")
piano = []   # (set, wo, jc, seq, workstation, qta, start, end, metodo)
for art, codice, lotti in FATTE:
    for s, ls in LOTTI_SET.items():
        fatti = [l for l in ls if l in lotti]
        if not fatti:
            continue
        frazione = float(len(fatti)) / len(ls)
        jcs = frappe.db.sql("""SELECT jc.name, jc.work_order, jc.docstatus, jc.status, jc.for_quantity, jc.sequence_id,
                IFNULL(jc.workstation, jc.workstation_type) AS reparto, jc.expected_start_date, jc.expected_end_date,
                jc.time_required, (SELECT COUNT(*) FROM `tabJob Card Time Log` t WHERE t.parent=jc.name) AS nlog
            FROM `tabJob Card` jc JOIN `tabWork Order` wo ON wo.name=jc.work_order
            WHERE wo.project=%s AND wo.docstatus=1 AND jc.docstatus<2 AND wo.production_item=%s
              AND jc.custom_consegna_set=%s AND IFNULL(jc.custom_descrizione_fase,'') LIKE %s""",
            (PROJECT, art, SET[s]["consegna"], "%" + codice + "%"), as_dict=True)
        if len(jcs) != 1:
            p("!!!", codice, "set", s, ": Job Card trovate", len(jcs), [j.name for j in jcs])
            continue
        j = jcs[0]
        wo = frappe.db.get_value("Work Order", j.work_order, ["skip_transfer", "transfer_material_against", "status"], as_dict=True)
        piano.append({"set": s, "codice": codice, "jc": j, "wo": j.work_order, "wo_info": wo, "frazione": frazione,
                      "qta": round(j.for_quantity * frazione, 3)})

# date: per Work Order, a ritroso
p("=== DATE STIMATE ===")
per_wo = {}
for r in piano:
    per_wo.setdefault(r["wo"], []).append(r)
for wo, rs in per_wo.items():
    rs.sort(key=lambda r: r["jc"].sequence_id or 0)
    s = rs[0]["set"]
    off = SET[s]["ritardo"]
    metodo = "piano-ritardo"
    for r in rs:
        st, en = get_datetime(r["jc"].expected_start_date), get_datetime(r["jc"].expected_end_date)
        r["start"], r["end"] = st - datetime.timedelta(days=off), en - datetime.timedelta(days=off)
    if off == 0 or rs[-1]["end"] > SET[s]["ancora"]:
        metodo = "a ritroso da ancora"
        fine = SET[s]["ancora"]
        for r in reversed(rs):
            dur = get_datetime(r["jc"].expected_end_date) - get_datetime(r["jc"].expected_start_date)
            if dur.total_seconds() <= 0:
                dur = datetime.timedelta(minutes=r["jc"].time_required or 60)
            r["end"], r["start"] = fine, fine - dur
            fine = r["start"]
    for r in rs:
        r["metodo"] = metodo
        j = r["jc"]
        p("set", r["set"], "|", r["codice"], "|", j.name, "| WO", wo, "| reparto", j.reparto, "| stato", j.status, "doc", j.docstatus,
          "| log esistenti", j.nlog, "| qta", r["qta"], "di", j.for_quantity, "| pianif.", j.expected_start_date, "->", j.expected_end_date,
          "| STIMA", r["start"].strftime("%d/%m/%Y %H:%M"), "->", r["end"].strftime("%d/%m/%Y %H:%M"), "|", metodo,
          "| WO skip_transfer", r["wo_info"].skip_transfer, "transfer_against", r["wo_info"].transfer_material_against,
          "| PARZIALE" if r["frazione"] < 1 else "")

# sovrapposizioni per reparto rispetto alla capacità
p("=== SOVRAPPOSIZIONI PER REPARTO ===")
for rep in sorted(set(r["jc"].reparto for r in piano)):
    cap = frappe.db.get_value("Workstation", rep, "production_capacity") or 1
    ev = []
    for r in piano:
        if r["jc"].reparto == rep:
            ev.append((r["start"], 1)); ev.append((r["end"], -1))
    ev.sort(key=lambda e: (e[0], e[1]))
    cur = mx = 0
    for _, d in ev:
        cur += d; mx = max(mx, cur)
    p(rep, "| capacità", cap, "| massima contemporaneità stimata", mx, "| OK" if mx <= cap else "| !!! SUPERA LA CAPACITA")

p("=== RIEPILOGO ===")
p("Job Card da allineare:", len(piano), "| di cui parziali:", len([r for r in piano if r["frazione"] < 1]),
  "| già con log:", len([r for r in piano if r["jc"].nlog]), "| già confermate:", len([r for r in piano if r["jc"].docstatus == 1]))
with open(OUT, "w") as f:
    f.write("\n".join(righe) + "\n")
print("\n".join(righe[-12:]))
print("Scritto", OUT, "-", len(righe), "righe")
