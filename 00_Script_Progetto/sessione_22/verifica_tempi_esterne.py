# Sessione 22 - SOLA LETTURA. Confronto tempi fasi esterne a sistema (time_in_mins) con TT del ciclo
# di Simone (T09-0100_Ciclo_e_fasi_26-19008.xlsx, colonna "TT [H]" = Attivita/set x C/T, lotto da 10 liner).
# TT_ESTERNE: codice fase -> [pezzi/set, C/T h, TT h, fornitore, note] (da dati_tt_esterne_t09.json)
# Uso: exec(open(f).read(), {"frappe": frappe, "TT_ESTERNE": TT_ESTERNE}) oppure incollato con TT_ESTERNE definito
bom_default = frappe.db.sql("SELECT name, item FROM `tabBOM` WHERE is_default=1 AND is_active=1 AND docstatus=1", as_dict=True)
uguali = []
diversi = []
mancanti = []
for b in bom_default:
    ops = frappe.db.sql("SELECT name, idx, time_in_mins, fixed_time, description FROM `tabBOM Operation` WHERE parent=%s AND workstation_type='Lavorazione Esterna' ORDER BY idx", b.name, as_dict=True)
    for r in ops:
        cod = frappe.utils.strip_html(r.description or "").strip().split(" ")[0]
        att = r.time_in_mins or 0
        if cod in TT_ESTERNE and TT_ESTERNE[cod][2]:
            nuovo = round(TT_ESTERNE[cod][2] * 60, 1)
            riga = [b.item[:8], cod, att, nuovo, TT_ESTERNE[cod][0], TT_ESTERNE[cod][3], r.fixed_time]
            if abs(att - nuovo) < 1:
                uguali.append(riga)
            else:
                diversi.append(riga)
        else:
            mancanti.append([b.item[:8], cod, att, r.fixed_time])
print("BOM default attive:", len(bom_default))
print("Fasi esterne: uguali al TT", len(uguali), "| diverse", len(diversi), "| senza TT nel ciclo T09", len(mancanti))
print("")
print("=== DIVERSE (prodotto, fase, min attuali -> min da TT, pezzi/set, fornitore, fixed_time) ===")
for x in diversi:
    print(x[0], x[1], x[2], "->", x[3], "| set", x[4], "| x%.1f" % (x[3] / x[2] if x[2] else 0), "|", x[5], "| fixed", x[6])
print("")
print("=== SENZA TT NEL CICLO T09 (prodotto, fase, min attuali, fixed_time) ===")
for x in mancanti:
    print(x[0], x[1], x[2], "| fixed", x[3])
print("")
print("=== UGUALI ===")
for x in uguali:
    print(x[0], x[1], x[2], "| set", x[4], "|", x[5])
jc_aperte = frappe.db.sql("SELECT COUNT(*) FROM `tabJob Card` WHERE docstatus=0 AND workstation_type='Lavorazione Esterna'")[0][0]
print("")
print("Job Card esterne in bozza (non si aggiornano cambiando la BOM):", jc_aperte)
print("Nessuna scrittura eseguita.")
