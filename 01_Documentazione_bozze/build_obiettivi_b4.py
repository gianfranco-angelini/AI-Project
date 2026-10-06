import sys, os, json
sys.path.insert(0, "/root/.claude/skills/synced/593ea5d8-9a85-4668-a3fb-0290e8e227e7_746b874a-eee2-4e96-b44c-f02049e430c1/docx-startit/scripts")
import startit_docx as S

NOME = "Analisi_Obiettivi_BU_Combustion_B4.docx"
meta = {
    "Documento": NOME,
    "Versione": "Bozza 4 — 6 ottobre 2026",
    "Data": "6 ottobre 2026",
    "Redatto da": "Start I.T. S.r.l.",
    "Destinatario": "Remazel Engineering S.p.A. — BU Combustion",
    "Sistema": "M.E.S. Remazel — ERPNext v16",
    "Riferimento": "T09-0100 (Job 26-19008) · T08-0100 (Job 24-19006) — combustionerp.remazel.com",
    "Stato": "Bozza operativa",
}
titolo = ["ANALISI OBIETTIVI", "SISTEMA BU COMBUSTION"]
sottotitolo = ["Stato di realizzazione dei dodici obiettivi su ERPNext v16", "e piano delle attività residue",
               "Remazel Engineering S.p.A. — BU Combustion"]
C = []
h = lambda l, t: C.append(("h", l, t))
p = lambda t: C.append(("p", t))
bl = lambda items: C.append(("bullets", items))
tb = lambda cols, head, rows: C.append(("table", cols, head, rows))
bx = lambda k, t, ps: C.append(("box", k, t, ps))

def obiettivo(num, titolo_, intest, richiesta, stato, resta, box_=None):
    h(2, num + " " + titolo_)
    p("**" + intest + "**")
    p("**Richiesta:** " + richiesta)
    p("**Stato al 6 ottobre 2026**")
    bl(stato)
    if resta:
        p("**Cosa resta per chiudere il punto**")
        bl(resta)
    if box_:
        bx(*box_)

# 1
h(1, "1. Scopo del documento e metodo di valutazione")
p("Il documento aggiorna la Bozza 3 del 12 settembre 2026 e risponde punto per punto al documento «Sistema di Pianificazione e Monitoraggio della Produzione: Obiettivi e Priorità» trasmesso dalla BU Combustion, che elenca dodici obiettivi su tre aree con priorità alta, media o bassa.")
p("Rispetto alla Bozza 3 cambia la base di valutazione: la commessa di riferimento non è più solo la T08-0100 ma la **T09-0100**, caricata e pianificata a sistema con 6 set di consegna, 348 Work Order e 3.306 Job Card. Le valutazioni derivano dal sistema in esercizio su cs-erp01, non da un ambiente dimostrativo.")
tb([2200, 6860], ["Valutazione", "Significato"], [
    ["Nativo", "Funzione presente in ERPNext v16: richiede configurazione, non sviluppo"],
    ["Nativo + custom", "La base esiste; va completata con campi, report o automatismi"],
    ["Custom", "Non presente: sviluppata interamente dentro il modello dati della piattaforma"],
    ["Fuori portata", "Richiede un motore applicativo che ERPNext non possiede"],
])

