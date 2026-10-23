# Lista Job Card - testo di "Descrizione Fase" a capo invece che troncato (solo grafica)  (v2)
# Esecuzione: bench --site site1.local console -> exec(open('/home/frappe-user/jc_lista_larghezze.py').read())
#
# Crea (o aggiorna) il Client Script "JobCard_List_Larghezze" (Job Card, vista List).
# v2: nella lista v16 le colonne hanno larghezza inline calcolata da ERPNext (style="width:...; flex:...")
#     e l'attributo data-fieldname. Le larghezze non si toccano (header e righe restano allineati):
#     si toglie il troncamento e il testo della descrizione va a capo.
# Lo stile vale solo sulla pagina List/Job Card/List (body[data-route], verificato da console browser).
# Ripristino: frappe.delete_doc("Client Script", "JobCard_List_Larghezze"); frappe.db.commit()

NOME = "JobCard_List_Larghezze"

JS = """(function () {
    const vecchio = document.getElementById("rmz-jc-list-larghezze");
    if (vecchio) vecchio.remove();
    const R = 'body[data-route="List/Job Card/List"]';
    const C = R + ' .list-row-col[data-fieldname="custom_descrizione_fase"]';
    const s = document.createElement("style");
    s.id = "rmz-jc-list-larghezze";
    s.textContent = `
        ${R} .list-row .level-left { overflow: visible !important; }
        ${C}, ${C} .ellipsis, ${C} a {
            white-space: normal !important; overflow: visible !important; text-overflow: clip !important;
        }
        ${C} a { display: inline !important; line-height: 1.35; }
        ${R} .list-row { height: auto !important; min-height: 40px; padding-top: 6px; padding-bottom: 6px; }
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
    cs.view = "List"
    cs.enabled = 1
    cs.save()
    print("Aggiornato:", NOME)
else:
    cs = frappe.get_doc({"doctype": "Client Script", "name": NOME, "dt": "Job Card", "view": "List",
                         "enabled": 1, "script": JS})
    cs.insert()
    print("Creato:", cs.name)
frappe.db.commit()
frappe.clear_cache(doctype="Job Card")

print("Dopo:")
for c in frappe.get_all("Client Script", filters={"dt": "Job Card"}, fields=["name", "view", "enabled"]):
    print("  ", c.name, "|", c.view, "| attivo:", c.enabled)
print("FINE - ricaricare la lista Job Card con Ctrl+Shift+R")
