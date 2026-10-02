# Sessione 22 — Custom Field su Job Card (custom_consegna_set, custom_production_plan), Server Script
# WorkOrder_Consegna_Set (Before Insert su Work Order) e riallineamento T08. Incollato in console.
# Eseguito: 57 WO T08 con consegna, 557 Job Card aggiornate.
SCRIVI = False
cf = [
    {"dt": "Job Card", "fieldname": "custom_consegna_set", "label": "Consegna set", "fieldtype": "Date", "fetch_from": "work_order.expected_delivery_date", "insert_after": "custom_descrizione_fase", "read_only": 1, "in_list_view": 1, "in_standard_filter": 1},
    {"dt": "Job Card", "fieldname": "custom_production_plan", "label": "Production Plan", "fieldtype": "Link", "options": "Production Plan", "fetch_from": "work_order.production_plan", "insert_after": "custom_consegna_set", "read_only": 1, "in_standard_filter": 1},
]
for c in cf:
    print("Custom Field", c["fieldname"], "esiste:", bool(frappe.db.exists("Custom Field", {"dt": c["dt"], "fieldname": c["fieldname"]})))
print("Server Script esiste:", bool(frappe.db.exists("Server Script", "WorkOrder_Consegna_Set")))
print("WO senza consegna ma con riga SO:", frappe.db.sql("SELECT COUNT(*) FROM `tabWork Order` WHERE expected_delivery_date IS NULL AND IFNULL(sales_order_item,'')!=''")[0][0])
print("Job Card totali:", frappe.db.count("Job Card"))
if SCRIVI:
    for c in cf:
        if not frappe.db.exists("Custom Field", {"dt": c["dt"], "fieldname": c["fieldname"]}):
            d = frappe.new_doc("Custom Field")
            d.update(c)
            d.insert()
    if not frappe.db.exists("Server Script", "WorkOrder_Consegna_Set"):
        s = frappe.new_doc("Server Script")
        s.name = "WorkOrder_Consegna_Set"
        s.script_type = "DocType Event"
        s.reference_doctype = "Work Order"
        s.doctype_event = "Before Insert"
        s.script = 'if doc.sales_order_item and not doc.expected_delivery_date:\n    doc.expected_delivery_date = frappe.db.get_value("Sales Order Item", doc.sales_order_item, "delivery_date")\n'
        s.insert()
    frappe.db.commit()
    frappe.db.sql("UPDATE `tabWork Order` wo JOIN `tabSales Order Item` soi ON soi.name = wo.sales_order_item SET wo.expected_delivery_date = soi.delivery_date WHERE wo.expected_delivery_date IS NULL")
    frappe.db.sql("UPDATE `tabJob Card` jc JOIN `tabWork Order` wo ON wo.name = jc.work_order SET jc.custom_consegna_set = wo.expected_delivery_date, jc.custom_production_plan = wo.production_plan")
    frappe.db.commit()
    print("-> WO senza consegna rimasti:", frappe.db.sql("SELECT COUNT(*) FROM `tabWork Order` WHERE expected_delivery_date IS NULL AND IFNULL(sales_order_item,'')!=''")[0][0])
    print("-> Job Card con consegna:", frappe.db.sql("SELECT custom_consegna_set, custom_production_plan, COUNT(*) FROM `tabJob Card` GROUP BY custom_consegna_set, custom_production_plan"))
