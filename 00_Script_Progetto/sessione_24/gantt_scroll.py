# Sessione 24 - Gantt: area con altezza della finestra, barre di scorrimento sempre visibili.
# Aggiorna i Client Script Gantt_Remazel_Task / _Work_Order / _Job_Card.
# Uso: exec(open("/home/frappe-user/script_progetto/gantt_scroll.py").read(), {"frappe": frappe, "SCRIVI": False})
SCRIVI = globals().get("SCRIVI", False)
A = '            .gantt .today-highlight { fill: #5a4a2a !important; opacity: 0.35 !important; }\n'
B = '            .gantt .today-highlight { fill: #5a4a2a !important; opacity: 0.35 !important; }\n            .gantt-container { max-height: calc(100vh - 230px) !important; overflow: auto !important; }\n'
for nome in ["Gantt_Remazel_Task", "Gantt_Remazel_Work_Order", "Gantt_Remazel_Job_Card"]:
    cs = frappe.get_doc("Client Script", nome)
    if "max-height: calc(100vh" in cs.script:
        print(nome, ": già aggiornato")
    elif A not in cs.script:
        print(nome, ": punto di inserimento NON trovato")
    elif SCRIVI:
        cs.script = cs.script.replace(A, B, 1)
        cs.save()
        print(nome, ": aggiornato")
    else:
        print(nome, ": PROVA, verrebbe aggiornato")
if SCRIVI:
    frappe.db.commit()