# 2
h(1, "2. Richieste ricevute, ordinate per priorità")
tb([700, 1000, 7360], ["Punto", "Priorità", "Richiesta (formulazione della BU Combustion)"], [
    ["1a", "Alta", "«Visualizzazione delle commesse di BU nel tempo (es. diagramma di Gantt) [...] con visualizzazione globale della saturazione della BU nel tempo»"],
    ["1b", "Alta", "«Definire, per ogni prodotto (Equipment) i relativi punti di monitoraggio [...] per ogni commessa visualizzata sul Master Plan»"],
    ["2a", "Alta", "«Inserire, modificare ed eliminare cicli e fasi di produzione in maniera agile e veloce»"],
    ["2b", "Alta", "«Generare schede di lavoro per ogni fase di produzione, ognuna corredata di tutti i documenti necessari»"],
    ["1c", "Media", "«Ripianificare le commesse o alcune loro attività in maniera veloce [...] tramite un calendario»"],
    ["1d", "Media", "«Evidenziare automaticamente i periodi in cui la richiesta di risorse supera la capacità della BU»"],
    ["2c", "Media", "«Timbrare le fasi di produzione svolte tramite un codice a barre [...] il sistema ricava il tempo impiegato»"],
    ["3", "Media", "«Tenere sotto controllo le lavorazioni presso fornitori ed i relativi tempi di invio e ricezione merce»"],
    ["1e", "Bassa", "«Al verificarsi di situazioni di sovraccarico, proporre soluzioni alternative di pianificazione»"],
    ["1f", "Bassa", "«Creare dashboard e KPI per monitorare lo stato della produzione e l'avanzamento delle commesse»"],
    ["1g", "Bassa", "«Definire dei buffer all'interno di ogni prodotto (Equipment)»"],
    ["2d", "Bassa", "«Gestire la produzione in lotti e generare numeri di serie per l'identificazione dei componenti»"],
])

# 3
h(1, "3. Quadro di sintesi")
tb([700, 900, 1700, 1700, 4060], ["Ob.", "Priorità", "Stato B3 (12/09)", "Stato B4 (06/10)", "Sintesi"], [
    ["1a", "Alta", "Parziale", "Completato", "Master Plan multi-commessa e saturazione su tutte le commesse"],
    ["1b", "Alta", "Parziale", "Completato", "Punti di monitoraggio generati dalla distinta, legati ai Work Order"],
    ["2a", "Alta", "Parziale", "In corso", "Cicli completi con tempi reali; manca l'import da Excel per l'utente"],
    ["2b", "Alta", "Parziale", "In corso", "Infrastruttura documentale pronta; mancano documenti e stampa"],
    ["1c", "Media", "Da realizzare", "Completato", "Ritardo con propagazione ai Work Order padre e verifica consegna set"],
    ["1d", "Media", "Completato", "Completato", "Report di carico su calendario aggiornato"],
    ["2c", "Media", "Da realizzare", "Da avviare", "Prerequisiti presenti (operatori, accessi per reparto)"],
    ["3", "Media", "Da realizzare", "In corso", "Fornitore e conto lavoro su Job Card; Ordine conto lavoro e SAP da completare"],
    ["1e", "Bassa", "Da riformulare", "Riformulato", "Coperto da simulazione (1c) e carico (1d)"],
    ["1f", "Bassa", "Completato", "Completato", "Indicatori estesi alla T09"],
    ["1g", "Bassa", "Da realizzare", "Completato", "Buffer per Project con ricalcolo automatico"],
    ["2d", "Bassa", "Parziale", "In corso", "Matricole decise; aperta la tracciabilità del lotto materiale"],
])
bx("positivo", "Sintesi", [
    "**Sei obiettivi su dodici sono completati** (erano due alla Bozza 3), quattro sono in corso con una base già utilizzabile, uno è da avviare e uno è stato riformulato.",
    "Tutti e quattro gli obiettivi a priorità alta hanno avuto avanzamenti: due sono chiusi (1a, 1b), due attendono principalmente informazioni da Remazel (documenti di fase per 2b, procedura di import condivisa per 2a).",
])

# 4
h(1, "4. Obiettivo 1 — Master Plan e Pianificazione della Produzione")
obiettivo("4.1", "1a — Master Plan di Business Unit", "Priorità alta — Nativo + custom — COMPLETATO",
    "visualizzazione delle commesse di BU nel tempo con Gantt e saturazione globale della BU.",
    ["Due commesse a sistema (T08-0100 e T09-0100), ciascuna con il proprio Project collegato a Work Order, Job Card, ordine e piani di produzione.",
     "Spazio di lavoro pubblico **«Produzione Remazel»** con menu dedicato: Gantt di tutte le commesse (Master Plan), Gantt dei Work Order e dei punti di monitoraggio per set.",
     "Report **«Carico Reparti Settimanale»** sulla somma di tutte le commesse aperte, con il calendario aziendale 2026-2029."],
    ["Caricamento delle altre commesse di BU: dipende dalle decisioni della Direzione BU, non dalla configurazione."])
