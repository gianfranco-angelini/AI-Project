# 📋 CONTESTO PROGRESSIVO — ERPNext v16 @ Remazel Engineering

> **Questo documento è la memoria persistente del progetto. Viene aggiornato a ogni sessione aggiungendo i progressi in fondo. Non rimuovere mai le sezioni precedenti.**
> **Versione consolidata**: unisce il contesto storico (sessioni 1-15) con gli aggiornamenti/correzioni successivi. Dove i due documenti erano in conflitto, vince l'informazione più recente (indicato inline).

---

## ⚠️ NOTA DI SCALATA
Chi riceve questo contesto deve, **a fine sessione**, aggiornarlo con i progressi fatti e riscriverlo nel Project Cowork "Ciclo produzione Remazel Combustion". La catena non si interrompe. Il blocco aggiornato va anche restituito all'utente da incollare nella chat successiva come primo messaggio, nel caso il Project non sia ancora caricato.

---

## PROGETTO — INQUADRAMENTO GENERALE

- Cliente: **Remazel Engineering S.p.A.**, divisione **BU Combustion**
- Fornitore/implementatore: **Start I.T. S.r.l.** — Gian è il lead implementor
- Progetto: **M.E.S. Remazel** (Manufacturing Execution System) su ERPNext v16
- Go-live target: **30 settembre 2026**
- Contatto cliente primario: **Simone** (Responsabile Produzione)
- Altri utenti ERPNext: Fabio Picco, Omar Ferrari, Sergey Mylnikov
- Marco Lasorella: in copia email, nessun account ERPNext
- Commesse centrali:
  - **T08-0100** (Job 24-19006, ASSY LINER COMPLETE) — pilota, già a regime
  - **T09-0100** (Job 26-19008, Liner FR7EA DLN 24k) — struttura identica a T08

⚠️ **CORREZIONE IMPORTANTE**: il nome prodotto corretto è **"M.E.S. Remazel"**. Le varianti "E.M.S. Remazel" e "M.S.E." sono **errori confermati** — non usarle più in nessun documento, anche se compaiono nelle sessioni storiche sotto riportate.

---

## AMBIENTE

| Parametro | Valore |
|---|---|
| Server | cs-erp01 (Ubuntu) |
| Sito Frappe | combustionerp.remazel.com / site1.local |
| Utente server | frappe-user |
| Directory | /home/frappe-user/frappe-bench |
| Versione ERPNext | v16 |
| Host SSH | combustionerp.remazel.com (nome interno macchina: cs-erp01) |
| Bench CLI | 5.29.1 |
| Rete | uscita verso internet sì, raggiungibile dall'esterno no (DNS interno) |
| SAP Business One | 10.5, raggiungibile da cs-erp01 (Service Layer, porta 50000) |

~~⚠️ Il sito risponde solo in HTTP~~ → **Superato in sessione 18**: HTTPS attivo su `https://combustionerp.remazel.com` (certificato wildcard `*.remazel.com`, redirect automatico da 80).
File pubblici scaricabili da browser scrivendoli in `frappe.get_site_path("public","files", <nome>)` → URL `https://combustionerp.remazel.com/files/<nome>`. Cancellarli dopo il download (non richiedono autenticazione).

---

## PREFERENZE OPERATIVE

- Risposte dirette e concise, senza preamboli
- Esecuzione passo-passo con verifica prima di ogni modifica
- Riscrivi sempre file completi, mai snippet parziali
- Comunico in italiano — Non ripetere passi già confermati
- **Metodo di lavoro**: codice incollato direttamente in bench console, NO file da scaricare/SCP → **aggiornato in sessione 18**: per gli script lunghi, file compresso gzip+base64 creato con un solo `echo` in bash ed eseguito con `exec(open(...).read())`
- ⚠️ Specificare sempre **dove** va incollato il codice (bash vs `bench --site site1.local console`)
- Conferma prima di agire: concordare struttura/outline prima di generare documenti
- Tono comunicazioni verso il cliente: soft-ma-fermo, riferimenti generici di ruolo (non nomi), framing sempre di rischio (dato mancante), mai di lamentela
- Numeri e dati nelle presentazioni: significativi e difendibili, mai tecnicamente corretti ma fuorvianti
- Disciplina versioning: ogni variante di documento deve avere identificativo di versione nel nome file (`_B1`, `_B2`, `_v4`...); mai sovrascrivere senza incrementare

---

## 📐 FORMATO DOCUMENTI WORD

⚠️ **Lo standard completo NON sta più in questo file**: vive nella skill `docx-remazel`, che è
l'unica fonte di verità e va invocata (`/docx-remazel`) ogni volta che si crea o si modifica un
`.docx` di progetto. Qui restano solo i riferimenti essenziali e le correzioni storiche, perché
duplicare la specifica in due posti ha già causato disallineamenti.

**Revisione dello standard al 15/09/2026**: `12_Memorie/SKILL_docx-remazel_REVISIONE.md` nella
struttura di progetto. Da salvare nella skill dalla card di revisione — le copie su disco sono
cache di sola lettura e non persistono.

### Regola che vince su tutte
**Il file fisico caricato batte la specifica scritta.** Se Gian carica un documento e lo indica
come riferimento, quel file vince su qualunque valore scritto altrove. È nata da un caso reale:
la skill prescriveva il footer a 3 celle mentre il file di riferimento usava il paragrafo
singolo. Ha vinto il file.

**Documento di riferimento**: `Analisi_Obiettivi_BU_Combustion_B2.docx` (senza suffisso
`_Remazel`), nella versione con header 2400/3000/3660, footer a paragrafo singolo, tabella info
2384/6676, titolo 20pt.

### Valori chiave (dettaglio completo nella skill)
| Elemento | Valore |
|---|---|
| Titolo copertina / sottotitolo | 20pt bold centrato nero / 12pt |
| Heading 1 / Heading 2 | 14pt / 13pt, colore `2E74B5` |
| Tabelle a piena larghezza | **9060 DXA**, sempre |
| Tabella info copertina | **2384 / 6676 DXA**, intestazione `Campo` / `Valore` |
| Header di pagina | **2400 / 3000 / 3660 DXA** |
| Footer | **paragrafo singolo** centrato, `pBdr top space=11`, titolo incluso, em-dash |
| Indice | campo `TOC \o "1-3"`, voci popolate, **su pagina propria** |
| Stili TOC1 / TOC2 | `after=100` / `after=100` + `ind left=220` |
| Campo Sistema | **`M.E.S. Remazel`** — mai E.M.S. né M.S.E. |
| Redatto da / Destinatario | `Start I.T. S.r.l.` / riferimento d'ufficio, mai nomi propri |
| Pagina | A4 11906×16838, margini 1417/1134, header/footer 720 |
| Lingua | it-IT su run, `docDefaults`, `themeFontLang`, separatori |

### Naming
`{Tipo}_{Oggetto}_{Commessa}_{Versione}.docx` — **senza prefisso `ERPNext_`**, **senza suffisso
`_Remazel`**, commessa **senza trattino** (`T080100`). Il campo `Documento` della tabella info
deve coincidere col nome file reale.

### Flusso di lavoro obbligatorio
```
unzip → modifica XML diretta → rezip → validate.py → conversione PDF di verifica
```
Mai passare da LibreOffice per aggiornare il TOC: converte i bordi da livello-tabella a
livello-cella e sporca l'XML. La validazione è obbligatoria, la resa PDF da sola non intercetta
gli errori di schema.

```bash
python3 /mnt/skills/public/docx/scripts/office/validate.py file.docx -v
```


---

## SESSIONE 1-12
(vedi blocco originale — omesso per brevità, non eliminare nelle prossime sessioni)

---

## SESSIONE 13 — Fix Submit All Draft WO + Start All WO (28/08/2026)

### Stato finale WO commessa T08-0100
- **58 WO totali** — tutti `docstatus=1`, status = **"In Process"**
- Capacity planning **disabilitato** (sessione 13): `disable_capacity_planning=1`
- Guida `ERPNext_Guida_Test_Pianificazione_B2.docx` consegnata

---

## SESSIONE 14 — Riabilitazione Capacity Planning + fix CapacityError (28/08/2026)

### Obiettivo
Riabilitare `disable_capacity_planning=0` per avere Job Card con date pianificate per-operazione. Test completo del workflow Production Plan → WO + Submit All Draft → Start All.

### Fix applicati (definitivi in DB)

**1. Controllo Qualità — time_in_mins**
- Problema: valori enormi (7200–24000 min/pezzo) causavano CapacityError su workstation "Controllo Qualità"
- Fix: `UPDATE tabBOM Operation SET time_in_mins=5 WHERE operation='Controllo Qualità'`
- Motivazione: QC è ispezione attiva 5 min/pezzo; i valori originali rappresentavano lead time errati
- ⚠️ **Superato in sessione 15**: sostituito con i tempi reali del ciclo v5 (0,2–50 min a seconda della fase)

