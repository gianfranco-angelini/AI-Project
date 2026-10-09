# Sessione 24 - MODIFICA UNICA Gantt / monitoraggio (nuove etichette in INGLESE).
# 1) avanzamento Task da Job Card (Server Script: After Submit Job Card, Daily, API) + calcolo iniziale
# 2) colore Task per Project (+ Server Script Before Insert)
# 3) un solo script grafico per Task / Work Order / Job Card (colori, completato visibile, frecce, Gantt fornitori)
# 4) workspace e sidebar: Master Plan, Project, Production Entries, Supplier Gantt
# SCRIVI=False: esegue tutto e fa ROLLBACK (prova completa). SCRIVI=True: COMMIT.
# Uso: exec(open("/home/frappe-user/script_progetto/modifica_gantt.py").read(), {"frappe": frappe, "SCRIVI": False})
import json
SCRIVI = globals().get("SCRIVI", False)
WS = "Produzione Remazel"
OUT = "/home/frappe-user/script_progetto/modifica_gantt_%s.txt" % ("scrivi" if SCRIVI else "prova")
COLORI = {"PROJ-0002": "#3a6bbf", "PROJ-0001": "#2e8b57"}
righe = []
def p(*a):
    righe.append(" ".join([str(x) for x in a]))

# ------------------------------------------------------------------ codice comune avanzamento (Server Script)
CODICE_AVANZAMENTO = '''
def rmz_peso(t):
    r = frappe.db.sql("""SELECT IFNULL(SUM(IFNULL(jc.time_required,0)),0),
        IFNULL(SUM(IFNULL(jc.time_required,0) * IFNULL(CASE WHEN jc.docstatus=1 THEN 1
            ELSE LEAST(IFNULL(jc.total_completed_qty,0)/NULLIF(jc.for_quantity,0),1) END,0)),0),
        COUNT(jc.name), IFNULL(SUM(jc.docstatus=1),0)
        FROM `tabJob Card` jc JOIN `tabWork Order` wo ON wo.name=jc.work_order
        WHERE wo.custom_task=%s AND wo.docstatus=1 AND jc.docstatus<2""", (t,))[0]
    tl = frappe.db.sql("""SELECT MIN(tl.from_time), MAX(tl.to_time) FROM `tabJob Card Time Log` tl
        JOIN `tabJob Card` jc ON jc.name=tl.parent JOIN `tabWork Order` wo ON wo.name=jc.work_order
        WHERE wo.custom_task=%s AND jc.docstatus<2""", (t,))[0]
    return [float(r[0] or 0), float(r[1] or 0), int(r[2] or 0), int(r[3] or 0), tl[0], tl[1]]

def rmz_ricalcola(t):
    tot, fatto, n, nch, ini, fin = rmz_peso(t)
    for c in frappe.get_all("Task", filters={"parent_task": t}, pluck="name"):
        a = rmz_ricalcola(c)
        tot = tot + a[0]
        fatto = fatto + a[1]
        n = n + a[2]
        nch = nch + a[3]
        if a[4] and (not ini or a[4] < ini):
            ini = a[4]
        if a[5] and (not fin or a[5] > fin):
            fin = a[5]
    perc = round(100.0 * fatto / tot, 1) if tot else 0
    vals = {"progress": perc,
        "act_start_date": frappe.utils.getdate(ini) if ini else None,
        "act_end_date": frappe.utils.getdate(fin) if (fin and n and nch == n) else None}
    # la barra del Gantt parte dall'inizio reale se il lavoro è iniziato prima del pianificato
    exp = frappe.db.get_value("Task", t, "exp_start_date")
    if ini and (not exp or frappe.utils.get_datetime(ini) < frappe.utils.get_datetime(exp)):
        vals["exp_start_date"] = ini
    frappe.db.set_value("Task", t, vals, update_modified=False)
    return [tot, fatto, n, nch, ini, fin]

def rmz_radice(t):
    padre = frappe.db.get_value("Task", t, "parent_task")
    while padre:
        t = padre
        padre = frappe.db.get_value("Task", t, "parent_task")
    return t
'''
SERVER_SCRIPTS = {
    "Task_Progress_JobCard_Submit": {"script_type": "DocType Event", "reference_doctype": "Job Card", "doctype_event": "After Submit",
        "script": CODICE_AVANZAMENTO + '''
t = frappe.db.get_value("Work Order", doc.work_order, "custom_task")
if t:
    rmz_ricalcola(rmz_radice(t))
'''},
    "Task_Progress_Daily": {"script_type": "Scheduler Event", "event_frequency": "Daily",
        "script": CODICE_AVANZAMENTO + '''
aperti = frappe.get_all("Project", filters={"status": "Open"}, pluck="name")
for r in frappe.get_all("Task", filters={"project": ["in", aperti], "parent_task": ["is", "not set"]}, pluck="name"):
    rmz_ricalcola(r)
'''},
    "Task_Progress_API": {"script_type": "API", "api_method": "recalculate_task_progress",
        "script": CODICE_AVANZAMENTO + '''
pr = frappe.form_dict.get("project")
flt = {"parent_task": ["is", "not set"]}
if pr:
    flt["project"] = pr
else:
    flt["project"] = ["in", frappe.get_all("Project", filters={"status": "Open"}, pluck="name")]
radici = frappe.get_all("Task", filters=flt, pluck="name")
for r in radici:
    rmz_ricalcola(r)
frappe.response["message"] = "Progress recalculated: %s groups" % len(radici)
'''},
    "Task_Color_By_Project": {"script_type": "DocType Event", "reference_doctype": "Task", "doctype_event": "Before Insert",
        "script": '''
COLORS = %s
PALETTE = ["#8e44ad", "#c0392b", "#d68910", "#16a085", "#2c3e50"]
if doc.project and not doc.color:
    if doc.project in COLORS:
        doc.color = COLORS[doc.project]
    else:
        n = frappe.db.count("Project", {"name": ["<", doc.project]})
        doc.color = PALETTE[n %% len(PALETTE)]
''' % json.dumps(COLORI)},
}

