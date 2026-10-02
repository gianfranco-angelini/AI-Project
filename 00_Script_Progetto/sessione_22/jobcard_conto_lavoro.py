# jobcard_conto_lavoro.py — Expediting fase 1: campi conto lavoro su Job Card + Server Script + riallineamento T08
# exec(open(f).read(), {"frappe": frappe, "SCRIVI_CL": False/True})
SCRIVI = globals().get("SCRIVI_CL", False)
print("=== MODALITA':", "SCRITTURA" if SCRIVI else "PROVA (nessuna scrittura)", "===")
DEP = "eval:doc.workstation_type=='Lavorazione Esterna' || doc.workstation=='Lavorazione Esterna'"
CAMPI = [
    {"fieldname": "custom_sb_conto_lavoro", "label": "Conto lavoro", "fieldtype": "Section Break", "insert_after": "custom_documenti_tecnici", "collapsible": 0, "depends_on": DEP},
    {"fieldname": "custom_fornitore", "label": "Fornitore", "fieldtype": "Link", "options": "Supplier", "insert_after": "custom_sb_conto_lavoro", "in_standard_filter": 1, "allow_on_submit": 1},
    {"fieldname": "custom_ordine_sap", "label": "N\u00b0 ordine SAP", "fieldtype": "Data", "insert_after": "custom_fornitore", "allow_on_submit": 1},
    {"fieldname": "custom_stato_cl", "label": "Stato conto lavoro", "fieldtype": "Select", "options": "Da inviare\nPresso fornitore\nRientrato", "insert_after": "custom_ordine_sap", "read_only": 1, "in_standard_filter": 1, "allow_on_submit": 1},
    {"fieldname": "custom_cb_conto_lavoro", "fieldtype": "Column Break", "insert_after": "custom_stato_cl"},
    {"fieldname": "custom_data_uscita", "label": "Data uscita", "fieldtype": "Date", "insert_after": "custom_cb_conto_lavoro", "allow_on_submit": 1},
    {"fieldname": "custom_rientro_previsto", "label": "Rientro previsto", "fieldtype": "Date", "insert_after": "custom_data_uscita", "read_only": 1, "allow_on_submit": 1},
    {"fieldname": "custom_rientro_effettivo", "label": "Rientro effettivo", "fieldtype": "Date", "insert_after": "custom_rientro_previsto", "allow_on_submit": 1},
]
SCRIPT_FORN = 'if doc.operation_id and not doc.get("custom_fornitore"):\n    wo_op = frappe.db.get_value("Work Order Operation", doc.operation_id, ["idx", "parent"], as_dict=True)\n    if wo_op:\n        bom_no = frappe.db.get_value("Work Order", wo_op.parent, "bom_no")\n        if bom_no:\n            forn = frappe.db.get_value("BOM Operation", {"parent": bom_no, "idx": wo_op.idx}, "custom_fornitore")\n            if forn:\n                doc.custom_fornitore = forn\nif (doc.workstation_type == "Lavorazione Esterna" or doc.workstation == "Lavorazione Esterna") and not doc.get("custom_stato_cl"):\n    doc.custom_stato_cl = "Da inviare"\n'
SCRIPT_CL = 'if doc.workstation_type == "Lavorazione Esterna" or doc.workstation == "Lavorazione Esterna":\n    if doc.get("custom_data_uscita"):\n        giorni = 0\n        if doc.expected_start_date and doc.expected_end_date:\n            secondi = frappe.utils.time_diff_in_seconds(doc.expected_end_date, doc.expected_start_date)\n            giorni = int((secondi + 86399) // 86400)\n        doc.custom_rientro_previsto = frappe.utils.add_days(doc.custom_data_uscita, giorni)\n    elif doc.expected_end_date:\n        doc.custom_rientro_previsto = frappe.utils.getdate(doc.expected_end_date)\n    if doc.get("custom_rientro_effettivo"):\n        doc.custom_stato_cl = "Rientrato"\n    elif doc.get("custom_data_uscita"):\n        doc.custom_stato_cl = "Presso fornitore"\n    else:\n        doc.custom_stato_cl = "Da inviare"\n'
SCRIPTS = [["JobCard_Fornitore", "Before Insert", SCRIPT_FORN], ["JobCard_Conto_Lavoro", "Before Save", SCRIPT_CL], ["JobCard_Conto_Lavoro_Submitted", "Before Save (Submitted Document)", SCRIPT_CL]]
for c in CAMPI:
    print("Campo", c["fieldname"], "esiste:", bool(frappe.db.exists("Custom Field", {"dt": "Job Card", "fieldname": c["fieldname"]})))