**2. Lavorazione Esterna — workstation e time_in_mins**
- Problema: workstation "Lavorazione Esterna" aveva Holiday List "Festivi Italia 2026-2027" + orari limitati; time_in_mins molto alti (fino a 9000 min) causavano CapacityError
- Fix workstation: rimossa Holiday List, impostato orario 00:00-23:59 (24h, no festivi)
- Fix time_in_mins: `UPDATE tabBOM Operation SET time_in_mins=60 WHERE operation='Lavorazione Esterna'`
- Motivazione: Lavorazione Esterna è lavoro esterno (fornitore); il tempo effettivo è irrilevante per capacity planning; tracciamento reale via date apertura/chiusura Job Card

**3. Lock DB durante eliminazione WO**
- Problema: `frappe.delete_doc()` dava `QueryTimeoutError (1205 Lock wait timeout)`
- Soluzione: `bench restart` + DELETE SQL diretto invece di `delete_doc()`

**4. Commit non persistiti**
- Problema: UPDATE a `tabBOM Operation` eseguiti durante sessione con WO in submit non persistivano (rollback automatico)
- Soluzione: verificare sempre con SELECT dopo ogni UPDATE; riapplicare dopo bench restart se necessario

### Server Script creati/aggiornati

**"Start_All_WO"** (api_method: `start_all_wo`) — creato in sessione 14
```python
wos = frappe.get_all("Work Order", filters={"docstatus": 1, "status": "Not Started"}, pluck="name")
total = len(wos)
started = 0
errors = []
for wo_name in wos:
    try:
        frappe.db.set_value("Work Order", wo_name, "status", "In Process")
        frappe.db.commit()
        started += 1
    except Exception as e:
        errors.append({"name": wo_name, "error": str(e)})
frappe.response["message"] = {"started": started, "total": total, "errors": errors}
```
⚠️ Il Client Script chiama `method: 'start_all_wo'` (minuscolo, con i due punti visibili nella UI sono solo label).

### Configurazione Workstation finale

| Workstation | Holiday List | Orari | Note |
|---|---|---|---|
| Saldatura | Festivi Italia 2026-2027 | 07:00-13:00 / 14:00-17:00 | ✅ |
| Molatura | Festivi Italia 2026-2027 | 07:00-13:00 / 14:00-17:00 | ✅ |
| Lavorazioni Meccaniche | Festivi Italia 2026-2027 | 07:00-13:00 / 14:00-17:00 | ✅ |
| Montaggio | Festivi Italia 2026-2027 | 07:00-13:00 / 14:00-17:00 | ✅ |
| Controllo Qualità | Festivi Italia 2026-2027 | 07:00-13:00 / 14:00-17:00 | ✅ |
| Lavorazione Esterna | **Nessuna** | **00:00-23:59** | ✅ Intentional: no capacity limit |

### Stato finale sessione 14
- ✅ `disable_capacity_planning = 0` (capacity planning attivo)
- ✅ 58 WO creati, submitted, "In Process"
- ✅ Job Card generate con **Expected Start/End Date** per ogni operazione
- ✅ Esempio verificato: Job Card "Controllo Qualità" → 31/08/2026 07:00 → 07:05 (5 min ✅)
- ✅ Workflow completo funzionante: Production Plan → Work Order + → Submit All Draft → Start All

### Colonne Production Plan per reset
- `tabProduction Plan Item`: `ordered_qty`, `produced_qty`, `pending_qty`
- `tabProduction Plan Sub Assembly Item`: `ordered_qty`, `wo_produced_qty`

### Procedura reset completo (per future esecuzioni)
```python
# 1. bench restart  (fuori dalla console, per liberare lock DB)
# 2. In console:
frappe.db.sql("DELETE FROM `tabJob Card Time Log` WHERE 1=1")
frappe.db.sql("DELETE FROM `tabJob Card` WHERE 1=1")
frappe.db.sql("DELETE FROM `tabWork Order Item` WHERE 1=1")
frappe.db.sql("DELETE FROM `tabWork Order Operation` WHERE 1=1")
frappe.db.sql("DELETE FROM `tabWork Order` WHERE 1=1")
frappe.db.commit()
frappe.db.sql("UPDATE `tabProduction Plan Item` SET ordered_qty=0, produced_qty=0, pending_qty=0")
frappe.db.sql("UPDATE `tabProduction Plan Sub Assembly Item` SET ordered_qty=0, wo_produced_qty=0")
frappe.db.commit()
# 3. UI: Production Plan → Work Order + → Submit All Draft → Start All
```

---

## SESSIONE 15 — Ciclo v5 di Simone: analisi e diff contro ERPNext (30/08/2026)

### Input ricevuto
File **`T080100 Ciclo e fasi 5.xlsx`** da Simone (4 fogli: `Ciclo e fasi`, `Tabelle`, `Fasi critiche`, `Matricole + avanzamento RX`).

⚠️ La versione precedente (`T080100 Ciclo e fasi 4.xlsx`) non era disponibile e le sessioni 1-12 non ne registrano il nome. Il confronto è stato fatto **contro l'export reale di ERPNext**, che è comunque il dato che serve.

### Struttura del ciclo v5
- **61 articoli distinti** su 7 livelli (L0→L6), **17 materie prime** (codici `001-*`), **543 operazioni**
- Colonne chiave foglio `Ciclo e fasi`: A–G = livello di indentazione · H = n. fase (10, 20, …) · I = codice fase RZL · O = Attività/set · P = Persone/attività · Q = Tempo/item [H] · R = attrezzaggio · S = Tempo/set · T = descrizione · Z = fornitore
- Ore per set da 10 liner: **1.304 h interne** vs **19.580 h esterne/attesa** → il ciclo è per il ~94% fuori casa

### Famiglie di fase (suffisso codice RZL) — 15 contro le 6 Workstation ERPNext
| Sigla | Significato | Workstation proposta |
|---|---|---|
| MT | Montaggio / raddrizzamento / marcatura | Montaggio |
| SA | Saldatura | Saldatura |
| ML | Molatura / lavaggio / pulizia | Molatura |
| QC | Controllo dimensionale / databook | Controllo Qualità |
| VT | Visual Test | Controllo Qualità |
| PT | Liquidi penetranti | Controllo Qualità |
| MX | Definizione mappe radiografiche + marcatura | Controllo Qualità |
| VX | Valutazione lastre RX | Controllo Qualità |
| TE | Flussaggio ad aria | Controllo Qualità |
| ST | Formatura / calibratura CNC | Lavorazioni Meccaniche |
| LA | Lavorazione meccanica / laser / stampaggio | Lavorazione Esterna |
| LT | Taglio sviluppo / calandratura | Lavorazione Esterna |
| TT | Trattamento termico / brasatura / coating TBC-HFC | Lavorazione Esterna |
| RX | Radiografia | Lavorazione Esterna |
| FE | Microfusione / SLM | Lavorazione Esterna |

**Criterio oggettivo interno/esterno**: colonna P "Persone/attività" valorizzata = lavoro interno (446 fasi); vuota = fornitore o attesa (141 fasi). Tutte le 44 fasi `LA` sono esterne → l'unica lavorazione a macchina interna sono le 25 fasi `ST`.

### Export ERPNext per il confronto
Script in `Script_Console_Sessione15.md` → scrive `public/files/export_bom_T080100.json`.
Risultato: **57 BOM attive, 95 righe componenti, 578 BOM Operation, 74 item, 6 Operation, 6 Workstation, 58 WO**.

### RISULTATO DEL DIFF v5 vs ERPNext

| Area | v5 | ERPNext | Delta |
|---|---|---|---|
| Articoli con BOM | 61 | 57 | **−4** |
| Operazioni | 543 | 578 | **+35** |
| Descrizioni operazione distinte | 543 | 6 | — |
| Famiglie di fase / Workstation | 15 | 6 | −9 |

**Dettaglio operazioni** (allineamento LCS per famiglia): 291 allineate · 217 solo tempo da correggere · 70 presenti in ERPNext senza corrispondenza nel v5 · 35 da aggiungere · 29 righe su BOM inesistenti.

### ✅ CHIARITO DA GIAN — il QC iniziale NON è un errore
Dove il ciclo v5 non indica un QC, si intende che **il materiale esce e rientra**: il controllo è al rientro.
Il "Controllo Qualità" a idx 1 presente in ERPNext è quindi il **controllo in accettazione della materia prima**, ed è corretto.

Verifica eseguita sui dati:
- 41 articoli v5 partono da materia prima; **34 su 34** di quelli con BOM esistente hanno il QC come primo step
- **20 assiemi** (che ricevono semilavorati già controllati) **non** hanno il QC iniziale — corretto
- nel v5, 135 dei 183 "rientri di materiale" hanno già un controllo esplicito a valle; i restanti sono le righe materia prima, dove il QC arriva dopo la lavorazione esterna

→ **Le 35 operazioni "in più" di ERPNext sono quelle giuste.** Regola da mantenere e da estendere agli articoli mancanti.

### Anomalie da chiudere

**A. BOM mancanti (bloccante)**
`T08-0100-P2400` (FRAME WHEEL *WELDED*), `P2401` (OUTER RING), `P2402` (INNER RING), `P2403` (RADIAL PLATE, 6 per P2400). P2400 va anche aggiunto come componente di `A2000`.

**B. P2400 vs P2404 — alternative, non componenti**
Sotto ASSY CAP il v5 elenca sia P2400 *WELDED* (5 fasi) sia P2404 *CASTED* (microfuso), entrambi qty 1. Sono due tecnologie alternative: decidere con Simone quale entra in BOM A2000, l'altra va gestita come BOM alternativa.
→ **Risolto in sessione 15 parte 2**: v. sotto (solo P2404 in BOM ufficiale).