obiettivo("4.2", "1b — Dettagli di commessa nel Master Plan", "Priorità alta — Nativo + custom — COMPLETATO",
    "punti di monitoraggio definiti per prodotto, con apertura a tendina delle sotto-attività sul Master Plan.",
    ["Per la T09: 42 punti di monitoraggio, per ogni set un gruppo e sei macro-assiemi (A1000, A2000, A3000, P4000, P5000, assemblaggio finale A0001) con dipendenze e date ricavate dai Work Order.",
     "Ogni Work Order è collegato al proprio punto di monitoraggio (campo dedicato): l'avanzamento delle fasi risale al punto.",
     "La struttura è generata automaticamente dall'albero di distinta: costituisce il **template per famiglia di prodotto** riutilizzabile per le commesse successive."],
    None)
obiettivo("4.3", "1c — Riprogrammazione agile delle commesse", "Priorità media — Custom — COMPLETATO",
    "ripianificare commesse o singole attività in modo rapido.",
    ["Funzioni **Simula Ritardo** e **Applica Ritardo** dal menu «Pianificazione» di ogni Job Card.",
     "Lo spostamento si propaga alle fasi successive dello stesso Work Order e ai **Work Order padre** fino al prodotto finito del set.",
     "Il risultato è confrontato con la **consegna del set** e con il buffer: il sistema segnala se il set resta nei tempi, consuma il buffer o supera la consegna."],
    ["Decisione sul comportamento in caso di sovraccarico di reparto generato dallo spostamento: bloccare oppure accettare e segnalare (oggi: accettato e visibile nel report 1d)."])
obiettivo("4.4", "1d — Visualizzazione dei sovraccarichi di capacità", "Priorità media — Custom — COMPLETATO",
    "evidenza automatica dei periodi in cui la richiesta supera la capacità.",
    ["Report «Carico Reparti Settimanale»: minuti pianificati contro capacità per reparto e settimana, con stato ok / attenzione / sovraccarico.",
     "Capacità reali dei reparti a sistema (Saldatura 7, Molatura 5, Montaggio 5, Controllo Qualità 3, Lavorazioni Meccaniche 1); le lavorazioni esterne sono escluse dal calcolo di saturazione."],
    None)
obiettivo("4.5", "1e — Proposta di pianificazioni alternative", "Priorità bassa — Fuori portata — RIFORMULATO",
    "proposta automatica di soluzioni in caso di sovraccarico.",
    ["La proposta automatica richiede un motore APS che ERPNext non possiede.",
     "La versione riformulata è disponibile: il pianificatore vede il sovraccarico (1d) e simula lo spostamento di una fase vedendone subito l'effetto sulla consegna del set (1c)."],
    ["Valutazione di un prodotto APS di terze parti, successiva all'avvio."])
obiettivo("4.6", "1f — Dashboard e KPI", "Priorità bassa — Nativo — COMPLETATO",
    "dashboard e KPI sullo stato della produzione e delle commesse.",
    ["Indicatori e grafici nello spazio di lavoro per T08 e T09: ordini, pezzi prodotti, Job Card aperte, avvio ordini per settimana, ordini per stato, carico per reparto.",
     "I componenti sono nativi e configurabili da interfaccia: nuovi indicatori si aggiungono senza sviluppo."],
    None)
obiettivo("4.7", "1g — Buffer di commessa", "Priorità bassa — Nativo + custom — COMPLETATO",
    "buffer definibili per prodotto.",
    ["Campo **Buffer Project** (giorni, default 5) sul singolo Project, modificabile per ordine.",
     "La scadenza interna (consegna meno buffer) si ricalcola a ogni salvataggio e guida la pianificazione a ritroso dei set."],
    None)

