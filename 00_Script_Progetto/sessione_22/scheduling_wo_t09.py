# Sessione 22 - Scheduling all'indietro dei WO T09 in bozza (348 WO, 6 Production Plan).
# Regole: 3B fine set = consegna - Buffer Project (PROJ-0002); 2A inizio non prima di adesso.
# Passo 1 (indietro): dal prodotto finito ai livelli bassi, ogni WO deve finire prima dell'inizio del padre.
# Passo 2 (avanti): dai livelli bassi in su, inizio = max(inizio a ritroso, adesso, fine dei figli).
# Durata WO = somma delle operazioni (time_in_mins del WO). Postazioni 24h (Lavorazione Esterna):
# tempo continuo; postazioni interne: giorni lavorativi del loro calendario, minuti/giorno da orario.
# Scrive solo planned_start_date dei WO in bozza. La capacità vera la calcola ERPNext al submit.
# Uso: exec(open(f).read(), {"frappe": frappe, "SCRIVI": False})
import datetime
import math
SCRIVI = globals().get("SCRIVI", False)
PPS = ["MFG-PP-2026-00002", "MFG-PP-2026-00003", "MFG-PP-2026-00004", "MFG-PP-2026-00005", "MFG-PP-2026-00006", "MFG-PP-2026-00007"]
PRJ = "PROJ-0002"
print("=== MODALITA':", "SCRITTURA" if SCRIVI else "PROVA (nessuna scrittura)", "===")

CONTROLLO = [
    ["Work Order", ["production_plan", "production_plan_item", "production_plan_sub_assembly_item", "production_item", "planned_start_date", "expected_delivery_date"]],
    ["Work Order Operation", ["workstation", "workstation_type", "time_in_mins"]],
    ["Production Plan Sub Assembly Item", ["production_item", "parent_item_code", "bom_level"]],
    ["Workstation", ["workstation_type", "holiday_list", "working_hours"]],
]
for c in CONTROLLO:
    meta = frappe.get_meta(c[0])
    for campo in c[1]:
        if not meta.has_field(campo):
            frappe.throw("Campo mancante: " + c[0] + "." + campo)

adesso = frappe.utils.now_datetime().replace(microsecond=0)
buffer = frappe.db.get_value("Project", PRJ, "custom_buffer_giorni") or 0
CAL = {}

def calendario(tipo, ws_nome):
    chiave = ws_nome or tipo
    if chiave in CAL:
        return CAL[chiave]
    nome = ws_nome
    if not nome:
        lista = frappe.get_all("Workstation", filters={"workstation_type": tipo}, pluck="name", limit=1)
        if lista:
            nome = lista[0]
        elif frappe.db.exists("Workstation", tipo):
            nome = tipo
    info = {"minuti": 1440, "h24": True, "fest": set(), "ora_inizio": datetime.time(0, 0), "ora_fine": datetime.time(23, 59), "nome": nome}
    if nome:
        ws = frappe.get_doc("Workstation", nome)
        minuti = 0
        primo = None
        ultimo = None
        for h in ws.working_hours:
            if h.get("enabled") == 0:
                continue
            minuti = minuti + (frappe.utils.to_timedelta(h.end_time) - frappe.utils.to_timedelta(h.start_time)).total_seconds() / 60
            if primo is None or frappe.utils.to_timedelta(h.start_time) < primo:
                primo = frappe.utils.to_timedelta(h.start_time)
            if ultimo is None or frappe.utils.to_timedelta(h.end_time) > ultimo:
                ultimo = frappe.utils.to_timedelta(h.end_time)
        if minuti > 0 and minuti < 1430:
            info["minuti"] = minuti
            info["h24"] = False
            info["ora_inizio"] = (datetime.datetime.min + primo).time()
            info["ora_fine"] = (datetime.datetime.min + ultimo).time()
        if ws.holiday_list:
            for d in frappe.db.sql("SELECT holiday_date FROM `tabHoliday` WHERE parent=%s", ws.holiday_list, pluck=True):
                info["fest"].add(d)
    CAL[chiave] = info
    return info

def indietro(fine, minuti, info):
    if minuti <= 0:
        return fine
    if info["h24"]:
        return fine - datetime.timedelta(minutes=minuti)
    giorni = int(math.ceil(minuti / info["minuti"]))
    d = fine.date()
    if fine.time() <= info["ora_inizio"]:
        d = d - datetime.timedelta(days=1)
    contati = 0
    while True:
        if d not in info["fest"]:
            contati = contati + 1
            if contati >= giorni:
                break
        d = d - datetime.timedelta(days=1)
    return datetime.datetime.combine(d, info["ora_inizio"])

def avanti(inizio, minuti, info):
    if minuti <= 0:
        return inizio
    if info["h24"]:
        return inizio + datetime.timedelta(minutes=minuti)
    giorni = int(math.ceil(minuti / info["minuti"]))
    d = inizio.date()
    if inizio.time() > info["ora_inizio"]:
        d = d + datetime.timedelta(days=1)
    contati = 0
    while True:
        if d not in info["fest"]:
            contati = contati + 1
            if contati >= giorni:
                break
        d = d + datetime.timedelta(days=1)
    return datetime.datetime.combine(d, info["ora_fine"])

