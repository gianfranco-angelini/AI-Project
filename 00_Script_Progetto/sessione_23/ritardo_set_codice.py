APPLICA = __APPLICA__
job_card_name = frappe.form_dict.get("job_card_name")
nuova_data_fine = frappe.form_dict.get("nuova_data_fine")
jc = frappe.get_doc("Job Card", job_card_name)
vecchia_fine = frappe.utils.getdate(jc.expected_end_date)
nuova_fine = frappe.utils.getdate(nuova_data_fine)
scarto_giorni = frappe.utils.date_diff(nuova_fine, vecchia_fine)
idx_corrente = frappe.db.get_value("Work Order Operation", jc.operation_id, "idx")

nuove = {}
nuove[jc.name] = [jc.expected_start_date, nuova_fine, jc.work_order, jc.operation, jc.workstation]
downstream = frappe.db.sql("""
    SELECT jc2.name, jc2.operation, jc2.workstation, jc2.expected_start_date, jc2.expected_end_date
    FROM `tabJob Card` jc2
    JOIN `tabWork Order Operation` woo ON woo.name = jc2.operation_id
    WHERE jc2.work_order = %s AND woo.idx > %s AND jc2.status != 'Completed' AND jc2.docstatus < 2
    ORDER BY woo.idx
""", (jc.work_order, idx_corrente), as_dict=True)
for d in downstream:
    nuove[d.name] = [
        frappe.utils.add_days(d.expected_start_date, scarto_giorni) if d.expected_start_date else None,
        frappe.utils.add_days(d.expected_end_date, scarto_giorni) if d.expected_end_date else None,
        jc.work_order, d.operation, d.workstation]

# cascata verso i Work Order padre (stesso Production Plan): se il figlio finisce dopo l'inizio del padre,
# il padre (Job Card non completate) slitta degli stessi giorni, e cosi via fino al prodotto finito
coda = [jc.work_order]
visti = []
giri = 0
wo_impattati = [jc.work_order]
while coda and giri < 80:
    giri = giri + 1
    wo = coda.pop(0)
    if wo in visti:
        continue
    visti.append(wo)
    fine = None
    for r in frappe.db.sql("SELECT name, expected_end_date FROM `tabJob Card` WHERE work_order=%s AND docstatus<2", wo, as_dict=True):
        e = nuove[r.name][1] if r.name in nuove else r.expected_end_date
        if e and (fine is None or frappe.utils.getdate(e) > fine):
            fine = frappe.utils.getdate(e)
    w = frappe.db.get_value("Work Order", wo, ["production_plan", "production_plan_sub_assembly_item"], as_dict=True)
    if not w or not w.production_plan_sub_assembly_item:
        continue
    padre_item = frappe.db.get_value("Production Plan Sub Assembly Item", w.production_plan_sub_assembly_item, "parent_item_code")
    padri = frappe.get_all("Work Order", filters={"production_plan": w.production_plan, "production_item": padre_item, "docstatus": 1}, pluck="name")
    for p in padri:
        jcs = frappe.db.sql("SELECT name, operation, workstation, expected_start_date, expected_end_date FROM `tabJob Card` WHERE work_order=%s AND docstatus<2 AND status != 'Completed'", p, as_dict=True)
        inizio = None
        for r in jcs:
            s = nuove[r.name][0] if r.name in nuove else r.expected_start_date
            if s and (inizio is None or frappe.utils.getdate(s) < inizio):
                inizio = frappe.utils.getdate(s)
        if inizio and fine and fine > inizio:
            delta = frappe.utils.date_diff(fine, inizio)
            for r in jcs:
                bs = nuove[r.name][0] if r.name in nuove else r.expected_start_date
                be = nuove[r.name][1] if r.name in nuove else r.expected_end_date
                nuove[r.name] = [frappe.utils.add_days(bs, delta) if bs else None, frappe.utils.add_days(be, delta) if be else None, p, r.operation, r.workstation]
            if p not in wo_impattati:
                wo_impattati.append(p)
            coda.append(p)

# fine del prodotto finito del set (WO senza riga sub-assembly nello stesso Production Plan)
pp = frappe.db.get_value("Work Order", jc.work_order, "production_plan")
fg = None
if pp:
    for c in frappe.get_all("Work Order", filters={"production_plan": pp, "docstatus": 1}, fields=["name", "production_plan_sub_assembly_item"]):
        if not c.production_plan_sub_assembly_item:
            fg = c.name
fine_fg = None
if fg:
    for r in frappe.db.sql("SELECT name, expected_end_date FROM `tabJob Card` WHERE work_order=%s AND docstatus<2", fg, as_dict=True):
        e = nuove[r.name][1] if r.name in nuove else r.expected_end_date
        if e and (fine_fg is None or frappe.utils.getdate(e) > fine_fg):
            fine_fg = frappe.utils.getdate(e)
if not fine_fg:
    fine_fg = nuova_fine

consegna = jc.get("custom_consegna_set") or frappe.db.get_value("Work Order", fg or jc.work_order, "expected_delivery_date")
project_name = frappe.db.get_value("Work Order", jc.work_order, "project")
buffer = (frappe.db.get_value("Project", project_name, "custom_buffer_giorni") or 0) if project_name else 0
sfora_reale = False
sfora_interna = False
avviso = None
if consegna:
    consegna = frappe.utils.getdate(consegna)
    interna = frappe.utils.add_days(consegna, -buffer)
    if fine_fg > consegna:
        sfora_reale = True
        avviso = f"ATTENZIONE: il set con consegna {consegna} finirebbe il {fine_fg}, {frappe.utils.date_diff(fine_fg, consegna)} giorni OLTRE LA CONSEGNA."
    elif fine_fg > interna:
        sfora_interna = True
        avviso = f"Avviso: il set resta entro la consegna ({consegna}) ma sfora il buffer di {frappe.utils.date_diff(fine_fg, interna)} giorni (fine prevista {fine_fg})."
    else:
        avviso = f"OK: il set finisce il {fine_fg}, entro la consegna ({consegna}) con buffer rispettato."

dettaglio = []
for k in nuove:
    v = nuove[k]
    dettaglio.append({"job_card": k, "operazione": str(v[2]) + " - " + str(v[3]), "workstation": v[4], "nuovo_inizio": str(v[0]) if v[0] else "", "nuova_fine": str(v[1]) if v[1] else ""})

if APPLICA:
    for k in nuove:
        v = nuove[k]
        if k == jc.name:
            frappe.db.set_value("Job Card", k, "expected_end_date", v[1], update_modified=False)
        else:
            frappe.db.set_value("Job Card", k, {"expected_start_date": v[0], "expected_end_date": v[1]}, update_modified=False)
    frappe.db.commit()

frappe.response["message"] = {
    "work_order": jc.work_order,
    "job_card_origine": job_card_name,
    "scarto_giorni": scarto_giorni,
    "scarto_applicato_giorni": scarto_giorni,
    "job_card_impattate": len(nuove),
    "job_card_aggiornate": list(nuove.keys()) if APPLICA else [],
    "work_order_impattati": wo_impattati,
    "fine_lavorazione_prevista": str(fine_fg),
    "consegna_set": str(consegna) if consegna else "",
    "sfora_deadline_interna": sfora_interna,
    "sfora_deadline_reale": sfora_reale,
    "avviso": avviso,
    "dettaglio": dettaglio
}