# 5
h(1, "5. Obiettivo 2 — Programmazione ed Avanzamento della Produzione")
obiettivo("5.1", "2a — Cicli di produzione", "Priorità alta — Nativo + custom — IN CORSO",
    "inserimento, modifica ed eliminazione agile di cicli e fasi.",
    ["Cicli T08 e T09 completi a sistema: codici fase dell'Ufficio Tecnico, fornitore strutturato sulle fasi esterne, tempi delle fasi esterne pari al tempo di attraversamento del lotto (TT) concordato con la Produzione.",
     "Regola di codifica T08/T09 definita: articolo identico → codice T08; diverso → codice T09 con il proprio ciclo.",
     "Il confronto tra file del ciclo e sistema è già automatizzato, ma eseguito da Start I.T."],
    ["Procedura di import del ciclo da Excel eseguibile dall'utente, con riepilogo delle differenze prima della conferma, ed export nello stesso formato."])
obiettivo("5.2", "2b — Schede di lavoro", "Priorità alta — Custom — IN CORSO",
    "schede di lavoro per fase corredate di documenti di qualità, disegni, direttive di saldatura.",
    ["Infrastruttura pronta: i documenti si associano una volta alla fase di distinta e compaiono in automatico su ogni Job Card generata.",
     "Le Job Card riportano descrizione di fase, consegna del set e piano di appartenenza."],
    ["Decisione su quali documenti associare a quali fasi, chi li mantiene e con quale codifica di revisione.",
     "Formato di stampa della scheda di lavoro (prerequisito anche del punto 2c)."])
obiettivo("5.3", "2c — Timbratura delle fasi di produzione", "Priorità media — Nativo + custom — DA AVVIARE",
    "timbratura con codice a barre e calcolo del tempo impiegato.",
    ["Il meccanismo nativo è quello richiesto: la Job Card registra inizio e fine e calcola il tempo.",
     "Prerequisito soddisfatto: 21 operatori con utente e accesso limitato alle Job Card del proprio reparto.",
     "Decisione già presa: postazioni operatore fisse con monitor industriale e lettori cablati."],
    ["Codice a barre sulla scheda stampata (dopo il punto 2b) e schermata di reparto ridotta (lettura codice, avvio/chiusura fase).",
     "Regole per i casi anomali: fase aperta a fine turno, ripresa il giorno successivo, più operatori sulla stessa fase.",
     "Le lavorazioni esterne non si timbrano: sono gestite dall'obiettivo 3."])
obiettivo("5.4", "2d — Lotti e numeri di serie", "Priorità bassa — Nativo + custom — IN CORSO",
    "produzione in lotti e numeri di serie per l'identificazione.",
    ["Deciso: **matricola e marcatura solo sul prodotto finito**, assegnate a fine produzione con numerazione provvisoria; campo per la matricola definitiva senza rinominare il documento.",
     "Il **lotto di produzione** coincide con il set di consegna: ogni Work Order e Job Card ne riporta il riferimento.",
     "Template di controllo saldature (40 parametri) predisposto."],
    ["Tracciabilità del **lotto materiale** (colata/certificato): campo dedicato **non obbligatorio** oppure lettura da SAP; da definire quali livelli tracciare.",
     "Validazione del template saldature e suo collegamento al prodotto finito."])

# 6
h(1, "6. Obiettivo 3 — Expediting delle lavorazioni esterne")
p("**Priorità media — Custom — IN CORSO**")
p("Il ciclo della T09 conta circa 21.400 ore di attraversamento presso fornitori per set da 10 liner: le lavorazioni esterne determinano il rispetto delle date di consegna più di qualsiasi altro fattore.")
p("**Stato al 6 ottobre 2026**")
bl(["Fornitore strutturato su tutte le 165 fasi esterne di distinta e riportato in automatico sulle 768 Job Card esterne della T09.",
    "Sezione «Conto lavoro» sulla Job Card: n° ordine SAP, data promessa dal fornitore, uscita, rientro previsto e stato (Da inviare / Presso fornitore / Rientrato).",
    "Tempi delle fasi esterne pari al lead time del fornitore comprensivo di trasporto; calendario delle chiusure dei fornitori allineato a quello di Remazel.",
    "Decisione sul modello: l'ordine al fornitore resta emesso da SAP, dove sono gestiti anche i magazzini dei fornitori; ERPNext traccia invio, rientro e ritardi."])
