# Sessione 24 - Voci URL del Workspace Sidebar "Produzione Remazel" trasformate in voci DocType con filtri.
# In v16 le voci URL si aprono sempre in una nuova scheda (target="_blank" nel template) e la nuova scheda
# mostra il menu del modulo (Projects, Manufacturing). Le voci DocType si aprono nella stessa scheda e il
# menu Produzione Remazel resta. Si aprono in vista Lista con i filtri: il Gantt si sceglie dal selettore viste.
# Le scorciatoie della Workspace non vengono toccate.
# Uso: exec(open("/home/frappe-user/script_progetto/sidebar_doctype.py").read(), {"frappe": frappe, "SCRIVI": False})
import json
from urllib.parse import urlsplit, parse_qsl

SCRIVI = globals().get("SCRIVI", False)
WS = "Produzione Remazel"

def converti(url):
    # /app/task/view/gantt?project=PROJ-0002 -> ("Task", [["Task", "project", "=", "PROJ-0002"]])
    parti = urlsplit(url or "")
    seg = [s for s in parti.path.split("/") if s]
    if len(seg) < 2 or seg[0] not in ("app", "desk"):
        return None
    slug = seg[1]
    if slug in ("query-report", "report", "dashboard-view"):
        return None
    doctype = frappe.db.get_value("DocType", {"name": slug.replace("-", " ").title()}, "name") \
        or frappe.db.get_value("DocType", {"name": ["like", slug.replace("-", " ")]}, "name")
    if not doctype:
        return None
    filtri = []
    for campo, valore in parse_qsl(parti.query):
        if not frappe.get_meta(doctype).has_field(campo) and campo not in ("name",):
            print("   campo non trovato su", doctype, ":", campo)
            return None
        if valore.startswith("["):
            op, val = json.loads(valore)
            filtri.append([doctype, campo, op, val])
        else:
            filtri.append([doctype, campo, "=", valore])
    return doctype, filtri

modifiche = 0
saltate = 0
sb = frappe.get_doc("Workspace Sidebar", WS)
for it in sb.items:
    if it.type != "Link" or it.link_type != "URL":
        continue
    esito = converti(it.url)
    if not esito:
        print("SALTATA |", it.label, "|", it.url)
        saltate += 1
        continue
    doctype, filtri = esito
    print("Sidebar |", it.label, "|", it.url, "-> DocType", doctype, "filtri", json.dumps(filtri))
    it.link_type = "DocType"
    it.link_to = doctype
    it.filters = json.dumps(filtri)
    it.url = None
    modifiche += 1

print("Modifiche:", modifiche, "| Saltate:", saltate)
if SCRIVI and modifiche:
    sb.save()
    frappe.db.commit()
    print("SCRITTO (commit)")
else:
    frappe.db.rollback()
    print("PROVA: nulla scritto")
