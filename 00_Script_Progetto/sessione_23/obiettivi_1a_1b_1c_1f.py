# Sessione 23 - Chiusura obiettivi 1c / 1a / 1b / 1f (05/10/2026).
# 1c: Simula/Applica_Ritardo_JobCard -> confronto con la CONSEGNA DEL SET (custom_consegna_set - Buffer Project)
#     e cascata verso i Work Order padre fino al prodotto finito del set.
# 1a: Master Plan multi-commessa: scorciatoie Gantt Project / WO T09 / Task T09 nel Workspace, fix Gantt su Project,
#     report Carico Reparti con il "Calendario Remazel 2026-2029" (era "Festivi Italia 2026-2027").
# 1b: punti di monitoraggio T09: Task per set (gruppo) e per macro-assieme, con date dai Work Order; campo
#     Work Order.custom_task (legame WO -> Task).
# 1f: KPI e grafici per la T09 (copie filtrate su PROJ-0002) nel Workspace.
# Uso: exec(open(f).read(), {"frappe": frappe, "SCRIVI": False})
import json
SCRIVI = globals().get("SCRIVI", False)
print("=== MODALITA':", "SCRITTURA" if SCRIVI else "PROVA (nessuna scrittura)", "===")
CODICE_RITARDO = 'APPLICA = __APPLICA__\njob_card_name = frappe.form_dict.get("job_card_name")\nnuova_data_fine = frappe.form_dict.get("nuova_data_fine")\njc = frappe.get_doc("Job Card", job_card_name)\nvecchia_fine = frappe.utils.getdate(jc.expected_end_date)\nnuova_fine = frappe.utils.getdate(nuova_data_fine)\nscarto_giorni = frappe.utils.date_diff(nuova_fine, vecchia_fine)\nidx_corrente = frappe.db.get_value("Work Order Operation", jc.operation_id, "idx")\n\nnuove = {}\nnuove[jc.name] = [jc.expected_start_date, nuova_fine, jc.work_order, jc.operation, jc.workstation]\ndownstream = frappe.db.sql("""\n    SELECT jc2.name, jc2.operation, jc2.workstation, jc2.expected_start_date, jc2.expected_end_date\n    FROM `tabJob Card` jc2\n    JOIN `tabWork Order Operation` woo ON woo.name = jc2.operation_id\n    WHERE jc2.work_order = %s AND woo.idx > %s AND jc2.status != \'Completed\' AND jc2.docstatus < 2\n    ORDER BY woo.idx\n""", (jc.work_order, idx_corrente), as_dict=True)\nfor d in downstream:\n    nuove[d.name] = [\n        frappe.utils.add_days(d.expected_start_date, scarto_giorni) if d.expected_start_date else None,\n        frappe.utils.add_days(d.expected_end_date, scarto_giorni) if d.expected_end_date else None,\n        jc.work_order, d.operation, d.workstation]\n\n# cascata verso i Work Order padre (stesso Production Plan): se il figlio finisce dopo l\'inizio del padre,\n# il padre (Job Card non completate) slitta degli stessi giorni, e cosi via fino al prodotto finito\ncoda = [jc.work_order]\nvisti = []\ngiri = 0\nwo_impattati = [jc.work_order]\nwhile coda and giri < 80:\n    giri = giri + 1\n    wo = coda.pop(0)\n    if wo in visti:\n        continue\n    visti.append(wo)\n    fine = None\n    for r in frappe.db.sql("SELECT name, expected_end_date FROM `tabJob Card` WHERE work_order=%s AND docstatus<2", wo, as_dict=True):\n        e = nuove[r.name][1] if r.name in nuove else r.expected_end_date\n        if e and (fine is None or frappe.utils.getdate(e) > fine):\n            fine = frappe.utils.getdate(e)\n    w = frappe.db.get_value("Work Order", wo, ["production_plan", "production_plan_sub_assembly_item"], as_dict=True)\n    if not w or not w.production_plan_sub_assembly_item:\n        continue\n    padre_item = frappe.db.get_value("Production Plan Sub Assembly Item", w.production_plan_sub_assembly_item, "parent_item_code")\n    padri = frappe.get_all("Work Order", filters={"production_plan": w.production_plan, "production_item": padre_item, "docstatus": 1}, pluck="name")\n    for p in padri:\n        jcs = frappe.db.sql("SELECT name, operation, workstation, expected_start_date, expected_end_date FROM `tabJob Card` WHERE work_order=%s AND docstatus<2 AND status != \'Completed\'", p, as_dict=True)\n        inizio = None\n        for r in jcs:\n            s = nuove[r.name][0] if r.name in nuove else r.expected_start_date\n            if s and (inizio is None or frappe.utils.getdate(s) < inizio):\n                inizio = frappe.utils.getdate(s)\n        if inizio and fine and fine > inizio:\n            delta = frappe.utils.date_diff(fine, inizio)\n            for r in jcs:\n                bs = nuove[r.name][0] if r.name in nuove else r.expected_start_date\n                be = nuove[r.name][1] if r.name in nuove else r.expected_end_date\n                nuove[r.name] = [frappe.utils.add_days(bs, delta) if bs else None, frappe.utils.add_days(be, delta) if be else None, p, r.operation, r.workstation]\n            if p not in wo_impattati:\n                wo_impattati.append(p)\n            coda.append(p)\n\n# fine del prodotto finito del set (WO senza riga sub-assembly nello stesso Production Plan)\npp = frappe.db.get_value("Work Order", jc.work_order, "production_plan")\nfg = None\nif pp:\n    for c in frappe.get_all("Work Order", filters={"production_plan": pp, "docstatus": 1}, fields=["name", "production_plan_sub_assembly_item"]):\n        if not c.production_plan_sub_assembly_item:\n            fg = c.name\nfine_fg = None\nif fg:\n    for r in frappe.db.sql("SELECT name, expected_end_date FROM `tabJob Card` WHERE work_order=%s AND docstatus<2", fg, as_dict=True):\n        e = nuove[r.name][1] if r.name in nuove else r.expected_end_date\n        if e and (fine_fg is None or frappe.utils.getdate(e) > fine_fg):\n            fine_fg = frappe.utils.getdate(e)\nif not fine_fg:\n    fine_fg = nuova_fine\n\nconsegna = jc.get("custom_consegna_set") or frappe.db.get_value("Work Order", fg or jc.work_order, "expected_delivery_date")\nproject_name = frappe.db.get_value("Work Order", jc.work_order, "project")\nbuffer = (frappe.db.get_value("Project", project_name, "custom_buffer_giorni") or 0) if project_name else 0\nsfora_reale = False\nsfora_interna = False\navviso = None\nif consegna:\n    consegna = frappe.utils.getdate(consegna)\n    interna = frappe.utils.add_days(consegna, -buffer)\n    if fine_fg > consegna:\n        sfora_reale = True\n        avviso = f"ATTENZIONE: il set con consegna {consegna} finirebbe il {fine_fg}, {frappe.utils.date_diff(fine_fg, consegna)} giorni OLTRE LA CONSEGNA."\n    elif fine_fg > interna:\n        sfora_interna = True\n        avviso = f"Avviso: il set resta entro la consegna ({consegna}) ma sfora il buffer di {frappe.utils.date_diff(fine_fg, interna)} giorni (fine prevista {fine_fg})."\n    else:\n        avviso = f"OK: il set finisce il {fine_fg}, entro la consegna ({consegna}) con buffer rispettato."\n\ndettaglio = []\nfor k in nuove:\n    v = nuove[k]\n    dettaglio.append({"job_card": k, "operazione": str(v[2]) + " - " + str(v[3]), "workstation": v[4], "nuovo_inizio": str(v[0]) if v[0] else "", "nuova_fine": str(v[1]) if v[1] else ""})\n\nif APPLICA:\n    for k in nuove:\n        v = nuove[k]\n        if k == jc.name:\n            frappe.db.set_value("Job Card", k, "expected_end_date", v[1], update_modified=False)\n        else:\n            frappe.db.set_value("Job Card", k, {"expected_start_date": v[0], "expected_end_date": v[1]}, update_modified=False)\n    frappe.db.commit()\n\nfrappe.response["message"] = {\n    "work_order": jc.work_order,\n    "job_card_origine": job_card_name,\n    "scarto_giorni": scarto_giorni,\n    "scarto_applicato_giorni": scarto_giorni,\n    "job_card_impattate": len(nuove),\n    "job_card_aggiornate": list(nuove.keys()) if APPLICA else [],\n    "work_order_impattati": wo_impattati,\n    "fine_lavorazione_prevista": str(fine_fg),\n    "consegna_set": str(consegna) if consegna else "",\n    "sfora_deadline_interna": sfora_interna,\n    "sfora_deadline_reale": sfora_reale,\n    "avviso": avviso,\n    "dettaglio": dettaglio\n}\n'
PRJ = "PROJ-0002"

