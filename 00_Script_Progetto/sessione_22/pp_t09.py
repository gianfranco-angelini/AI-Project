# pp_t09.py — un Production Plan per set di consegna della commessa T09-0100 (SAL-ORD-2026-00002)
# exec(open(f).read(), {"frappe": frappe, "SCRIVI_PP": False/True})
SCRIVI = globals().get("SCRIVI_PP", False)
SO = "SAL-ORD-2026-00002"
PRJ = "PROJ-0002"
print("=== MODALITA':", "SCRITTURA" if SCRIVI else "PROVA (nessuna scrittura)", "===")
t08 = frappe.get_doc("Production Plan", "MFG-PP-2026-00001")
so = frappe.get_doc("Sales Order", SO)
gia = frappe.db.sql("SELECT DISTINCT pi.sales_order_item FROM `tabProduction Plan Item` pi JOIN `tabProduction Plan` pp ON pp.name = pi.parent WHERE pp.docstatus < 2 AND pi.sales_order = %s", SO, pluck=True)
print("Righe SO già pianificate:", gia)
n = 0
for riga in so.items:
    n = n + 1
    if riga.name in gia:
        print("\n## Set", n, "già pianificato, salto")
        continue
    pp = frappe.new_doc("Production Plan")
    pp.company = t08.company
    pp.posting_date = frappe.utils.nowdate()
    pp.get_items_from = "Sales Order"
    pp.project = PRJ
    for f in ["for_warehouse", "include_subcontracted_items", "include_non_stock_items", "skip_available_sub_assembly_item", "combine_items", "combine_sub_items", "sub_assembly_warehouse", "include_safety_stock", "ignore_existing_ordered_qty"]:
        pp.set(f, t08.get(f))
    pp.append("sales_orders", {"sales_order": SO, "sales_order_date": so.transaction_date, "customer": so.customer, "grand_total": so.grand_total})
    pp.get_items()
    tenere = []
    for r in pp.po_items:
        if r.sales_order_item == riga.name:
            tenere.append(r)
    pp.po_items = []
    for r in tenere:
        r.planned_start_date = frappe.utils.now_datetime()
        pp.append("po_items", r.as_dict(no_default_fields=True))
    pp.get_sub_assembly_items()
    livelli = {}
    for s in pp.sub_assembly_items:
        livelli[s.bom_level] = livelli.get(s.bom_level, 0) + 1
    print("\n## Set", n, "| consegna", riga.delivery_date, "| qty", riga.qty)
    for r in pp.po_items:
        print("   po_item", r.item_code, r.planned_qty, r.bom_no, "| riga SO", r.sales_order_item)
    print("   sub-assembly:", len(pp.sub_assembly_items), "| per livello:", livelli)
    if SCRIVI:
        pp.insert()
        pp.submit()
        frappe.db.commit()
        print("   -> creato", pp.name, "| status", frappe.db.get_value("Production Plan", pp.name, "status"))
print("\n=== FINE ===")
