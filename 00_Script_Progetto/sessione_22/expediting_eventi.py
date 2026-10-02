# Sessione 22 - Expediting a EVENTI sulla Job Card esterna (decisione di Gian 02/10/2026).
# Inizia = materiale partito verso il fornitore; Completa = materiale rientrato. Date dai Time Log.
# A mano solo: N. ordine SAP, Data promessa fornitore.
# 1) nuovo campo custom_data_promessa; 2) Data uscita / Rientro effettivo diventano sola lettura (da eventi);
# 3) chiusura sezione Conto lavoro (custom_sb_fine_conto_lavoro); 4) Server Script rivisti;
# 5) riallineamento Job Card esterne senza Time Log (pulisce la prova su PO-JOB05173).
# Uso: exec(open(f).read(), {"frappe": frappe, "SCRIVI": False})
SCRIVI = globals().get("SCRIVI", False)
DEP = "eval:doc.workstation_type=='Lavorazione Esterna' || doc.workstation=='Lavorazione Esterna'"
print("=== MODALITA':", "SCRITTURA" if SCRIVI else "PROVA (nessuna scrittura)", "===")

NUOVI = [
    {"fieldname": "custom_data_promessa", "label": "Data promessa fornitore", "fieldtype": "Date", "insert_after": "custom_ordine_sap", "allow_on_submit": 1, "depends_on": DEP, "description": "Facoltativa. Se compilata, il rientro previsto è questa data."},
    {"fieldname": "custom_sb_fine_conto_lavoro", "label": "", "fieldtype": "Section Break", "insert_after": "custom_rientro_effettivo"},
]
MODIFICHE = {
    "custom_stato_cl": {"insert_after": "custom_data_promessa"},
    "custom_data_uscita": {"label": "Uscita (da Inizia)", "read_only": 1, "description": "Data del primo avvio (Inizia) della Job Card: materiale partito verso il fornitore."},
    "custom_rientro_effettivo": {"label": "Rientro (da Completa)", "read_only": 1, "description": "Data del completamento: materiale rientrato dal fornitore."},
    "custom_rientro_previsto": {"description": "Data promessa se presente; altrimenti uscita + durata pianificata; altrimenti fine pianificata."},
}

SCRIPT_CL = '''if doc.workstation_type == "Lavorazione Esterna" or doc.workstation == "Lavorazione Esterna":
    inizio = None
    fine = None
    aperto = False
    qta = 0
    for t in doc.time_logs:
        if t.from_time:
            f = frappe.utils.get_datetime(t.from_time)
            if inizio is None or f < inizio:
                inizio = f
            if t.to_time:
                e = frappe.utils.get_datetime(t.to_time)
                if fine is None or e > fine:
                    fine = e
            else:
                aperto = True
        qta = qta + frappe.utils.flt(t.completed_qty)
    doc.custom_data_uscita = frappe.utils.getdate(inizio) if inizio else None
    rientrato = doc.docstatus == 1 or (fine is not None and not aperto and frappe.utils.flt(doc.for_quantity) > 0 and qta >= frappe.utils.flt(doc.for_quantity))
    doc.custom_rientro_effettivo = frappe.utils.getdate(fine) if (rientrato and fine) else None
    if doc.get("custom_data_promessa"):
        doc.custom_rientro_previsto = doc.custom_data_promessa
    elif doc.custom_data_uscita:
        giorni = 0
        if doc.expected_start_date and doc.expected_end_date:
            secondi = frappe.utils.time_diff_in_seconds(doc.expected_end_date, doc.expected_start_date)
            giorni = int((secondi + 86399) // 86400)
        doc.custom_rientro_previsto = frappe.utils.add_days(doc.custom_data_uscita, giorni)
    elif doc.expected_end_date:
        doc.custom_rientro_previsto = frappe.utils.getdate(doc.expected_end_date)
    if doc.custom_rientro_effettivo:
        doc.custom_stato_cl = "Rientrato"
    elif doc.custom_data_uscita:
        doc.custom_stato_cl = "Presso fornitore"
    else:
        doc.custom_stato_cl = "Da inviare"
'''
compile(SCRIPT_CL, "script_cl", "exec")

