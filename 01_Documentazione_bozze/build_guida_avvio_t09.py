import sys, os, json
sys.path.insert(0, "/root/.claude/skills/synced/593ea5d8-9a85-4668-a3fb-0290e8e227e7_746b874a-eee2-4e96-b44c-f02049e430c1/docx-startit/scripts")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import startit_docx as S
from stima_pagine import stima_pagine

NOME = "Guida_Avvio_T09_Remazel_B2.docx"
meta = {
    "Documento": NOME,
    "Versione": "Bozza 2 — 6 ottobre 2026",
    "Data": "6 ottobre 2026",
    "Redatto da": "Start I.T. S.r.l.",
    "Destinatario": "Remazel Engineering S.p.A. — BU Combustion",
    "Sistema": "M.E.S. Remazel — ERPNext v16",
    "Riferimento": "T09-0100 (Job 26-19008) — PROJ-0002 — combustionerp.remazel.com",
    "Stato": "Bozza operativa — decisioni da completare",
}
titolo = ["GUIDA ALL'AVVIO", "DELLA T09-0100"]
sottotitolo = ["Percorso passo per passo dallo stato attuale", "all'uso del sistema in produzione",
               "Remazel Engineering S.p.A. — BU Combustion"]

C = []
h = lambda l, t: C.append(("h", l, t))
p = lambda t: C.append(("p", t))
bl = lambda items: C.append(("bullets", items))
tb = lambda cols, head, rows: C.append(("table", cols, head, rows))
bx = lambda k, t, ps: C.append(("box", k, t, ps))
st = lambda items: C.append(("steps", items))

DA = "Da decidere"

# ------------------------------------------------------------------ 1
h(1, "1. Scopo e modo d'uso")
p("La guida porta la T09-0100 dallo stato attuale del sistema all'uso quotidiano in produzione. Ogni passo indica la funzione che lo esegue, cosa fare, come verificarlo e lo stato al 6 ottobre 2026. I passi si eseguono nell'ordine; le funzioni non ancora pronte arrivano in corsa, senza fermare la produzione.")
p("Le istruzioni a video sono nel **Manuale Utente**; i concetti nella **Guida Concettuale**.")
tb([2200, 6860], ["Stato", "Significato"], [
    ["Fatto", "Già eseguito: non va rifatto"],
    ["Da fare", "Pronto per essere eseguito"],
    ["Da decidere", "Richiede una decisione prima di procedere"],
    ["In sviluppo", "Funzione che arriva in corsa"],
])

# ------------------------------------------------------------------ 2
h(1, "2. Punto di partenza")
p("Quanto segue è già a sistema per la T09 e **non va rifatto**.")
tb([3400, 4160, 1500], ["Elemento", "Situazione", "Stato"], [
    ["Cicli e distinte T09", "Codifica T08/T09 applicata; tempi interni e tempi di attraversamento esterni", "Fatto"],
    ["Ordine cliente e Project", "Sales Order con 6 righe di consegna; PROJ-0002 con Buffer Project 5 giorni", "Fatto"],
    ["Piani di produzione", "6 Production Plan, uno per set", "Fatto"],
    ["Work Order", "348 rilasciati (58 per set), date a ritroso dalla consegna", "Fatto"],
    ["Job Card", "Oltre 3.300 pianificate sulla capacità dei reparti; circa 770 esterne con fornitore", "Fatto"],
    ["Reparti e calendari", "Postazioni reali; Calendario Remazel e Calendario Fornitori 2026-2029", "Fatto"],
    ["Punti di monitoraggio", "42 Task (7 per set) collegati ai Work Order", "Fatto"],
    ["Monitoraggio", "Spazio di lavoro «Produzione Remazel», Master Plan, Gantt, carico reparti, indicatori", "Fatto"],
    ["Utenti", "21 operatori con accesso per reparto; profilo Responsabile Processo MES", "Fatto"],
    ["Ritardi", "Simula e Applica Ritardo con effetto sulla consegna del set", "Fatto"],
])

# ------------------------------------------------------------------ 3
h(1, "3. Verifiche iniziali")
p("Prima di coinvolgere i reparti. Funzione: **Amministratore del sistema** con la **Pianificazione di produzione**.")
tb([600, 3000, 3960, 1500], ["N.", "Verifica", "Esito atteso", "Stato"], [
    ["1", "Backup completo del sistema", "Copia del database e dei file, conservata fuori dal server", "Da fare"],
    ["2", "Numeri per set", "58 Work Order per set; Job Card coerenti; differenza 3.330 / 3.306 spiegata", "Da fare"],
    ["3", "Fornitore sulle fasi esterne", "Nessuna Job Card esterna senza fornitore", "Da fare"],
    ["4", "Fine set contro consegna", "Set 3-6 entro consegna − buffer; set 1-2 da allineare (capitolo 4)", "Da fare"],
    ["5", "Chiusura dei Work Order", "Scarico di produzione registrabile senza trasferimento di materiale", "Da fare"],
    ["6", "Percorso a video", "Spazio di lavoro, Gantt, Job Card, Simula Ritardo funzionanti dal browser", "Da fare"],
])

