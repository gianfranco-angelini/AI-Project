# Job Card esterne da caricare (mail Simone 23/10/2026) - SOLA LETTURA
# Prerequisito: /home/frappe-user/jc_esterne_23102026_dati.py (lista GRUPPI)
# Esecuzione in console:
#   exec(open('/home/frappe-user/jc_esterne_23102026_dati.py').read())
#   exec(open('/home/frappe-user/jc_esterne_1_lettura.py').read())

print("=" * 70)
print("A - Server Script e impostazioni che toccano la Job Card")
print("=" * 70)
ss = frappe.get_all("Server Script", filters={"reference_doctype": "Job Card"},
                    fields=["name", "script_type", "doctype_event", "disabled"])
for s in ss:
    print("  ", s.name, "|", s.script_type, "|", s.doctype_event, "| disabled:", s.disabled)
for s in ss:
    if "uscita" in (frappe.db.get_value("Server Script", s.name, "script") or "").lower():
        print()
        print("--- script", s.name, "---")
        print(frappe.db.get_value("Server Script", s.name, "script"))
api = frappe.get_all("Server Script", filters={"script_type": "API"}, fields=["name", "api_method", "disabled"])
print("Server Script API:")
for s in api:
    print("  ", s.name, "|", s.api_method, "| disabled:", s.disabled)
ms = frappe.get_single("Manufacturing Settings")
for k in ["disable_capacity_planning", "allow_overtime", "job_card_excess_transfer",
          "enforce_time_logs", "add_corrective_operation_cost_in_finished_good_valuation",
          "overproduction_percentage_for_work_order", "set_op_cost_and_scrape_from_sub_assemblies"]:
    if ms.meta.get_field(k):
        print("Manufacturing Settings", k, "=", ms.get(k))
f = frappe.get_meta("Job Card").get_field("custom_stato_cl")
print("custom_stato_cl opzioni:", (f.options or "").replace("\n", " / "))

print()
print("=" * 70)
print("B - Job Card del file")
print("=" * 70)
mancanti = []
tot = 0
for g in GRUPPI:
    print()
    print(">>", g["cod"], "| qty file:", g["qty"], "| uscita:", g["uscita"], "| rientro:", g["rientro"], "|", g["nota"])
    somma = 0
    for n in g["jc"]:
        tot = tot + 1
        if not frappe.db.exists("Job Card", n):
            mancanti.append(n)
            print("   ", n, "NON ESISTE")
            continue
        d = frappe.db.get_value("Job Card", n,
            ["work_order", "production_item", "operation", "custom_descrizione_fase", "workstation",
             "for_quantity", "total_completed_qty", "status", "docstatus", "sequence_id",
             "custom_consegna_set", "custom_data_uscita", "custom_rientro_previsto",
             "custom_rientro_effettivo", "custom_stato_cl", "custom_fornitore",
             "expected_start_date", "expected_end_date", "is_subcontracted"], as_dict=True)
        somma = somma + (d.for_quantity or 0)
        tl = frappe.get_all("Job Card Time Log", filters={"parent": n},
                            fields=["from_time", "to_time", "time_in_mins", "completed_qty", "employee"])
        print("   ", n, "|", d.work_order, "|", d.production_item, "| op:", d.operation, "| ws:", d.workstation,
              "| qty:", d.for_quantity, "| fatta:", d.total_completed_qty, "|", d.status, "| ds:", d.docstatus,
              "| seq:", d.sequence_id)
        print("        fase:", (d.custom_descrizione_fase or "")[:60], "| set:", d.custom_consegna_set,
              "| prev:", d.expected_start_date, "->", d.expected_end_date)
        print("        CL: forn:", d.custom_fornitore, "| stato:", d.custom_stato_cl, "| usc:", d.custom_data_uscita,
              "| rient.prev:", d.custom_rientro_previsto, "| rient.eff:", d.custom_rientro_effettivo,
              "| subc:", d.is_subcontracted)
        for t in tl:
            print("        log:", t.from_time, "->", t.to_time, "|", t.time_in_mins, "min | qty", t.completed_qty, "|", t.employee)
    print("   somma for_quantity:", somma, "vs file:", g["qty"])

print()
print("Job Card nel file:", tot, "| non trovate:", len(mancanti), mancanti)
print("FINE - nessuna modifica effettuata")