**C. Microfusi — materiale sbagliato e QC accettazione mancante**
`P2112`, `P2302`, `P2305`, `P2404` sono gli unici 4 articoli il cui materiale nel v5 non ha codice `001-*` (`AMS 5390 Hastelloy-X Cast`, `AMS 5390 Cast/SLM`, `AMS 2175 FSX 414 Cast`). In ERPNext è stata assegnata d'ufficio una lamiera (`001-0023-C0593`, `001-0023-C0849`) e — unica eccezione su tutta la commessa — **manca il QC in accettazione**: il primo step è "Lavorazione Esterna". Servono i codici articolo delle fusioni; da lì derivano sia le righe BOM corrette sia i 4 QC mancanti.
→ **Ancora aperto**: i codici articolo reali dei microfusi restano da fornire (v. task in sospeso). Nel frattempo risolto con soluzione provvisoria F000 (v. sessione 15 parte 2).

**D. BOM Operation anonime (il problema più grosso per l'operatore)**
In ERPNext `description` = nome della workstation. Nessun codice fase RZL, nessun riferimento alla saldatura W. In Job Card l'operatore vede 5 righe identiche "Controllo Qualità" senza sapere cosa controllare. Il v5 fornisce descrizione e codice fase per tutte le 543 operazioni → **ricostruire le BOM Operation dal v5 anziché patcharle**. Test avviato su `BOM-T08-0100-P5000-001` (vedi `Script_Console_Sessione15.md`).
→ **Completato in sessione 15 parte 2** (v. Step 5).

**E. Conversione quantità — trappola**
La colonna "Attività/set" del v5 è la **qty assoluta nel set da 10 liner**, NON la qty rispetto al padre. Es. `P2110`=60 sotto `P2109`=60 → **1** per padre, non 6. La qty ERPNext = qty_figlio / qty_padre.

**F. Lead time fittizi**
`P2302`, `P2305`, `P2112`, `P2404` hanno 1000 h/set sulla fase FE: è lead time del microfusore, non tempo lavorazione. Non caricarlo come `time_in_mins` (→ 60.000 min → CapacityError). Mantenere i 60 min fissi su Lavorazione Esterna.

**G. Tempi QC reali ora disponibili**
Il fix di sessione 14 (`Controllo Qualità` = 5 min per tutti) può essere sostituito con i tempi reali del v5 (0,2–50 min a seconda della fase).
→ **Completato** in sessione 15 parte 2.

**H. Errori formali nel file di Simone**
- Codici fase duplicati: `T08-0100-A2000-20VT` su fase 60 e 110; `T08-0100-P2201-10RX` due volte
- 7 fasi senza Tempo/item: `A0001-20QC` (databook), `P1300-10QC`, `A2000-10QC`, `P2401-10QC`, `P2402-10QC`, `P2404-10FE`, `P2301-10VX`
- 9 righe `*CONFERMARE GRUPPO*`: marcature DOTPEEN su A0001 e A1000, W63 su A1000, W41 su A2000, rivestimento TBC Liner, HFC su P6000, materiale `001-0023-C0846`
  → **Chiarito da Simone**: sono **definitive**, la sigla `*CONFERMARE GRUPPO*` si ignora.
- `P2108` a 1 per liner ma le note di fase citano "n.6 anelli P2108" → verificare
  → **Risolto**: P2108 = 6 pz/liner (v. Step 1 sessione 15 parte 2).

**I. P1600 COOLING RING**
Usato in due punti dell'albero (1 in P1130, 6 in P1120) con lo stesso ciclo di 15 fasi. Item unico, BOM unica; le due qty vanno solo sulle righe BOM dei rispettivi padri.

### Fogli secondari del v5 — materiale sfruttabile
- **`Fasi critiche`**: 34 criticità classificate (errore fornitore / inefficienza di processo / lavorazione complessa) con fornitore e azione correttiva → base pronta per i **Quality Inspection Template**
- **`Matricole + avanzamento RX`**: 58 matricole RZL (S 5494→, M23004→) × 44 saldature (W1…W61) → candidato per **Serial No + Quality Inspection per saldatura**

### Deliverable prodotti (pacchetto `T080100_Documenti_30082026.zip`)
| File | Contenuto |
|---|---|
| `Analisi_Ciclo_T080100_v5.xlsx` | Albero BOM con qty già convertite per ERPNext · 587 operazioni mappate su workstation con `time_in_mins` proposto · 13 anomalie |
| `Diff_Ciclo_v5_vs_ERPNext.xlsx` | Sintesi / Articoli / Componenti / Operazioni dettaglio (642 righe di confronto riga per riga) |
| `Mail_Simone_Ciclo_v5.md` | Bozza mail con i 6 punti da chiarire |
| `Script_Console_Sessione15.md` | Script export ERPNext + test descrizione BOM Operation |
| `export_bom_T080100.json` | Export grezzo ERPNext del 28/08/2026 (fonte del diff) |

---

## SESSIONE 15 — PARTE 2: risposte di Simone ed esecuzione (01/09/2026)

### Risposte di Simone (mail 01/09/2026)
1. **Solo P2404** (microfuso). P2400/P2401/P2402/P2403 restano come variante tecnologica, **a sistema ma non collegata alla BOM ufficiale**. A2000 conteneva già solo P2404 → nessuna modifica.
2. **Rimuovere le materie prime dai microfusi**; la BOM parte dalla lavorazione esterna (creazione microfuso dal fornitore) seguita dal QC dimensionale. Vincolo ERPNext (BOM senza materiali non salvabile) risolto con **un unico codice grezzo di fusione `F000`**, materiale fittizio, proposto da Simone.
   ⚠️ **F000 è provvisorio**: restano da fornire i codici articolo reali dei componenti microfusi (P2112, P2302, P2305, P2404) — task ancora aperto.
3. **P2108 = 6 pz/liner** (era 1). Ciclo corretto da Simone il 30/08.
4. Rinumerazioni: `A2000-20VT` (fase 110) → **`A2000-30VT`**; `P2201` fase 50 → **`P2201-10MX`**.
5. Tempi mancanti: A0001-20QC = 2 gg **pieni** (→ 1080 min, 2 giornate da 9 h) · P1300-10QC = 10 min · A2000-10QC = 10 min · P2401-10QC = 10 min · P2402-10QC = 10 min · P2301-10VX = 5 min · **P2404-10FE = 100 gg = lead time fornitore, nessun impatto su capacità interna** (resta 60 min su Lavorazione Esterna).
6. Fasi `*CONFERMARE GRUPPO*` → **definitive**, la sigla si ignora.

### Interventi eseguiti in ERPNext

**Step 1 — P2108 da 1 a 6 pz**
`UPDATE tabBOM Item SET qty=6, stock_qty=6, qty_consumed_per_unit=6` su `BOM-T08-0100-P2100-002`, poi `doc.update_exploded_items(save=True)`.
⚠️ **Scoperta importante**: l'explosion caricata dallo script di import delle sessioni precedenti si fermava al primo livello (codici `T08-`), mentre ERPNext esplode fino alle materie prime. Rigenerata l'explosion di tutte le 57 BOM con 8 passate (l'albero ha 7 livelli) → converge a 125 righe. Trovate e cancellate **21 righe orfane** appartenenti a 5 BOM cancellate (`BOM-T08-0100-A0001`, `A1000`, `A2000`, `A3000`, `P1103` — senza suffisso numerico). Risultato finale: **104 righe, tutte materie prime**.

**Step 3 — Item F000 e microfusi**
Creato item `F000` "Grezzo di fusione" (Raw Materials, Nos, is_stock_item=1). Sostituita la lamiera con F000 in P2112, P2302, P2305, P2404; `stock_qty` portato da **0** (anomalia preesistente: non consumava nulla) a 1.
Verifica explosion: F000 = 1 sui quattro articoli, 2 su P2300, 6 su P2100, **9 su A2000 e A0001** (1 da P2404 + 2 da P2300 + 6 da P2100) → catena coerente.
⚠️ Al go-live serve un carico iniziale di F000 o resta necessario `allow_negative_stock=1` (task ancora aperto — v. anche nota sotto: `allow_negative_stock` va **azzerato prima del go-live**). → **Superato in sessione 18**: `allow_negative_stock` resta a 1 per scelta di Gian, nessun carico iniziale.

**Step 4 — Variante tecnologica P2400**
Creati item P2400/P2401/P2402/P2403 + le due materie prime mancanti `001-0023-C0835` (AMS 5536 Hastelloy-X sp.6mm) e `001-0023-C0838` (sp.12,7mm), che non esistevano a sistema. Create 4 BOM attive **non agganciate ad A2000**. Totale BOM attive: **61**.
⚠️ `BOM Operation` richiede `workstation_type` (non `workstation`): è il campo usato da tutte le BOM del progetto. Senza, l'insert fallisce con "Workstation or Workstation Type is mandatory".

**Job Card leggibili — risolto**
`Job Card` non ha il campo `wo_operation`, ma ha **`operation_id`** (Data) che contiene il `name` della riga `Work Order Operation`. Soluzione adottata:
- Custom Field su Job Card: `custom_descrizione_fase` (Data, read_only, in_list_view, insert_after `operation`)
- Server Script **"JobCard_Descrizione_Fase"** (DocType Event, Job Card, Before Insert):
```python
if doc.operation_id:
    desc = frappe.db.get_value('Work Order Operation', doc.operation_id, 'description')
    if desc:
        doc.custom_descrizione_fase = desc
```
La colonna "Descrizione Fase" compare nella lista Job Card.

**Step 5 — Ricostruzione delle 613 BOM Operation dal ciclo v5**
Backup preventivo delle 610 righe in `public/files/backup_bom_operations.json`. Poi, per ogni BOM attiva: DELETE delle operazioni + reinserimento dal v5 con `frappe.new_doc("BOM Operation")` + `db_insert()` (name via `frappe.generate_hash(length=10)`, docstatus=1, idx e sequence_id progressivi).
Risultato: **613 operazioni, 594 descrizioni distinte** (erano 6). Le 19 ripetizioni sono controlli in accettazione di articoli con lo stesso materiale.

Regole di generazione applicate:
| Regola | Valore |
|---|---|
| Descrizione | `<codice fase RZL> - <attività>` + ` (<fornitore>)` se il fornitore non è `*` |
| QC accettazione | prima operazione dove il v5 ha la riga materia prima — `Controllo accettazione materia prima <codice> - <materiale>`, 5 min |
| Tempo fasi interne | `Tempo/item` × 60, minimo 1 min |
| Tempo fasi esterne | 60 min fissi (il valore v5 è lead time fornitore) |
| Ordine | ordine delle righe del file, **non** il numero di fase (in P2402 la numerazione è errata: due fasi 30) |
| P1600 | usato in due punti dell'albero, preso solo il primo blocco di 15 fasi |
| **6 saldature in conto lavoro** | `P6000-10SA`, `P2201-10SA`, `P2109-10SA`, `P2111-10SA`, `P2105-10SA`, `P2107-10SA` (H.T. SRL / H.T.S. SRL) mappate su **Lavorazione Esterna**, non su Saldatura: non saturano il reparto interno |

Distribuzione finale: Controllo Qualità 305 · Lavorazione Esterna 134 · Saldatura 48 · Molatura 44 · Lavorazioni Meccaniche 23 · Montaggio 18.

**Step 6 — Reset e rigenerazione**
`bench restart` + procedura di reset di sessione 14, poi da UI: Production Plan → Work Order + → Submit All Draft → Start All.
Risultato: **58 WO "In Process"**, Job Card rigenerate con la descrizione parlante popolata automaticamente dal Server Script.

### Tecniche e trappole apprese
- **IPython e comprehension**: una generator expression dentro un `for` incollato in console dà `NameError: name 'f' is not defined`. Negli script da incollare usare solo cicli espliciti, niente comprehension annidate.
- **Distinguere sempre bash da console**: gli script Python vanno incollati dopo `bench --site site1.local console` (prompt `In [n]:`), mai al prompt `frappe-user@cs-erp01:~$`.
- **Script troppo lunghi per la chat**: comprimerli con `gzip` + `base64` dentro lo script stesso (613 operazioni = 57 KB JSON → 8 KB di blob), così restano autoconsistenti e non serve caricare file sul server.
- **Work Order creato via API**: `frappe.new_doc("Work Order")` non popola le operazioni. Chiamare esplicitamente `wo.set_work_order_operations()` prima di `insert()`, altrimenti nascono WO senza Job Card.
- **File pubblici**: caricabili da UI (menu → File, spunta "Private" deselezionata) → `sites/site1.local/public/files/`.
- ⚠️ **Console e snapshot MariaDB (REPEATABLE READ)**: dopo aver eseguito DELETE/UPDATE in console, la sessione tiene una transazione aperta e **non vede** i dati creati nel frattempo dal web server (es. i WO generati da UI): le query restituiscono 0. Rimedio: `frappe.db.commit()` prima di rileggere, oppure `frappe.db.close()` + `frappe.db.connect()`.

### Trappole aggiuntive bench console (raccolte, valide per tutte le sessioni successive)
- Console va sempre lanciata da `/home/frappe-user/frappe-bench`; `In [n]:` = Python, `$` = bash.
- ~~Blocchi lunghi richiedono `%cpaste` … `--`~~ (superato in sessione 18: la console attuale non lo richiede, `--` dà SyntaxError); le funzioni definite nello stesso blocco incollato non vedono le variabili del blocco — usare codice inline o passare tutto come parametro.
- `frappe.db.set_value(..., update_modified=False)` per aggiornare documenti submitted; mai `doc.save()` su record submitted.
- `create_job_card()` sovrascrive silenziosamente `planned_end_date` sul Work Order — ripristinare sempre le date WO dopo la chiamata.
- `set_operation_start_end_time(row, idx)` richiede due argomenti posizionali.
- `User.save()` elimina silenziosamente i ruoli aggiunti — usare INSERT SQL diretto in `tabHas Role` via `frappe.db.sql()`.
- `parent_page` del Workspace deve essere `''` (stringa vuota), non NULL, per la visibilità in sidebar.
- Dashboard Chart/Number Card con `Sum` su tabelle figlie falliscono in browser — usare il doctype `Job Card` con il campo `time_required`.
- Nei Query Report i segni `%` vanno raddoppiati (`%%`) per evitare l'interpretazione come placeholder di formato MySQLdb.

---

## SESSIONE 16 — Analisi obiettivi BU Combustion, T09-0100, chiusure amministrative (settimana dell'8-10/09/2026)

### Analisi 12 obiettivi di pianificazione produzione (da Simone)
- **11/12 realizzabili su ERPNext v16.** Unica eccezione: **Obiettivo 1e** (proposte di rischedulazione automatica), che richiede un vero motore APS. Riformulazione proposta: capacità di simulazione manuale, con valutazione di un APS di terze parti rimandata a **dopo il go-live**.
- Classificazione priorità: **alta** (1a, 1b, 2a, 2b) · **media** (1c, 1d, 2c, 3) · **bassa** (1e, 1f, 1g, 2d).
- **Obiettivo 3** (expediting subappalto esterno) copre ~94% del tempo ciclo → segnalato a Simone come possibile candidato a ripriorizzazione.
- Documento formale di risposta **`Analisi_Obiettivi_BU_Combustion_B3.docx`** prodotto e validato (OOXML pulito).

### T09-0100 — analisi BOM/ciclo
Completata l'analisi BOM/ciclo per T09-0100 (struttura identica a T08-0100). Output: **`Analisi_Ciclo_T090100_v1.xlsx`** (5 fogli). Anomalie residue da chiudere con Simone **prima** di procedere alla scrittura su ERPNext:
- residuo di codici fase copiati/incollati da T08
- codici fase duplicati
- marcature `*CONFERMARE GRUPPO*` non ancora risolte per questa commessa

### Chiusure amministrative
- **Item C0900/C0901**: **rimossi su istruzione di Simone del 7/09/2026** — non sono più un punto aperto, non vanno più citati come pendenti (superano la Priorità 3 della sessione 15, che chiedeva a cosa servissero).
- **Layout 22 postazioni**: ricevuto il 9/09/2026 — analisi rimandata alla settimana successiva, in coda.
- **Aggiornamento capacità reparti (postazioni CQ)**: in attesa di risposta di Simone.

---

## SESSIONE 17 — Consolidamento archivio documentale e riallineamento dei 13 documenti (14-15/09/2026)

Sessione interamente documentale. **Nessun intervento su ERPNext** (vedi sezione dedicata in
fondo per lo stato del fronte sistema, che resta invariato).

### Il problema di partenza
La documentazione era diventata ingestibile: **279 file `.docx`** sparsi su quattro alberi
(`$$$old`, `Downloads`, `New folder`, `Remazel-Combustion`), con versioni superate, varianti di
impaginazione e duplicati mescolati ai documenti correnti. Due cartelle diverse si chiamavano
entrambe `01_Documentazione`. Impossibile capire a occhio quale fosse la versione buona.

### Criterio di scelta della versione corrente
Per ogni famiglia documentale: **numero di versione più alto**; a parità di numero, la variante
**più conforme allo standard**, valutata in quest'ordine — tabella info `Campo/Valore` → campo
TOC presente → numero di Heading → formato A4.

⚠️ **Il nome file non basta.** Sono emersi:
- un documento salvato col nome di un'altra famiglia (il B3 degli Obiettivi si chiamava
  `Analisi_Prerequisiti_GoLive_BU_Combustion_B1.docx`)
- `Ciclo_Produttivo_T080100_v4.docx` del 27/08 con il **testo danneggiato**: un
  trova-e-sostituisci aveva rimosso la parola "ERPNext" da tutto il documento, lasciando frasi
  monche ("il ciclo produttivo di una commessa **in segue** questa sequenza"). Da scartare: la
  versione corrente è ricostruita dalla v3 e ha 11 occorrenze di "ERPNext" contro 0.
- versioni più recenti mai viste prima (`Piano_Operativo_Bozza6`, `Guida_Concettuale_v6`,
  `Audit_Rev2`, `Guida_Produzione_B3`, `Manuale_Operativo_v2`, `Manuale_Utente_B2`) che hanno
  superato quelle su cui si stava lavorando — con il risultato che due documenti riformattati
  sono stati buttati e rifatti sulla versione giusta.

### I 13 documenti correnti
Tutti allineati allo standard e validati (A4, tabelle 9060, indice su pagina propria, Sistema =
M.E.S. Remazel, lingua it-IT completa, zero errori di schema OOXML).

| Documento | Versione |
|---|---|
| `Analisi_Obiettivi_BU_Combustion_B3.docx` | Bozza 3 — 12/09/2026 |
| `Analisi_Prerequisiti_GoLive_BU_Combustion_B1.docx` | Bozza 1 — 11/09/2026 |
| `Ciclo_Produttivo_T080100_v4.docx` | Versione 4 |
| `Guida_Concettuale_T080100_v6.docx` | Versione 6 — 01/09/2026 |
| `Guida_Produzione_T080100_B3.docx` | Bozza 3 — 27/08/2026 |
| `Guida_Test_Pianificazione_T080100_B2.docx` | Bozza 2 — 28/08/2026 |
| `Manuale_Operativo_T080100_v2.docx` | Versione 2 — 27/08/2026 |
| `Manuale_Utente_Remazel_B2.docx` | Bozza 2 — 27/08/2026 |
| `Audit_T080100_Rev2.docx` | Rev. 2 — 27/08/2026 |
| `Piano_Operativo_T080100_Bozza6.docx` | Bozza 6 — 01/09/2026 |
| `Controlli_e_Sigle_T080100_v3.docx` | Versione 3 — 05/08/2026 |
| `Scenari_Conto_Lavoro_T080100_v1.docx` | Bozza 1 — 28/07/2026 |
| `Relazione_Lavorazioni_Esterne_T080100_B2.docx` | Bozza 2 — 28/07/2026 |

### Entità del lavoro per gruppi
- **Rifinitura** (Guida Test B2, Guida Concettuale v6): tabelle a 9060, `Sistema`, lingua
- **Gerarchia mancante** (Audit Rev2, Guida Produzione B3, Manuale Operativo v2, Manuale Utente
  B2): avevano il campo TOC ma **zero Heading**, quindi indice vuoto. Ricostruita la gerarchia
  riconoscendo i titoli da dimensione + pattern `N.` / `N.N` + soglia lunghezza
- **Ricostruzione da Letter** (Piano Operativo Bozza6, Controlli e Sigle v3, Scenari Conto
  Lavoro v1, Relazione Lavorazioni Esterne B2): formato Letter, nessun indice, tabella info
  "Voce/Contenuto", tabelle a 9744-9747

Il campo **Sistema era "E.M.S. Remazel" su 8 documenti**: è l'errore più ricorrente in assoluto.

### Struttura di progetto adottata
Replicata la struttura ufficiale Start I.T. già in uso:
```
Remazel-Combustion/
├── 00_Script_Progetto/            script ERPNext + utilità documentali
│   └── sequenza_carico_ERPNext/   import nell'ordine di caricamento
├── 01_Documentazione/             SOLO i 13 documenti correnti
│   ├── Dati/                      xlsx a supporto (BOM, cicli, riconciliazioni)
│   └── Email_Simone/
├── 03_Database/                   sql
├── 12_Memorie/                    memoria progetto + standard documentale
├── 99_Transito/  ·  _CESTINO/     materiale in transito / di altri progetti
└── (altre cartelle standard, vuote)
```
Versioni superate, varianti e duplicati **non stanno nella struttura di lavoro**: restano in
`remazel-comb.rar`, fotografia completa della vecchia cartella al 15/09/2026 (~200 MB).

### Strumenti prodotti (in `00_Script_Progetto`)
| Script | Funzione |
|---|---|
| `censimento_remazel.py` | Fotografa una cartella: per ogni documento dice se è conforme o cosa manca. Riconosce le versioni corrette per MD5. Non modifica nulla. |
| `consolida_remazel_v2.py` | Sceglie la versione corrente di ogni famiglia e archivia il resto |
| `confronta_docx.py` | Confronto testuale fra due documenti Word |

### ⚠️ Trappole tecniche apprese (dettaglio nella skill)

**Ordinamento XML OOXML** — modificare l'XML a mano rompe l'ordine richiesto dallo schema: il
file passa la validazione XML ma Word lo rifiuta con "contenuto non leggibile". Ordini critici:
in `pPr` il `pBdr` precede `spacing` e `jc`; in `rPr` `rFonts` è primo e `lang` è ultimo; in
`tblPr` `tblW` precede `tblBorders` che precede `tblLayout`; nei bordi l'ordine è
`top → left → bottom → right → insideH → insideV`. Conviene riordinare tutto automaticamente a
fine lavorazione, insieme alla rimozione dei figli duplicati.

**Riferimenti pendenti nei `.rels`** — è la causa vera del "Word ha rilevato contenuto
illeggibile": relazioni che puntano a parti assenti dal pacchetto (`stylesWithEffects.xml`,
`webSettings.xml`, `theme/theme1.xml`, `customXml/item1.xml`, `docProps/thumbnail.jpeg`). Vanno
rimosse da `word/_rels/document.xml.rels`, da `_rels/.rels` e dagli `<Override>` di
`[Content_Types].xml`.

