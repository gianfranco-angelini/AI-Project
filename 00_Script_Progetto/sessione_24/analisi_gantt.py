# Sessione 24 - SOLA LETTURA. Analisi completa della struttura Gantt / monitoraggio prima di un'unica modifica.
# Uso (console): exec(open("/home/frappe-user/script_progetto/analisi_gantt.py").read(), {"frappe": frappe})
OUT = "/home/frappe-user/script_progetto/analisi_gantt.txt"
righe = []
def p(*a):
    righe.append(" ".join([str(x) for x in a]))

# 1. Project
p("=== 1. PROJECT ===")
meta_pr = frappe.get_meta("Project")
for r in frappe.get_all("Project", fields=["name", "project_name", "status", "expected_start_date", "expected_end_date",
        "percent_complete_method", "percent_complete"], order_by="name"):
    p(r.name, "|", r.project_name, "|", r.status, "|", r.expected_start_date, "->", r.expected_end_date,
      "| metodo %", r.percent_complete_method, "|", r.percent_complete)
p("Project ha campo color:", bool(meta_pr.get_field("color")))

# 2. Task
p("=== 2. TASK ===")
meta_t = frappe.get_meta("Task")
p("Task campi utili:", [f for f in ["color", "progress", "exp_start_date", "exp_end_date", "act_start_date", "act_end_date",
    "is_group", "parent_task", "depends_on", "is_milestone", "task_weight"] if meta_t.get_field(f)])
for r in frappe.db.sql("""SELECT project, COUNT(*) n, SUM(is_group) gruppi, SUM(IFNULL(color,'')<>'') con_colore,
        SUM(IFNULL(progress,0)>0) con_progress, MIN(exp_start_date) da, MAX(exp_end_date) a
        FROM `tabTask` GROUP BY project""", as_dict=True):
    p("Project", r.project, "| task", r.n, "| gruppi", r.gruppi, "| con colore", r.con_colore, "| con progress", r.con_progress, "|", r.da, "->", r.a)
p("Dipendenze (Task Depends On) per project:")
for r in frappe.db.sql("""SELECT t.project, COUNT(*) n FROM `tabTask Depends On` d JOIN `tabTask` t ON t.name=d.parent GROUP BY t.project""", as_dict=True):
    p("   ", r.project, r.n)
p("Esempio Task T09 (primi 10):")
for r in frappe.get_all("Task", filters={"project": "PROJ-0002"}, fields=["name", "subject", "is_group", "parent_task", "color", "progress",
        "exp_start_date", "exp_end_date"], order_by="name", limit=10):
    deps = frappe.get_all("Task Depends On", filters={"parent": r.name}, pluck="task")
    p("   ", r.name, "|", r.subject, "| gruppo", r.is_group, "| padre", r.parent_task, "| colore", r.color, "| %", r.progress,
      "|", r.exp_start_date, "->", r.exp_end_date, "| dipende da", deps)

# 3. Work Order e collegamento ai Task
p("=== 3. WORK ORDER ===")
for r in frappe.db.sql("""SELECT project, COUNT(*) n, SUM(IFNULL(custom_task,'')<>'') con_task, MIN(planned_start_date) da,
        MAX(planned_end_date) a FROM `tabWork Order` WHERE docstatus=1 GROUP BY project""", as_dict=True):
    p("Project", r.project, "| WO", r.n, "| con Task", r.con_task, "|", r.da, "->", r.a)
p("Work Order ha campo color:", bool(frappe.get_meta("Work Order").get_field("color")))

# 4. Client Script legati ai Gantt (codice completo)
p("=== 4. CLIENT SCRIPT ===")
for r in frappe.get_all("Client Script", filters={"dt": ["in", ["Task", "Project", "Work Order"]]}, fields=["name", "dt", "view", "enabled", "script"]):
    p("##", r.name, "|", r.dt, "|", r.view, "| attivo", r.enabled)
    for l in (r.script or "").splitlines():
        p("    " + l)

# 5. Scorciatoie e link Gantt nello spazio di lavoro e nel menu laterale
p("=== 5. WORKSPACE / SIDEBAR ===")
if frappe.db.exists("Workspace", "Produzione Remazel"):
    ws = frappe.get_doc("Workspace", "Produzione Remazel")
    for s in ws.shortcuts:
        p("Scorciatoia |", s.label, "|", s.type, "|", s.link_to or "", "|", s.url or "", "|", s.get("doc_view") or "")
if frappe.db.exists("DocType", "Workspace Sidebar") and frappe.db.exists("Workspace Sidebar", "Produzione Remazel"):
    sb = frappe.get_doc("Workspace Sidebar", "Produzione Remazel")
    for tf in sb.meta.get_table_fields():
        for it in sb.get(tf.fieldname) or []:
            d = it.as_dict()
            p("Sidebar |", d.get("label"), "|", d.get("link_type"), "|", d.get("link_to"), "|", d.get("url") or "")

# 6. Gantt: viste salvate e impostazioni utente
p("=== 6. VISTE / IMPOSTAZIONI LISTA ===")
for dt in ["Task", "Project", "Work Order"]:
    for r in frappe.get_all("List View Settings", filters={"name": dt}, fields=["name", "disable_count", "disable_auto_refresh"]):
        p("List View Settings", r.name, r.disable_count, r.disable_auto_refresh)
    p(dt, "| filtri salvati:", frappe.get_all("List Filter", filters={"reference_doctype": dt}, pluck="filter_name"))

with open(OUT, "w") as f:
    f.write("\n".join(righe) + "\n")
print("Scritto", OUT, "-", len(righe), "righe")
