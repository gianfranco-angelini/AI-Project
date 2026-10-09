# Sessione 24 - SOLA LETTURA. Avanzamento dei punti di monitoraggio (Task) calcolato dalle Job Card dei Work Order collegati.
# % = minuti pianificati delle fasi completate / minuti pianificati totali (parziali in proporzione alla quantità).
# Uso (console): exec(open("/home/frappe-user/script_progetto/avanzamento_task_prova.py").read(), {"frappe": frappe})
PROJECT = globals().get("PROJECT", "PROJ-0002")
OUT = "/home/frappe-user/script_progetto/avanzamento_task_prova.txt"
righe = []
def p(*a):
    righe.append(" ".join([str(x) for x in a]))

tasks = frappe.get_all("Task", filters={"project": PROJECT},
    fields=["name", "subject", "is_group", "parent_task", "progress", "exp_start_date", "exp_end_date", "act_start_date", "act_end_date", "status"],
    order_by="exp_start_date, name")
peso = {}
for t in tasks:
    r = frappe.db.sql("""SELECT
            SUM(IFNULL(jc.time_required,0)) AS tot,
            SUM(IFNULL(jc.time_required,0) * CASE WHEN jc.docstatus=1 THEN 1
                ELSE LEAST(IFNULL(jc.total_completed_qty,0)/NULLIF(jc.for_quantity,0),1) END) AS fatto,
            COUNT(*) AS njc, SUM(jc.docstatus=1) AS nchiuse,
            (SELECT MIN(tl.from_time) FROM `tabJob Card Time Log` tl JOIN `tabJob Card` j2 ON j2.name=tl.parent
               JOIN `tabWork Order` w2 ON w2.name=j2.work_order WHERE w2.custom_task=%s AND j2.docstatus<2) AS inizio
        FROM `tabJob Card` jc JOIN `tabWork Order` wo ON wo.name=jc.work_order
        WHERE wo.custom_task=%s AND wo.docstatus=1 AND jc.docstatus<2""", (t.name, t.name), as_dict=True)[0]
    peso[t.name] = {"tot": float(r.tot or 0), "fatto": float(r.fatto or 0), "njc": r.njc or 0, "nchiuse": int(r.nchiuse or 0), "inizio": r.inizio}
# gruppi: somma dei figli (più eventuali WO collegati direttamente al gruppo)
figli = {}
for t in tasks:
    if t.parent_task:
        figli.setdefault(t.parent_task, []).append(t.name)
def totale(n):
    tot, fatto, njc, nch = peso[n]["tot"], peso[n]["fatto"], peso[n]["njc"], peso[n]["nchiuse"]
    ini = [peso[n]["inizio"]] if peso[n]["inizio"] else []
    for f in figli.get(n, []):
        a, b, c, d, e = totale(f)
        tot += a; fatto += b; njc += c; nch += d; ini += e
    return tot, fatto, njc, nch, ini

p("=== TASK", PROJECT, "===", len(tasks))
for t in tasks:
    tot, fatto, njc, nch, ini = totale(t.name)
    perc = round(100.0 * fatto / tot, 1) if tot else 0
    p(("GRUPPO " if t.is_group else "  ") + t.name, "|", (t.subject or "")[:45], "| JC", njc, "chiuse", nch,
      "| min tot", int(tot), "fatti", int(fatto), "| % calcolata", perc, "| % attuale", t.progress,
      "| inizio effettivo", min(ini) if ini else "-", "| act_start attuale", t.act_start_date or "-",
      "| pianif.", t.exp_start_date, "->", t.exp_end_date)
senza = frappe.db.sql("""SELECT COUNT(*) FROM `tabWork Order` WHERE project=%s AND docstatus=1 AND IFNULL(custom_task,'')=''""", PROJECT)[0][0]
p("Work Order del Project senza Task collegato:", senza)
p("=== Client Script Gantt_Fix_Task_Remazel ===")
for l in (frappe.db.get_value("Client Script", "Gantt_Fix_Task_Remazel", "script") or "").splitlines():
    p("   ", l)
p("=== Metodo % completamento del Project ===", frappe.db.get_value("Project", PROJECT, ["percent_complete_method", "percent_complete"]))
with open(OUT, "w") as f:
    f.write("\n".join(righe) + "\n")
print("Scritto", OUT, "-", len(righe), "righe")
