# MEMORIA_SESSIONE — Sessione 19 — 26-29 settembre 2026

> ⚠️ **Nota del 05/10/2026 (sessione 23)**: la regola "il repo GitHub non va più aggiornato" è **superata**.
> A fine sessione la memoria va allineata in OneDrive, Project Cowork e repo. Vedi `CONTESTO_PROGRESSIVO_ERPNext.md`, Regole operative → Memoria.


Sessione in **Claude Code cloud** (claude.ai/code), repo GitHub `gianfranco-angelini/AI-Project`,
branch `claude/cool-curie-q5r93n`. Nessun intervento su ERPNext. Tema: memoria di progetto,
standard documentale, passaggio a Claude Code sul PC.

---

## Ambiente

| Elemento | Stato |
|---|---|
| Sessione | Claude Code cloud, container Linux, **senza accesso al PC né a OneDrive** |
| Repo GitHub | `gianfranco-angelini/AI-Project`: trovato vuoto; ora contiene `CLAUDE.md` (del repo), `12_Memorie/CONTESTO_PROGRESSIVO_ERPNext.md`, `12_Memorie/SKILL_docx-remazel.md`, `Remazel-Combustion/CLAUDE.md`, questa memoria |
| Connettore Microsoft 365 | **Solo lettura**: permessi verificati, tutti `*.Read*`, nessun `ReadWrite` e nessuna funzione di scrittura. Legge mail, calendario, SharePoint; dei `.docx` restituisce solo il testo, non il file |
| SharePoint di progetto | sito StartIT → `Documenti condivisi/Clienti/Remazel/Progetti/Remazel-Combustion` = cartella OneDrive locale sincronizzata |
| Cartella locale | `C:\Users\gianfranco.angelini\OneDrive - Start Information Technology s.r.l\Documenti\Clienti\Remazel\Progetti\Remazel-Combustion` |
| Claude Code sul PC | v2.1.283, Opus 5.5, account Claude Team. Avvio con la funzione `remazel` del profilo PowerShell |
| **Copia principale della memoria** | **`12_Memorie` in OneDrive**. Il repo GitHub non va più aggiornato |

---

## Problemi risolti questa sessione

### 1. Contesto progressivo recuperato
- Il repo era vuoto: una prima ricostruzione dalla skill `erpnext-remazel` è stata sostituita dal
  file consolidato fornito da Gian (sessioni 1-18, 846 righe)
- Aggiunta la **Sessione 19** al contesto, con task aperti e riga "Ultimo aggiornamento" aggiornati
- Versione finale in OneDrive verificata su SharePoint: **69.110 byte**, identica al repo. La
  versione precedente (63.757 byte) è in `12_Memorie/Old`

### 2. Mail di Romeo del 23/09 ("I: Informazioni mancati ERPNext")
- **Richiesta**: per la riunione di **martedì 29/09**, far validare a Simone, con il supporto di
  Sergey, il **ciclo/fase dell'Equipment T09-0100**; poi implementare la **rendicontazione dei tempi
  su una parte di processo** come primo riscontro tangibile
- È un inoltro della mail di Simone del 22/09 (Cc Fabio Picco, Marco Lasorella, Sergey Mylnikov,
  Romeo); Romeo mette in Cc Marco Lasorella e Paolo Scaglia
- **Allegati reali**: `Anagrafica del personale.xlsx` (10 KB, già caricata in sess. 18) e
  **`T09-0100 Ciclo e fasi_26-19008.xlsx`** (1,9 MB, **non ancora analizzato**). I 7 file
  `image00X.png` sono firme
- **Risposta di Gian**: sì, se partecipa anche Sergey. Testo preparato (invio a cura di Gian):

  > Ciao Romeo,
  > sì, ha senso — anzi è la strada giusta. Se martedì partecipa anche Sergey possiamo far validare
  > a lui e Simone insieme il ciclo/fase di T09-0100 direttamente in sede, così chiudiamo eventuali
  > dubbi residui (codici fase duplicati, riferimenti ancora legati a T08) prima di importarlo a
  > sistema.
  > Per la rendicontazione tempistiche, propongo di partire da un pilota su una singola parte di
  > processo per avere un primo riscontro concreto, come suggerisci.
  > A martedì,
  > Gian

### 3. Codici articolo SAP: nessuna mail mancata
- Controllate tutte le 7 mail di Romeo e cercato "SAP", "codici articolo", "C0900/C0901" su tutta la
  casella: **nessuna mail con codici articolo SAP**
- Nelle mail di Romeo SAP compare solo come roadmap (presentazione `Progetto_Combustion_EVO_cdg_it`):
  *"gestionale in parallelo a SAP fino al 31.12.2026; avvio a regime dal 01.01.2027 con ERPNext per
  i nuovi ordini cliente"*
- C0900/C0901 restano chiusi (rimossi su istruzione di Simone il 7/09, sess. 16)

