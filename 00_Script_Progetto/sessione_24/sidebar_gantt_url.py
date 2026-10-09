# Sessione 24 - Annulla sidebar_doctype.py: le 4 voci del Workspace Sidebar "Produzione Remazel" tornano voci URL
# verso la vista Gantt. Convertite in DocType duplicavano "Work Order T09" e "Punti di monitoraggio T09".
# Uso: exec(open("/home/frappe-user/script_progetto/sidebar_gantt_url.py").read(), {"frappe": frappe, "SCRIVI": False})
SCRIVI = globals().get("SCRIVI", False)
WS = "Produzione Remazel"
GANTT = {
    "Master Plan": "/app/task/view/gantt?is_group=1",
    "Supplier Gantt": "/app/job-card/view/gantt?workstation=Lavorazione%20Esterna",
    "Gantt Work Order T09": "/app/work-order/view/gantt?project=PROJ-0002",
    "Gantt monitoraggio T09": "/app/task/view/gantt?project=PROJ-0002",
}

modifiche = 0
trovate = set()
sb = frappe.get_doc("Workspace Sidebar", WS)
for it in sb.items:
    if it.type != "Link" or it.label not in GANTT:
        continue
    trovate.add(it.label)
    if it.link_type == "URL" and it.url == GANTT[it.label]:
        continue
    print("Sidebar |", it.label, "|", it.link_type, it.link_to or "", it.filters or "", "-> URL", GANTT[it.label])
    it.link_type = "URL"
    it.url = GANTT[it.label]
    it.link_to = None
    it.filters = None
    it.route_options = None
    modifiche += 1

for etichetta in GANTT:
    if etichetta not in trovate:
        print("NON TROVATA |", etichetta)
print("Modifiche:", modifiche)
if SCRIVI and modifiche:
    sb.save()
    frappe.db.commit()
    print("SCRITTO (commit)")
else:
    frappe.db.rollback()
    print("PROVA: nulla scritto")