def operazioni(wo_nome):
    return frappe.db.sql("SELECT workstation, workstation_type, time_in_mins FROM `tabWork Order Operation` WHERE parent=%s ORDER BY idx", wo_nome, as_dict=True)

riepilogo = []
da_scrivere = []
for pp in PPS:
    wos = frappe.get_all("Work Order", filters={"production_plan": pp, "docstatus": 0}, fields=["name", "production_item", "production_plan_sub_assembly_item", "qty", "expected_delivery_date"])
    righe = {}
    for r in frappe.db.sql("SELECT name, production_item, parent_item_code, bom_level FROM `tabProduction Plan Sub Assembly Item` WHERE parent=%s", pp, as_dict=True):
        righe[r.name] = r
    fg = None
    per_item = {}
    livello = {}
    for w in wos:
        if not w.production_plan_sub_assembly_item:
            fg = w
            livello[w.name] = -1
        else:
            livello[w.name] = righe[w.production_plan_sub_assembly_item].bom_level
        per_item.setdefault(w.production_item, []).append(w.name)
    if not fg:
        print(pp, "ERRORE: WO prodotto finito non trovato")
        continue
    padri = {}
    figli = {}
    for w in wos:
        figli.setdefault(w.name, [])
    for w in wos:
        if w.name == fg.name:
            padri[w.name] = []
            continue
        pi = righe[w.production_plan_sub_assembly_item].parent_item_code
        lista = per_item.get(pi) or [fg.name]
        padri[w.name] = lista
        for p in lista:
            figli[p].append(w.name)
    ops = {}
    for w in wos:
        ops[w.name] = operazioni(w.name)
    consegna = fg.expected_delivery_date
    deadline = datetime.datetime.combine(frappe.utils.getdate(frappe.utils.add_days(consegna, -buffer)), datetime.time(17, 0))
    ordine = []
    for lv in range(-1, 12):
        for w in wos:
            if livello[w.name] == lv:
                ordine.append(w.name)
    tardi = {}
    for n in ordine:
        if n == fg.name:
            fine = deadline
        else:
            fine = None
            for p in padri[n]:
                if fine is None or tardi[p] < fine:
                    fine = tardi[p]
        t = fine
        i = len(ops[n]) - 1
        while i >= 0:
            o = ops[n][i]
            t = indietro(t, o.time_in_mins or 0, calendario(o.workstation_type, o.workstation))
            i = i - 1
        tardi[n] = t
    inizio_eff = {}
    fine_eff = {}
    i = len(ordine) - 1
    while i >= 0:
        n = ordine[i]
        s = tardi[n]
        if s < adesso:
            s = adesso
        for f in figli[n]:
            if fine_eff[f] > s:
                s = fine_eff[f]
        inizio_eff[n] = s
        t = s
        for o in ops[n]:
            t = avanti(t, o.time_in_mins or 0, calendario(o.workstation_type, o.workstation))
        fine_eff[n] = t
        i = i - 1
    primo = None
    in_passato = 0
    for n in ordine:
        if primo is None or tardi[n] < primo:
            primo = tardi[n]
        if tardi[n] < adesso:
            in_passato = in_passato + 1
        da_scrivere.append([n, inizio_eff[n]])
    ritardo = (fine_eff[fg.name].date() - deadline.date()).days
    oltre_consegna = (fine_eff[fg.name].date() - frappe.utils.getdate(consegna)).days
    riepilogo.append([pp, fg.qty, consegna, deadline.date(), primo, in_passato, len(ordine), fine_eff[fg.name], ritardo, oltre_consegna])

print("Adesso:", adesso, "| Buffer Project:", buffer, "gg")
print("Calendari usati:")
for k in CAL:
    print("   ", k, "->", CAL[k]["nome"], "| 24h" if CAL[k]["h24"] else "| %d min/g, %s-%s, festivi %d" % (CAL[k]["minuti"], CAL[k]["ora_inizio"], CAL[k]["ora_fine"], len(CAL[k]["fest"])))
print("")
for r in riepilogo:
    print(r[0], "| liner", r[1], "| consegna", r[2], "| fine prevista (-buffer)", r[3])
    print("    inizio necessario a ritroso:", r[4], "| WO con inizio nel passato:", r[5], "su", r[6])
    print("    fine effettiva liner:", r[7], "| scarto su fine prevista:", r[8], "gg | scarto su consegna:", r[9], "gg", "-> IN RITARDO" if r[9] > 0 else "-> OK")
if SCRIVI:
    for x in da_scrivere:
        frappe.db.set_value("Work Order", x[0], "planned_start_date", x[1], update_modified=False)
    frappe.db.commit()
    print("-> scritto planned_start_date su", len(da_scrivere), "WO")
else:
    print("PROVA: nessuna scrittura (", len(da_scrivere), "WO da aggiornare )")
