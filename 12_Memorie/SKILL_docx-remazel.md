---
name: docx-remazel
description: "Regole specifiche per i documenti Word dei progetti Remazel Engineering / BU Combustion (M.E.S. Remazel su ERPNext) prodotti da Start I.T. La grafica NON è definita qui: è quella dello standard aziendale docx-startit, da caricare sempre insieme a questa skill. Qui stanno solo i valori variabili Remazel (destinatario, sistema, riferimento), il naming, le regole di contenuto e di tono verso il cliente, la migrazione dei vecchi documenti in blu e le note d'ambiente. Usare per creare, aggiornare, impaginare o verificare qualsiasi .docx Remazel."
---

# Remazel Engineering — Documenti Word (derivata di docx-startit)

## 0. Regola di base

**La grafica è quella di `docx-startit`, senza eccezioni.** Prima di scrivere un documento
Remazel si caricano **entrambe** le skill: prima `docx-startit`, che definisce grafica,
geometria, stili, generatore e verifica in 15 punti, poi questa, che aggiunge solo le regole
Remazel.

Obiettivo: **standardizzare il più possibile**. Un documento Remazel è un documento Start I.T.
in cui cambiano solo i valori variabili. Se una regola di questa skill contraddice
`docx-startit` su un aspetto grafico, vale `docx-startit` e questa skill va corretta.

Questa skill non duplica la specifica grafica. La duplicazione ha già prodotto disallineamenti
(sessioni 17-19 del progetto): per qualsiasi valore di impaginazione si guarda `docx-startit`.

---

## 1. Valori variabili Remazel

