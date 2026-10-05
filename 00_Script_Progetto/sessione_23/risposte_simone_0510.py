# Sessione 23 - Applicazione risposte di Simone del 05/10/2026.
# A) Calendario Fornitori 2026-2029 = festività + chiusure aziendali del Calendario Remazel, SENZA sabati/domeniche;
#    assegnato alla postazione Lavorazione Esterna (vale per le pianificazioni future).
#    + elenco Job Card esterne T09 aperte che attraversano giorni di chiusura (solo segnalazione).
# B) P4000-10LA / P5000-10LA = TT 150 h (9000 min) sulla BOM; 12 WO T09 in bozza: tempo fase aggiornato,
#    data inizio = inizio del liner del set meno la durata (non prima di adesso), poi submit.
# C) Verifica microfusioni (FE): fasi presenti dopo la FE nelle BOM default.
# Uso: exec(open(f).read(), {"frappe": frappe, "SCRIVI": False})
import datetime
SCRIVI = globals().get("SCRIVI", False)
print("=== MODALITA':", "SCRITTURA" if SCRIVI else "PROVA (nessuna scrittura)", "===")
adesso = frappe.utils.now_datetime().replace(microsecond=0)

# ---------- A) Calendario Fornitori
HL_SRC = "Calendario Remazel 2026-2029"
HL_NEW = "Calendario Fornitori 2026-2029"
giorni = []
for h in frappe.db.sql("SELECT holiday_date, description FROM `tabHoliday` WHERE parent=%s ORDER BY holiday_date", HL_SRC, as_dict=True):
    if h.holiday_date.weekday() < 5:
        giorni.append(h)
print("A) Giorni di chiusura feriali da", HL_SRC, ":", len(giorni), "| esiste gia", HL_NEW, ":", bool(frappe.db.exists("Holiday List", HL_NEW)))
print("   Lavorazione Esterna holiday_list attuale:", frappe.db.get_value("Workstation", "Lavorazione Esterna", "holiday_list"))
chiusi = set()
for h in giorni:
    chiusi.add(h.holiday_date)
attraversano = []
for jc in frappe.db.sql("""SELECT name, work_order, expected_start_date, expected_end_date, custom_fornitore FROM `tabJob Card`
        WHERE project='PROJ-0002' AND docstatus=0 AND (workstation_type='Lavorazione Esterna' OR workstation='Lavorazione Esterna')
        AND expected_start_date IS NOT NULL AND expected_end_date IS NOT NULL""", as_dict=True):
    d = frappe.utils.getdate(jc.expected_start_date)
    fine = frappe.utils.getdate(jc.expected_end_date)
    n = 0
    while d <= fine:
        if d in chiusi:
            n = n + 1
        d = d + datetime.timedelta(days=1)
    if n:
        attraversano.append([jc.name, jc.custom_fornitore, jc.expected_start_date, jc.expected_end_date, n])
print("   JC esterne T09 che attraversano chiusure:", len(attraversano), "| giorni persi totali:", sum([x[4] for x in attraversano]) if attraversano else 0)
for x in attraversano[:10]:
    print("     ", x[0], x[1], x[2], "->", x[3], "| giorni chiusi", x[4])

# ---------- B) P4000 / P5000
TT_MIN = 9000.0
CODICI = ["T08-0100-P4000-10LA", "T08-0100-P5000-10LA"]
bom_ops = []
for b in frappe.db.sql("SELECT name FROM `tabBOM` WHERE item IN ('T08-0100-P4000','T08-0100-P5000') AND is_default=1 AND is_active=1 AND docstatus=1", pluck=True):
    for r in frappe.db.sql("SELECT name, parent, description, time_in_mins, fixed_time FROM `tabBOM Operation` WHERE parent=%s", b, as_dict=True):
        cod = frappe.utils.strip_html(r.description or "").strip().split(" ")[0]
        if cod in CODICI:
            bom_ops.append(r)
            print("B) BOM", r.parent, cod, "| min", r.time_in_mins, "->", TT_MIN, "| fixed", r.fixed_time)