# ------------------------------------------------------------------ client script unico (JS)
JS = r'''
(function() {
    const DT = "__DT__";
    if (!document.getElementById("gantt-remazel-style")) {
        const s = document.createElement("style");
        s.id = "gantt-remazel-style";
        s.textContent = `
            .gantt .grid-header, .gantt-container .grid-header { fill: #1a1a1a !important; }
            .gantt .upper-text, .gantt .lower-text { fill: #ffffff !important; font-weight: 600 !important; font-size: 11px !important; }
            .gantt text, .gantt-container text { fill: #ffffff !important; }
            .gantt .bar { fill: #3a6bbf; stroke: #1a1a1a !important; stroke-width: 1 !important; }
            .gantt .bar-progress { fill: #1f3f73; }
            .gantt .bar-label, .gantt .bar-label.big { fill: #ffffff !important; font-weight: 600 !important; font-size: 11px !important;
                paint-order: stroke fill !important; stroke: #1a1a1a !important; stroke-width: 3px !important; stroke-linejoin: round !important; }
            .gantt .arrow { stroke: #9aa4b2; stroke-width: 1.5 !important; }
            .gantt .grid-row { fill: transparent !important; }
            .gantt .grid-row:nth-child(even) { fill: #232323 !important; }
            .gantt .row-line, .gantt .tick { stroke: #3a3a3a !important; }
            .gantt .today-highlight { fill: #5a4a2a !important; opacity: 0.35 !important; }
            .gantt-container { max-height: calc(100vh - 230px) !important; overflow: auto !important; }
        `;
        document.head.appendChild(s);
    }
    const PROJECT_COLORS = __COLORI__;
    const STATE_COLORS = {"Da inviare": "#7a7a7a", "Presso fornitore": "#e08a00", "Rientrato": "#2e8b57"};
    const LATE = "#c62828";
    function darker(hex) {
        const n = parseInt((hex || "#3a6bbf").replace("#", ""), 16);
        const f = (v) => Math.max(0, Math.round(v * 0.55));
        return "#" + [f(n >> 16), f((n >> 8) & 255), f(n & 255)].map((v) => v.toString(16).padStart(2, "0")).join("");
    }
    function fields() {
        if (DT === "Task") return ["name", "project", "color", "parent_task", "act_start_date", "progress"];
        if (DT === "Job Card") return ["name", "custom_stato_cl", "expected_end_date", "custom_descrizione_fase", "custom_fornitore", "docstatus", "project"];
        return ["name", "project"];
    }
    function paint(svg, wrappers, m) {
        const now = frappe.datetime.now_datetime();
        wrappers.forEach((w) => {
            const d = m[w.getAttribute("data-id")];
            if (!d) return;
            let c = PROJECT_COLORS[d.project] || "#3a6bbf";
            if (DT === "Task" && d.color) c = d.color;
            if (DT === "Task") {
                const lab = w.querySelector(".bar-label");
                if (lab) {
                    if (!lab.dataset.rmzOrig) lab.dataset.rmzOrig = lab.textContent;
                    const da = d.act_start_date ? " · from " + d.act_start_date.split("-").reverse().slice(0, 2).join("/") : "";
                    lab.textContent = lab.dataset.rmzOrig + da + " · " + (Math.round((d.progress || 0) * 10) / 10) + "%";
                }
            }
            if (DT === "Job Card") {
                c = STATE_COLORS[d.custom_stato_cl] || "#7a7a7a";
                if (d.custom_stato_cl !== "Rientrato" && d.docstatus !== 1 && d.expected_end_date && d.expected_end_date < now) c = LATE;
                const lab = w.querySelector(".bar-label");
                if (lab && d.custom_descrizione_fase) lab.textContent = d.custom_descrizione_fase.split(" — ")[0] + " · " + (d.custom_fornitore || "");
            }
            const b = w.querySelector(".bar"), pr = w.querySelector(".bar-progress");
            if (b) b.style.setProperty("fill", c, "important");
            if (pr) pr.style.setProperty("fill", darker(c), "important");
        });
        const pos = {};
        wrappers.forEach((w) => {
            const b = w.querySelector(".bar");
            if (b) pos[w.getAttribute("data-id")] = {x: +b.getAttribute("x"), e: +b.getAttribute("x") + +b.getAttribute("width")};
        });
        svg.querySelectorAll("path[data-from]").forEach((a) => {
            const f = a.getAttribute("data-from"), t = a.getAttribute("data-to");
            if (!pos[f] || !pos[t]) return;
            const parentChild = m[f] && m[f].parent_task === t;
            const bad = !parentChild && pos[t].x < pos[f].e - 1;
            a.style.setProperty("stroke", parentChild ? "#5f6b7a" : (bad ? "#e53935" : "#9aa4b2"), "important");
        });
    }
    function apply() {
        const r = frappe.get_route();
        if (!r || r[1] !== DT || String(r[2]).toLowerCase() !== "gantt") return;
        const svg = document.querySelector(".gantt-container svg") || document.querySelector("svg.gantt");
        if (!svg) return;
        const wrappers = Array.from(svg.querySelectorAll(".bar-wrapper[data-id]"));
        if (!wrappers.length || !wrappers.some((w) => !w.dataset.rmzP)) return;
        const cache = (window["__rmz_c_" + DT] = window["__rmz_c_" + DT] || {});
        const ids = wrappers.map((w) => w.getAttribute("data-id"));
        const missing = ids.filter((i) => !cache[i]);
        const go = () => { paint(svg, wrappers, cache); wrappers.forEach((w) => (w.dataset.rmzP = "1")); };
        if (!missing.length) return go();
        frappe.call({method: "frappe.client.get_list",
            args: {doctype: DT, filters: [["name", "in", missing]], fields: fields(), limit_page_length: missing.length},
            callback: (res) => { (res.message || []).forEach((d) => (cache[d.name] = d)); go(); }});
    }
    if (!window["__rmz_obs_" + DT]) {
        window["__rmz_obs_" + DT] = new MutationObserver(() => { clearTimeout(window["__rmz_t_" + DT]); window["__rmz_t_" + DT] = setTimeout(apply, 300); });
        window["__rmz_obs_" + DT].observe(document.body, {childList: true, subtree: true});
    }
    if (DT === "Task") {
        frappe.listview_settings["Task"] = frappe.listview_settings["Task"] || {};
        const prev = frappe.listview_settings["Task"].onload;
        frappe.listview_settings["Task"].onload = function(lv) {
            if (prev) prev(lv);
            lv.page.add_inner_button(__("Recalculate progress"), () => {
                const f = (lv.filters || []).find((x) => x[1] === "project");
                frappe.call({method: "recalculate_task_progress", args: {project: f ? f[3] : ""},
                    callback: (r) => { window["__rmz_c_Task"] = {}; frappe.show_alert(r.message || "Done"); lv.refresh(); }});
            });
        };
    }
})();
'''
CLIENT_NEW = {"Gantt_Remazel_Task": "Task", "Gantt_Remazel_Work_Order": "Work Order", "Gantt_Remazel_Job_Card": "Job Card"}
CLIENT_OLD = ["Gantt_Fix_Remazel", "Gantt_Fix_Task_Remazel", "Gantt_Fix_Project_Remazel"]