**`tblGrid` segnaposto** — alcuni documenti hanno il grid con valori `100/200/300` mentre i
`tcW` sono corretti: ricostruire il grid **dai `tcW`**, non viceversa. Aggiungere un grid senza
rimuovere quello esistente produce due grid e un errore di schema.

**Header/footer multipli** — le varianti `first` (prima pagina) ed `even` (pagine pari) possono
essere **vuote**, lasciando copertina e pagine pari senza intestazione. Scrivere lo stesso
contenuto in tutti i file `header1/2/3.xml` e `footer1/2/3.xml`.

**Run vuoti** — `<w:r/>` senza figli falsano il conteggio della copertura lingua (sembrano run
non marcati). Vanno rimossi: sono innocui ma inutili.

**Indice su pagina propria** — serve un'interruzione esplicita dopo l'ultima voce, ma attenzione
a non sommarla a una già presente: due interruzioni generano una pagina bianca. Verificare
sempre sul PDF che pagina 3 contenga già del testo.

**`w:zoom` senza `w:percent`** in `settings.xml` è un errore di schema ricorrente.

### Correzione allo standard: il footer
La skill prescriveva il footer a **tabella di 3 celle**; il documento di riferimento caricato da
Gian usa il **paragrafo singolo** con il titolo incluso. Ha vinto il file. Da qui la regola
generale ora in testa alla skill: *il file fisico caricato batte la specifica scritta*.

