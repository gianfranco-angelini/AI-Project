# Sessione 22 — fixed_time=1 sulle fasi per lotto (Lavorazione Esterna, MX, Data Book) di tutte le
# BOM default attive + Workstation "Lavorazione Esterna" capacità 1 -> 50. Incollato in console.
# Eseguito: 214 fasi (165 esterne, 47 MX, 2 Data Book), capacità 50.
SCRIVI = False
bom_default = frappe.db.sql("SELECT name FROM `tabBOM` WHERE is_default=1 AND is_active=1 AND docstatus=1", pluck=True)
print("BOM default attive:", len(bom_default))
da_fare = []
per_tipo = {"Lavorazione Esterna": 0, "MX": 0, "Data Book": 0}
for b in bom_default:
    for r in frappe.db.sql("SELECT name, workstation_type, time_in_mins, fixed_time, description FROM `tabBOM Operation` WHERE parent=%s", b, as_dict=True):
        if r.fixed_time:
            continue
        d = frappe.utils.strip_html(r.description or "")
        cod = d.split(" ")[0]
        motivo = None
        if r.workstation_type == "Lavorazione Esterna":
            motivo = "Lavorazione Esterna"
        elif cod[-2:] == "MX":
            motivo = "MX"
        elif "databook" in d.lower().replace(" ", ""):
            motivo = "Data Book"
            print("   Data Book:", b, r.time_in_mins, d[:70])
        if motivo:
            da_fare.append(r.name)
            per_tipo[motivo] = per_tipo[motivo] + 1
print("Fasi da portare a fixed_time=1:", len(da_fare), per_tipo)
print("Capacità Lavorazione Esterna attuale:", frappe.db.get_value("Workstation", "Lavorazione Esterna", "production_capacity"), "-> 50")
if SCRIVI:
    for n in da_fare:
        frappe.db.set_value("BOM Operation", n, "fixed_time", 1, update_modified=False)
    frappe.db.set_value("Workstation", "Lavorazione Esterna", "production_capacity", 50)
    frappe.db.commit()
    print("-> scritto. Verifica fixed_time=1:", frappe.db.count("BOM Operation", {"name": ["in", da_fare], "fixed_time": 1}), "| capacità:", frappe.db.get_value("Workstation", "Lavorazione Esterna", "production_capacity"))
