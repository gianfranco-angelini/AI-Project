# MEMORIA_SESSIONE — Sessione 27 (registrata come "Sessione 20" sul branch awesome-planck) — 20 ottobre 2026

> Rinumerata 27 in sessione 28 (23/10): vedi la nota di riallineamento in `CONTESTO_PROGRESSIVO_ERPNext.md`. Le 50 Job Card del 09/10 sono l'allineamento della sessione 24 e si tengono.

Sessione in **Claude Code cloud** (claude.ai/code), repo GitHub `gianfranco-angelini/AI-Project`,
branch `claude/awesome-planck-8vao9v`. Intervento su ERPNext: comandi eseguiti da Gian in SSH su
`cs-erp01`, come `frappe-user`. Tema: verifica del T09 a sistema ed eliminazione di WO e Job Card
del T08.

---

## Ambiente

| Elemento | Stato |
|---|---|
| Server | `cs-erp01`, utente `frappe-user`, bench `/home/frappe-user/frappe-bench` |
| Sito | `site1.local` (`combustionerp.remazel.com`), ERPNext / Frappe v16, Python 3.14 nell'env |
| Console | `bench --site site1.local console` (IPython), cartella di lavoro `frappe-bench/sites` |
| Backup | `bench --site site1.local backup --with-files` eseguito il 20/10 prima dell'eliminazione |
| T08-0100 | PROJ-0001, SAL-ORD-2026-00001 (`T08-0100-A0001` × 1, consegna 18/12/2026) |
| T09-0100 | PROJ-0002, SAL-ORD-2026-00002 (`T09-0100-A0001` × 100 su 6 righe) |
| Copia principale della memoria | `12_Memorie` in OneDrive: questo file e il contesto vanno copiati lì |

---

## Problemi risolti questa sessione

### 1. Verifica del T09 a sistema
Gian ha segnalato di aver inserito Job e Work Order del T09 e del T08. Verificato con
`verifica_t08_t09.py`:
- **PROJ-0002**: Open, buffer 5 gg, fine 30/11/2027, deadline interna 25/11/2027
- **SAL-ORD-2026-00002**: 6 righe `T09-0100-A0001`, 10+20+20+20+20+10 = 100 pezzi, date 26/02,
  30/04, 30/06, 31/08, 29/10, 30/11/2027
- **348 WO** (31 In Process, 317 Not Started), 58 per consegna; **3.330 Job Card** (3.280 Open,
  50 Completed); 42 Task
- 43 codici T08 riusati con WO propri su PROJ-0002 (7 WO a codice, 14 per P1600)
- 0 WO senza project o Sales Order, 0 WO in Draft
- La prima query sui Sales Order non trovava nulla perché filtrava su `T08-0100` / `T09-0100`:
  gli articoli reali sono `T08-0100-A0001` / `T09-0100-A0001`

### 2. Anomalie T09 (aperte)
- **`po_no` ancora a segnaposto**: `99-99999` (SO-00001), `99-99998` (SO-00002). Il "Job" della
  segnalazione di Gian non riguardava il numero di commessa. Proposti 24-19006 / 26-19008
- **Consegne 1 e 2 in ritardo**: MFG-WO-2026-01210 fine 26/03/2027 contro una consegna al 26/02
  (+28 gg); MFG-WO-2026-01268 fine 08/06/2027 contro una consegna al 30/04 (+39 gg). Le altre 4
  chiudono da 7 a 11 gg prima. La deadline interna del Project non li rileva perché guarda solo
  l'ultima consegna
- **50 Job Card Completed** su WO pianificati fino al 2027: create il 02/10 e chiuse il 09/10 tra
  le 18:48:00 e le 18:48:04, sempre da `Administrator`. Sono le fasi 1 (Lavorazione Esterna) e 2
  (Controllo Qualità) di 25 WO, con 2 time log ciascuna e `is_subcontracted = 0`. È un'operazione
  massiva, non lavoro reale

### 3. Eliminazione T08 (eseguita, 0 errori)
- Inventario a sola lettura (`inventario_t08.py`): T08 isolato dal T09, nessun Link condiviso
- Eliminati: 557 Job Card (Draft, 0 time log), `MAT-MR-2026-00002` e `00003` (Draft, nulla a valle),
  58 WO (cancel + delete, 0 Stock Entry), Production Plan `MFG-PP-2026-00001` (cancel + delete)
- Tenuti: BOM T08, articoli, Workstation, script, 21 Task PROJ-0001, SAL-ORD-2026-00001, PROJ-0001
- Verifica: T08 a zero; T09 prima e dopo = (348 WO, 3.330 JC, 42 Task), **invariato**

### 4. Inciampi in console (risolti)
- `FileNotFoundError` su `exec(open("verifica_t08_t09.py"))`: la console è in `frappe-bench/sites`.
  Usare il percorso assoluto
- `NameError: name 'conta' is not defined`: con `exec()` nella console di bench le funzioni non si
  vedono tra loro. Usare `exec(open(...).read(), globals())`
- `SyntaxError` su `wc -l` / `ls`: blocco shell incollato nella console Python. Uscire con `exit()`

