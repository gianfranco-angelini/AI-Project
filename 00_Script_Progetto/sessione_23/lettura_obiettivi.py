# Sessione 23 - SOLA LETTURA. Codice e configurazione da leggere prima di chiudere 1c / 1a / 1b / 1f.
OUT = "/home/frappe-user/script_progetto/lettura_obiettivi.txt"
r = []
for n in ["Simula_Ritardo_JobCard", "Applica_Ritardo_JobCard"]:
    r.append("=== SERVER SCRIPT " + n + " | api_method " + str(frappe.db.get_value("Server Script", n, "api_method")) + " ===")
    r.append(frappe.db.get_value("Server Script", n, "script") or "")
r.append("=== CLIENT SCRIPT Job Card-Ritardo ===")
r.append(frappe.db.get_value("Client Script", "Job Card-Ritardo", "script") or "")
r.append("=== WORKSPACE ===")
for w in frappe.get_all("Workspace", filters={"name": ["like", "%Remazel%"]}, pluck="name"):
    d = frappe.get_doc("Workspace", w)
    r.append("Workspace " + w + " | public " + str(d.public))
    for s in d.shortcuts:
        r.append("  shortcut | " + str(s.label) + " | " + str(s.type) + " | " + str(s.link_to) + " | " + str(s.url or "") + " | " + str(s.stats_filter or ""))
    for l in d.links:
        r.append("  link | " + str(l.label) + " | " + str(l.type) + " | " + str(l.link_type) + " | " + str(l.link_to))
    for c in d.number_cards:
        r.append("  number card | " + str(c.number_card_name))
    for c in d.charts:
        r.append("  chart | " + str(c.chart_name))
r.append("=== NUMBER CARD ===")
for c in frappe.get_all("Number Card", fields=["name", "document_type", "function", "filters_json", "dynamic_filters_json"], filters={"creation": [">", "2026-07-01"]}):
    r.append(c.name + " | " + str(c.document_type) + " | " + str(c.function) + " | " + str(c.filters_json) + " | " + str(c.dynamic_filters_json))
r.append("=== DASHBOARD CHART ===")
for c in frappe.get_all("Dashboard Chart", fields=["name", "chart_type", "document_type", "report_name", "filters_json"], filters={"creation": [">", "2026-07-01"]}):
    r.append(c.name + " | " + str(c.chart_type) + " | " + str(c.document_type or c.report_name) + " | " + str(c.filters_json))
r.append("=== REPORT Carico Reparti Settimanale ===")
r.append(str(frappe.db.get_value("Report", "Carico Reparti Settimanale", "query")))
r.append("=== TASK PROJ-0001 ===")
for t in frappe.get_all("Task", filters={"project": "PROJ-0001"}, fields=["name", "subject", "parent_task", "is_group", "exp_start_date", "exp_end_date", "status"], order_by="name"):
    dip = frappe.get_all("Task Depends On", filters={"parent": t.name}, pluck="task")
    r.append(t.name + " | " + str(t.subject) + " | padre " + str(t.parent_task) + " | gruppo " + str(t.is_group) + " | " + str(t.exp_start_date) + " -> " + str(t.exp_end_date) + " | " + str(t.status) + " | dipende da " + ",".join(dip))
r.append("=== CAMPI TASK/WORK ORDER utili ===")
for dt in ["Task", "Work Order"]:
    m = frappe.get_meta(dt)
    for f in m.fields:
        if f.fieldname in ["project", "parent_task", "depends_on", "exp_start_date", "exp_end_date", "task", "custom_task"]:
            r.append(dt + "." + f.fieldname + " | " + str(f.fieldtype) + " | " + str(f.options))
open(OUT, "w").write("\n".join(r))
print("Righe:", len(r), "->", OUT)