Altre correzioni: campo TOC `\o "1-3"` (non `1-2`), tabella info **2384/6676** (il valore
precedente 2500/7000 sommava a 9500, incoerente), stili TOC1/TOC2 con `after=100` e
`ind left=220`, step-table con terza colonna a 6060 per sommare esattamente a 9060.

### Punti di contenuto aperti — in attesa di decisione
1. **Numerazione che non parte da 1** in `Audit_T080100_Rev2`, `Guida_Produzione_T080100_B3`,
   `Manuale_Operativo_T080100_v2`: il contenuto della sezione 1 c'è ma manca il titolo.
2. **Voce di indice spezzata** in `Guida_Produzione_T080100_B3`: "PARTE B" e "OPERATORE DI
   REPARTO" sono due paragrafi distinti.
3. **Accenti mancanti**: "Granularita", "possibilita", "tracciabilita", "Perche", "modalita".
4. **Campi persi** nella conversione delle tabelle info da schema "Voce/Contenuto":

   | Documento | Campi persi |
   |---|---|
   | `Piano_Operativo_T080100_Bozza6` | Oggetto, Base dati, Allegato |
   | `Controlli_e_Sigle_T080100_v3` | Oggetto, Base dati, Riferimento |
   | `Scenari_Conto_Lavoro_T080100_v1` | Oggetto, Base dati |
   | `Relazione_Lavorazioni_Esterne_T080100_B2` | Oggetto, Allegato |

### Task chiuso
✅ "Correggere formato dei documenti di sessione 9" — fatto, ma su **13 documenti**, non 5.

---

## SESSIONE 18 — Anagrafica, accessi, capacità, HTTPS, obiettivi 1g/1c/2b/2d, analisi conto lavoro (25-27/09/2026)

⚠️ **Lacuna di registrazione**: tra la sessione 17 (15/09) e questa sessione sono state fatte in altre chat attività che qui non risultano documentate: viste Gantt su PROJ-0001 (WO, Task Dettaglio, Task Macro-fasi, Client Script `Gantt_Fix_Remazel`), 21 Task su 2 livelli con 25 dipendenze, Server Script `JobCard_Avviso_Precedenze`. Da recuperare dalle chat precedenti e registrare a parte.

### 1. Anagrafica dipendenti
Fonte: mail di Simone del 22/09 "Informazioni mancati ERPNext", allegato `Anagrafica del personale.xlsx`.
- **21 persone**: 7 interne (INT), 14 esterne (EXT)
- Doppia funzione: Zouhaier e Mohisin (Montaggio - Molatura), Cannadoro (Molatura - Qualità)
- Crippa: Qualità 3 gg/settimana, condiviso tra Offshore e Combustion