### 4. Codici T08/T09: regola già decisa, riepilogata
- Componente T09 identico a uno T08 → nella BOM T09 si usa **direttamente il codice T08**. Niente
  alias né struttura aggiuntiva, nemmeno nelle stampe (mail di Simone del 25/09, confermata da Gian)
- Per i codici futuri Gian ha proposto uno schema neutro senza prefisso Equipment, collegato al
  progetto "Da Commessa a Prodotto" di Romeo
- In ERPNext: Work Order propri per Equipment anche sui componenti condivisi; nei report per
  articolo si filtra per Project
- Da verificare sul ciclo T09 del 22/09: residui di codici fase T08, codici fase duplicati,
  `*CONFERMARE GRUPPO*`

### 5. Postazioni: dato da riconciliare
| Reparto | Mail Simone 22/09 | Chiarimento 25/09 (a sistema) |
|---|---|---|
| Saldatura | 7 | 7 |
| Molatura | **6** | 5 |
| Montaggio | 5 (4 + 1 formatura) | 5 |
| Qualità | **2** (VT + PT + dimensionali) | 3 (dimensionali+VT, PT, flussaggio) |
| Formatura manuale | **1** | dentro Montaggio |
| Flussaggio | **1** | dentro Qualità |
| Formatura CNC | 1 | 1 (Lavorazioni Meccaniche) |

### 6. Standard documentale: decisione di Gian
- **Standard unico `docx-startit`** per tutti i documenti, Remazel compresi: *"standardizzare il più
  possibile"*
- **`docx-remazel` riscritta come derivata**: rimanda a `docx-startit` per tutta la grafica e tiene
  solo le regole Remazel. Testo in `12_Memorie/SKILL_docx-remazel.md` (10.697 byte)
- **Naming** `{Tipo}_{Oggetto}_Remazel_B{N}.docx`, **senza codice commessa** e senza `ERPNext_`
- **Documenti esistenti**: prendono il nome standard alla versione successiva, con il numero che
  prosegue (`Guida_Concettuale_T080100_v6` → `Guida_Concettuale_Remazel_B7`). Scelta fatta da
  Claude su indicazione generica di Gian: modificabile
- **Migrazione**: i 13 documenti in blu restano validi finché non vengono aggiornati;
  all'aggiornamento si estrae il contenuto e si rigenera con `startit_docx.py`

| Elemento | Prima (Remazel blu) | Ora (`docx-startit`) |
|---|---|---|
| Titoli e indice | `2E74B5` | `757F9B` |
| Heading 2 | 13pt | 12pt |
| Header col. 1 | testo "Start I.T. S.r.l." | logo `logo_startit.png` 3,8 cm |
| Footer | 3 celle / paragrafo singolo | 2 righe 8pt `888888`, `Pag.` a destra |
| Tabella info | 2500/7000, campo Commessa | 2384/6676, 8 campi con **Riferimento** |
| Indice | `\o "1-2"` / `"1-3"` | `TOC \o "1-4" \h \z \u` |
| Margine superiore | 1134 | 1620 |

Valori Remazel: Destinatario `Remazel Engineering S.p.A. — BU Combustion` (colonna 2 header:
`Remazel Engineering S.p.A.`), Sistema **`M.E.S. Remazel`**, Riferimento
`ERPNext — combustionerp.remazel.com`, Redatto da `Start I.T. S.r.l.`.

### 7. Generatore docx-startit provato
- `startit_docx.py` non ha dipendenze esterne. Documento di prova con valori Remazel: pacchetto
  valido (`validate.py`: *All validations PASSED*), PDF corretto con logo, header, tabella info e footer
- Numeri di pagina dell'indice in **due passate** tramite `pdftotext`: snippet testato e inserito
  nella skill (§5)
- Nel container mancavano `libreoffice-writer` (con il solo `libreoffice-core`, `soffice` risponde
  *"source file could not be loaded"* anche su un `.txt`), `poppler-utils` e `defusedxml`

### 8. Passaggio a Claude Code sul PC
- Il `Manuale_Utente_Installazione_ClaudeCode_Remazel_B1.docx` (26/09) descrive l'installazione
  locale: è la soluzione per scrivere sui file reali
- Differenza chiarita: **Claude Code web/cloud** (repo GitHub, nessun accesso al PC) vs **Claude
  Code sul PC** (`claude` da PowerShell nella cartella OneDrive, legge e scrive i file reali).
  Variante `claude remote-control`: gira sul PC e si comanda dall'app
- **Funzione `remazel`** nel profilo PowerShell (`notepad $PROFILE`):
  ```powershell
  function remazel {
      Set-Location "C:\Users\gianfranco.angelini\OneDrive - Start Information Technology s.r.l\Documenti\Clienti\Remazel\Progetti\Remazel-Combustion"
      claude @args
  }
  ```
  Uso: `remazel` oppure `remazel remote-control`. Se gli script sono bloccati:
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
- **Modalità di permesso**: usare la **default** (chiede prima di modifiche e comandi); si cambia
  con **Shift+Tab**. Evitare auto mode e accept edits. Il plan mode è utile per le proposte di
  struttura