# ---------- Workspace
ws_name = None
for w in frappe.get_all("Workspace", fields=["name", "label", "title"]):
    if "produzione" in ((w.label or "") + " " + (w.title or "") + " " + w.name).lower():
        ws_name = w.name
print("Workspace trovato:", ws_name)

# ---------- 1c
for n in ["Simula_Ritardo_JobCard", "Applica_Ritardo_JobCard"]:
    print("1c)", n, "| esiste", bool(frappe.db.exists("Server Script", n)))

# ---------- 1a
q = frappe.db.get_value("Report", "Carico Reparti Settimanale", "query") or ""
print("1a) Report Carico Reparti usa 'Festivi Italia 2026-2027':", "Festivi Italia 2026-2027" in q)
gfix = frappe.db.get_value("Client Script", "Gantt_Fix_Remazel", ["script", "view"], as_dict=True)
print("1a) Gantt_Fix_Remazel presente:", bool(gfix), "| Gantt_Fix_Project_Remazel esiste:", bool(frappe.db.exists("Client Script", "Gantt_Fix_Project_Remazel")))
SCORCIATOIE = [
    ["Master Plan commesse (Gantt)", "/app/project/view/gantt"],
    ["Gantt Work Order T09", "/app/work-order/view/gantt?project=PROJ-0002"],
    ["Gantt monitoraggio T09", "/app/task/view/gantt?project=PROJ-0002"],
    ["Carico Reparti Settimanale", "/app/query-report/Carico Reparti Settimanale"],
]

