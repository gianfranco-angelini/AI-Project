# CONTESTO PROGRESSIVO ERPNext — Remazel Engineering

> Fonte di verità normale: Project Cowork. Questo file è stato ricostruito il
> 2026-09-26 a partire dal contenuto della skill `anthropic-skills:erpnext-remazel`
> perché il repository `gianfranco-angelini/AI-Project` è risultato vuoto
> all'avvio della sessione. Nessuno storico sessioni precedenti era disponibile
> in questo repo: se esiste una versione più aggiornata nel Project Cowork,
> quella prevale.

## SESSIONE 1 — Ricostruzione contesto da skill (2026-09-26)

### Ambiente
- Server: cs-erp01 (Ubuntu), utente `frappe-user`, bench in `/home/frappe-user/frappe-bench`
- Sito: `combustionerp.remazel.com` / `site1.local`
- Versione: ERPNext v16 / Frappe v16
- Ordine di test: SAL-ORD-2026-00001
- WIP Warehouse: "Goods In Transit - Rema"

### Comportamenti noti ERPNext v16 già documentati (vedi skill per dettaglio completo)
- Sub-assembly / Production Plan: generazione WO solo da "Sub Assembly Items" →
  "Get Sub Assembly Items" → "Make Work Orders" (campo "Include Exploded Items"
  non esiste più in v16)
- WO in Draft invece di Not Started: causa `wip_warehouse` vuoto al submit →
  fix con Server Script Before Submit
- Submit massivo WO Draft: Server Script API `submit_all_draft_wo` + Client
  Script su Work Order List (richiede `server_script_enabled true` + restart)
- Amend da bench console: pattern `cancel → commit → copy_doc → insert →
  commit separato → submit → commit`
- DuplicateEntryError dopo rollback parziale: recuperare con `frappe.get_doc()`
  invece di ricreare
- CapacityError al submit WO: ignorabile finché le Workstation non hanno
  `total_working_hours` configurate
- UpdateAfterSubmitError: verificare sempre `docstatus` prima di modifiche
- Struttura BOM T08-0100: materia prima = codici `001-`, resto deve avere
  `bom_no` popolato su `tabBOM Item`

### Fix ancora aperti (pre go-live)
- [ ] Codici SAP definitivi C0900/C0901
- [ ] BOM per P2400/P2401/P2402/P2403
- [ ] Operatori reali in HR > Employee
- [ ] Prezzi reali PO (ora EUR 1 placeholder)
- [ ] Politica Quality Inspection
- [ ] `allow_negative_stock=0`
- [ ] SMTP
- [ ] Workspace Simone Sacchi
- [ ] Strategia go-live (pulizia dati test vs nuovo sito)
- [ ] Tempi standard BOM Operations (da Simone: min/pezzo per Saldatura,
      Molatura, Lavorazioni Meccaniche, Montaggio, Controllo Qualità,
      Lavorazione Esterna)

## 🎯 TASK PROSSIMA SESSIONE

- Confermare con Gian se esiste un `CONTESTO_PROGRESSIVO_ERPNext.md` più
  aggiornato nel Project Cowork e, in caso, allinearlo/sostituirlo a questo
- Recuperare da Simone i tempi standard BOM Operations
- Procedere con i fix aperti pre go-live secondo priorità indicata da Gian