- **Letture fuori dalla cartella** (es. `startit_docx.py` in `.claude\skills\...`): consentite con
  "Yes, keep allowing" (solo lettura; le modifiche restano soggette a conferma)
- Errore iniziale: il messaggio va incollato **dentro** Claude Code (riquadro `>`), non al prompt
  `PS C:\...>`; il trust prompt della cartella si conferma con **Invio**, non Esc

### 9. Sistemazione cartella OneDrive (verificata su SharePoint)
- `Cloude.md` (nome errato, non caricato da Claude Code) **eliminato**; creato **`CLAUDE.md`**
  (3.241 byte) dalla versione in `Remazel-Combustion/CLAUDE.md` del repo
- Errori intermedi corretti: copiato prima il `CLAUDE.md` del repo (sbagliato); download salvato
  come `CLAUDE (2).md`; skill nuova spostata per errore in `Old`
- `12_Memorie` finale: `Old/`, `CONTESTO_PROGRESSIVO_ERPNext.md`, `Cowork_Progetto_T080100.md`,
  `MEMORIA_SESSIONE_T08-0100.md`, `SKILL_docx-remazel.md`
- In `12_Memorie/Old`: `SKILL_docx-remazel_REVISIONE.md` (15/09), `docxremazelSKILLv2.md` (ancora
  con "E.M.S. Remazel", 28pt, blu), il contesto precedente
- Download dal browser: dall'app non c'è il tasto per scaricare, si usa GitHub → icona **Download raw file**

---

## Script e Query usati

Nessuno script su ERPNext. Strumenti usati:

```bash
# container cloud — prerequisiti per generare e verificare i docx
apt-get install -y --no-install-recommends libreoffice-writer
apt-get install -y poppler-utils
pip install -q defusedxml lxml

# verifica
python3 <skill docx>/scripts/office/validate.py file.docx
soffice --headless --convert-to pdf file.docx
pdftoppm -jpeg -r 60 file.pdf pag
```

Verifiche su SharePoint con il connettore M365 (`read_resource` sulla cartella
`file:///{driveId}/Clienti/Remazel/Progetti/Remazel-Combustion`): confronto delle dimensioni in
byte con le copie del repo.

---

## Fix ancora aperti

- [ ] **Salvare la skill**: su claude.ai, salvare `SKILL_docx-remazel.md` nella skill
      `docx-remazel` dalla card di revisione. Fino ad allora la skill caricata è quella vecchia in blu
      (il `CLAUDE.md` dice già che fa fede il file in `12_Memorie`)
- [ ] **Inviare la risposta a Romeo** (testo al punto 2)
- [ ] **Riconciliare le postazioni** con Simone (tabella al punto 5)
- [ ] **Aggiornare `LEGGIMI.md`**: punti 5-6 e "Nota sul footer" superati
- [ ] Verificare sul PC la presenza di **Python 3 e LibreOffice**; eventualmente aggiungere un
      paragrafo al manuale di installazione di Claude Code (B2)
- [ ] Verificare che nella sessione sul PC siano disponibili le skill `docx-startit` (logo,
      template, generatore) e `docx-remazel`
- [ ] Confermare o cambiare la regola di rinomina dei documenti esistenti (punto 6)
- [ ] Recuperare e registrare le attività 16-24/09 non documentate (Gantt PROJ-0001, 21 Task con
      25 dipendenze, Server Script `JobCard_Avviso_Precedenze`)

---

## Task prossima sessione (sul PC, un documento alla volta, prima la struttura)

1. **Materiale per la riunione del 29/09**: analizzare `T09-0100 Ciclo e fasi_26-19008.xlsx` (anomalie
   note, codici T08 riusati, 6 date di consegna 26/02, 30/04, 30/06, 31/08, 29/10, 30/11/2027) e
   proporre agenda e checklist di validazione con Simone e Sergey, più la proposta di pilota per la
   rendicontazione dei tempi
2. **Guida Produzione → B4** (via Mario Rossi / `HR-EMP-00001` e C0900/C0901, login operatore e filtro
   per reparto, fase divisa tra interno ed esterno, 58 WO / 581 Job Card)
3. **Analisi Obiettivi → B4** (stato reale di 1g, 1c, 2b, 2d, obiettivo 3 strada C1)
4. **Guida Concettuale → B7**, **Prerequisiti Go-Live → B2**
5. Nuovi: guida alle nuove funzioni (1c, 2b, 2d), analisi conto lavoro (obiettivo 3), analisi
   integrazione SAP B1 (fase 1 file, fase 2 Service Layer)
6. Correzioni di contenuto dalla sessione 17 (titoli di sezione mancanti, voce d'indice spezzata,
   accenti, campi persi nelle tabelle info)
7. A fine sessione: aggiungere la Sessione 20 in `12_Memorie/CONTESTO_PROGRESSIVO_ERPNext.md`