# ---------- 1b
task_esistenti = frappe.db.count("Task", {"project": PRJ})
print("1b) Task esistenti su", PRJ, ":", task_esistenti, "| campo Work Order.custom_task esiste:", bool(frappe.db.exists("Custom Field", {"dt": "Work Order", "fieldname": "custom_task"})))
piano_task = []
pps = frappe.get_all("Production Plan", filters={"project": PRJ, "docstatus": 1}, fields=["name"], order_by="name")
nset = 0
for p in pps:
    nset = nset + 1
    fg_item = frappe.db.sql("SELECT item_code FROM `tabProduction Plan Item` WHERE parent=%s LIMIT 1", p.name)[0][0]
    righe = frappe.db.sql("SELECT production_item, parent_item_code, bom_level FROM `tabProduction Plan Sub Assembly Item` WHERE parent=%s", p.name, as_dict=True)
    padre = {}
    for r in righe:
        if r.production_item not in padre:
            padre[r.production_item] = r.parent_item_code
    wos = frappe.get_all("Work Order", filters={"production_plan": p.name, "docstatus": 1}, fields=["name", "production_item", "planned_start_date", "planned_end_date", "expected_delivery_date"])
    gruppi = {}
    consegna = None
    for w in wos:
        consegna = w.expected_delivery_date
        it = w.production_item
        if it == fg_item:
            chiave = fg_item
        else:
            x = it
            g = 0
            while padre.get(x) and padre.get(x) != fg_item and g < 25:
                x = padre.get(x)
                g = g + 1
            chiave = x
        if chiave not in gruppi:
            gruppi[chiave] = {"wo": [], "inizio": None, "fine": None}
        gruppi[chiave]["wo"].append(w.name)
        if w.planned_start_date and (gruppi[chiave]["inizio"] is None or w.planned_start_date < gruppi[chiave]["inizio"]):
            gruppi[chiave]["inizio"] = w.planned_start_date
        if w.planned_end_date and (gruppi[chiave]["fine"] is None or w.planned_end_date > gruppi[chiave]["fine"]):
            gruppi[chiave]["fine"] = w.planned_end_date
    piano_task.append({"set": nset, "pp": p.name, "fg": fg_item, "consegna": consegna, "gruppi": gruppi})
    print("1b) Set", nset, p.name, "consegna", consegna, "| macro-gruppi:", len(gruppi))
    for k in gruppi:
        print("      ", k, "| WO", len(gruppi[k]["wo"]), "|", gruppi[k]["inizio"], "->", gruppi[k]["fine"])

