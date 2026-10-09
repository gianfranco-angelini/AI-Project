# Sessione 24 - SOLA LETTURA. Struttura del Workspace Sidebar "Produzione Remazel" e campi disponibili per le voci.
# Uso: exec(open("/home/frappe-user/script_progetto/sidebar_analisi.py").read(), {"frappe": frappe})
sb = frappe.get_doc("Workspace Sidebar", "Produzione Remazel")
print("Campi testata:", [(f.fieldname, f.fieldtype, f.options) for f in sb.meta.fields if f.fieldtype not in ("Section Break", "Column Break", "Tab Break")])
for tf in sb.meta.get_table_fields():
    cm = frappe.get_meta(tf.options)
    print("Tabella", tf.fieldname, "->", tf.options)
    print("  campi voce:", [(f.fieldname, f.fieldtype, (f.options or "")[:60]) for f in cm.fields if f.fieldtype not in ("Section Break", "Column Break")])
    for it in sb.get(tf.fieldname):
        d = it.as_dict()
        print("  ", {k: v for k, v in d.items() if k not in ("name", "owner", "creation", "modified", "modified_by", "parent", "parentfield", "parenttype", "doctype", "docstatus") and v not in (None, "", 0)})
