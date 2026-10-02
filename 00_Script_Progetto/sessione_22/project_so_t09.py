# project_so_t09.py — Project + Sales Order T09-0100 (commessa 26-19008, 100 liner) + po_no T08
# Lanciare con:  SCRIVI_T09 = False  (prova)  oppure  True  (scrittura), poi exec(...)
SCRIVI = globals().get("SCRIVI_T09", False)
DATA_ORDINE = "2026-05-11"   # data commessa 26-19008
CONSEGNE = [["2027-02-26", 10], ["2027-04-30", 20], ["2027-06-30", 20], ["2027-08-31", 20], ["2027-10-29", 20], ["2027-11-30", 10]]
ITEM = "T09-0100-A0001"
print("=== MODALITA':", "SCRITTURA" if SCRIVI else "PROVA (nessuna scrittura)", "===")

bom = frappe.db.get_value("Item", ITEM, "default_bom")
tso = frappe.get_doc("Sales Order", "SAL-ORD-2026-00001")
tpr = frappe.get_doc("Project", "PROJ-0001")
gia = frappe.db.get_value("Project", {"project_name": ["like", "T09-0100%"]}, "name")
print("BOM top:", bom, "| Project T09 già esistente:", gia)
tot = 0
for c in CONSEGNE:
    tot = tot + c[1]
print("Totale liner:", tot)

if gia:
    print("STOP: esiste già un Project T09")
else:
    pr = frappe.new_doc("Project")
    pr.project_name = "T09-0100 ASSY LINER COMPLETE"
    pr.status = "Open"
    pr.company = tpr.company
    pr.project_type = tpr.project_type
    pr.customer = tpr.customer
    pr.expected_start_date = DATA_ORDINE
    pr.expected_end_date = CONSEGNE[-1][0]
    pr.custom_buffer_giorni = 5
    pr.custom_deadline_interna = frappe.utils.add_days(CONSEGNE[-1][0], -5)
    pr.custom_fine_produzione_stimata = CONSEGNE[-1][0]
    print("\nPROJECT:", pr.project_name, "|", pr.expected_start_date, "->", pr.expected_end_date, "| deadline interna", pr.custom_deadline_interna, "| cliente", pr.customer)

    so = frappe.new_doc("Sales Order")
    so.customer = tso.customer
    so.company = tso.company
    so.transaction_date = DATA_ORDINE
    so.delivery_date = CONSEGNE[0][0]
    so.order_type = tso.order_type
    so.selling_price_list = tso.selling_price_list
    so.currency = tso.currency
    so.set_warehouse = tso.set_warehouse
    so.po_no = "99-99998"
    for c in CONSEGNE:
        so.append("items", {"item_code": ITEM, "qty": c[1], "delivery_date": c[0], "rate": tso.items[0].rate, "warehouse": tso.set_warehouse, "bom_no": bom})
    print("SALES ORDER:", so.customer, "| data", so.transaction_date, "| po_no", so.po_no, "| wh", so.set_warehouse)
    for r in so.items:
        print("   ", r.item_code, "qty", r.qty, "| consegna", r.delivery_date, "| bom", r.bom_no)

    if SCRIVI:
        pr.insert()
        so.project = pr.name
        for r in so.items:
            r.project = pr.name
        so.insert()
        so.submit()
        frappe.db.set_value("Project", pr.name, "sales_order", so.name, update_modified=False)
        frappe.db.commit()
        print("\n-> creati", pr.name, "e", so.name, "| status", frappe.db.get_value("Sales Order", so.name, "status"))

print("\npo_no T08 attuale:", frappe.db.get_value("Sales Order", "SAL-ORD-2026-00001", "po_no"))
if SCRIVI:
    frappe.db.set_value("Sales Order", "SAL-ORD-2026-00001", "po_no", "99-99999", update_modified=False)
    frappe.db.commit()
    print("-> po_no T08:", frappe.db.get_value("Sales Order", "SAL-ORD-2026-00001", "po_no"))
print("=== FINE ===")
