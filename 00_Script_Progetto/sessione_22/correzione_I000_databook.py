# Sessione 22 — AISI 304L: F000 -> I000 (mail Simone 04/09) su P3101/P3103/P3104 con ricalcolo
# esplosi a cascata; Data Book T09 1560 -> 1080 min. Incollato in console. Eseguito.
SCRIVI = False
BOM304 = ["BOM-T09-0100-P3101-001", "BOM-T09-0100-P3103-001", "BOM-T09-0100-P3104-001"]
CATENA = BOM304 + ["BOM-T09-0100-P3100-001", "BOM-T09-0100-A3000-001", "BOM-T09-0100-A0001-001"]
db = frappe.db.sql("SELECT name, time_in_mins FROM `tabBOM Operation` WHERE parent='BOM-T09-0100-A0001-001' AND description LIKE '%%Data Book%%'", as_dict=True)
if SCRIVI:
    if not frappe.db.exists("Item", "I000"):
        it = frappe.copy_doc(frappe.get_doc("Item", "F000"))
        it.item_code = "I000"
        it.item_name = "Grezzo INOX AISI 304L (fittizio)"
        it.description = "Grezzo INOX AISI 304L — codice fittizio, materiale del fornitore (indicazione Simone 04/09/2026)"
        it.barcodes = []
        it.insert()
    for b in BOM304:
        frappe.db.sql("UPDATE `tabBOM Item` SET item_code='I000', item_name=%s, description=%s WHERE parent=%s AND item_code='F000'", ("Grezzo INOX AISI 304L (fittizio)", "Grezzo INOX AISI 304L (fittizio)", b))
    frappe.db.commit()
    for b in CATENA:
        frappe.get_doc("BOM", b).update_exploded_items(save=True)
    for r in db:
        frappe.db.set_value("BOM Operation", r.name, "time_in_mins", 1080, update_modified=False)
    frappe.db.commit()
