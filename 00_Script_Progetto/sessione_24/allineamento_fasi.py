# Sessione 24 - Allineamento fasi completate T09 (file 26-19008_EG.xlsx del 06/10/2026).
# SCRIVI=False: esegue tutto (date, tempi, conferma) e alla fine fa ROLLBACK -> prova completa senza scrivere.
# SCRIVI=True : stesse operazioni con COMMIT.
# Uso (console): exec(open("/home/frappe-user/script_progetto/allineamento_fasi.py").read(), {"frappe": frappe, "SCRIVI": False})
import datetime
from frappe.utils import get_datetime, getdate, add_days

SCRIVI = globals().get("SCRIVI", False)
PROJECT = "PROJ-0002"
FG = "T09-0100-A0001"
BUFFER = 5
ANCORA = datetime.datetime(2026, 10, 6, 17, 0, 0)
NOTA = "Allineamento da avanzamento 06/10/2026 (file 26-19008_EG) - date e tempi STIMATI da piano, non consuntivo"
OUT = "/home/frappe-user/script_progetto/allineamento_fasi_%s.txt" % ("scrivi" if SCRIVI else "prova")
ESTERNO = "Lavorazione Esterna"

LOTTI_SET = {1: [1], 2: [2, 3], 3: [4, 5], 4: [6, 7], 5: [8, 9], 6: [10]}
TUTTI = list(range(1, 11))
FATTE = [  # articolo (parte finale), fase (parte finale), lotti completati
    ("P1800", "P1800-10LT", TUTTI),
    ("P1400", "P1400-10LT", [1, 2, 3, 4, 5]),
    ("P1400", "P1400-10QC", [1, 2, 3, 4, 5]),
    ("P3104", "P3104-10LT", TUTTI),
    ("P3104", "P3104-10QC", TUTTI),
    ("P3203", "P3203-10LT", TUTTI),
    ("P3203", "P3203-10QC", TUTTI),
    ("P3302", "P3302-10LT", [1, 2, 3, 4, 5, 6, 7, 8]),
    ("P3302", "P3302-10QC", [1, 2, 3, 4, 5, 6, 7, 8]),
    ("P2108", "P2108-10LA", TUTTI),
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

def lunedi_se_weekend(dt):
    while dt.weekday() >= 5:
        dt = dt + datetime.timedelta(days=1)
    return dt

# ---- set
consegne = [r[0] for r in frappe.db.sql("""SELECT DISTINCT jc.custom_consegna_set FROM `tabJob Card` jc
    JOIN `tabWork Order` wo ON wo.name = jc.work_order
    WHERE wo.project=%s AND wo.docstatus=1 AND jc.docstatus<2 AND jc.custom_consegna_set IS NOT NULL
    ORDER BY jc.custom_consegna_set""", PROJECT)]
SET = {}
for i, c in enumerate(consegne, 1):
    fine = frappe.db.sql("""SELECT MAX(planned_end_date) FROM `tabWork Order` WHERE project=%s AND docstatus=1
        AND production_item=%s AND expected_delivery_date=%s""", (PROJECT, FG, c))[0][0]
    rit = max(0, (getdate(fine) - add_days(getdate(c), -BUFFER)).days) if fine else 0
    SET[i] = {"consegna": c, "ritardo": rit, "ancora": giorni_lav_indietro(ANCORA, 6 - i)}
    p("set", i, "| consegna", c, "| ritardo gg", rit, "| ancora", SET[i]["ancora"])

# ---- Job Card
piano = []
for art, codice, lotti in FATTE:
    for s, ls in LOTTI_SET.items():
        fatti = [l for l in ls if l in lotti]
        if not fatti:
            continue
        jcs = frappe.db.sql("""SELECT jc.name, jc.work_order, jc.docstatus, jc.for_quantity, jc.sequence_id,
                IFNULL(jc.workstation, jc.workstation_type) AS reparto, jc.expected_start_date, jc.expected_end_date,
                jc.time_required, wo.production_item
            FROM `tabJob Card` jc JOIN `tabWork Order` wo ON wo.name=jc.work_order
            WHERE wo.project=%s AND wo.docstatus=1 AND jc.docstatus<2 AND wo.production_item LIKE %s
              AND jc.custom_consegna_set=%s AND IFNULL(jc.custom_descrizione_fase,'') LIKE %s""",
            (PROJECT, "%-" + art, SET[s]["consegna"], "%-" + codice + "%"), as_dict=True)
        if len(jcs) != 1:
            p("!!!", codice, "set", s, ": Job Card trovate", len(jcs), [j.name for j in jcs])
            continue
        j = jcs[0]
        fr = float(len(fatti)) / len(ls)
        piano.append({"set": s, "codice": j.production_item + " " + codice, "jc": j, "wo": j.work_order,
                      "frazione": fr, "qta": round(j.for_quantity * fr, 3)})

# ---- date stimate
per_wo = {}
for r in piano:
    per_wo.setdefault(r["wo"], []).append(r)
ancora_set = dict((s, SET[s]["ancora"]) for s in SET)   # scende man mano: un controllo dopo l'altro nello stesso set
for wo in sorted(per_wo, key=lambda w: (per_wo[w][0]["set"], w)):
    rs = sorted(per_wo[wo], key=lambda r: r["jc"].sequence_id or 0)
    s = rs[0]["set"]
    off = SET[s]["ritardo"]
    for r in rs:
        r["start"] = get_datetime(r["jc"].expected_start_date) - datetime.timedelta(days=off)
        r["end"] = get_datetime(r["jc"].expected_end_date) - datetime.timedelta(days=off)
        r["metodo"] = "piano-ritardo"
    if off == 0 or rs[-1]["end"] > ancora_set[s]:
        fine = ancora_set[s]
        for r in reversed(rs):
            dur = get_datetime(r["jc"].expected_end_date) - get_datetime(r["jc"].expected_start_date)
            if dur.total_seconds() <= 0:
                dur = datetime.timedelta(minutes=r["jc"].time_required or 60)
            r["end"], r["start"], r["metodo"] = fine, fine - dur, "a ritroso"
            fine = r["start"]
        if rs[-1]["jc"].reparto != ESTERNO:
            ancora_set[s] = rs[-1]["start"]   # il controllo successivo dello stesso set finisce quando inizia questo
    else:
        # fasi interne in fine settimana -> lunedì stessa ora (se resta prima dell'ancora)
        for r in rs:
            if r["jc"].reparto != ESTERNO and r["start"].weekday() >= 5:
                d = lunedi_se_weekend(r["start"]) - r["start"]
                if r["end"] + d <= ancora_set[s]:
                    r["start"], r["end"] = r["start"] + d, r["end"] + d

# ---- capacità
for rep in sorted(set(r["jc"].reparto for r in piano)):
    cap = frappe.db.get_value("Workstation", rep, "production_capacity") or 1
    ev = []
    for r in piano:
        if r["jc"].reparto == rep:
            ev += [(r["start"], 1), (r["end"], -1)]
    ev.sort(key=lambda e: (e[0], e[1]))
    cur = mx = 0
    for _, d in ev:
        cur += d; mx = max(mx, cur)
    p("CAPACITA", rep, "| cap", cap, "| max contemporanee", mx, "| OK" if mx <= cap else "| !!! SUPERA")

# ---- esecuzione (in ordine di sequenza)
ok = err = 0
for r in sorted(piano, key=lambda r: (r["set"], r["wo"], r["jc"].sequence_id or 0)):
    j = r["jc"]
    try:
        doc = frappe.get_doc("Job Card", j.name)
        if doc.docstatus != 0 or doc.time_logs:
            p("SALTATA", j.name, "(già con tempi o confermata)")
            continue
        if r["frazione"] < 1:
            # parziale: nessun tempo registrato (la sequenza impedisce il controllo prima della fase esterna completa);
            # solo nota, la Job Card resta da eseguire e si registra quando la fase è completa
            # nota scritta direttamente sul campo: il salvataggio del documento attiverebbe il controllo di sequenza
            frappe.db.set_value("Job Card", doc.name, "remarks", ((doc.remarks or "") + "\n" + "Al 06/10/2026 (file 26-19008_EG) completati %s su %s pezzi: da registrare a fase completa" % (r["qta"], doc.for_quantity)).strip(), update_modified=False)
            azione = "solo nota (parziale)"
        else:
            doc.expected_start_date = r["start"]
            doc.expected_end_date = r["end"]
            doc.append("time_logs", {"from_time": r["start"], "to_time": r["end"],
                                     "time_in_mins": (r["end"] - r["start"]).total_seconds() / 60.0,
                                     "completed_qty": r["qta"]})
            doc.remarks = ((doc.remarks or "") + "\n" + NOTA).strip()
            doc.save()
            doc.submit()
            azione = "confermata"
        doc.reload()
        p("OK set", r["set"], "|", r["codice"], "|", j.name, "|", r["start"].strftime("%d/%m/%Y %H:%M"), "->",
          r["end"].strftime("%d/%m/%Y %H:%M"), "|", r["metodo"], "| qta", r["qta"], "|", azione, "| stato", doc.status,
          "| stato CL", doc.get("custom_stato_cl") or "")
        ok += 1
    except Exception as e:
        err += 1
        p("ERRORE set", r["set"], "|", r["codice"], "|", j.name, "|", repr(e)[:300])
        frappe.clear_messages()

p("=== RIEPILOGO === Job Card", len(piano), "| ok", ok, "| errori", err, "| modalità", "SCRIVI (commit)" if SCRIVI else "PROVA (rollback)")
if SCRIVI and err == 0:
    frappe.db.commit()
else:
    frappe.db.rollback()
    if SCRIVI:
        p("!!! errori presenti: ROLLBACK, nulla è stato scritto")
with open(OUT, "w") as f:
    f.write("\n".join(righe) + "\n")
print("\n".join(righe[-6:]))
print("Scritto", OUT)
