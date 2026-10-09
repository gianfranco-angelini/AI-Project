# Sessione 24 - Ripristino URL menu e scorciatoie "Produzione Remazel": /desk/produzione-remazel/... -> /app/...
# Il prefisso con la shell non è una route valida in v16 (apre una nuova scheda e va alla home).
# Uso: exec(open("/home/frappe-user/script_progetto/sidebar_ripristino.py").read(), {"frappe": frappe, "SCRIVI": False})
SCRIVI = globals().get("SCRIVI", False)
WS = "Produzione Remazel"
PREF = "/desk/" + frappe.scrub(WS).replace("_", "-") + "/"

def vecchio(url):
    if url and url.startswith(PREF):
        return "/app/" + url[len(PREF):]
    return url

modifiche = 0
sb = frappe.get_doc("Workspace Sidebar", WS)
for it in sb.items:
    if it.link_type == "URL" and vecchio(it.url) != it.url:
        print("Sidebar |", it.label, "|", it.url, "->", vecchio(it.url))
        it.url = vecchio(it.url)
        modifiche += 1
ws = frappe.get_doc("Workspace", WS)
for s in ws.shortcuts:
    if s.type == "URL" and vecchio(s.url) != s.url:
        print("Scorciatoia |", s.label, "|", s.url, "->", vecchio(s.url))
        s.url = vecchio(s.url)
        modifiche += 1
print("Modifiche:", modifiche)
if SCRIVI and modifiche:
    sb.save()
    ws.save()
    frappe.db.commit()
    print("SCRITTO (commit)")
else:
    frappe.db.rollback()
    print("PROVA: nulla scritto")