**Decisione**: ogni persona che registra tempo sui Job Card ha un record Employee, sempre `Active`, senza `relieving_date` per chi lavora a chiamata. Il consuntivo (chi, quando, quante ore) viene dai Job Card Time Log. Nessun doctype `Contract`, nessun controllo di disponibilità in pianificazione.

Eseguito:
- `employment_type` è un **Link** al doctype `Employment Type`, non un Select: creati i record `Dipendente Remazel` ed `Esterno` (un primo tentativo errato via Property Setter è stato rimosso)
- Custom Field `Employee.custom_funzione` (Data): funzione testuale come da file di Simone
- 21 Employee creati con `insert(ignore_mandatory=True)`; `date_of_joining` = data di creazione, **segnaposto** da correggere se serve la data reale
- Eliminato `HR-EMP-00001` (Mario Rossi, dipendente di test del setup iniziale, senza collegamenti)

### 2. Utenti e accessi operatori
- **21 User** `nome.cognome@mes.remazel.com` (sottodominio fittizio, non caselle reali; accenti normalizzati, es. `andre.samar`), password individuali di 8 caratteri impostate con `update_password` (SMTP assente, nessuna mail di benvenuto)
- Ruolo **`Operatore di Reparto`**: `desk_access=1`, Custom DocPerm su Job Card con read/write/report, senza create/delete/submit
- **24 User Permission** `allow=Workstation`, `applicable_for=Job Card`: una per reparto, due per i 3 operatori a doppia funzione. L'operatore vede solo le Job Card del proprio reparto, senza filtri manuali
- `Employee.user_id` collegato per tutti e 21
- File consegnato: `Credenziali_Operatori_Reparto_T080100.xlsx` (unico punto con le password in chiaro, da conservare in modo sicuro)
- Nota: `tabUser` non ha un campo `employee`; il collegamento passa da `Employee.user_id`

### 3. Postazioni di lavoro e capacità reparti
Storia del dato: 09/09 layout TO-BE V2 (22 poi 24 stazioni) · 22/09 riepilogo con numeri diversi · **25/09 chiarimento definitivo di Simone**: il layout del 9/09 è lo stato **futuro**, quello da usare oggi è:

| Reparto | Stazioni | Dettaglio |
|---|---|---|
| Saldatura | 7 | 6 manuali + 1 a resistenza |
| Molatura | 5 | — |
| Montaggio | 5 | 1 carpenteria + 1 montaggio/formatura manuale + 3 montaggio |
| Formatura CNC | 1 | → Lavorazioni Meccaniche |
| Qualità | 3 | dimensionali+VT, PT, flussaggio ad aria |

Eseguito:
- `Workstation.production_capacity` (campo nativo, postazioni parallele): Saldatura 7, Molatura 5, Montaggio 5, Controllo Qualità 3, Lavorazioni Meccaniche 1, Lavorazione Esterna 1. Nessuna nuova Workstation, i 6 Workstation Type esistenti coincidono già con i nomi usati nelle BOM Operation
- Query Report **"Carico Reparti Settimanale"** corretto: la capacità ora è `giorni × 540 × production_capacity` del reparto, il totale settimana usa la somma delle capacità interne (prima era fisso a 540 per reparto e ×5 sul totale)
- Risultato: picco di saturazione Controllo Qualità **42%** (settimana al 13/12); il "sovraccarico" segnalato in passato era un artefatto del modello a postazione singola
- Le 581 Job Card esistenti **non** sono state toccate: le loro date sono valori già scritti, `production_capacity` incide sul report e sui futuri Work Order
- ⚠️ Issue noto ERPNext: con `production_capacity > 1` il controllo di sovrapposizione dello stesso dipendente su Job Card concorrenti non sempre blocca

### 4. HTTPS su combustionerp.remazel.com
- Setup production di bench: nginx gestito da `config/nginx.conf` (symlink in `/etc/nginx/conf.d/frappe-bench.conf`), supervisor per web/worker/redis. Il file nginx non si edita a mano
- Certificato wildcard `*.remazel.com` (RapidSSL). Fullchain = `star.remazel.com.crt` + `intermediate.crt` in quest'ordine
- File: `/home/frappe-user/frappe-bench/certs/combustionerp.remazel.com.crt` (644) e `.key` (600), proprietario `root:root`. Verificata la corrispondenza chiave/certificato con MD5 del modulus
- Procedura: `bench setup remove-domain combustionerp.remazel.com --site site1.local` → `bench setup add-domain combustionerp.remazel.com --site site1.local --ssl-certificate ... --ssl-certificate-key ...` → `bench setup nginx` → `sudo nginx -t` → `sudo systemctl reload nginx`
- Redirect 80 → 443 automatico
- Backup in `/home/frappe-user/site_config.json.bak-YYYYMMDD` e `nginx.conf.bak-YYYYMMDD`
- Documento: `Procedura_Rinnovo_Certificato_SSL_Remazel_B2.docx` (standard `docx-startit`, destinatario documento interno)

### 5. SMTP via Microsoft 365 — in sospeso
- Microsoft ha disattivato l'autenticazione SMTP con sola password: serve OAuth2 con app registrata su Entra ID
- Casella scelta: **`noreply@remazel.com`**
- Rete: cs-erp01 esce verso internet, non è raggiungibile dall'esterno; `combustionerp.remazel.com` risolve già in DNS interno. L'OAuth richiede solo che il browser di chi autorizza raggiunga il sito in HTTPS: prerequisito ora soddisfatto
- Redirect URI da registrare: `https://combustionerp.remazel.com/api/method/frappe.integrations.doctype.connected_app.connected_app.callback`
- Da fare: Connected App in ERPNext, App registration su Entra ID (permessi delegati `IMAP.AccessAsUser.All`, `SMTP.Send`, `offline_access`), client secret, autorizzazione con l'utente della casella, Email Account metodo OAuth

### 6. Microfusi, prezzi, stock negativo — decisioni di Gian
- **Codici microfusi**: restano `F000` e i codici attuali `T08-0100-P2112/P2302/P2305/P2404`. Punto chiuso per decisione, non più bloccante
- **Prezzi**: sui 4 microfusi `standard_rate = 1000,00` e Item Price `Standard Buying = 1000,00`. `valuation_rate` non toccato (è calcolato dal magazzino). Nessun altro prezzo reale: si resta sui fittizi, punto chiuso per decisione
- **`allow_negative_stock` resta a 1**, scelta deliberata di Gian: si testano i cicli a magazzino vuoto lasciando andare lo stock in negativo, **nessun carico fittizio**. Supera tutte le indicazioni precedenti di azzerarlo prima del go-live

### 7. Equipment, commessa e codici condivisi
- **T08-0100 e T09-0100 sono Equipment** (design di prodotto); la commessa è il **Job** (24-19006, 26-19008)
- Risposta di Simone del 25/09: se un componente T09 è identico a uno T08, nella BOM T09 si usa **direttamente il codice T08**; il contrario non accade. **Niente alias**, niente struttura aggiuntiva, anche nelle stampe
- Inviata a Simone (a cura di Gian) la considerazione: il codice appartiene al prodotto, non all'Equipment; per i **codici futuri** conviene uno schema neutro senza prefisso Equipment. Segnalato il collegamento con il progetto **"Da Commessa a Prodotto" (ETO → MTO)** di Romeo Brunasso
- Governance: le decisioni di produzione le governa **Simone con Gian**; Romeo guida il Controllo di Gestione
- Verifica a sistema: `PROJ-0001` porta il nome dell'Equipment, e il **Job non era scritto da nessuna parte**. Soluzione: `Sales Order.po_no` (campo nativo per l'ordine cliente) valorizzato con segnaposto **`99-99999`** su `SAL-ORD-2026-00001`; i Sales Order successivi useranno `99-99998` a scalare, da sostituire con i Job reali. ⚠️ Esecuzione del comando non confermata con output: da verificare
- Tracciabilità "quanti pezzi di un codice, per quale Equipment/Job": pulita solo se ogni Equipment genera **Work Order propri** per i componenti condivisi. Nei report standard raggruppati per articolo va sempre aggiunto il filtro Project

### 8. Obiettivi di Simone — stato reale e sviluppo
A fine sessione 16 il documento B3 dichiarava 11/12 obiettivi **fattibili**, ma l'incrocio con lo stato di implementazione (12/09) dava solo 1d e 1f completi; le quattro priorità alte (1a, 1b, 2a, 2b) erano parziali. In questa sessione:

**1g — Buffer di commessa ✅**
- Custom Field su Project: `custom_fine_produzione_stimata` (Date, sola lettura), `custom_buffer_giorni` (Int, modificabile, default **5**), `custom_deadline_interna` (Date, sola lettura)
- PROJ-0001: buffer 5 gg, deadline interna **13/12/2026** (reale 18/12/2026)
- Lezione: con lo scheduling backward la fine produzione coincide sempre con la deadline, quindi il buffer è un **parametro di input**, non un valore calcolato
- ⚠️ `custom_deadline_interna` è stata calcolata da script: **non si ricalcola da sola** se si modifica il buffer. Serve un Server Script `Before Save` su Project