for s in SCRIPTS:
    print("Script", s[0], "esiste:", bool(frappe.db.exists("Server Script", s[0])))
# riallineamento Job Card esterne esistenti, con controllo del codice fase
piano = []
anomalie = []
for jc in frappe.db.sql("SELECT name, operation_id, work_order, expected_end_date, custom_descrizione_fase FROM `tabJob Card` WHERE (workstation_type='Lavorazione Esterna' OR workstation='Lavorazione Esterna') AND docstatus<2", as_dict=True):
    wo_op = frappe.db.get_value("Work Order Operation", jc.operation_id, ["idx", "parent"], as_dict=True) if jc.operation_id else None
    if not wo_op:
        anomalie.append(jc.name + " senza operation_id valido")
        continue
    bom_no = frappe.db.get_value("Work Order", wo_op.parent, "bom_no")
    bo = frappe.db.get_value("BOM Operation", {"parent": bom_no, "idx": wo_op.idx}, ["custom_fornitore", "description"], as_dict=True)
    if not bo or not bo.custom_fornitore:
        anomalie.append(jc.name + " fase BOM senza fornitore")
        continue
    cod_bom = frappe.utils.strip_html(bo.description or "").strip().split(" ")[0]
    cod_jc = frappe.utils.strip_html(jc.custom_descrizione_fase or "").strip().split(" ")[0]
    if cod_jc and cod_jc != cod_bom:
        anomalie.append(jc.name + " codice diverso: JC " + cod_jc + " / BOM " + cod_bom)
        continue
    piano.append([jc.name, bo.custom_fornitore, jc.expected_end_date, cod_bom])
print("\nJob Card esterne da allineare:", len(piano), "| anomalie:", len(anomalie))
for a in anomalie[:15]:
    print("   !", a)
for p in piano[:5]:
    print("   esempio:", p[0], p[3], "->", p[1], "| rientro previsto", p[2])
if SCRIVI:
    for c in CAMPI:
        if not frappe.db.exists("Custom Field", {"dt": "Job Card", "fieldname": c["fieldname"]}):
            d = frappe.new_doc("Custom Field")
            d.dt = "Job Card"
            d.update(c)
            d.insert()
    frappe.db.commit()
    for s in SCRIPTS:
        if not frappe.db.exists("Server Script", s[0]):
            x = frappe.new_doc("Server Script")
            x.name = s[0]
            x.script_type = "DocType Event"
            x.reference_doctype = "Job Card"
            x.doctype_event = s[1]
            x.script = s[2]
            x.insert()
    frappe.db.commit()
    for p in piano:
        frappe.db.set_value("Job Card", p[0], {"custom_fornitore": p[1], "custom_stato_cl": "Da inviare", "custom_rientro_previsto": frappe.utils.getdate(p[2]) if p[2] else None}, update_modified=False)
    frappe.db.commit()
    print("\n-> Job Card esterne con fornitore:", frappe.db.sql("SELECT custom_fornitore, COUNT(*) FROM `tabJob Card` WHERE IFNULL(custom_fornitore,'')!='' GROUP BY custom_fornitore ORDER BY 2 DESC"))
    print("-> stato:", frappe.db.sql("SELECT custom_stato_cl, COUNT(*) FROM `tabJob Card` WHERE (workstation_type='Lavorazione Esterna' OR workstation='Lavorazione Esterna') GROUP BY custom_stato_cl"))