# ------------------------------------------------------------------ 4
h(1, "4. Allineamento dei set 1 e 2")
p("I set 1 e 2 sono in produzione da maggio, ma il sistema li ha pianificati come se partissero il 2 ottobre. Finché lo stato reale non è registrato, date e ritardi di questi set non sono attendibili.")
st([
    ["Modulo", ["L'amministratore del sistema estrae dal sistema il modulo Excel di rilevazione: una riga per ogni fase dei set 1 e 2, con Work Order, articolo, codice e descrizione della fase, reparto."]],
    ["Rilevazione", ["La Pianificazione di produzione compila per ogni fase: eseguita (Sì / No / In corso), data di fine reale; per le esterne in corso: data di uscita, n° ordine SAP, data promessa.", "Funzione responsabile e data: " + DA + "."]],
    ["Caricamento", ["L'amministratore del sistema carica il modulo: fasi eseguite chiuse con le date reali, fasi esterne in corso registrate presso il fornitore. Prima una prova che elenca le modifiche, poi la scrittura."]],
    ["Ripianificazione", ["Le fasi ancora da eseguire ripartono dallo stato reale; il sistema ricalcola la fine di ciascun set."]],
    ["Verifica", ["Master Plan e Gantt dei set 1 e 2: fine prevista contro consegna. Eventuali ritardi residui si governano con Simula Ritardo."]],
])

# ------------------------------------------------------------------ 5
h(1, "5. Regole di reparto")
p("Da fissare prima dell'avvio, perché ogni reparto registri allo stesso modo. Funzione: **Pianificazione di produzione**.")
tb([3200, 3860, 2000], ["Regola", "Proposta", "Stato"], [
    ["Conferma delle Job Card completate", "Il responsabile di reparto o la Pianificazione, ogni giorno, in blocco dall'elenco", DA],
    ["Fase aperta a fine turno", "Pause a fine turno, Resume alla ripresa", DA],
    ["Più operatori sulla stessa fase", "Ciascuno avvia la scheda con il proprio nome", DA],
    ["Esito dei controlli qualità", "Nei commenti della Job Card, fino alla validazione del template", DA],
    ["Fase iniziata prima della precedente", "Ammessa con avviso; valutata dal responsabile", DA],
])

# ------------------------------------------------------------------ 6
h(1, "6. Preparazione degli utenti")
tb([600, 3400, 3560, 1500], ["N.", "Attività", "Funzione", "Stato"], [
    ["1", "Consegna delle credenziali agli operatori, una per persona", "Pianificazione di produzione", "Da fare"],
    ["2", "Formazione degli operatori del reparto pilota (30 minuti, sulle Job Card reali)", "Pianificazione di produzione", "Da fare"],
    ["3", "Formazione della Pianificazione: Master Plan, Gantt, ritardi, conferma Job Card", "Amministratore del sistema", "Da fare"],
    ["4", "Formazione di chi segue le lavorazioni esterne", "Amministratore del sistema", "Da fare"],
    ["5", "Copia del Manuale Utente disponibile in reparto", "Pianificazione di produzione", "Da fare"],
])

# ------------------------------------------------------------------ 7
h(1, "7. Avvio nel reparto pilota")
p("Reparto pilota e referente: **" + DA + "**. Proposta: Controllo Qualità (molte fasi brevi, pochi operatori) oppure Saldatura (reparto più carico).")
st([
    ["Partenza", ["Dal giorno concordato ogni fase del reparto pilota si registra sulla Job Card: Start, Pause/Resume, Complete con la quantità."]],
    ["Controllo giornaliero", ["Per le prime due settimane, 10 minuti al giorno fra referente e Pianificazione: Job Card aperte da ieri, fasi completate non confermate, avvisi di precedenza."]],
    ["Correzioni", ["Le anomalie si annotano e si correggono subito: regola non chiara, scheda mancante, tempo errato."]],
    ["Esito", ["Al termine del pilota: registrazioni complete e puntuali, nessun blocco ricorrente. Se l'esito è positivo si passa al capitolo 8."]],
])

# ------------------------------------------------------------------ 8
h(1, "8. Estensione agli altri reparti")
p("Un reparto alla volta, con la stessa sequenza: formazione, partenza, controllo giornaliero per una settimana. Ordine proposto: dal reparto con meno operatori a quello con più operatori, in modo da affinare le regole prima dei reparti più carichi.")