---

## Script e Query usati

Tutti in `/home/frappe-user/frappe-bench`, creati con heredoc `cat > file <<'EOF'` dalla shell,
controllati con `wc -l` e `python3 -m py_compile`, eseguiti in console con:

```python
exec(open("/home/frappe-user/frappe-bench/<script>.py").read(), globals())
```

| Script | Righe | Tipo | Contenuto |
|---|---|---|---|
| `verifica_t08_t09.py` | 82 | sola lettura | Sales Order/`po_no`, Project, WO per project e stato, WO orfani, codici T08 su più project, JC per project, WO in Draft |
| `inventario_t08.py` | 113 | sola lettura | WO/JC T08, Production Plan, scansione di tutti i Link verso Work Order / Job Card / Project / Sales Order / Production Plan, Stock Entry, incroci con T09, Task |
| `elimina_t08.py` | — | scrittura | Controlli di sicurezza (Stock Entry, Stock Reservation Entry, JC e WO di altri project, MR non Draft o con PO), poi JC → MR → WO cancel/delete (3 passate) → PP cancel/delete, verifica finale e confronto T09 prima/dopo. `DRY_RUN = True` di default |

Query singole in console:

```python
# Sales Order e righe
frappe.db.sql("select name, po_no, project, docstatus, status, delivery_date from `tabSales Order` order by name", as_dict=True)
frappe.db.sql("select parent, idx, item_code, qty, delivery_date from `tabSales Order Item` order by parent, idx", as_dict=True)

# WO dei livelli T09 con date pianificate e date di consegna
frappe.db.sql("select name, production_item, qty, status, planned_start_date, planned_end_date, expected_delivery_date from `tabWork Order` where project='PROJ-0002' and production_item like 'T09-%%' order by planned_end_date", as_dict=True)

# Job Card Completed T09: dettaglio e time log
frappe.db.sql("select name, work_order, operation, sequence_id, for_quantity, total_completed_qty, total_time_in_mins, is_subcontracted, owner, modified_by, creation, modified from `tabJob Card` where project='PROJ-0002' and status='Completed' order by creation limit 10", as_dict=True)
frappe.db.sql("select count(*) n, count(distinct tl.parent) jc from `tabJob Card Time Log` tl join `tabJob Card` jc on jc.name=tl.parent where jc.project='PROJ-0002' and jc.status='Completed'", as_dict=True)

# Material Request del PP T08 e documenti a valle
frappe.db.sql("select distinct mr.name, mr.docstatus, mr.status, mr.material_request_type from `tabMaterial Request` mr join `tabMaterial Request Item` mri on mri.parent=mr.name where mri.production_plan='MFG-PP-2026-00001'", as_dict=True)
```

Preparate ma **non ancora eseguite**:

```python
# Stock Entry sui WO T09 (prima di decidere sulle 50 JC Completed)
frappe.db.sql("select se.stock_entry_type, se.docstatus, count(*) n, min(se.creation) primo, max(se.creation) ultimo from `tabStock Entry` se join `tabWork Order` wo on wo.name=se.work_order where wo.project='PROJ-0002' group by se.stock_entry_type, se.docstatus", as_dict=True)

# Time log di esempio
frappe.db.sql("select tl.parent, tl.employee, tl.from_time, tl.to_time, tl.time_in_mins, tl.completed_qty from `tabJob Card Time Log` tl where tl.parent in ('PO-JOB05551','PO-JOB05552') order by tl.parent, tl.idx", as_dict=True)
```

Riportare `elimina_t08.py` in modalità prova (se non già fatto):

```bash
sed -i 's/^DRY_RUN = False$/DRY_RUN = True/' elimina_t08.py && grep -n "^DRY_RUN" elimina_t08.py
```

---

## Fix ancora aperti

- [ ] Confermare e scrivere `po_no` reali: 24-19006 (SO-00001), 26-19008 (SO-00002)
- [ ] 50 Job Card T09 Completed del 09/10: origine, Stock Entry, tenere o annullare
- [ ] Consegne 1 e 2 T09 in ritardo (+28, +39 gg): comunicazione a Simone, buffer per consegna
- [ ] Task PROJ-0001, SAL-ORD-2026-00001, PROJ-0001: tenere o eliminare
- [ ] `elimina_t08.py` riportato a `DRY_RUN = True`: da confermare
- [ ] Registrare le attività 28/09-19/10 non documentate (riunione 29/09, creazione T09, chiusura JC)
- [ ] Copiare questo file e `CONTESTO_PROGRESSIVO_ERPNext.md` in `12_Memorie` su OneDrive

---

## Task prossima sessione

1. Decisioni della Priorità 0 del contesto progressivo (`po_no`, 50 JC, ritardi, oggetti T08 rimasti)
2. Pilota conto lavoro C1 su una Job Card esterna **T09** (il T08 non ha più WO)
3. Rendicontazione tempi su una parte del processo T09
4. Guida Produzione → B4 con i numeri nuovi (T09: 348 WO, 3.330 Job Card)
