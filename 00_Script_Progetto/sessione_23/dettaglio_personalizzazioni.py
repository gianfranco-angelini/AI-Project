# Sessione 23 - SOLA LETTURA. Dettaglio delle personalizzazioni Remazel per la Guida Personalizzazioni.
# Uso (console): exec(open("/home/frappe-user/script_progetto/dettaglio_personalizzazioni.py").read(), {"frappe": frappe})
OUT = "/home/frappe-user/script_progetto/dettaglio_personalizzazioni.txt"
righe = []

def p(*a):
    righe.append(" ".join([str(x) for x in a]))

p("=== SERVER SCRIPT (prime 12 righe) ===")
for r in frappe.get_all("Server Script", fields=["name", "script_type", "reference_doctype", "doctype_event", "api_method", "disabled", "modified", "script"], order_by="name"):
    p("##", r.name, "|", r.script_type, "|", r.reference_doctype or "", "|", r.doctype_event or "", "| api:", r.api_method or "", "| disabilitato" if r.disabled else "", "| mod", str(r.modified)[:10])
    for l in (r.script or "").splitlines()[:12]:
        p("    " + l)
p("=== CLIENT SCRIPT (prime 8 righe) ===")
for r in frappe.get_all("Client Script", fields=["name", "dt", "view", "modified", "script"], order_by="name"):
    p("##", r.name, "|", r.dt, "|", r.view, "| mod", str(r.modified)[:10])
    for l in (r.script or "").splitlines()[:8]:
        p("    " + l)
p("=== PROPERTY SETTER (dopo 01/07/2026) ===")
for r in frappe.get_all("Property Setter", filters={"creation": [">", "2026-07-01"]}, fields=["doc_type", "field_name", "property", "value", "creation"], order_by="doc_type, field_name"):
    p(r.doc_type, "|", r.field_name or "(doctype)", "|", r.property, "|", (r.value or "")[:80].replace("\n", "\\n"), "|", str(r.creation)[:10])
p("=== RUOLI (creati dopo 01/07/2026) ===")
for r in frappe.get_all("Role", filters={"creation": [">", "2026-07-01"]}, fields=["name", "desk_access", "is_custom"]):
    p("Ruolo |", r.name, "| desk", r.desk_access, "| custom", r.is_custom)
p("=== ROLE PROFILE ===")
for r in frappe.get_all("Role Profile", fields=["name"]):
    p("Profilo |", r.name, "|", ", ".join(frappe.get_all("Has Role", filters={"parent": r.name, "parenttype": "Role Profile"}, pluck="role")))
p("=== CUSTOM DOCPERM per DocType ===")
for r in frappe.db.sql("SELECT parent, GROUP_CONCAT(role SEPARATOR ', ') ruoli FROM `tabCustom DocPerm` GROUP BY parent", as_dict=True):
    p(r.parent, "|", r.ruoli)
p("=== USER PERMISSION (conteggio per allow / applicable_for) ===")
for r in frappe.db.sql("SELECT allow, IFNULL(applicable_for,'') af, COUNT(*) n FROM `tabUser Permission` GROUP BY allow, af", as_dict=True):
    p(r.allow, "|", r.af, "|", r.n)
p("=== WORKSPACE SIDEBAR ===")
if frappe.db.exists("DocType", "Workspace Sidebar"):
    for r in frappe.get_all("Workspace Sidebar", fields=["name"]):
        p("Sidebar |", r.name)
p("=== REPORT Carico Reparti Settimanale (prime 15 righe query) ===")
q = frappe.db.get_value("Report", "Carico Reparti Settimanale", "query") or ""
for l in q.splitlines()[:15]:
    p("    " + l)
p("=== JOB CARD PROJ-0002 per docstatus / esterne ===")
for r in frappe.db.sql("""SELECT jc.docstatus, COUNT(*) n, SUM(jc.workstation='Lavorazione Esterna') est
    FROM `tabJob Card` jc JOIN `tabWork Order` wo ON wo.name = jc.work_order
    WHERE wo.project='PROJ-0002' GROUP BY jc.docstatus""", as_dict=True):
    p("docstatus", r.docstatus, "| JC", r.n, "| esterne", r.est)

with open(OUT, "w") as f:
    f.write("\n".join(righe) + "\n")
print("Scritto", OUT, "-", len(righe), "righe")