wos = frappe.get_all("Work Order", filters={"project": "PROJ-0002", "docstatus": 0}, fields=["name", "production_item", "qty", "production_plan", "planned_start_date"], order_by="production_plan, production_item")
piano = []
for w in wos:
    ops = frappe.db.sql("SELECT name, description, time_in_mins, workstation_type FROM `tabWork Order Operation` WHERE parent=%s ORDER BY idx", w.name, as_dict=True)
    durata = 0
    da_agg = []
    for o in ops:
        cod = frappe.utils.strip_html(o.description or "").strip().split(" ")[0]
        t = o.time_in_mins or 0
        if cod in CODICI:
            da_agg.append(o.name)
            t = TT_MIN
        durata = durata + t
    fg_start = frappe.db.get_value("Work Order", {"production_plan": w.production_plan, "production_item": "T09-0100-A0001", "docstatus": 1}, "planned_start_date")
    inizio = frappe.utils.get_datetime(fg_start) - datetime.timedelta(minutes=durata) if fg_start else adesso
    if inizio < adesso:
        inizio = adesso
    piano.append([w.name, w.production_item, w.qty, w.production_plan, da_agg, durata, fg_start, inizio])
    print("B) WO", w.name, w.production_item, "qty", w.qty, w.production_plan, "| fasi da aggiornare", len(da_agg), "| durata h %.0f" % (durata / 60), "| inizio liner", fg_start, "| inizio WO ->", inizio)

# ---------- C) Microfusioni
print("C) Fasi dopo la FE (BOM default):")
for b in frappe.db.sql("SELECT DISTINCT bo.parent FROM `tabBOM Operation` bo JOIN `tabBOM` b ON b.name=bo.parent WHERE b.is_default=1 AND b.is_active=1 AND b.docstatus=1 AND bo.description LIKE '%%-10FE%%'", pluck=True):
    ops = frappe.db.sql("SELECT idx, description, workstation_type FROM `tabBOM Operation` WHERE parent=%s ORDER BY idx", b, as_dict=True)
    dopo = False
    seq = []
    for o in ops:
        cod = frappe.utils.strip_html(o.description or "").strip().split(" ")[0]
        if cod.endswith("FE"):
            dopo = True
            seq.append("[" + cod[-6:] + "]")
        elif dopo:
            seq.append(cod[-6:] + "(" + (o.workstation_type or "")[:6] + ")")
    print("   ", b, "| fasi totali", len(ops), "| FE e successive:", " ".join(seq))

if SCRIVI:
    if not frappe.db.exists("Holiday List", HL_NEW):
        hl = frappe.new_doc("Holiday List")
        hl.holiday_list_name = HL_NEW
        hl.from_date = "2026-01-01"
        hl.to_date = "2029-12-31"
        for h in giorni:
            hl.append("holidays", {"holiday_date": h.holiday_date, "description": h.description})
        hl.insert()
        print("-> creata", HL_NEW, "con", len(giorni), "giorni")
    frappe.db.set_value("Workstation", "Lavorazione Esterna", "holiday_list", HL_NEW)
    print("-> Lavorazione Esterna: holiday_list =", HL_NEW)
    for r in bom_ops:
        frappe.db.set_value("BOM Operation", r.name, {"time_in_mins": TT_MIN, "fixed_time": 1}, update_modified=False)
    frappe.db.commit()
    ok = 0
    for x in piano:
        try:
            for opn in x[4]:
                frappe.db.set_value("Work Order Operation", opn, {"time_in_mins": TT_MIN}, update_modified=False)
            frappe.db.set_value("Work Order", x[0], "planned_start_date", x[7], update_modified=False)
            frappe.db.commit()
            d = frappe.get_doc("Work Order", x[0])
            d.submit()
            frappe.db.commit()
            ok = ok + 1
            d.reload()
            print("-> submit", x[0], x[1], "|", d.planned_start_date, "->", d.planned_end_date)
        except Exception as e:
            frappe.db.rollback()
            print("ERRORE", x[0], repr(e)[:300])
    print("-> WO sottomessi:", ok, "su", len(piano), "| WO T09 per docstatus:", frappe.db.sql("SELECT docstatus, COUNT(*) FROM `tabWork Order` WHERE project='PROJ-0002' GROUP BY docstatus"))
    print("Chiudere e riaprire la console prima di altre operazioni.")
else:
    print("PROVA: nessuna scrittura")