# --- verifica stato attuale
for n in NUOVI:
    print("Campo", n["fieldname"], "esiste:", bool(frappe.db.exists("Custom Field", {"dt": "Job Card", "fieldname": n["fieldname"]})))
for k in MODIFICHE:
    print("Campo", k, "attuale:", frappe.db.get_value("Custom Field", {"dt": "Job Card", "fieldname": k}, ["label", "read_only", "insert_after"], as_dict=True))
esterne = "(workstation_type='Lavorazione Esterna' OR workstation='Lavorazione Esterna')"
con_log = frappe.db.sql("SELECT COUNT(DISTINCT jc.name) FROM `tabJob Card` jc JOIN `tabJob Card Time Log` tl ON tl.parent = jc.name WHERE jc.docstatus < 2 AND " + esterne.replace("workstation", "jc.workstation"))[0][0]
senza_log = frappe.db.sql("SELECT COUNT(*) FROM `tabJob Card` jc WHERE jc.docstatus < 2 AND " + esterne.replace("workstation", "jc.workstation") + " AND NOT EXISTS (SELECT 1 FROM `tabJob Card Time Log` tl WHERE tl.parent = jc.name)")[0][0]
print("JC esterne con Time Log:", con_log, "| senza Time Log (da riallineare):", senza_log)
print("Da ripulire (uscita/rientro a mano):", frappe.db.sql("SELECT name, custom_data_uscita, custom_rientro_effettivo, custom_stato_cl FROM `tabJob Card` WHERE custom_data_uscita IS NOT NULL OR custom_rientro_effettivo IS NOT NULL"))

if SCRIVI:
    for n in NUOVI:
        if not frappe.db.exists("Custom Field", {"dt": "Job Card", "fieldname": n["fieldname"]}):
            cf = frappe.new_doc("Custom Field")
            cf.dt = "Job Card"
            cf.update(n)
            cf.insert()
            print("-> creato", n["fieldname"])
    for k in MODIFICHE:
        cf = frappe.get_doc("Custom Field", {"dt": "Job Card", "fieldname": k})
        cf.update(MODIFICHE[k])
        cf.save()
        print("-> aggiornato", k)
    for nome in ["JobCard_Conto_Lavoro", "JobCard_Conto_Lavoro_Submitted"]:
        ss = frappe.get_doc("Server Script", nome)
        ss.script = SCRIPT_CL
        ss.save()
        print("-> Server Script aggiornato", nome, "|", ss.doctype_event)
    frappe.db.sql("UPDATE `tabJob Card` jc SET jc.custom_data_uscita = NULL, jc.custom_rientro_effettivo = NULL, jc.custom_stato_cl = 'Da inviare', jc.custom_rientro_previsto = DATE(jc.expected_end_date) WHERE jc.docstatus < 2 AND " + esterne.replace("workstation", "jc.workstation") + " AND NOT EXISTS (SELECT 1 FROM `tabJob Card Time Log` tl WHERE tl.parent = jc.name)")
    frappe.db.commit()
    frappe.clear_cache(doctype="Job Card")
    print("-> riallineate JC esterne senza Time Log. Stato:", frappe.db.sql("SELECT custom_stato_cl, COUNT(*) FROM `tabJob Card` WHERE docstatus < 2 AND " + esterne + " GROUP BY custom_stato_cl"))
    print("-> uscita/rientro residui:", frappe.db.sql("SELECT COUNT(*) FROM `tabJob Card` WHERE custom_data_uscita IS NOT NULL OR custom_rientro_effettivo IS NOT NULL")[0][0])
    print("Chiudere e riaprire la console prima di altre operazioni sulle Job Card.")
else:
    print("PROVA: nessuna scrittura")