**1c — Riprogrammazione agile ✅ (livello 1)**
- Server Script API `Simula_Ritardo_JobCard` (`/api/method/simula_ritardo_jobcard`, nessuna scrittura) e `Applica_Ritardo_JobCard` (`/api/method/applica_ritardo_jobcard`, scrive le date). Parametri: `job_card_name`, `nuova_data_fine`
- Logica: calcola lo scarto in giorni e sposta di pari entità tutte le Job Card successive (`idx` maggiore) dello **stesso Work Order** non completate, preservando le durate
- Confronto automatico con `custom_deadline_interna` ed `expected_end_date` del Project, con avviso esplicito
- Test su `MFG-WO-2026-01152` / `PO-JOB04994`: +3 gg → 9 Job Card spostate, fine al 21/12, **sforamento della deadline reale di 3 giorni** rilevato correttamente
- Limiti: la cascata tra Work Order padre/figlio (livello 2) non è gestita; nessun pulsante in interfaccia (solo API); logica testata in console, chiamata HTTP all'endpoint non ancora provata
- Il riempimento di postazioni libere con lavoro di altri prodotti è già permesso (avvisi di precedenza non bloccanti); manca solo una vista "coda per postazione"

**2b — Documenti tecnici sulle Job Card ✅ (infrastruttura)**
- DocType figlio **`Operazione Documento Tecnico`**: `tipo_documento` (Disegno / WPS / Controllo Qualita / Altro), `file` (Attach), `nota`
- Campo Table `custom_documenti_tecnici` su **BOM Operation** (con `allow_on_submit=1`, necessario perché le 61 BOM sono submitted) e su **Job Card** (sola lettura)
- Server Script **`JobCard_Documenti_Tecnici`** (Before Insert su Job Card): risale da `operation_id` al Work Order Operation, poi alla BOM Operation con stesso `bom_no` e stesso `idx`, e copia i documenti. Si allega una volta per fase, si propaga a ogni Job Card
- Verificato il match su dati reali (BOM Operation `9ebe51e9d8`), riga di test rimossa. Presuppone che l'ordine delle operazioni del WO coincida con quello della BOM
- Mancano i documenti veri (disegni, WPS, criteri di controllo): nessuno è stato fornito

**2d — Lotti e numeri di serie ✅ (infrastruttura, dati segnaposto)**
- ⚠️ Il file `T080100 Ciclo e fasi 5.xlsx` / foglio matricole e i file in `01_Documentazione/Dati` sono **file di lavoro di Gian** prodotti per strutturare il sistema, **non dati reali** del cliente
- `has_serial_no` già attivo su `T08-0100-A0001`
- **58 Serial No** `PLACEHOLDER-T08-0001` … `0058`, stato Inactive, descrizione "SEGNAPOSTO … NON è una matricola reale"
- **40 Quality Inspection Parameter** (W1…W61 presenti nel file di lavoro) e Template **"Controllo Saldature per Matricola (SCHEMA - da validare)"**
- **Decisione architetturale presa**: tracciabilità per matricola tramite **Quality Inspection per Serial No**, non split dei WO a qty=1

**Divisione di una fase tra interno ed esterno — nativo, da documentare**
- ERPNext consente più Job Card sulla stessa Work Order Operation con quantità parziali e Workstation diverse (pulsante "Create Job Card" finché resta quantità scoperta, `show_create_job_card_button`). Esempio: 10 pezzi, 5 su Saldatura e 5 su Lavorazione Esterna
- Casi discussi: 1) esternalizzazione decisa prima di partire (cambio Workstation sulla Job Card); 2) decisa a metà lavorazione (chiusura parziale + nuova Job Card per il residuo); 3) vero conto lavoro con uscita fisica = **obiettivo 3**; 4) split della quantità

### 9. Obiettivo 3 — Expediting e conto lavoro: analisi completa
**Fatti rilevati a sistema:**

| Aspetto | Dato |
|---|---|
| Fasi esterne | 134, in 58 BOM su 61 |
| Posizione | 90 in mezzo al ciclo, 44 in testa, 0 in coda; fino a 6 per articolo |
| Job Card esterne | 130, tutte Open |
| Fornitori citati nei cicli | 18 distinti (A.M.C. CONTROL SRL 36 fasi, SOMECAR 14, INOXEA 14, BONADEI 13, …) |
| Supplier a sistema | 20, quasi tutti già presenti |
| Anomalie anagrafiche | "A.M.C. CONTROL" (1 fase) vs "A.M.C. CONTROL SRL"; "H.T. SRL" e "H.T.S. SRL" da verificare; 1 fase senza fornitore |
| Strumenti v16 | Subcontracting Order / Receipt / BOM / Inward Order presenti; `is_subcontracted` su BOM Operation, Work Order Operation e Job Card |
| Documenti | 0 Purchase Order, 0 Subcontracting Order |
| Magazzini | 4 standard, nessun magazzino presso fornitore |

**Correzione importante**: la v16 supporta il **conto lavoro per singola fase dalla Job Card** (Purchase Order di conto lavoro creato dalla Job Card). Non serve spezzare gli articoli né ridisegnare le BOM, come ipotizzato in un primo momento sulla base delle versioni precedenti.

**SAP Business One:**
- Versione **10.5**, raggiungibile in rete da cs-erp01; gestisce acquisti, fornitori e magazzino per tutta l'azienda
- Per BU Combustion **su SAP B1 non esiste alcuna distinta base**; la rendicontazione di ore e consumi oggi è su **fogli Excel** separati
- Il flusso aziendale Autodesk → SAP B1 non è applicabile a questa BU (prodotti complessi, brevettati, disegni cliente spesso solo in PDF)
- ERPNext è quindi la **fonte unica** di distinta base, produzione e rendicontazione per la BU; il tracciamento di uscita e rientro del conto lavoro è **compito di ERPNext**
- Nessun connettore ufficiale ERPNext ↔ SAP B1: B1if è il middleware SAP (progetto dedicato). Strada scelta: **integrazione propria via Service Layer** (API REST nativa di SAP B1 10.x, porta 50000), senza B1if

**Visione concordata:**
- Fase 1: dato un fabbisogno (es. "100 × T08-0100") il Production Plan esplode la BOM e calcola materiali e acquisti (con lead time e fornitore); il risultato si esporta in un **file** per SAP B1
- Fase 2: se la fase 1 regge, interconnessione automatica via Service Layer

**Decisione sulla strada:** **C1 — conto lavoro per fase nativo v16**. Prima un **pilota su una sola Job Card esterna** in mezzo al ciclo con fornitore A.M.C. CONTROL SRL, poi estensione alle 134 fasi via script. Script di lettura preparato: `pilota_1_lettura.py` (Job Card candidate, codice v16 delle funzioni di conto lavoro, pulsanti JS, campi Job Card) — **output in attesa**.

### 10. Documentazione e archivio
- La struttura di progetto vive su SharePoint: sito StartIT → `Documenti condivisi/Clienti/Remazel/Progetti/Remazel-Combustion`. Verificata la presenza dei 13 documenti correnti e delle sottocartelle `Dati` ed `Email_Simone`: la copia locale originale può essere eliminata
- Il connettore Microsoft 365 permette **solo lettura**: i file generati vanno caricati a mano. Indirizzamento funzionante: `file:///{driveId}/Clienti/Remazel/Progetti/Remazel-Combustion` (i link https di condivisione non sono accettati)
- Lette la Guida Produzione B3 e la Guida Concettuale v6: da aggiornare (v. task aperti)

### 11. Comunicazioni con Simone
- 25/09 postazioni: chiarito, numeri applicati. **Da confermargli** che anagrafica e postazioni sono a sistema
- 25/09 codici condivisi: confermata la sua impostazione, inviate le considerazioni su codifica neutra e progetto di Romeo
- Riunione proposta da Romeo (mail 23/09) per **martedì 29/09**: validazione ciclo T09-0100 con Simone e Sergey, poi rendicontazione tempi su una parte di processo
- T09-0100: Simone ha rinviato il 22/09 `T09-0100 Ciclo e fasi_26-19008.xlsx` e le 6 date di consegna (26/02, 30/04, 30/06, 31/08, 29/10, 30/11/2027)

### Trappole tecniche apprese (sessione 18)
- **Incolla lunghi via SSH vengono troncati.** Metodo standard ora: script compresso `gzip | base64` in una sola riga → `echo '...' | base64 -d | gunzip > /home/frappe-user/<nome>.py` in bash → verifica con `wc -l` → in console `exec(open('/home/frappe-user/<nome>.py').read())`
- **Questa console IPython non richiede `%cpaste`**: rileva l'incolla multiriga da sola; una riga `--` finale dà `SyntaxError` e annulla l'intero blocco
- **Dentro `exec(...)` lambda e comprehension non vedono le variabili dello script** (`NameError`): usare solo cicli espliciti
- Sempre `cd /home/frappe-user/frappe-bench` prima di `bench`; `exec(...)` va lanciato in console (`In [n]:`), non in bash
- `Employee.employment_type` è un Link a `Employment Type`
- `Server Script` in inserimento via API richiede `name` impostato esplicitamente ("Please set the document name")
- `Serial No.description` è read_only: il valore passato prima dell'insert viene scartato; scriverlo dopo con `frappe.db.set_value`
- `Quality Inspection Template`: il campo `specification` è un Link al master `Quality Inspection Parameter`, da creare prima
- `Item` non ha `default_company`: l'azienda si ricava con `frappe.db.get_value("Company", {"name": ["like", "%Remazel%"]}, "name")` (Remazel Engineering SpA)
- Campi custom su righe di documenti submitted (BOM Operation): servono `allow_on_submit=1`, oppure `db_insert` diretto delle righe figlie; `doc.save()` dà `UpdateAfterSubmitError`
- Mai lasciare segnaposto letterali nei comandi da incollare: `report.query = "<...>"` è stato salvato così com'era e ha dovuto essere corretto
- `bench setup add-domain` (bench 5.29.1): `--site` va dopo il sottocomando; se il dominio esiste già senza SSL serve prima `remove-domain`
- Con la chiave privata a `600 root`, `openssl rsa` richiede `sudo`
- In SSH si usa l'hostname `combustionerp.remazel.com`; `cs-erp01` è il nome interno della macchina

