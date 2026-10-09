# Sessione 24 - Aggiorna SOLO il Client Script Gantt_Remazel_Task: etichetta con inizio reale e percentuale.
# Uso: exec(open("/home/frappe-user/script_progetto/gantt_etichette.py").read(), {"frappe": frappe, "SCRIVI": False})
SCRIVI = globals().get("SCRIVI", False)
A1 = '        if (DT === "Task") return ["name", "project", "color", "parent_task"];'
B1 = '        if (DT === "Task") return ["name", "project", "color", "parent_task", "act_start_date", "progress"];'
A2 = '            if (DT === "Task" && d.color) c = d.color;'
B2 = '            if (DT === "Task" && d.color) c = d.color;\n            if (DT === "Task") {\n                const lab = w.querySelector(".bar-label");\n                if (lab) {\n                    if (!lab.dataset.rmzOrig) lab.dataset.rmzOrig = lab.textContent;\n                    const da = d.act_start_date ? " · from " + d.act_start_date.split("-").reverse().slice(0, 2).join("/") : "";\n                    lab.textContent = lab.dataset.rmzOrig + da + " · " + (Math.round((d.progress || 0) * 10) / 10) + "%";\n                }\n            }'
cs = frappe.get_doc("Client Script", "Gantt_Remazel_Task")
js = cs.script
if B1 in js:
    print("Già aggiornato: nessuna modifica")
else:
    ok = A1 in js and A2 in js
    print("Punti di inserimento trovati:", ok)
    if ok and SCRIVI:
        cs.script = js.replace(A1, B1, 1).replace(A2, B2, 1)
        cs.save()
        frappe.db.commit()
        print("Gantt_Remazel_Task aggiornato (commit)")
    elif ok:
        print("PROVA: lo script verrebbe aggiornato; rilanciare con SCRIVI True")
