# Contesto — Progetto M.E.S. Remazel (BU Combustion)

Prima azione di ogni sessione: leggere per intero `12_Memorie/CONTESTO_PROGRESSIVO_ERPNext.md`
(stato ERPNext, standard documentale, regole operative, task aperti) e confermare a Gian
cosa si è capito prima di agire. Non ripetere passi già confermati come eseguiti.

## Riferimenti rapidi
- Cliente: Remazel Engineering S.p.A. — BU Combustion. Contatto primario: Responsabile Produzione
- Fornitore: Start I.T. S.r.l. — Gian, lead implementor
- Server ERPNext: cs-erp01 (host SSH `combustionerp.remazel.com`), bench
  `/home/frappe-user/frappe-bench`, sito `site1.local`, HTTPS attivo
  ⚠️ Nessun accesso SSH diretto da qui: i comandi li esegue Gian e incolla l'output.
  Indicare sempre **dove** va eseguito il codice: bash come `frappe-user`, oppure
  `bench --site site1.local console`
- Equipment: T08-0100 (Job 24-19006, pilota a regime) · T09-0100 (Job 26-19008, in importazione)
- Go-live target: 30/09/2026

## Regole operative (sempre valide)
- Italiano, diretto e conciso, senza preamboli
- Esecuzione passo-passo con verifica prima di ogni modifica
- Riscrivere sempre file completi, mai snippet parziali
- Prima di generare un documento: proporre la struttura e attendere l'approvazione.
  Un documento alla volta, con controllo del risultato prima del successivo
- Ogni variante di documento ha il numero di versione nel nome: mai sovrascrivere senza incrementare

## Documenti Word
- Standard unico **`docx-startit`**: caricare sempre prima la skill `docx-startit`
  (grafica, logo, template, generatore `startit_docx.py`, verifica in 15 punti),
  poi la skill `docx-remazel`, che contiene solo le regole Remazel
- Il testo aggiornato di `docx-remazel` è in `12_Memorie/SKILL_docx-remazel.md`: se la skill
  caricata non coincide con quel file (es. prescrive titoli blu `2E74B5` o il footer a
  paragrafo singolo), fa fede il file in `12_Memorie`
- Valori Remazel: Sistema = **M.E.S. Remazel** (mai E.M.S. né M.S.E.), Destinatario =
  `Remazel Engineering S.p.A. — BU Combustion`, naming `{Tipo}_{Oggetto}_Remazel_B{N}.docx`
  senza codice commessa
- I 13 documenti in `01_Documentazione` sono nella vecchia grafica blu: all'aggiornamento
  si rigenerano nello standard `docx-startit`
- Prima di generare, verificare che sul PC ci siano Python 3 e LibreOffice (per PDF di
  verifica e validazione); se mancano, dirlo a Gian prima di procedere

## Struttura cartella
- `00_Script_Progetto/` — script ERPNext + utilità documentali
- `01_Documentazione/` — SOLO i documenti correnti (una versione per famiglia)
  - `Dati/` — xlsx a supporto
  - `Email_Simone/`
- `03_Database/` — sql
- `12_Memorie/` — memoria di progetto e standard documentale
  - `Old/` — versioni superate, da non usare
- `99_Transito/`, `Transfer/`, `_CESTINO/` — materiale in transito, non toccare senza indicazione

`LEGGIMI.md` descrive la struttura al 15/09/2026: i suoi punti 5-6 e la "Nota sul footer"
sono superati dal contesto progressivo.

## A fine sessione
Aggiornare `12_Memorie/CONTESTO_PROGRESSIVO_ERPNext.md` aggiungendo in fondo la sezione della
sessione (`## SESSIONE N — titolo (data)`), aggiornare i task aperti, senza rimuovere le
sezioni precedenti.
