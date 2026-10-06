src = frappe.get_doc("Workspace", "Manufacturing-simone.sacchi")
print("Origine:", src.name, "| titolo", src.title, "| scorciatoie", len(src.shortcuts), "| link", len(src.links), "| number card", len(src.number_cards), "| chart", len(src.charts))
if frappe.db.exists("Workspace", "Produzione Remazel"):
    print("Esiste gia: nessuna modifica")
else:
    d = frappe.copy_doc(src)
    d.label = "Produzione Remazel"
    d.title = "Produzione Remazel"
    d.public = 1
    d.for_user = ""
    d.is_hidden = 0
    d.module = "Manufacturing"
    d.insert(ignore_permissions=True)
    frappe.db.commit()
    nuovo = frappe.get_doc("Workspace", "Produzione Remazel")
    print("Creato:", nuovo.name, "| pubblico", nuovo.public, "| scorciatoie", len(nuovo.shortcuts), "| number card", len(nuovo.number_cards), "| chart", len(nuovo.charts))
