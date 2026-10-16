# Sessione 26 (16/10/2026) - SOLA LETTURA
# Elenco delle fasi da avviare per far partire il sistema sulla T09-0100 (PROJ-0002).
# Per ogni Work Order non completato prende la prima Job Card non completata (ordine del ciclo)
# e la classifica:
#   PRONTA        = fasi precedenti del WO completate e, se e' la prima fase di un assieme,
#                   tutti i WO dei componenti dello stesso set completati
#   IN ATTESA     = prima fase di un assieme con componenti non ancora completati
# Stampa il riepilogo e scrive il CSV in /home/frappe-user/script_progetto/prossime_fasi_t09.csv
# Uso in bench --site site1.local console:
#   exec(open("/home/frappe-user/script_progetto/prossime_fasi.py").read(), {"frappe": frappe})
import csv

PROJECT = "PROJ-0002"
OUT = "/home/frappe-user/script_progetto/prossime_fasi_t09.csv"
oggi = frappe.utils.now_datetime()

wos = frappe.get_all("Work Order",
                     filters={"project": PROJECT, "docstatus": 1, "status": ["not in", ["Completed", "Stopped", "Closed"]]},
                     fields=["name", "production_item", "production_plan", "expected_delivery_date", "status"])
print("Work Order aperti:", len(wos))

# WO per set e articolo, per trovare i componenti di un assieme nello stesso set
wo_per_pp_item = {}
for w in frappe.get_all("Work Order", filters={"project": PROJECT, "docstatus": 1},
                        fields=["name", "production_item", "production_plan", "status"]):
    chiave = (w.production_plan, w.production_item)
    if chiave not in wo_per_pp_item:
        wo_per_pp_item[chiave] = []
    wo_per_pp_item[chiave].append(w)

righe = []
conta_stato = {"PRONTA": 0, "IN ATTESA": 0}
conta_reparto = {}
for w in wos:
    jcs = frappe.get_all("Job Card", filters={"work_order": w.name, "docstatus": ["!=", 2]},
                         fields=["name", "status", "operation_id", "workstation", "expected_start_date",
                                 "expected_end_date", "custom_descrizione_fase", "custom_fornitore",
                                 "custom_stato_cl", "custom_consegna_set"])
    if not jcs:
        continue
    ordinate = []
    for jc in jcs:
        idx = frappe.db.get_value("Work Order Operation", jc.operation_id, "idx") or 999
        ordinate.append((idx, jc))
    ordinate.sort(key=lambda x: x[0])
    prossima = None
    posizione = 0
    for n, coppia in enumerate(ordinate):
        if coppia[1].status != "Completed":
            prossima = coppia[1]
            posizione = n
            break
    if prossima is None:
        continue
    stato = "PRONTA"
    mancanti = ""
    if posizione == 0:
        componenti = frappe.get_all("Work Order Item", filters={"parent": w.name}, pluck="item_code")
        aperti = []
        for item in componenti:
            for cw in wo_per_pp_item.get((w.production_plan, item), []):
                if cw.status != "Completed":
                    aperti.append(item)
                    break
        if aperti:
            stato = "IN ATTESA"
            mancanti = ", ".join(aperti)
    in_ritardo = "SI" if prossima.expected_start_date and prossima.expected_start_date < oggi else ""
    conta_stato[stato] = conta_stato[stato] + 1
    if stato == "PRONTA":
        conta_reparto[prossima.workstation] = conta_reparto.get(prossima.workstation, 0) + 1
    righe.append([stato, str(prossima.custom_consegna_set or w.expected_delivery_date or ""), w.production_plan,
                  w.name, w.production_item, prossima.name, prossima.workstation,
                  prossima.custom_descrizione_fase or "", prossima.custom_fornitore or "",
                  prossima.custom_stato_cl or "", str(prossima.expected_start_date or ""), in_ritardo, mancanti])

righe.sort(key=lambda r: (r[0] != "PRONTA", r[10]))
with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
    scrittore = csv.writer(f, delimiter=";")
    scrittore.writerow(["Stato", "Consegna set", "Production Plan", "Work Order", "Articolo", "Job Card", "Reparto",
                        "Descrizione fase", "Fornitore", "Stato conto lavoro", "Inizio pianificato",
                        "Inizio gia' passato", "Componenti non completati"])
    for r in righe:
        scrittore.writerow(r)

print("Fasi PRONTE:", conta_stato["PRONTA"], "| IN ATTESA dei componenti:", conta_stato["IN ATTESA"])
print("--- Fasi pronte per reparto ---")
for rep in sorted(conta_reparto):
    print(rep, ":", conta_reparto[rep])
print("--- Prime 25 fasi pronte, per inizio pianificato ---")
for r in righe[:25]:
    if r[0] != "PRONTA":
        break
    print(r[10][:16], "|", r[1], "|", r[5], "|", r[6], "|", r[7][:55], "|", r[8], "|", "RITARDO" if r[11] else "")
print("CSV:", OUT, "righe:", len(righe))
