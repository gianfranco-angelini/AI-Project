# Script sessione 22 (02/10/2026) — carico T09-0100

Ordine di esecuzione (tutti in `bench --site site1.local console`, come `frappe-user`):

| # | Script | Cosa fa | Esito |
|---|---|---|---|
| 1 | `confronto_t09_t08.py` | Confronta ogni articolo del ciclo T09 del 22/09 con la controparte T08 (fasi, materiale, componenti) | Sola lettura |
| 2 | `import_t09_prova.py` / `import_t09_scrivi.py` | 14 Item + 14 BOM T09/T08-0200 + BOM-T08-0100-P2301-002 (10VX). Dati in `dati_import_t09.json` | Eseguito |
| 3 | `project_so_t09.py` | PROJ-0002 + SAL-ORD-2026-00002 (100 liner, 6 set) + po_no T08 | Eseguito |
| 4 | `fixed_time_lavorazione_esterna.py` | fixed_time su 214 fasi per lotto + capacità Lavorazione Esterna 50 | Eseguito |
| 5 | `campi_consegna_set_jobcard.py` | Campi Consegna set / Production Plan su Job Card + Server Script WorkOrder_Consegna_Set | Eseguito |
| 6 | `correzione_I000_databook.py` | F000 -> I000 per AISI 304L, Data Book T09 1080 min | Eseguito |
| 7 | `pp_t09.py` | 6 Production Plan (MFG-PP-2026-00002…00007) | Eseguito |
| 8 | `jobcard_conto_lavoro.py` | Expediting fase 1: sezione Conto lavoro su Job Card, Server Script JobCard_Fornitore / JobCard_Conto_Lavoro(_Submitted), riallineamento 130 Job Card esterne T08 | Eseguito |

Gli script con `globals().get(...)` vanno lanciati passando le variabili:
`exec(open(f).read(), {"frappe": frappe, "SCRIVI_PP": True})` — `exec` non vede le variabili della console.
Gli altri hanno `SCRIVI = False` in testa: cambiare a `True` per scrivere.
| 9 | `project_buffer_ricalcolo.py` | Server Script Project_Deadline_Interna (Before Save) + etichetta "Buffer Project" | Eseguito |
| 10 | `verifica_tempi_esterne.py` + `dati_tt_esterne_t09.json` | Sola lettura: fasi esterne a sistema vs TT del ciclo T09 (129 fasi) | Eseguito |
| 11 | `tempi_esterne_tt.py` + `dati_tt_minuti_finale.json` | Durata fasi esterne = TT (T09 22/09 prevale, poi T08 v5), esclusi P4000/P5000. Backup valori in `backup_sessione22/` | Eseguito (152/152) |
| 12 | `scheduling_wo_t09.py` | Scheduling WO T09 in bozza: indietro dalla consegna − buffer, poi avanti (2A); scrive planned_start_date | Eseguito (348 WO) |
| 13 | `expediting_eventi.py` | Expediting a eventi: Data promessa, Uscita/Rientro da Inizia/Completa (sola lettura), chiusura sezione, Server Script rivisti, riallineamento JC esterne | Eseguito |
