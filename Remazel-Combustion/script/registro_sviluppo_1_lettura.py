# Registro punti di sviluppo (Simone) - punti 1, 2, 3 - SOLA LETTURA
# Esecuzione: bench --site site1.local console -> exec(open('/home/frappe-user/registro_sviluppo_1_lettura.py').read())
# Nessuna scrittura sul database.

print("=" * 70)
print("PUNTO 2 - Utente / Employee di Simone Sacchi")
print("=" * 70)
utenti = frappe.get_all("User", filters={"full_name": ["like", "%Sacchi%"]},
                        fields=["name", "full_name", "enabled", "user_type", "last_login"])
if not utenti:
    print("Nessun User con 'Sacchi' nel nome")
for u in utenti:
    print("USER", u.name, "|", u.full_name, "| enabled:", u.enabled, "| tipo:", u.user_type, "| ultimo login:", u.last_login)
    ruoli = frappe.get_all("Has Role", filters={"parent": u.name, "parenttype": "User"}, fields=["role"])
    elenco = []
    for r in ruoli:
        elenco.append(r.role)
    print("   ruoli:", ", ".join(sorted(elenco)))
    perms = frappe.get_all("User Permission", filters={"user": u.name},
                           fields=["allow", "for_value", "applicable_for", "apply_to_all_doctypes"])
    print("   User Permission:", len(perms))
    for p in perms:
        print("     ", p.allow, "=", p.for_value, "| per:", p.applicable_for, "| tutti:", p.apply_to_all_doctypes)

dipendenti = frappe.get_all("Employee", filters={"employee_name": ["like", "%Sacchi%"]},
                            fields=["name", "employee_name", "status", "user_id", "department", "designation"])
if not dipendenti:
    print("Nessun Employee con 'Sacchi' nel nome")
for e in dipendenti:
    print("EMPLOYEE", e.name, "|", e.employee_name, "|", e.status, "| user_id:", e.user_id,
          "| reparto:", e.department, "| mansione:", e.designation)

print()
print("Ruolo 'Operatore di Reparto' - permessi su Job Card (Custom DocPerm)")
cdp = frappe.get_all("Custom DocPerm", filters={"parent": "Job Card", "role": "Operatore di Reparto"},
                     fields=["permlevel", "read", "write", "create", "submit", "delete", "report", "if_owner"])
for c in cdp:
    print("  ", c)

print()
print("=" * 70)
print("PUNTO 1 - Workstation e cambio Workstation su Job Card")
print("=" * 70)
ws = frappe.get_all("Workstation", fields=["name", "production_capacity"], order_by="name")
for w in ws:
    n_open = frappe.db.count("Job Card", {"workstation": w.name, "docstatus": 0})
    print("  ", w.name, "| capacita:", w.production_capacity, "| Job Card aperte (docstatus 0):", n_open)

meta = frappe.get_meta("Job Card")
for nome in ["workstation", "operation", "for_quantity", "is_subcontracted", "status"]:
    f = meta.get_field(nome)
    if f:
        print("  campo", nome, "| tipo:", f.fieldtype, "| read_only:", f.read_only,
              "| read_only_depends_on:", f.read_only_depends_on, "| allow_on_submit:", f.allow_on_submit,
              "| permlevel:", f.permlevel)
    else:
        print("  campo", nome, "NON presente")

print()
print("=" * 70)
print("PUNTO 3 - Lista Job Card: colonne e ricerca")
print("=" * 70)
print("title_field:", meta.title_field, "| show_title_field_in_link:", meta.show_title_field_in_link)
print("search_fields:", meta.search_fields)
print("sort_field:", meta.sort_field, meta.sort_order)
print()
print("Campi in_list_view (ordine idx):")
for f in meta.fields:
    if f.in_list_view:
        print("  ", f.idx, f.fieldname, "|", f.label, "|", f.fieldtype)
print()
print("Campi in_standard_filter:")
for f in meta.fields:
    if f.in_standard_filter:
        print("  ", f.fieldname, "|", f.label)
print()
print("Campi codice/descrizione (candidati per ricerca):")
for nome in ["production_item", "item_name", "work_order", "project", "custom_descrizione_fase", "operation", "bom_no"]:
    f = meta.get_field(nome)
    if f:
        print("  ", nome, "| idx:", f.idx, "| list:", f.in_list_view, "| std_filter:", f.in_standard_filter,
              "| global_search:", f.in_global_search, "| bold:", f.bold)
    else:
        print("  ", nome, "NON presente")
print()
print("Property Setter su Job Card:")
ps = frappe.get_all("Property Setter", filters={"doc_type": "Job Card"},
                    fields=["field_name", "property", "value"], order_by="field_name")
for p in ps:
    print("  ", p.field_name, "|", p.property, "=", str(p.value)[:120])
print()
print("Custom Field su Job Card:")
cf = frappe.get_all("Custom Field", filters={"dt": "Job Card"},
                    fields=["fieldname", "label", "fieldtype", "insert_after", "in_list_view", "in_standard_filter"])
for c in cf:
    print("  ", c.fieldname, "|", c.label, "|", c.fieldtype, "| dopo:", c.insert_after,
          "| list:", c.in_list_view, "| std_filter:", c.in_standard_filter)
print()
if frappe.db.exists("List View Settings", "Job Card"):
    lvs = frappe.get_doc("List View Settings", "Job Card")
    print("List View Settings Job Card | fields:", lvs.fields)
    print("   disable_count:", lvs.disable_count, "| disable_auto_refresh:", lvs.disable_auto_refresh)
else:
    print("List View Settings Job Card: NON presente")
print()
print("Client Script su Job Card:")
cs = frappe.get_all("Client Script", filters={"dt": "Job Card"}, fields=["name", "view", "enabled"])
for c in cs:
    print("  ", c.name, "| vista:", c.view, "| attivo:", c.enabled)
print()
print("FINE - nessuna modifica effettuata")
