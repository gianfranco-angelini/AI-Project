# Job Card esterne (mail Simone 23/10/2026) - fasi NON iniziali bloccate da OperationSequenceError
# Opzione B: azzera sequence_id (0) SOLO sulle Job Card indicate, poi carica il time log come jc_esterne_2_carica.py
# Prerequisito: /home/frappe-user/jc_esterne_23102026_dati.py (lista GRUPPI)
#
# Esecuzione in console:
#   exec(open('/home/frappe-user/jc_esterne_23102026_dati.py').read())
#   SIMULA = True
#   exec(open('/home/frappe-user/jc_esterne_3_sequenza.py').read())
#   SIMULA = False     # solo dopo una simulazione pulita
#   exec(open('/home/frappe-user/jc_esterne_3_sequenza.py').read())
#
# Motivo: ERPNext (validate_sequence_id) blocca quantita' completate su una Job Card se le fasi precedenti
# del Work Order non risultano completate (= Job Card inviate). Il controllo legge il sequence_id della
# Job Card stessa: se 0 il controllo non si applica (la colonna e' NOT NULL, None da IntegrityError). Work Order Operation e BOM restano invariati.
# Verificato: JobCard_Avviso_Precedenze e Gantt_Remazel_Job_Card non usano sequence_id.
#
# Ripristino sequence_id (se serve): il valore originale e' stampato a video per ogni Job Card;
#   frappe.db.set_value("Job Card", "<nome>", "sequence_id", <valore>, update_modified=False); frappe.db.commit()

try:
    SIMULA
except NameError:
    SIMULA = True

CODICI = ["T08-0100-P6000-10SA"]

print("=" * 70)
print("MODALITA':", "SIMULAZIONE (rollback)" if SIMULA else "SCRITTURA")
print("=" * 70)

ok = []
errori = []

for g in GRUPPI:
    if g["cod"] not in CODICI:
        continue
    print()
    print(">>", g["cod"], "| uscita", g["uscita"], "| rientro", g["rientro"], "| qty file", g["qty"])
    da = frappe.utils.get_datetime(g["uscita"] + " 08:00:00")
    a = frappe.utils.get_datetime(g["rientro"] + " 17:00:00")
    minuti = frappe.utils.time_diff_in_seconds(a, da) / 60.0
    for n in g["jc"]:
        try:
            seq = frappe.db.get_value("Job Card", n, "sequence_id")
            frappe.db.set_value("Job Card", n, "sequence_id", 0, update_modified=False)
            jc = frappe.get_doc("Job Card", n)
            if jc.docstatus != 0:
                print("   ", n, "SALTATA: docstatus", jc.docstatus)
                frappe.db.rollback()
                continue
            jc.set("time_logs", [])
            jc.append("time_logs", {"from_time": da, "to_time": a, "time_in_mins": minuti,
                                    "completed_qty": jc.for_quantity})
            jc.save()
            print("   ", n, "| seq originale", seq, "-> ora", jc.sequence_id, "| ws:", jc.workstation,
                  "| qty", jc.for_quantity, "| fatta", jc.total_completed_qty, "|", jc.status,
                  "| usc", jc.custom_data_uscita, "| rient", jc.custom_rientro_effettivo, "|", jc.custom_stato_cl)
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
