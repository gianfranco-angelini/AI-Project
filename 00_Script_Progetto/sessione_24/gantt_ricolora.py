# Sessione 24 - Gantt: ricolora le barre anche quando si cambia scala (Day/Week/Month) senza ricaricare la pagina.
# Aggiorna i Client Script Gantt_Remazel_Task / _Work_Order / _Job_Card.
# Uso: exec(open("/home/frappe-user/script_progetto/gantt_ricolora.py").read(), {"frappe": frappe, "SCRIVI": False})
SCRIVI = globals().get("SCRIVI", False)
OLD = '    function apply() {\n        const r = frappe.get_route();\n        if (!r || r[1] !== DT || String(r[2]).toLowerCase() !== "gantt") return;\n        const svg = document.querySelector(".gantt-container svg") || document.querySelector("svg.gantt");\n        if (!svg) return;\n        const wrappers = Array.from(svg.querySelectorAll(".bar-wrapper[data-id]"));\n        if (!wrappers.length) return;\n        const ids = wrappers.map((w) => w.getAttribute("data-id"));\n        const key = ids.join(",");\n        if (svg.dataset.rmz === key) return;\n        svg.dataset.rmz = key;\n        frappe.call({method: "frappe.client.get_list",\n            args: {doctype: DT, filters: [["name", "in", ids]], fields: fields(), limit_page_length: ids.length},\n            callback: (res) => { const m = {}; (res.message || []).forEach((d) => (m[d.name] = d)); paint(svg, wrappers, m); }});\n    }\n'
NEW = '    function apply() {\n        const r = frappe.get_route();\n        if (!r || r[1] !== DT || String(r[2]).toLowerCase() !== "gantt") return;\n        const svg = document.querySelector(".gantt-container svg") || document.querySelector("svg.gantt");\n        if (!svg) return;\n        const wrappers = Array.from(svg.querySelectorAll(".bar-wrapper[data-id]"));\n        if (!wrappers.length || !wrappers.some((w) => !w.dataset.rmzP)) return;\n        const cache = (window["__rmz_c_" + DT] = window["__rmz_c_" + DT] || {});\n        const ids = wrappers.map((w) => w.getAttribute("data-id"));\n        const missing = ids.filter((i) => !cache[i]);\n        const go = () => { paint(svg, wrappers, cache); wrappers.forEach((w) => (w.dataset.rmzP = "1")); };\n        if (!missing.length) return go();\n        frappe.call({method: "frappe.client.get_list",\n            args: {doctype: DT, filters: [["name", "in", missing]], fields: fields(), limit_page_length: missing.length},\n            callback: (res) => { (res.message || []).forEach((d) => (cache[d.name] = d)); go(); }});\n    }\n'
A2 = 'callback: (r) => { frappe.show_alert(r.message || "Done"); lv.refresh(); }});'
B2 = 'callback: (r) => { window["__rmz_c_Task"] = {}; frappe.show_alert(r.message || "Done"); lv.refresh(); }});'
for nome in ["Gantt_Remazel_Task", "Gantt_Remazel_Work_Order", "Gantt_Remazel_Job_Card"]:
    cs = frappe.get_doc("Client Script", nome)
    if "rmzP" in cs.script:
        print(nome, ": già aggiornato")
    elif OLD not in cs.script:
        print(nome, ": blocco apply() NON trovato")
    elif SCRIVI:
        cs.script = cs.script.replace(OLD, NEW, 1).replace(A2, B2, 1)
        cs.save()
        print(nome, ": aggiornato")
    else:
        print(nome, ": PROVA, verrebbe aggiornato")
if SCRIVI:
    frappe.db.commit()