# ---------- 1f
COPIE_NC = [["Ordini Commessa", "Ordini Commessa T09"], ["Pezzi Prodotti", "Pezzi Prodotti T09"]]
COPIE_CH = [["Ordini di Produzione per Stato", "Ordini di Produzione per Stato T09"], ["Avvio Ordini per Settimana", "Avvio Ordini per Settimana T09"]]
for c in COPIE_NC:
    print("1f) Number Card", c[0], "->", c[1], "| esiste gia:", bool(frappe.db.exists("Number Card", c[1])))
for c in COPIE_CH:
    print("1f) Dashboard Chart", c[0], "->", c[1], "| esiste gia:", bool(frappe.db.exists("Dashboard Chart", c[1])))

if not SCRIVI:
    print("PROVA: nessuna scrittura")
else:
    # 1c
    for n, applica in [["Simula_Ritardo_JobCard", "False"], ["Applica_Ritardo_JobCard", "True"]]:
        ss = frappe.get_doc("Server Script", n)
        ss.script = CODICE_RITARDO.replace("__APPLICA__", applica)
        ss.save()
        print("-> 1c aggiornato", n)
    # 1a
    if "Festivi Italia 2026-2027" in q:
        frappe.db.set_value("Report", "Carico Reparti Settimanale", "query", q.replace("Festivi Italia 2026-2027", "Calendario Remazel 2026-2029"))
        print("-> 1a report Carico Reparti su Calendario Remazel 2026-2029")
    if gfix and not frappe.db.exists("Client Script", "Gantt_Fix_Project_Remazel"):
        cs = frappe.new_doc("Client Script")
        cs.name = "Gantt_Fix_Project_Remazel"
        cs.dt = "Project"
        cs.view = gfix.view
        cs.enabled = 1
        cs.script = gfix.script.replace("'Work Order'", "'Project'").replace('"Work Order"', '"Project"')
        cs.insert()
        print("-> 1a Client Script Gantt_Fix_Project_Remazel creato")
    # 1b
    if not frappe.db.exists("Custom Field", {"dt": "Work Order", "fieldname": "custom_task"}):
        cf = frappe.new_doc("Custom Field")
        cf.dt = "Work Order"
        cf.fieldname = "custom_task"
        cf.label = "Punto di monitoraggio (Task)"
        cf.fieldtype = "Link"
        cf.options = "Task"
        cf.insert_after = "project"
        cf.read_only = 1
        cf.allow_on_submit = 1
        cf.in_standard_filter = 1
        cf.insert()
        print("-> 1b campo Work Order.custom_task creato")
    if task_esistenti == 0:
        nt = 0
        for s in piano_task:
            inizi = []
            fini = []
            for k in s["gruppi"]:
                if s["gruppi"][k]["inizio"]:
                    inizi.append(s["gruppi"][k]["inizio"])
                if s["gruppi"][k]["fine"]:
                    fini.append(s["gruppi"][k]["fine"])
            tg = frappe.new_doc("Task")
            tg.subject = "T09 Set " + str(s["set"]) + " - consegna " + frappe.utils.formatdate(s["consegna"], "dd/MM/yyyy")
            tg.project = PRJ
            tg.is_group = 1
            tg.exp_start_date = min(inizi)
            tg.exp_end_date = max(fini)
            tg.insert()
            nt = nt + 1
            figli = []
            for k in s["gruppi"]:
                if k == s["fg"]:
                    continue
                nome_it = frappe.db.get_value("Item", k, "item_name") or ""
                t = frappe.new_doc("Task")
                t.subject = "Set " + str(s["set"]) + " - " + k.replace("T08-0100-", "").replace("T09-0100-", "") + " " + nome_it
                t.project = PRJ
                t.parent_task = tg.name
                t.exp_start_date = s["gruppi"][k]["inizio"]
                t.exp_end_date = s["gruppi"][k]["fine"]
                t.insert()
                nt = nt + 1
                figli.append(t.name)
                for w in s["gruppi"][k]["wo"]:
                    frappe.db.set_value("Work Order", w, "custom_task", t.name, update_modified=False)
            if s["fg"] in s["gruppi"]:
                t = frappe.new_doc("Task")
                t.subject = "Set " + str(s["set"]) + " - A0001 ASSEMBLAGGIO FINALE"
                t.project = PRJ
                t.parent_task = tg.name
                t.exp_start_date = s["gruppi"][s["fg"]]["inizio"]
                t.exp_end_date = s["gruppi"][s["fg"]]["fine"]
                for f in figli:
                    t.append("depends_on", {"task": f})
                try:
                    t.insert()
                except Exception as e:
                    print("   dipendenze non accettate, Task senza dipendenze:", repr(e)[:150])
                    frappe.db.rollback()
                    t = frappe.new_doc("Task")
                    t.subject = "Set " + str(s["set"]) + " - A0001 ASSEMBLAGGIO FINALE"
                    t.project = PRJ
                    t.parent_task = tg.name
                    t.exp_start_date = s["gruppi"][s["fg"]]["inizio"]
                    t.exp_end_date = s["gruppi"][s["fg"]]["fine"]
                    t.insert()
                nt = nt + 1
                for w in s["gruppi"][s["fg"]]["wo"]:
                    frappe.db.set_value("Work Order", w, "custom_task", t.name, update_modified=False)
            frappe.db.commit()
        print("-> 1b Task creati:", nt, "| WO collegati:", frappe.db.count("Work Order", {"project": PRJ, "custom_task": ["is", "set"]}))
    else:
        print("-> 1b Task gia presenti su", PRJ, ": salto")
    # 1f
    nuove_nc = []
    nuovi_ch = []
    for c in COPIE_NC:
        if frappe.db.exists("Number Card", c[0]) and not frappe.db.exists("Number Card", c[1]):
            d = frappe.copy_doc(frappe.get_doc("Number Card", c[0]))
            d.label = c[1]
            d.name = c[1]
            d.filters_json = (d.filters_json or "").replace("PROJ-0001", PRJ)
            d.insert()
            nuove_nc.append(d.name)
    for c in COPIE_CH:
        if frappe.db.exists("Dashboard Chart", c[0]) and not frappe.db.exists("Dashboard Chart", c[1]):
            d = frappe.copy_doc(frappe.get_doc("Dashboard Chart", c[0]))
            d.chart_name = c[1]
            d.name = c[1]
            d.filters_json = (d.filters_json or "").replace("PROJ-0001", PRJ)
            d.insert()
            nuovi_ch.append(d.name)
    print("-> 1f creati: Number Card", nuove_nc, "| Chart", nuovi_ch)
    # Workspace: scorciatoie (1a) e KPI T09 (1f)
    if ws_name:
        ws = frappe.get_doc("Workspace", ws_name)
        blocchi = json.loads(ws.content or "[]")
        presenti = []
        for s in ws.shortcuts:
            presenti.append(s.label)
        for sc in SCORCIATOIE:
            if sc[0] not in presenti:
                ws.append("shortcuts", {"label": sc[0], "type": "URL", "url": sc[1], "color": "Blue"})
                blocchi.append({"id": frappe.generate_hash(length=10), "type": "shortcut", "data": {"shortcut_name": sc[0], "col": 3}})
        for n in nuove_nc:
            ws.append("number_cards", {"number_card_name": n, "label": n})
            blocchi.append({"id": frappe.generate_hash(length=10), "type": "number_card", "data": {"number_card_name": n, "col": 3}})
        for n in nuovi_ch:
            ws.append("charts", {"chart_name": n, "label": n})
            blocchi.append({"id": frappe.generate_hash(length=10), "type": "chart", "data": {"chart_name": n, "col": 6}})
        ws.content = json.dumps(blocchi)
        ws.save()
        print("-> Workspace", ws_name, "aggiornato: scorciatoie", len(ws.shortcuts), "| number card", len(ws.number_cards), "| chart", len(ws.charts))
    frappe.db.commit()
    frappe.clear_cache()
    print("FATTO. Chiudere e riaprire la console; nel browser ricaricare con Ctrl+F5.")
