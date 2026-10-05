# Sessione 23 - SOLA LETTURA. Inventario delle personalizzazioni ERPNext per il documento di riepilogo.
# Uso (console): exec(open("/home/frappe-user/script_progetto/inventario_personalizzazioni.py").read(), {"frappe": frappe})
OUT = "/home/frappe-user/script_progetto/inventario_personalizzazioni.txt"
righe = []

def p(*a):
    righe.append(" ".join([str(x) for x in a]))

p("=== CUSTOM FIELD per DocType ===")
for r in frappe.db.sql("SELECT dt, fieldname, label, fieldtype FROM `tabCustom Field` ORDER BY dt, idx", as_dict=True):
    p(r.dt, "|", r.fieldname, "|", r.label, "|", r.fieldtype)
p("=== SERVER SCRIPT ===")
for r in frappe.get_all("Server Script", fields=["name", "script_type", "reference_doctype", "doctype_event", "api_method", "disabled"], order_by="name"):
    p(r.name, "|", r.script_type, "|", r.reference_doctype or "", "|", r.doctype_event or r.api_method or "", "| DISABILITATO" if r.disabled else "")
p("=== CLIENT SCRIPT ===")
for r in frappe.get_all("Client Script", fields=["name", "dt", "view", "enabled"], order_by="name"):
    p(r.name, "|", r.dt, "|", r.view, "| attivo" if r.enabled else "| DISATTIVO")
p("=== REPORT NON STANDARD ===")
for r in frappe.get_all("Report", filters={"is_standard": "No"}, fields=["name", "ref_doctype", "report_type"]):
    p(r.name, "|", r.ref_doctype, "|", r.report_type)
p("=== DOCTYPE CUSTOM ===")
for r in frappe.get_all("DocType", filters={"custom": 1}, fields=["name", "istable", "module"]):
    p(r.name, "| tabella figlia" if r.istable else "| documento", "|", r.module)
p("=== WORKSPACE / DASHBOARD / NUMBER CARD / CHART (creati dopo 01/07/2026) ===")
for dt in ["Workspace", "Dashboard", "Number Card", "Dashboard Chart", "Print Format"]:
    for r in frappe.get_all(dt, filters={"creation": [">", "2026-07-01"]}, fields=["name"], order_by="creation"):
        p(dt, "|", r.name)
p("=== RUOLI CUSTOM ===")
for r in frappe.get_all("Role", filters={"is_custom": 1}, fields=["name"]):
    p("Ruolo |", r.name)
p("=== PROPERTY SETTER per DocType (dopo 01/07/2026) ===")
for r in frappe.db.sql("SELECT doc_type, COUNT(*) n FROM `tabProperty Setter` WHERE creation > '2026-07-01' GROUP BY doc_type", as_dict=True):
    p(r.doc_type, "|", r.n)
p("=== WORKSTATION ===")
for r in frappe.get_all("Workstation", fields=["name", "workstation_type", "production_capacity", "holiday_list"]):
    p(r.name, "|", r.workstation_type, "| capacita", r.production_capacity, "|", r.holiday_list or "24h, nessun calendario")
p("=== HOLIDAY LIST ===")
for r in frappe.get_all("Holiday List", fields=["name", "from_date", "to_date"]):
    p(r.name, "|", r.from_date, "->", r.to_date, "| giorni", frappe.db.count("Holiday", {"parent": r.name}))
p("=== PROJECT ===")
for r in frappe.get_all("Project", fields=["name", "project_name", "expected_start_date", "expected_end_date", "custom_buffer_giorni", "custom_deadline_interna"]):
    p(r.name, "|", r.project_name, "|", r.expected_start_date, "->", r.expected_end_date, "| buffer", r.custom_buffer_giorni, "| deadline", r.custom_deadline_interna)
p("=== CONTEGGI ===")
for pr in ["PROJ-0001", "PROJ-0002"]:
    p(pr, "| WO", frappe.db.sql("SELECT docstatus, COUNT(*) FROM `tabWork Order` WHERE project=%s GROUP BY docstatus", pr), "| JC", frappe.db.count("Job Card", {"project": pr}), "| Task", frappe.db.count("Task", {"project": pr}))
p("User attivi:", frappe.db.count("User", {"enabled": 1, "user_type": "System User"}), "| Employee attivi:", frappe.db.count("Employee", {"status": "Active"}))
for r in frappe.db.sql("SELECT role, COUNT(DISTINCT parent) n FROM `tabHas Role` WHERE parenttype='User' AND role IN ('Operatore di Reparto','Responsabile Processo MES') GROUP BY role", as_dict=True):
    p("Utenti con ruolo", r.role, "|", r.n)
p("=== MANUFACTURING SETTINGS ===")
ms = frappe.get_single("Manufacturing Settings")
p("capacity planning disattivo", ms.disable_capacity_planning, "| giorni", ms.capacity_planning_for_days, "| minuti tra operazioni", ms.mins_between_operations)
p("allow_negative_stock", frappe.db.get_single_value("Stock Settings", "allow_negative_stock"))
open(OUT, "w").write("\n".join(righe))
print("Righe scritte:", len(righe), "->", OUT)
