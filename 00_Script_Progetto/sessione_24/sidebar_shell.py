# Sessione 24 - Le voci URL del menu e delle scorciatoie di "Produzione Remazel" puntano a /desk/produzione-remazel/...
# In v16 il primo segmento dopo /desk/ può nominare la "shell" (il menu laterale): così la pagina si apre restando
# nel menu Produzione Remazel invece di passare al menu del modulo (Projects, Manufacturing).
# Uso: exec(open("/home/frappe-user/script_progetto/sidebar_shell.py").read(), {"frappe": frappe, "SCRIVI": False})
SCRIVI = globals().get("SCRIVI", False)
WS = "Produzione Remazel"
PREF = "/desk/" + frappe.scrub(WS).replace("_", "-") + "/"

def nuovo(url):
    if not url:
        return url
    for vecchio in ("/app/", "/desk/"):
        if url.startswith(vecchio) and not url.startswith(PREF):
            return PREF + url[len(vecchio):]
    return url

modifiche = 0
sb = frappe.get_doc("Workspace Sidebar", WS)
for it in sb.items:
    if it.link_type == "URL" and nuovo(it.url) != it.url:
        print("Sidebar |", it.label, "|", it.url, "->", nuovo(it.url))
        it.url = nuovo(it.url)
        modifiche += 1
ws = frappe.get_doc("Workspace", WS)
for s in ws.shortcuts:
    if s.type == "URL" and nuovo(s.url) != s.url:
        print("Scorciatoia |", s.label, "|", s.url, "->", nuovo(s.url))
        s.url = nuovo(s.url)
        modifiche += 1
print("Modifiche:", modifiche, "| prefisso", PREF)
if SCRIVI and modifiche:
    sb.save()
    ws.save()
    frappe.db.commit()
    print("SCRITTO (commit)")
else:
    frappe.db.rollback()
    print("PROVA: nulla scritto")
