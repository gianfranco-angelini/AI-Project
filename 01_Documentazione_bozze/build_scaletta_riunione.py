import sys, os, json
sys.path.insert(0, "/root/.claude/skills/synced/593ea5d8-9a85-4668-a3fb-0290e8e227e7_746b874a-eee2-4e96-b44c-f02049e430c1/docx-startit/scripts")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import startit_docx as S
from stima_pagine import stima_pagine

NOME = "Scaletta_Riunione_Avvio_T09_Remazel_B2.docx"
meta = {
    "Documento": NOME,
    "Versione": "Bozza 2 — 6 ottobre 2026",
    "Data": "6 ottobre 2026",
    "Redatto da": "Start I.T. S.r.l.",
    "Destinatario": "Documento interno",
    "Sistema": "M.E.S. Remazel — ERPNext v16",
    "Riferimento": "T09-0100 (Job 26-19008) — riunione di avvio",
    "Stato": "Uso interno",
}
titolo = ["SCALETTA RIUNIONE", "AVVIO T09-0100"]
sottotitolo = ["Traccia per la presentazione dell'avvio", "e per le decisioni da prendere", "Documento interno"]

C = []
h = lambda l, t: C.append(("h", l, t))
p = lambda t: C.append(("p", t))
bl = lambda items: C.append(("bullets", items))
tb = lambda cols, head, rows: C.append(("table", cols, head, rows))
bx = lambda k, t, ps: C.append(("box", k, t, ps))

h(1, "1. Messaggio chiave")
bx("positivo", "Da dire in apertura e in chiusura", [
    "«La T09 può partire adesso con quello che c'è. Il resto lo aggiungiamo mentre la produzione va avanti, senza fermarla.»",
])

h(1, "2. Scaletta (45 minuti)")
tb([1000, 2600, 5460], ["Tempo", "Punto", "Cosa dire o mostrare"], [
    ["5'", "Dove siamo", "6 obiettivi su 12 completati; T09 pianificata: 6 set, 348 Work Order, oltre 3.300 Job Card; 21 operatori con accesso per reparto"],
    ["10'", "Dimostrazione", "Produzione Remazel → Gantt di un set → una Job Card (descrizione, fornitore) → Pianificazione → Simula Ritardo (solo Simula, non Applica) → effetto sulla consegna"],
    ["10'", "Il go", "Cosa parte subito e cosa arriva dopo (capitolo 3)"],
    ["15'", "Decisioni", "Le sei decisioni del capitolo 4: per ognuna funzione responsabile e data"],
    ["5'", "Chiusura", "Rilettura delle decisioni; primo controllo settimanale in calendario"],
])

h(1, "3. Parte subito / arriva dopo")
tb([4530, 4530], ["Parte subito", "Arriva dopo, senza fermare la produzione"], [
    ["Pianificazione T09 (348 Work Order, 6 set)", "Ordine conto lavoro e cruscotto delle esterne"],
    ["Job Card nei reparti interni, da un reparto pilota", "Lettura dei movimenti da SAP"],
    ["Master Plan, Gantt per set, carico reparti", "Pianificazione a ritroso da interfaccia per i prossimi ordini"],
    ["Simula e Applica Ritardo", "Timbratura con codice a barre e stampa della scheda"],
    ["Matricola sul prodotto finito", "Lotto materiale, etichette in inglese"],
])

h(1, "4. Decisioni da prendere")
tb([600, 4460, 2200, 1800], ["N.", "Decisione", "Funzione", "Data"], [
    ["1", "Chi rileva lo stato reale dei set 1 e 2, e entro quando", "", ""],
    ["2", "Reparto pilota e suo referente", "", ""],
    ["3", "Chi conferma le Job Card completate; fasi aperte a fine turno; più operatori sulla stessa fase", "", ""],
    ["4", "Lavorazioni esterne nel frattempo: modalità transitoria sulla Job Card o fuori dal sistema fino all'Ordine conto lavoro", "", ""],
    ["5", "Utente SAP di sola lettura (IT) e informazioni sul conto lavoro in SAP (Acquisti)", "", ""],
    ["6", "Controllo settimanale di 30 minuti: giorno, ora, partecipanti", "", ""],
])