---


## 🖥️ FRONTE ERPNEXT — stato al 27/09/2026

### Configurazione a regime
- **58 Work Order** "In Process", **581 Job Card** (dato 01/09), 130 delle quali su Lavorazione Esterna
- Ciclo **v6** caricato; capacity planning attivo (`disable_capacity_planning=0`)
- 613 BOM Operation con descrizione parlante; Server Script `JobCard_Descrizione_Fase` e `JobCard_Documenti_Tecnici`
- Backward scheduling dalla scadenza 18/12/2026; deadline interna PROJ-0001 al 13/12/2026 (buffer 5 gg)
- **Capacità reparti reale**: Saldatura 7, Molatura 5, Montaggio 5, Controllo Qualità 3, Lavorazioni Meccaniche 1
- **21 Employee + 21 User** operatori con ruolo `Operatore di Reparto` e User Permission per reparto
- **HTTPS attivo** su `combustionerp.remazel.com` con certificato wildcard `*.remazel.com`
- `allow_negative_stock = 1` per scelta: si lavora in negativo, nessun carico fittizio
- Server Script API `Simula_Ritardo_JobCard` / `Applica_Ritardo_JobCard`
- Infrastruttura documenti tecnici (2b) e matricole segnaposto + template saldature (2d) pronte

### Dati per il go-live (30/09/2026)
| Dato | Stato |
|---|---|
| Codici articolo microfusi | ✅ chiuso per decisione: restano `F000` e i codici attuali |
| Prezzi fornitore reali | ✅ chiuso per decisione: restano i fittizi (1000,00 sui 4 microfusi) |
| Anagrafica dipendenti | ✅ caricata (21 persone) |
| Postazioni e capacità reparti | ✅ applicate (dato Simone del 25/09) |
| Numeri Job reali | ⏳ segnaposto `99-99999` su `po_no`, da sostituire |
| Matricole reali | ⏳ segnaposto `PLACEHOLDER-T08-xxxx` |
| Documenti tecnici (disegni, WPS, controlli) | ⏳ non forniti; infrastruttura pronta |

---

## 🎯 TASK APERTI / PROSSIMA SESSIONE (aggiornato al 27/09/2026)

### Priorità 1 — Obiettivo 3: conto lavoro per fase (strada C1)
- Eseguire `pilota_1_lettura.py` e analizzare come la v16 gestisce `is_subcontracted` sulla Job Card (articolo che esce, articolo servizio, magazzino fornitore, aggancio della fase successiva al rientro)
- Prerequisiti del pilota: magazzino presso fornitore; normalizzare "A.M.C. CONTROL" su "A.M.C. CONTROL SRL"; verificare se "H.T. SRL" e "H.T.S. SRL" sono la stessa azienda; assegnare il fornitore alla fase che ne è priva
- Pilota su una Job Card esterna in mezzo al ciclo (A.M.C. CONTROL SRL), flusso completo documentato passo per passo
- Se regge: estensione alle 134 fasi via script, report dei rientri in ritardo

### Priorità 2 — SMTP Microsoft 365 (OAuth)
Connected App + App registration Entra ID per `noreply@remazel.com` (dettagli in sessione 18, punto 5).

### Priorità 3 — T09-0100
- Verificare se il ciclo rinviato il 22/09 risolve le anomalie note (residuo codici T08, duplicati, `*CONFERMARE GRUPPO*`)
- Import con i componenti identici a T08 referenziati con il **codice T08** (regola di Simone)
- Project dedicato all'Equipment T09-0100, Sales Order con `po_no = 99-99998`, Work Order propri anche per i componenti condivisi
- Usare le 6 date di consegna per lo scheduling
- Preparare la riunione di **martedì 29/09** con Simone e Sergey

### Priorità 4 — Correzioni tecniche emerse in sessione 18
- Server Script `Before Save` su Project per ricalcolare `custom_deadline_interna` quando cambia il buffer
- Verificare che `po_no = 99-99999` sia stato davvero scritto su `SAL-ORD-2026-00001`
- Pulsanti in interfaccia (Client Script su Job Card) per simulare e applicare il ritardo; provare la chiamata HTTP agli endpoint
- Validare con Simone il template "Controllo Saldature per Matricola" e la regola "Quality Inspection per matricola"
- Comunicare a Simone che anagrafica e postazioni sono a sistema

### Priorità 5 — Documentazione
- **Guida Produzione → B4**: rimuovere i riferimenti a Mario Rossi / `HR-EMP-00001` e ai codici C0900/C0901; nuovo flusso operatore con login personale e filtro automatico per reparto; divisione di una fase tra interno ed esterno (più Job Card con quantità parziali); numeri aggiornati (58 WO, 581 Job Card)
- **Guida Concettuale → v7**: aggiornare la tabella "azioni prima del go-live"; spiegare `production_capacity`, buffer e deadline interna
- Documentare le nuove funzioni: simulazione/applicazione ritardo (1c), documenti tecnici (2b), matricole e controllo saldature (2d)
- Punti di contenuto ancora aperti dalla sessione 17: titoli di sezione mancanti, voce d'indice spezzata, accenti mancanti, campi persi nelle tabelle info
- Recuperare e registrare le attività 16-24/09 non documentate (Gantt, Task, precedenze)

### Priorità 6 — Integrazione SAP Business One
- Fase 1: Production Plan di prova (es. 100 × T08-0100) per verificare l'esplosione dei fabbisogni; definire il formato del file da passare a SAP B1
- Fase 2: integrazione via Service Layer (credenziali e utente tecnico da ottenere da chi amministra SAP B1)

### Priorità 7 — Dopo il go-live
- Motore APS di terze parti per l'obiettivo 1e
- Cascata ritardi tra Work Order padre/figlio (1c livello 2) e vista "coda per postazione"
- Codifica articoli neutra per i nuovi codici, da concordare con Simone

---

## 📌 REGOLE OPERATIVE CONSOLIDATE

**Documenti**
- Si lavora **solo** in `01_Documentazione`, che contiene una sola versione per famiglia (ora su SharePoint: `Clienti/Remazel/Progetti/Remazel-Combustion`)
- Prima di consegnare: `censimento_remazel.py` dice se qualcosa è fuori standard
- Ogni variante deve avere l'identificativo di versione nel nome: mai sovrascrivere senza incrementare
- Il campo `Documento` della tabella info deve coincidere col nome file reale
- Verificare sempre il **contenuto interno**, non solo il nome file
- Documenti di progetto per il cliente: skill `docx-remazel`; procedure interne Start I.T.: skill `docx-startit`

**Comunicazione col cliente**
- Tono soft-ma-fermo; riferimenti d'ufficio, non nomi propri, nei documenti formali
- I vincoli si presentano come **disponibilità del dato**, non come limiti di sviluppo
- Numeri significativi e difendibili, mai tecnicamente corretti ma fuorvianti
- Non rispiegare a Simone concetti che conosce già (es. la distinzione tra Job e commessa)

**ERPNext**
- `bench` si lancia da `/home/frappe-user/frappe-bench`; in SSH l'host è `combustionerp.remazel.com`
- Script lunghi: file compresso gzip+base64 → `wc -l` → `exec(open(...).read())` in console; niente `%cpaste` / `--`
- Negli script niente lambda né comprehension: solo cicli espliciti
- `frappe.db.set_value(..., update_modified=False)` sui documenti submitted; mai `doc.save()`
- Dopo DELETE/UPDATE in console: `frappe.db.commit()` prima di rileggere, altrimenti lo snapshot MariaDB non vede i dati creati dal web server
- Prima di scrivere su un doctype, verificare tipo e nome reale dei campi (`frappe.get_meta`), non dedurli
- Dati inventati o provvisori sempre etichettati in modo inequivocabile (`PLACEHOLDER-`, `99-9999x`, "SEGNAPOSTO")
- `allow_negative_stock` resta a 1: non riportarlo a 0 senza conferma esplicita di Gian

---

*Ultimo aggiornamento: **Sessione 18** — 27 settembre 2026 (anagrafica e accessi operatori, capacità reparti, HTTPS, obiettivi 1g/1c/2b/2d, analisi conto lavoro e SAP B1)*
*⚠️ A fine ogni sessione: aggiornare questo file nel Project E restituire il blocco all'utente.*
