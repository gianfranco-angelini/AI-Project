# Sessione 24 - SOLA LETTURA. Estrazione delle operazioni T09 (PROJ-0002) per il confronto con i codici 371 dei monitor.
# Per ogni BOM usata dai Work Order del Project: operazioni (codice fase RZL, tipo, workstation, interna/esterna, tempo
# pianificato) + dati delle Job Card (quante, completate, minuti registrati). NON scrive nulla sul database.
# Output: CSV + copia gzip/base64 da incollare in chat.
# Uso (console): exec(open("/home/frappe-user/script_progetto/estrai_operazioni_t09.py").read(), {"frappe": frappe})
import re, csv, gzip, base64, io, collections

PROJECT = "PROJ-0002"
OUT = "/home/frappe-user/script_progetto/operazioni_t09.csv"
OUT64 = "/home/frappe-user/script_progetto/operazioni_t09.b64"
RE_COD = re.compile(r"^\s*(T\d\d-\d{4}-[AP]\d{4}-\d\d([A-Z]{2}))")

ops = frappe.db.sql("""
    SELECT b.item, b.name AS bom, bo.idx, bo.operation, bo.workstation, bo.description, bo.time_in_mins
    FROM `tabBOM` b JOIN `tabBOM Operation` bo ON bo.parent = b.name AND bo.parenttype = 'BOM'
    WHERE b.name IN (SELECT DISTINCT bom_no FROM `tabWork Order` WHERE project = %s AND docstatus < 2)
    ORDER BY b.item, bo.idx""", PROJECT, as_dict=True)

jc = frappe.db.sql("""
    SELECT wo.bom_no AS bom, woo.description,
           COUNT(*) AS n_jc, SUM(jc.status = 'Completed') AS jc_completate,
           SUM(IFNULL(jc.total_time_in_mins, 0)) AS minuti_registrati
    FROM `tabJob Card` jc
    JOIN `tabWork Order` wo ON wo.name = jc.work_order
    LEFT JOIN `tabWork Order Operation` woo ON woo.name = jc.operation_id
    WHERE wo.project = %s AND jc.docstatus < 2
    GROUP BY wo.bom_no, woo.description""", PROJECT, as_dict=True)
jc_map = {(r.bom, (r.description or "").strip()): r for r in jc}

campi = ["item", "bom", "idx", "codice_fase", "tipo", "esterna", "workstation", "operation",
         "time_in_mins", "n_jc", "jc_completate", "minuti_registrati", "descrizione"]
righe = []
riep = collections.Counter()
senza_codice = 0
for o in ops:
    desc = (o.description or "").strip()
    m = RE_COD.match(desc)
    cod, tipo = (m.group(1), m.group(2)) if m else ("", "")
    if not m:
        senza_codice += 1
    est = 1 if (o.workstation or "") == "Lavorazione Esterna" else 0
    j = jc_map.get((o.bom, desc), {})
    righe.append({
        "item": o.item, "bom": o.bom, "idx": o.idx, "codice_fase": cod, "tipo": tipo, "esterna": est,
        "workstation": o.workstation, "operation": o.operation, "time_in_mins": o.time_in_mins,
        "n_jc": j.get("n_jc", 0), "jc_completate": j.get("jc_completate", 0) or 0,
        "minuti_registrati": j.get("minuti_registrati", 0) or 0, "descrizione": desc.replace("\n", " "),
    })
    riep[("EST" if est else "INT", tipo or "??")] += 1

buf = io.StringIO()
w = csv.DictWriter(buf, fieldnames=campi, delimiter=";")
w.writeheader()
w.writerows(righe)
testo = buf.getvalue()
with open(OUT, "w", encoding="utf-8") as f:
    f.write(testo)
b64 = base64.b64encode(gzip.compress(testo.encode("utf-8"), 9)).decode()
with open(OUT64, "w") as f:
    f.write(b64)

print("BOM:", len(set(r["bom"] for r in righe)), "| operazioni:", len(righe), "| senza codice fase:", senza_codice)
print("Job Card collegate:", sum(r["n_jc"] for r in righe), "| gruppi JC senza operazione BOM:",
      len([k for k in jc_map if k not in set((r["bom"], r["descrizione"]) for r in righe)]))
for k in sorted(riep):
    print("  ", k[0], k[1], riep[k])
print("CSV:", OUT)
print("Da incollare in chat:", OUT64, "(", len(b64), "caratteri )")