h(1, "5. Cosa dire e cosa evitare")
bx("info", "Da dire con chiarezza", [
    "**Il dato vale quanto le registrazioni**: se i reparti non chiudono le Job Card, il sistema mostra ritardi falsi. Per questo si parte da un reparto pilota.",
    "**I set 1 e 2 risultano in ritardo perché sono già in produzione**, non per un errore: si corregge con la rilevazione dello stato reale.",
    "**Magazzino, acquisti e prezzi restano in SAP**: ERPNext pianifica e misura, non duplica SAP.",
])
bx("criticita", "Da evitare", [
    "Date per Ordine conto lavoro e collegamento SAP: dipendono dall'accesso SAP e dalle informazioni degli Acquisti.",
    "«È tutto automatico»: la pianificazione dei prossimi ordini passa ancora dall'amministratore; per la T09 è già fatta.",
    "«Commessa» per indicare il Project: la commessa è il Job.",
    "Numeri precisi non verificati: per le Job Card «oltre 3.300».",
])

h(1, "6. Materiale")
tb([4530, 4530], ["Da distribuire", "Solo come riferimento"], [
    ["Riepilogo personalizzazioni e avvio (B1)", "Analisi Obiettivi BU Combustion (B4)"],
    ["Prerequisiti per il Go-Live (B2)", "Manuale Utente (B3), Guida Concettuale (B8)"],
])
bx("nota", "Prima di entrare", [
    "Provare nel browser il percorso della dimostrazione: spazio di lavoro, Gantt del set, Job Card, Simula Ritardo.",
])

h(1, "7. Link alle personalizzazioni")
p("Collegamenti diretti al sistema (accesso con le proprie credenziali). Nel file Word: Ctrl + clic per aprire.")
h(2, "7.1 Per la dimostrazione")
tb([2900, 6160], ["Cosa", "Link"], [
    ["Spazio di lavoro", "https://combustionerp.remazel.com/app/produzione-remazel"],
    ["Master Plan (Gantt Project)", "https://combustionerp.remazel.com/app/project/view/gantt"],
    ["Project T09-0100", "https://combustionerp.remazel.com/app/project/PROJ-0002"],
    ["Gantt Work Order T09", "https://combustionerp.remazel.com/app/work-order/view/gantt?project=PROJ-0002"],
    ["Gantt punti di monitoraggio T09", "https://combustionerp.remazel.com/app/task/view/gantt?project=PROJ-0002"],
    ["Job Card T09", "https://combustionerp.remazel.com/app/job-card?project=PROJ-0002"],
    ["Job Card per Simula Ritardo", "https://combustionerp.remazel.com/app/job-card/PO-JOB05552"],
    ["Esterne presso fornitore", "https://combustionerp.remazel.com/app/job-card?custom_stato_cl=Presso%20fornitore"],
    ["Carico Reparti Settimanale", "https://combustionerp.remazel.com/app/query-report/Carico%20Reparti%20Settimanale"],
])
h(2, "7.2 Impostazioni e personalizzazioni")
tb([2900, 6160], ["Cosa", "Link"], [
    ["Reparti (postazioni, calendario)", "https://combustionerp.remazel.com/app/workstation"],
    ["Calendario Remazel", "https://combustionerp.remazel.com/app/holiday-list/Calendario%20Remazel%202026-2029"],
    ["Calendario Fornitori", "https://combustionerp.remazel.com/app/holiday-list/Calendario%20Fornitori%202026-2029"],
    ["Impostazioni produzione", "https://combustionerp.remazel.com/app/manufacturing-settings"],
    ["Production Plan", "https://combustionerp.remazel.com/app/production-plan"],
    ["Distinte base", "https://combustionerp.remazel.com/app/bom"],
    ["Indicatori (Number Card)", "https://combustionerp.remazel.com/app/number-card"],
    ["Grafici (Dashboard Chart)", "https://combustionerp.remazel.com/app/dashboard-chart"],
    ["Menu laterale", "https://combustionerp.remazel.com/app/workspace-sidebar/Produzione%20Remazel"],
    ["Operatori (Employee)", "https://combustionerp.remazel.com/app/employee"],
    ["Permessi per reparto", "https://combustionerp.remazel.com/app/user-permission"],
    ["Matricole (Serial No)", "https://combustionerp.remazel.com/app/serial-no"],
    ["Campi Job Card (Personalizza modulo)", "https://combustionerp.remazel.com/app/customize-form?doc_type=Job%20Card"],
    ["Script lato server", "https://combustionerp.remazel.com/app/server-script"],
    ["Script lato client", "https://combustionerp.remazel.com/app/client-script"],
])
bx("criticita", "In dimostrazione", [
    "Sulla Job Card usare solo **Simula Ritardo**: Applica Ritardo modifica le date pianificate.",
])

doc = S.Documento(meta, titolo, sottotitolo, C)
OUT = "/home/user/AI-Project/01_Documentazione_bozze/" + NOME
pagine = stima_pagine(C)
S.scrivi(doc, OUT, "Documento interno", "Scaletta riunione avvio T09", pagine)
from linkify import linkify
print(OUT, "pagine stimate:", max(pagine.values()), "link:", linkify(OUT))
