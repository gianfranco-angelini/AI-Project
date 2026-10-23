# Lista Job Card - colonna "Descrizione Fase" piu' larga e testo a capo (solo grafica)
# Esecuzione: bench --site site1.local console -> exec(open('/home/frappe-user/jc_lista_larghezze.py').read())
#
# Crea (o aggiorna) il Client Script "JobCard_List_Larghezze" (Job Card, vista List).
# Lo stile vale solo sulla pagina List/Job Card/List (selettore body[data-route]); la vista Report non cambia.
# Ripristino: frappe.delete_doc("Client Script", "JobCard_List_Larghezze"); frappe.db.commit()

NOME = "JobCard_List_Larghezze"

JS = """(function () {
    if (document.getElementById("rmz-jc-list-larghezze")) return;
    const R = 'body[data-route="List/Job Card/List"]';
    const s = document.createElement("style");
    s.id = "rmz-jc-list-larghezze";
    s.textContent = `
        ${R} .list-row-col.list-subject { flex: 4 1 0 !important; max-width: none !important; }
        ${R} .list-row-col.list-subject .ellipsis,
        ${R} .list-row-col.list-subject a { white-space: normal !important; overflow: visible !important; text-overflow: clip !important; }
        ${R} .list-row { height: auto !important; min-height: 40px; }
    `;
    document.head.appendChild(s);
})();
"""

print("Client Script presenti su Job Card:")
for c in frappe.get_all("Client Script", filters={"dt": "Job Card"}, fields=["name", "view", "enabled"]):
    print("  ", c.name, "|", c.view, "| attivo:", c.enabled)

if frappe.db.exists("Client Script", NOME):
    cs = frappe.get_doc("Client Script", NOME)
    cs.script = JS
    cs.enabled = 1
    cs.save()
    print("Aggiornato:", NOME)
else:
    cs = frappe.get_doc({"doctype": "Client Script", "name": NOME, "dt": "Job Card", "view": "List",
                         "enabled": 1, "script": JS})
    cs.insert()
    print("Creato:", cs.name)
frappe.db.commit()

print("Dopo:")
for c in frappe.get_all("Client Script", filters={"dt": "Job Card"}, fields=["name", "view", "enabled"]):
    print("  ", c.name, "|", c.view, "| attivo:", c.enabled)
print("FINE - ricaricare la lista Job Card con Ctrl+Shift+R")
