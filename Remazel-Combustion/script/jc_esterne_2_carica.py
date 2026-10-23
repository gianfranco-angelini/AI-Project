# Job Card esterne da caricare (mail Simone 23/10/2026) - CARICAMENTO gruppi completi
# Prerequisito: /home/frappe-user/jc_esterne_23102026_dati.py (lista GRUPPI)
#
# Esecuzione in console:
#   exec(open('/home/frappe-user/jc_esterne_23102026_dati.py').read())
#   SIMULA = True      # prima prova: valida tutto e annulla (rollback), nessuna scrittura
#   exec(open('/home/frappe-user/jc_esterne_2_carica.py').read())
#   SIMULA = False     # solo dopo una simulazione pulita
#   exec(open('/home/frappe-user/jc_esterne_2_carica.py').read())
#
# Cosa fa, solo per i gruppi in cui la quantita' del file copre tutte le Job Card del gruppo:
#   - sostituisce i time log con UNA riga: uscita 08:00 -> rientro 17:00, completed_qty = for_quantity,
#     senza employee (evita il controllo di sovrapposizione per dipendente su decine di Job Card contemporanee)
#   - salva la Job Card (resta in bozza, docstatus 0, nessun submit): i Server Script JobCard_Conto_Lavoro
#     ricalcolano Uscita, Rientro effettivo e Stato conto lavoro = Rientrato
#   - porta la capacita' della Workstation "Lavorazione Esterna" da 50 a 999 (decisione Gian 23/10):
#     con 50 il controllo di sovrapposizione blocca il caricamento (fino a 69 Job Card contemporanee
#     a settembre) e ogni salvataggio successivo di queste Job Card
# Gruppi parziali (quantita' file < somma Job Card): saltati, elencati in fondo (da chiarire con Simone).
#
# Ripristino capacita' (se serve): frappe.db.set_value("Workstation", "Lavorazione Esterna", "production_capacity", 50); frappe.db.commit()

try:
    SIMULA
except NameError:
    SIMULA = True

WS = "Lavorazione Esterna"
CAPACITA = 999

print("=" * 70)
print("MODALITA':", "SIMULAZIONE (rollback)" if SIMULA else "SCRITTURA")
print("=" * 70)
print("Capacita'", WS, "attuale:", frappe.db.get_value("Workstation", WS, "production_capacity"))

ok = []
errori = []
saltati = []
parziali = []

for g in GRUPPI:
    somma = 0
    for n in g["jc"]:
        somma = somma + frappe.utils.flt(frappe.db.get_value("Job Card", n, "for_quantity"))
    if g["qty"] < somma:
        parziali.append(g["cod"] + " | file " + str(g["qty"]) + " < Job Card " + str(somma))
        continue
    print()
    print(">>", g["cod"], "| uscita", g["uscita"], "| rientro", g["rientro"], "| qty file", g["qty"], "| somma JC", somma)
    da = frappe.utils.get_datetime(g["uscita"] + " 08:00:00")
    a = frappe.utils.get_datetime(g["rientro"] + " 17:00:00")
    minuti = frappe.utils.time_diff_in_seconds(a, da) / 60.0
    for n in g["jc"]:
        try:
            frappe.db.set_value("Workstation", WS, "production_capacity", CAPACITA)
            jc = frappe.get_doc("Job Card", n)
            if jc.docstatus != 0:
                saltati.append(n + " docstatus " + str(jc.docstatus))
                print("   ", n, "SALTATA: docstatus", jc.docstatus)
                continue
            jc.set("time_logs", [])
            jc.append("time_logs", {"from_time": da, "to_time": a, "time_in_mins": minuti,
                                    "completed_qty": jc.for_quantity})
            jc.save()
            print("   ", n, "| ws:", jc.workstation, "| seq", jc.sequence_id, "| qty", jc.for_quantity,
                  "| fatta", jc.total_completed_qty, "|", jc.status, "| usc", jc.custom_data_uscita,
                  "| rient", jc.custom_rientro_effettivo, "|", jc.custom_stato_cl)
            if SIMULA:
                frappe.db.rollback()
            else:
                frappe.db.commit()
            ok.append(n)
        except Exception as e:
            frappe.db.rollback()
            errori.append(n + " | " + type(e).__name__ + " | " + str(e)[:200])
            print("   ", n, "ERRORE", type(e).__name__, str(e)[:200])
        frappe.local.message_log = []

print()
print("=" * 70)
print("Riepilogo", "(SIMULAZIONE - nulla scritto)" if SIMULA else "(SCRITTO)")
print("=" * 70)
print("Job Card OK:", len(ok))
print("Errori:", len(errori))
for x in errori:
    print("  ", x)
print("Saltate:", len(saltati))
for x in saltati:
    print("  ", x)
print("Gruppi parziali NON caricati:", len(parziali))
for x in parziali:
    print("  ", x)
print("Capacita'", WS, "ora:", frappe.db.get_value("Workstation", WS, "production_capacity"))