| Variabile `docx-startit` | Valore Remazel |
|---|---|
| `{Destinatario}` (tabella info, ultima riga del sottotitolo) | `Remazel Engineering S.p.A. — BU Combustion` |
| Colonna 2 dell'intestazione | `Remazel Engineering S.p.A.` |
| `{Oggetto}` (colonna 3 dell'intestazione) | titolo breve, una riga, max ~40 caratteri |
| Campo `Sistema` | **`M.E.S. Remazel`** |
| Campo `Riferimento` | `ERPNext — combustionerp.remazel.com` (oppure il modulo coinvolto, es. `ERPNext — Produzione / Job Card`) |
| Campo `Redatto da` | `Start I.T. S.r.l.` |

La tabella info resta quella standard a **8 campi**, nell'ordine di `docx-startit`:
Documento, Versione, Data, Redatto da, Destinatario, Sistema, Riferimento, Stato.
**Non si aggiunge un campo Commessa.** Equipment (T08-0100, T09-0100) e Job (24-19006,
26-19008) si citano nel corpo del documento, dove servono.

### Sistema: sempre M.E.S. Remazel
Il nome corretto è **M.E.S. Remazel** (Manufacturing Execution System). Le varianti
**E.M.S. Remazel** e **M.S.E.** sono errori confermati, trovati su 8 documenti in passato.
Controllarlo sempre, anche nel testo del corpo.

---

## 2. Naming

Pattern `docx-startit`: `{Tipo}_{Oggetto}_{Cliente}_B{N}.docx`, con `{Cliente}` = `Remazel`.

- **Nessun codice commessa o Equipment nel nome** (niente `T080100`, `T090100`)
- **Nessun prefisso `ERPNext_`**
- Il numero di bozza si incrementa a ogni consegna e non si azzera mai; la bozza precedente
  non si sovrascrive
- Il campo `Documento` della tabella info coincide esattamente con il nome del file

Esempi: `Analisi_Integrazione_SAP_Remazel_B1.docx`,
`Guida_Produzione_Remazel_B4.docx`, `Agenda_Validazione_Ciclo_Remazel_B1.docx`.

### Documenti esistenti con il vecchio nome
Quando uno dei documenti correnti passa alla versione successiva, prende il nome standard:
restano il tipo e l'oggetto, il numero **prosegue** da quello precedente, e le sigle `v`,
`Rev`, `Bozza` diventano `B`.

| Nome attuale | Prossima versione |
|---|---|
| `Analisi_Obiettivi_BU_Combustion_B3.docx` | `Analisi_Obiettivi_BU_Combustion_Remazel_B4.docx` |
| `Guida_Produzione_T080100_B3.docx` | `Guida_Produzione_Remazel_B4.docx` |
| `Guida_Concettuale_T080100_v6.docx` | `Guida_Concettuale_Remazel_B7.docx` |
| `Audit_T080100_Rev2.docx` | `Audit_Remazel_B3.docx` |

Se due documenti diversi finirebbero con lo stesso nome (es. una guida per T08 e una per
T09), l'oggetto va reso più specifico con una parola descrittiva, non con il codice commessa.

---

## 3. Migrazione dei documenti in blu

I 13 documenti correnti del 15/09/2026 sono nella **vecchia grafica Remazel**:
- titoli blu `2E74B5`
- header con testo "Start I.T. S.r.l." al posto del logo
- footer a paragrafo singolo
- margine superiore 1134

Non si ritoccano per restare in blu. **Quando un documento va aggiornato, passa alla grafica
`docx-startit`**:

1. estrarre il contenuto (testo, tabelle, box) dal documento esistente;
2. rigenerarlo con `startit_docx.py` (§5), invece di correggere l'XML vecchio: correggere a
   mano colori, margini e header di un documento vecchio è la strada che produce le derive
   di formato;
3. applicare le modifiche di contenuto richieste;
4. nuovo nome secondo §2, verifica completa secondo `docx-startit` §15.

Fino al loro aggiornamento, i documenti in blu restano validi così come sono.

### Valori superati — non usare più
| Elemento | Valore vecchio | Valore attuale |
|---|---|---|
| Colore titoli e indice | `2E74B5` | `757F9B` |
| Heading 2 | 13pt | 12pt |
| Header colonna 1 | testo `Start I.T. S.r.l.` | logo `logo_startit.png` |
| Footer | tabella a 3 celle / paragrafo singolo | 2 righe, 8pt `888888`, `Pag.` a destra |
| Tabella info | 2500/7000, campo Commessa | 2384/6676, campo Riferimento |
| Indice | `TOC \o "1-2"` o `"1-3"` | `TOC \o "1-4" \h \z \u` |
| Margine superiore | 1134 | 1620 |
| Naming | prefisso `ERPNext_`, codice commessa, `_v{N}` | `{Tipo}_{Oggetto}_Remazel_B{N}` |
| Riferimento impaginazione | `Analisi_Obiettivi_BU_Combustion_B2.docx` | template e generatore di `docx-startit` |

---

## 4. Regole di contenuto e di tono

**Destinatari e nomi**
- Nei documenti formali il destinatario è indicato come **ufficio/funzione**, mai con nomi
  propri (es. `Responsabile Produzione`, non il nome della persona).
- Stesso criterio nel corpo: ruoli, non persone.

**Tono verso il cliente**
- Soft ma fermo. I vincoli si presentano come **disponibilità del dato** (dato mancante,
  dato da confermare), mai come limite di sviluppo o come lamentela.
- Numeri significativi e difendibili: mai tecnicamente corretti ma fuorvianti.
- Non rispiegare concetti che l'interlocutore conosce già (es. la differenza fra Job e
  commessa).

**Dati provvisori**
Qualsiasi dato inventato o segnaposto è etichettato in modo inequivocabile nel documento:
`PLACEHOLDER-T08-xxxx`, `99-99999`, "SEGNAPOSTO", `F000 (grezzo di fusione provvisorio)`.
Mai presentarlo come dato reale.

**Terminologia**
Italiano dove esiste un termine consolidato (commessa, ciclo di lavorazione, distinta base,
conto lavoro). Restano in inglese i nomi di sistema e dei doctype (Work Order, Job Card,
BOM, Production Plan, Workstation, Server Script).

**Flusso di lavoro con Gian**
Prima si propone la **struttura** (titoli e contenuto previsto per sezione), si scrive solo
dopo l'approvazione. Un documento alla volta, con controllo del risultato prima del successivo.

---

## 5. Produzione con il generatore di docx-startit