# ------------------------------------------------------------------ 9
h(1, "9. Lavorazioni esterne")
p("Modalità nel periodo transitorio: **" + DA + "**.")
tb([2800, 3460, 2800], ["Opzione", "Come funziona", "Effetto"], [
    ["A — Transitoria sulla Job Card", "N° ordine SAP e data promessa sulla Job Card; Start alla spedizione, Complete al rientro", "Esterne subito visibili e ritardi calcolati; una registrazione per Job Card"],
    ["B — Fuori dal sistema", "Le esterne restano seguite come oggi fino all'Ordine conto lavoro", "Nessun lavoro aggiuntivo; le date delle esterne restano quelle pianificate"],
])
bx("nota", "In arrivo", [
    "**Ordine conto lavoro**: raggruppa le fasi inviate allo stesso fornitore e registra spedizione e rientro con un'unica azione, senza operatore. Con il cruscotto delle esterne (scadute, in scadenza, tutte) e, appena disponibile l'accesso, la lettura dei movimenti da SAP.",
])

# ------------------------------------------------------------------ 10
h(1, "10. Routine di controllo")
tb([1900, 4360, 2800], ["Frequenza", "Cosa", "Dove"], [
    ["Ogni giorno", "Job Card completate da confermare; Job Card ferme; fasi esterne con rientro previsto superato", "Elenco Job Card con filtri"],
    ["Ogni settimana", "Fine prevista di ogni set contro consegna; saturazione dei reparti nelle settimane successive; ritardi da simulare", "Master Plan, Gantt del set, Carico Reparti Settimanale"],
    ["Ogni mese", "Tempi effettivi contro tempi pianificati delle fasi più ricorrenti; aggiornamento dei calendari", "Job Card, calendari"],
])
p("Controllo settimanale di 30 minuti con Pianificazione di produzione e amministratore del sistema: giorno e partecipanti **" + DA + "**.")

# ------------------------------------------------------------------ 11
h(1, "11. Chiusura dei Work Order e dei set")
st([
    ["Work Order", ["Quando tutte le Job Card sono confermate: scarico di produzione (Finish). Il Work Order passa a Completed e il componente è disponibile per l'assieme superiore."]],
    ["Prodotto finito", ["Alla chiusura del Work Order di A0001 si assegna la matricola provvisoria; la matricola definitiva va nel campo «Matricola reale»."]],
    ["Set", ["Quando tutti i Work Order del set sono Completed, il set è chiuso: si confronta la fine reale con la consegna e il buffer."]],
])

# ------------------------------------------------------------------ 12
h(1, "12. Cosa arriva in corsa")
tb([3600, 3460, 2000], ["Funzione", "Beneficio", "Stato"], [
    ["Ordine conto lavoro e cruscotto esterne", "Esterne gestite per fornitore, ritardi in evidenza", "In sviluppo"],
    ["Lettura dei movimenti da SAP", "Spedizioni e rientri senza doppia registrazione", "In sviluppo"],
    ["Pianificazione a ritroso e punti di monitoraggio da interfaccia", "Autonomia sui prossimi ordini", "In sviluppo"],
    ["Import/export del ciclo da Excel", "Modifica agile dei cicli", "In sviluppo"],
    ["Documenti di fase e stampa della scheda", "Scheda completa in reparto", "Da decidere"],
    ["Timbratura con codice a barre", "Registrazione più rapida", "Da decidere"],
    ["Lotto materiale", "Tracciabilità della colata", "Da decidere"],
    ["Etichette in inglese", "Lingua finale del sistema", "Fase successiva"],
])

# ------------------------------------------------------------------ 13
h(1, "13. Riepilogo delle decisioni")
tb([600, 4460, 2200, 1800], ["N.", "Decisione", "Funzione", "Data"], [
    ["1", "Rilevazione dello stato reale dei set 1 e 2", "", ""],
    ["2", "Reparto pilota e referente", "", ""],
    ["3", "Regole di reparto (capitolo 5)", "", ""],
    ["4", "Lavorazioni esterne nel periodo transitorio (capitolo 9)", "", ""],
    ["5", "Utente SAP di sola lettura e informazioni sul conto lavoro in SAP", "", ""],
    ["6", "Controllo settimanale: giorno e partecipanti", "", ""],
])

doc = S.Documento(meta, titolo, sottotitolo, C)
OUT = "/home/user/AI-Project/01_Documentazione_bozze/" + NOME
pagine = stima_pagine(C)
json.dump(pagine, open("/home/user/AI-Project/01_Documentazione_bozze/pagine_avvio_t09.json", "w"), ensure_ascii=False, indent=0)
S.scrivi(doc, OUT, "Remazel Engineering S.p.A.", "Guida Avvio T09-0100", pagine)
print(OUT, "pagine stimate:", max(pagine.values()))
