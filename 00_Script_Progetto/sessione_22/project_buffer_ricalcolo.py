# Sessione 22 - Ricalcolo automatico della deadline interna sul Project
# 1) crea/aggiorna il Server Script "Project_Deadline_Interna" (Before Save su Project)
# 2) rinomina le etichette: "Buffer Commessa" -> "Buffer Project"
# 3) ricalcola subito PROJ-0001 e PROJ-0002
# Uso: incollare in bench console (cd /home/frappe-user/frappe-bench && bench --site site1.local console)

NOME_SS = "Project_Deadline_Interna"
CODICE_SS = """if doc.expected_end_date:
    buffer = doc.get("custom_buffer_giorni") or 0
    doc.custom_deadline_interna = frappe.utils.add_days(doc.expected_end_date, -buffer)
"""

# 1) Server Script
if frappe.db.exists("Server Script", NOME_SS):
    ss = frappe.get_doc("Server Script", NOME_SS)
    print("Server Script esistente: aggiorno")
else:
    ss = frappe.new_doc("Server Script")
    ss.name = NOME_SS
    print("Server Script nuovo: creo")
ss.script_type = "DocType Event"
ss.reference_doctype = "Project"
ss.doctype_event = "Before Save"
ss.disabled = 0
ss.script = CODICE_SS
ss.save()

# 2) Etichette senza "commessa"
cf = frappe.get_doc("Custom Field", {"dt": "Project", "fieldname": "custom_buffer_giorni"})
print("Prima:", cf.label, "|", cf.description)
cf.label = "Buffer Project (giorni)"
cf.description = "Giorni di margine di sicurezza da riservare prima della scadenza reale (Expected End Date). Modificabile per singolo Project, di default 5."
cf.save()
cf2 = frappe.get_doc("Custom Field", {"dt": "Project", "fieldname": "custom_deadline_interna"})
print("Prima:", cf2.label, "|", cf2.description)
cf2.description = "Expected End Date meno il Buffer Project: scadenza interna di sicurezza, non comunicata al cliente. Si ricalcola a ogni salvataggio."
cf2.save()

# 3) Ricalcolo immediato
for p in ["PROJ-0001", "PROJ-0002"]:
    d = frappe.get_doc("Project", p)
    vecchia = d.custom_deadline_interna
    d.save()
    print(p, "fine:", d.expected_end_date, "buffer:", d.custom_buffer_giorni, "deadline:", vecchia, "->", d.custom_deadline_interna)

frappe.db.commit()
frappe.clear_cache(doctype="Project")
print("OK")