try:
    # ---------- 1. Server Script
    for nome, cfg in SERVER_SCRIPTS.items():
        if frappe.db.exists("Server Script", nome):
            ss = frappe.get_doc("Server Script", nome)
        else:
            ss = frappe.new_doc("Server Script")
            ss.name = nome
            ss.__newname = nome
        for k, v in cfg.items():
            ss.set(k, v)
        ss.disabled = 0
        ss.save() if not ss.is_new() else ss.insert()
        p("Server Script", nome, "OK")
    # calcolo iniziale (stesso codice degli script)
    exec(CODICE_AVANZAMENTO, globals())
    for pr in ["PROJ-0002", "PROJ-0001"]:
        for r in frappe.get_all("Task", filters={"project": pr, "parent_task": ["is", "not set"]}, pluck="name"):
            rmz_ricalcola(r)
    for t in frappe.get_all("Task", filters={"project": "PROJ-0002"}, fields=["name", "subject", "is_group", "progress", "act_start_date", "act_end_date", "exp_start_date", "exp_end_date"], order_by="name"):
        p(("GROUP " if t.is_group else "   ") + t.name, "|", t.subject, "| %", t.progress, "| act", t.act_start_date, "->", t.act_end_date or "-",
          "| barra", t.exp_start_date, "->", t.exp_end_date)

    # ---------- 2. Colori Task
    for pr, col in COLORI.items():
        n = frappe.db.sql("UPDATE `tabTask` SET color=%s WHERE project=%s", (col, pr))
        p("Colore", col, "-> Task di", pr, ":", frappe.db.count("Task", {"project": pr, "color": col}))

    # ---------- 3. Client Script
    for nome, dt in CLIENT_NEW.items():
        cs = frappe.get_doc("Client Script", nome) if frappe.db.exists("Client Script", nome) else frappe.new_doc("Client Script")
        if cs.is_new():
            cs.name = nome
            cs.__newname = nome
        cs.dt = dt
        cs.view = "List"
        cs.enabled = 1
        cs.script = JS.replace("__DT__", dt).replace("__COLORI__", json.dumps(COLORI))
        cs.save() if not cs.is_new() else cs.insert()
        p("Client Script", nome, "(", dt, ") OK")
    for nome in CLIENT_OLD:
        if frappe.db.exists("Client Script", nome):
            frappe.db.set_value("Client Script", nome, "enabled", 0)
            p("Client Script", nome, "disattivato (non cancellato)")

    # ---------- 4. Workspace
    ws = frappe.get_doc("Workspace", WS)
    MAPPA = {"Commesse": ("Project", None, None),
             "Master Plan commesse (Gantt)": ("Master Plan", "URL", "/app/task/view/gantt?is_group=1"),
             "Movimenti Magazzino": ("Production Entries", "URL", "/app/stock-entry?stock_entry_type=Manufacture")}
    content = ws.content
    for s in ws.shortcuts:
        if s.label in MAPPA:
            nuovo, tipo, url = MAPPA[s.label]
            content = content.replace('"shortcut_name":"%s"' % s.label, '"shortcut_name":"%s"' % nuovo).replace('"shortcut_name": "%s"' % s.label, '"shortcut_name": "%s"' % nuovo)
            p("Scorciatoia", s.label, "->", nuovo, url or "")
            s.label = nuovo
            if tipo:
                s.type = tipo
                s.url = url
                s.link_to = None
    if not [s for s in ws.shortcuts if s.label == "Supplier Gantt"]:
        ws.append("shortcuts", {"label": "Supplier Gantt", "type": "URL", "url": "/app/job-card/view/gantt?workstation=Lavorazione%20Esterna", "color": "Orange"})
        blocchi = json.loads(content)
        pos = next((i for i, b in enumerate(blocchi) if b.get("type") == "shortcut" and b.get("data", {}).get("shortcut_name") == "Master Plan"), len(blocchi) - 1)
        blocchi.insert(pos + 1, {"id": frappe.generate_hash(length=10), "type": "shortcut", "data": {"shortcut_name": "Supplier Gantt", "col": 3}})
        content = json.dumps(blocchi)
        p("Scorciatoia Supplier Gantt aggiunta")
    ws.content = content
    ws.save()

    # ---------- 4b. Sidebar
    if frappe.db.exists("DocType", "Workspace Sidebar") and frappe.db.exists("Workspace Sidebar", WS):
        sb = frappe.get_doc("Workspace Sidebar", WS)
        tf = sb.meta.get_table_fields()[0].fieldname
        modello = None
        for it in sb.get(tf):
            if it.label == "Master Plan commesse":
                it.label = "Master Plan"
                it.url = "/app/task/view/gantt?is_group=1"
                modello = it
                p("Sidebar: Master Plan")
            elif it.label == "Commesse (Project)":
                it.label = "Project"
                p("Sidebar: Project")
        if modello and not [it for it in sb.get(tf) if it.label == "Supplier Gantt"]:
            d = modello.as_dict()
            for k in ["name", "idx", "creation", "modified", "owner", "modified_by", "parent", "parentfield", "parenttype", "doctype"]:
                d.pop(k, None)
            d["label"] = "Supplier Gantt"
            d["url"] = "/app/job-card/view/gantt?workstation=Lavorazione%20Esterna"
            righe_sb = sb.get(tf)
            i = righe_sb.index(modello)
            sb.append(tf, d)
            nuova = sb.get(tf).pop()
            sb.get(tf).insert(i + 1, nuova)
            for k, it in enumerate(sb.get(tf), 1):
                it.idx = k
            p("Sidebar: Supplier Gantt aggiunta")
        sb.save()
    esito = "OK"
except Exception as e:
    esito = "ERRORE: " + repr(e)[:400]
    p(esito)

p("=== ESITO ===", esito, "| modalità", "SCRIVI (commit)" if (SCRIVI and esito == "OK") else "PROVA/ERRORE (rollback)")
if SCRIVI and esito == "OK":
    frappe.db.commit()
else:
    frappe.db.rollback()
with open(OUT, "w") as f:
    f.write("\n".join(righe) + "\n")
print("\n".join(righe[-8:]))
print("Scritto", OUT)