```python
import sys
sys.path.insert(0, '<cartella skill docx-startit>/scripts')
import startit_docx as s

nome = 'Analisi_Integrazione_SAP_Remazel_B1.docx'
meta = {
    'Documento':    nome,
    'Versione':     'Bozza 1 — 28 settembre 2026',
    'Data':         '28 settembre 2026',
    'Redatto da':   'Start I.T. S.r.l.',
    'Destinatario': 'Remazel Engineering S.p.A. — BU Combustion',
    'Sistema':      'M.E.S. Remazel',
    'Riferimento':  'ERPNext — combustionerp.remazel.com',
    'Stato':        'Bozza operativa',
}
contenuto = [
    ('h', 1, '1. Titolo sezione'),
    ('p', 'Testo con **grassetto**.'),
    ('bullets', ['**Concetto** spiegazione', 'Altra voce']),
    ('table', [2400, 6660], ['Colonna', 'Colonna'], [['a', 'b']]),
    ('box', 'nota', 'Titolo box', ['Testo.']),      # nota | criticita | positivo | info
    ('steps', [('Titolo passo', ['Dettaglio 1', 'Dettaglio 2'])]),
    ('code', ['bench --site site1.local console']),
]
doc = s.Documento(meta,
                  ['TITOLO RIGA 1', 'TITOLO RIGA 2'],
                  ['Riga descrittiva', 'Remazel Engineering S.p.A. — BU Combustion'],
                  contenuto)
s.scrivi(doc, nome, 'Remazel Engineering S.p.A.', 'Oggetto breve')
```

Le colonne di ogni tabella devono sommare a **9060**. Codici, comandi e script vanno nel
riquadro `code` (Courier New), specificando sempre **dove** vanno eseguiti (bash come
`frappe-user` in `/home/frappe-user/frappe-bench`, oppure `bench --site site1.local console`).

### Numeri di pagina dell'indice (due passate)
```python
import subprocess
s.scrivi(doc, nome, 'Remazel Engineering S.p.A.', 'Oggetto breve')            # passata 1
subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', nome], check=True)
testo = subprocess.run(['pdftotext', '-layout', nome.replace('.docx', '.pdf'), '-'],
                       capture_output=True, text=True).stdout.split('\f')
pagine = {}
for it in contenuto:
    if it[0] == 'h':
        for n in range(2, len(testo)):             # dalla pagina 3: salta copertina e indice
            if it[2] in testo[n]:
                pagine[it[2]] = n + 1
                break
s.scrivi(doc, nome, 'Remazel Engineering S.p.A.', 'Oggetto breve', pagine=pagine)  # passata 2
```
Se l'indice occupa più di una pagina, far partire il ciclo dalla prima pagina del corpo
(altrimenti i titoli vengono trovati nelle voci dell'indice). Poi validazione, conversione
finale e controllo visivo di **ogni** pagina (`docx-startit` §13 e §15).

---

## 6. Note d'ambiente (container Claude Code)

Nei container di Claude Code gli strumenti di verifica possono mancare. Controllare e installare
prima di iniziare:

```bash
dpkg -l libreoffice-writer >/dev/null 2>&1 || apt-get install -y --no-install-recommends libreoffice-writer
which pdftoppm >/dev/null || apt-get install -y poppler-utils
python3 -c "import defusedxml" 2>/dev/null || pip install -q defusedxml lxml
```

- Con il solo `libreoffice-core` installato, `soffice` risponde *"source file could not be
  loaded"* anche con un file di testo: manca `libreoffice-writer`.
- Il validatore sta nella skill `docx`: `.../docx/scripts/office/validate.py <file>.docx`.
- Il generatore scrive in `/tmp/_build_docx`: si esegue da una cartella di lavoro
  (scratchpad), mai dalla cartella della skill, che è di sola lettura.

---

## 7. Dove vivono i documenti

- Struttura di progetto su SharePoint: sito StartIT →
  `Documenti condivisi/Clienti/Remazel/Progetti/Remazel-Combustion/01_Documentazione`
  (una sola versione per famiglia). Le versioni superate stanno in `remazel-comb.rar`.
- Il connettore Microsoft 365 è di **sola lettura**: i file prodotti li carica Gian a mano.
- Per modificare un documento esistente serve il file `.docx` caricato nella sessione.
