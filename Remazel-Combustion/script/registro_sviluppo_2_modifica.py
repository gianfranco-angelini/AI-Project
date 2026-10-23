# Registro punti di sviluppo (Simone) - punti 2 e 3 - MODIFICA
# Esecuzione: bench --site site1.local console -> exec(open('/home/frappe-user/registro_sviluppo_2_modifica.py').read())
#
# Punto 2: collega l'Employee HR-EMP-00023 all'utente simone.sacchi@remazel.com
#          SENZA creare la User Permission automatica (limiterebbe la visibilita' di Simone)
# Punto 3: lista Job Card
#          - Descrizione Fase diventa la prima colonna (title_field), tolta la colonna doppia
#          - Codice articolo (production_item) filtrabile dalla barra filtri e ricercabile nei link
#
# Ripristino (se serve):
#   frappe.db.set_value("Employee", "HR-EMP-00023", "user_id", None)
#   frappe.delete_doc("Property Setter", "Job Card-main-title_field")
#   frappe.delete_doc("Property Setter", "Job Card-main-search_fields")
#   frappe.delete_doc("Property Setter", "Job Card-production_item-in_standard_filter")
#   frappe.db.set_value("Custom Field", "Job Card-custom_descrizione_fase", "in_list_view", 1)
#   frappe.db.commit(); frappe.clear_cache(doctype="Job Card")

from frappe.custom.doctype.property_setter.property_setter import make_property_setter

EMP = "HR-EMP-00023"
USR = "simone.sacchi@remazel.com"

print("=" * 70)
print("PUNTO 2 - Employee", EMP, "-> User", USR)
print("=" * 70)
gia = frappe.db.get_value("Employee", {"user_id": USR, "name": ["!=", EMP]}, "name")
if gia:
    print("STOP: l'utente e' gia' collegato all'Employee", gia, "- nessuna modifica")
else:
    emp = frappe.get_doc("Employee", EMP)
    print("Prima: user_id =", emp.user_id, "| create_user_permission =", emp.create_user_permission)
    emp.user_id = USR
    emp.create_user_permission = 0
    emp.save()
    frappe.db.commit()
    print("Dopo:  user_id =", frappe.db.get_value("Employee", EMP, "user_id"))
    up = frappe.db.count("User Permission", {"user": USR})
    print("User Permission di Simone:", up, "(atteso 0)")

print()
print("=" * 70)
print("PUNTO 3 - Lista Job Card")
print("=" * 70)
meta = frappe.get_meta("Job Card")
print("Prima: title_field =", meta.title_field, "| search_fields =", meta.search_fields)

make_property_setter("Job Card", None, "title_field", "custom_descrizione_fase", "Data", for_doctype=True)
make_property_setter("Job Card", None, "search_fields",
                     "production_item,item_name,work_order,custom_descrizione_fase", "Data", for_doctype=True)
make_property_setter("Job Card", "production_item", "in_standard_filter", "1", "Check")
frappe.db.set_value("Custom Field", "Job Card-custom_descrizione_fase", "in_list_view", 0)
frappe.db.commit()
frappe.clear_cache(doctype="Job Card")

meta = frappe.get_meta("Job Card")
print("Dopo:  title_field =", meta.title_field, "| search_fields =", meta.search_fields)
print()
print("Colonne lista (dopo la colonna titolo = Descrizione Fase):")
for f in meta.fields:
    if f.in_list_view:
        print("  ", f.idx, f.fieldname, "|", f.label)
print()
print("Filtri standard:")
for f in meta.fields:
    if f.in_standard_filter:
        print("  ", f.fieldname, "|", f.label)
print()
print("FINE - ricaricare la lista Job Card con Ctrl+Shift+R")