p("**Cosa resta per chiudere il punto**")
bl(["**Ordine conto lavoro**: raggruppa le fasi inviate allo stesso fornitore, registra spedizione e rientro con un'unica azione e completa in automatico le Job Card al rientro.",
    "**Cruscotto expediting**: fasi da ordinare, presso fornitore, in ritardo; evidenza delle fasi a cavallo dei periodi di chiusura.",
    "**Collegamento con SAP** in sola lettura per i movimenti verso e dai magazzini fornitore; in prospettiva emissione dell'ordine da ERPNext verso SAP."])

# 7
h(1, "7. Piano delle attività residue")
tb([600, 2600, 1100, 4760], ["Fase", "Intervento", "Priorità", "Note"], [
    ["1", "3 — Ordine conto lavoro e cruscotto", "Media", "Massimo impatto sul rispetto delle consegne; base dati già pronta"],
    ["2", "Subentro in corsa set 1-2", "—", "Modulo di rilevazione dello stato reale e allineamento; rende attendibili date e ritardi"],
    ["3", "2a — Import/export del ciclo", "Alta", "Rende autonoma la gestione dei cicli per le commesse successive"],
    ["4", "2b — Documenti e stampa scheda", "Alta", "Subordinato alla decisione su documenti e revisioni"],
    ["5", "2c — Timbratura", "Media", "Dopo la stampa della scheda (2b)"],
    ["6", "2d — Lotto materiale", "Bassa", "Campo non obbligatorio o lettura da SAP"],
    ["7", "3 — Collegamento SAP", "Media", "Subordinato all'accesso in sola lettura al database SAP"],
])

# 8
h(1, "8. Punti da decidere")
tb([2400, 4560, 2100], ["Punto", "Decisione richiesta", "Funzione"], [
    ["Commesse nel Master Plan", "Quali commesse di BU caricare oltre T08 e T09, con quale dettaglio e in quale ordine", "Direzione BU"],
    ["Documentazione di fase", "Quali documenti associare a quali fasi, chi li mantiene, codifica delle revisioni", "Ufficio Tecnico"],
    ["Timbratura", "Regole per fasi aperte a fine turno, riprese e più operatori", "Pianificazione di produzione"],
    ["Lotto materiale", "Livelli da tracciare e fonte del numero di colata", "Qualità"],
    ["Ripianificazione", "Comportamento in caso di sovraccarico generato da uno spostamento", "Pianificazione di produzione"],
    ["Avanzamento set 1-2", "Stato reale delle fasi già eseguite", "Pianificazione di produzione"],
    ["Conto lavoro in SAP", "Documenti usati, codice del pezzo a metà ciclo, magazzini fornitore", "Acquisti"],
    ["Accesso SAP", "Utente di sola lettura sul database e accesso al Service Layer", "IT"],
])

# 9
h(1, "9. Nota conclusiva")
p("Dalla Bozza 3 il sistema è passato da una commessa pilota a una commessa in esercizio, la T09-0100, interamente pianificata sulla capacità reale dei reparti e sui tempi reali dei fornitori. Sei obiettivi su dodici sono completati e gli altri dispongono di una base già utilizzabile.")
p("Le attività residue a maggiore impatto sono due: l'expediting delle lavorazioni esterne, che governa la parte del ciclo che determina le date di consegna, e l'allineamento dello stato reale dei set già avviati, che rende attendibili le previsioni. Si resta a disposizione per la revisione congiunta del piano e delle decisioni del capitolo 8.")

doc = S.Documento(meta, titolo, sottotitolo, C)
OUT = "/home/user/AI-Project/01_Documentazione_bozze/" + NOME
pagine = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else None
S.scrivi(doc, OUT, "Remazel Engineering S.p.A.", "Analisi Obiettivi BU Combustion", pagine)
print(OUT)
