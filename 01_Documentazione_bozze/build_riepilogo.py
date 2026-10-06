import sys, subprocess, re, os
sys.path.insert(0, "/root/.claude/skills/synced/593ea5d8-9a85-4668-a3fb-0290e8e227e7_746b874a-eee2-4e96-b44c-f02049e430c1/docx-startit/scripts")
import startit_docx as S

NOME = "Riepilogo_Personalizzazioni_Avvio_Remazel_B1.docx"
meta = {
    "Documento": NOME,
    "Versione": "Bozza 1 — 6 ottobre 2026",
    "Data": "6 ottobre 2026",
    "Redatto da": "Start I.T. S.r.l.",
    "Destinatario": "Remazel Engineering S.p.A. — BU Combustion",
    "Sistema": "M.E.S. Remazel — ERPNext v16",
    "Riferimento": "T09-0100 (Job 26-19008) · T08-0100 (Job 24-19006) — combustionerp.remazel.com",
    "Stato": "Bozza operativa",
}
titolo = ["RIEPILOGO PERSONALIZZAZIONI", "E AVVIO DEL CICLO"]
sottotitolo = ["Stato degli obiettivi, funzioni realizzate su ERPNext v16,", "guida all'avvio e al subentro in corsa",
               "Remazel Engineering S.p.A. — BU Combustion"]

C = []
h = lambda l, t: C.append(("h", l, t))
p = lambda t: C.append(("p", t))
bl = lambda items: C.append(("bullets", items))
tb = lambda cols, head, rows: C.append(("table", cols, head, rows))
bx = lambda k, t, ps: C.append(("box", k, t, ps))
st = lambda items: C.append(("steps", items))

# ------------------------------------------------------------------ 1
h(1, "1. Scopo del documento e situazione in sintesi")
p("Il documento riassume, alla data del 6 ottobre 2026, quanto realizzato sul sistema **M.E.S. Remazel** per la BU Combustion: lo stato dei dodici obiettivi di pianificazione e monitoraggio della produzione, le personalizzazioni introdotte su ERPNext v16, la procedura per avviare il ciclo di una commessa e quella per allineare a sistema una produzione già in corso.")
p("La commessa in esercizio è la **T09-0100** (Job 26-19008, 100 liner in 6 set di consegna). La **T08-0100** è temporaneamente sospesa sul sistema: i suoi codici, distinte e cicli restano la base dati comune, e la T09 utilizza il codice T08 per tutti gli articoli identici.")
tb([3600, 5460], ["Indicatore", "Valore al 6 ottobre 2026"], [
    ["Set di consegna T09", "6 set (10 / 20 / 20 / 20 / 20 / 10 liner), consegne dal 26/02/2027 al 30/11/2027"],
    ["Work Order T09", "348, tutti rilasciati (58 per set)"],
    ["Job Card T09", "3.306, di cui 768 su lavorazioni esterne"],
    ["Obiettivi completati", "6 su 12 (1a, 1b, 1c, 1d, 1f, 1g)"],
    ["Obiettivi in corso", "4 (2a, 2b, 2d, 3); 1 da avviare (2c); 1 riformulato (1e)"],
    ["Ore di lavorazione esterna per set da 10 liner", "circa 21.400 ore di attraversamento presso fornitori, contro un lavoro interno nell'ordine delle 1.300 ore"],
])
bx("info", "Esito della pianificazione dei set", [
    "Con la capacità reale dei reparti e i lead time dei fornitori, i **set 3-6** risultano pianificati in anticipo di 7-11 giorni sulla data di consegna. I **set 1 e 2** risultano in ritardo di 28 e 39 giorni.",
    "Il ritardo dei set 1 e 2 è **indicativo**: i due set sono in produzione da maggio e il sistema li ha pianificati come se partissero oggi. Il dato si correggerà con l'allineamento dell'avanzamento reale (capitolo 5).",
])

# ------------------------------------------------------------------ 2
h(1, "2. Stato dei 12 obiettivi")
p("La tabella riprende gli obiettivi trasmessi dalla BU Combustion con la priorità assegnata e lo stato aggiornato. Il dettaglio di ciascun obiettivo è nel documento Analisi_Obiettivi_BU_Combustion (prossima revisione B4).")
tb([700, 900, 2700, 1200, 3560], ["Ob.", "Priorità", "Richiesta", "Stato", "Cosa c'è a sistema / cosa manca"], [
    ["1a", "Alta", "Master Plan di BU nel tempo con saturazione", "Completato", "Workspace pubblico «Produzione Remazel» con Gantt di tutte le commesse, Gantt Work Order T09 e report di carico reparti su tutte le commesse aperte"],
    ["1b", "Alta", "Punti di monitoraggio per prodotto", "Completato", "42 punti di monitoraggio T09 (per ogni set: gruppo + 6 macro-assiemi con dipendenze), ogni Work Order collegato al proprio punto; struttura generata dall'albero di distinta, riusabile per famiglia di prodotto"],
    ["2a", "Alta", "Modifica agile di cicli e fasi", "In corso", "Cicli T08 e T09 completi con tempi reali. Manca la procedura di import/confronto del ciclo da Excel eseguibile dall'utente"],
    ["2b", "Alta", "Schede di lavoro con documenti", "In corso", "Documenti associati alla fase di distinta e propagati in automatico alla Job Card. Mancano i documenti reali e la stampa della scheda"],
    ["1c", "Media", "Ripianificazione rapida", "Completato", "Simulazione e applicazione del ritardo con propagazione ai Work Order padre e confronto con la consegna del set"],
    ["1d", "Media", "Evidenza dei sovraccarichi", "Completato", "Report «Carico Reparti Settimanale» con saturazione per reparto"],
    ["2c", "Media", "Timbratura fasi con codice a barre", "Da avviare", "Base disponibile: tempi su Job Card, 21 operatori con accesso filtrato per reparto. Mancano codice a barre, postazione di reparto e regole dei casi anomali"],
    ["3", "Media", "Expediting lavorazioni esterne", "In corso", "Fornitore, n° ordine SAP, data promessa, uscita e rientro sulla Job Card. Manca l'Ordine conto lavoro con il collegamento a SAP"],
    ["1e", "Bassa", "Proposte alternative di pianificazione", "Riformulato", "Coperto dalla simulazione del ritardo (1c) e dal report di carico (1d); un motore APS resta una valutazione successiva"],
    ["1f", "Bassa", "Dashboard e KPI", "Completato", "Indicatori e grafici per T08 e T09 nel Workspace"],
    ["1g", "Bassa", "Buffer per prodotto", "Completato", "Buffer in giorni sul singolo Project con ricalcolo automatico della scadenza interna"],
    ["2d", "Bassa", "Lotti e numeri di serie", "In corso", "Matricola e marcatura sul prodotto finito, assegnate a fine produzione. Aperta la tracciabilità del lotto materiale"],
])

# ------------------------------------------------------------------ 3
h(1, "3. Personalizzazioni a sistema")
p("Tutte le personalizzazioni sono realizzate con strumenti nativi di ERPNext (campi aggiuntivi, script lato server e lato client, report, spazi di lavoro), senza modifiche al codice dell'applicazione: restano compatibili con gli aggiornamenti di versione, come verificato con l'aggiornamento a ERPNext 16.37 del 2 ottobre 2026.")

h(2, "3.1 Pianificazione, capacità e calendari")
tb([2600, 1500, 4960], ["Elemento", "Dove", "Funzione"], [
    ["Capacità reparti", "Workstation", "Saldatura 7, Molatura 5, Montaggio 5, Controllo Qualità 3, Lavorazioni Meccaniche 1 postazioni; Lavorazione Esterna 50 (fornitori in parallelo)"],
    ["Calendario Remazel 2026-2029", "Holiday List", "Sabati, domeniche, festività e chiusure aziendali; orario reparti 07-17. Assegnato ai cinque reparti interni"],
    ["Calendario Fornitori 2026-2029", "Holiday List", "Festività e chiusure aziendali senza i fine settimana; assegnato alla Lavorazione Esterna (i fornitori chiudono negli stessi periodi di Remazel)"],
    ["Tempi delle fasi esterne", "Distinta (BOM Operation)", "Durata = tempo di attraversamento del lotto (TT) dal ciclo dell'Ufficio Tecnico, comprensivo di spedizione; tempo fisso per lotto"],
    ["Capacity planning", "Impostazioni produzione", "Attivo su 365 giorni: al rilascio del Work Order le Job Card vengono pianificate sulla capacità reale"],
    ["Buffer Project", "Project, sezione Timeline", "Giorni di margine prima della consegna (default 5), modificabili per singolo Project; la scadenza interna si ricalcola a ogni salvataggio"],
])

h(2, "3.2 Work Order e Job Card")
tb([2900, 1500, 4660], ["Elemento", "Tipo", "Funzione"], [
    ["Consegna set / Production Plan", "Campi su Job Card", "Ogni scheda di lavoro riporta la data di consegna e il set a cui appartiene: distingue lavorazioni uguali di set diversi"],
    ["Punto di monitoraggio", "Campo su Work Order", "Collega il Work Order al punto di monitoraggio (Task) del proprio set"],
    ["Descrizione fase", "Campo su Job Card", "Descrizione leggibile della fase con il codice dell'Ufficio Tecnico"],
    ["WorkOrder_Consegna_Set", "Script (creazione WO)", "Copia la data di consegna della riga d'ordine sul Work Order"],
    ["WO Default WIP Warehouse", "Script (rilascio WO)", "Imposta il magazzino di lavorazione se mancante"],
    ["WO_Project_Fallback", "Script (creazione WO)", "Garantisce il collegamento del Work Order al Project"],
    ["JobCard_Descrizione_Fase / Documenti_Tecnici", "Script (creazione JC)", "Riportano sulla Job Card descrizione e documenti della fase di distinta"],
    ["JobCard_Avviso_Precedenze", "Script (salvataggio JC)", "Avvisa se si avvia una fase prima della precedente (avviso, non blocco)"],
])

h(2, "3.3 Lavorazioni esterne (expediting)")
tb([2900, 1500, 4660], ["Elemento", "Tipo", "Funzione"], [
    ["Fornitore", "Campo su fase di distinta e Job Card", "Fornitore strutturato su ciascuna delle 165 fasi esterne, copiato in automatico sulla Job Card"],
    ["Sezione «Conto lavoro»", "Campi su Job Card", "N° ordine SAP, data promessa dal fornitore, uscita, rientro previsto, rientro effettivo, stato (Da inviare / Presso fornitore / Rientrato)"],
    ["JobCard_Fornitore", "Script (creazione JC)", "Imposta fornitore e stato iniziale"],
    ["JobCard_Conto_Lavoro", "Script (salvataggio JC)", "Calcola rientro previsto (data promessa, altrimenti uscita + tempo del lotto) e stato"],
])
bx("nota", "Evoluzione decisa", [
    "Per le lavorazioni esterne non si registra l'avvio sulla singola Job Card: sarà introdotto l'**Ordine conto lavoro**, che raggruppa le fasi inviate allo stesso fornitore e registra spedizione e rientro con un'unica azione.",
    "Le giacenze presso i fornitori restano gestite in SAP; il sistema le leggerà tramite un collegamento in sola lettura.",
])

h(2, "3.4 Ripianificazione")
tb([2900, 1500, 4660], ["Elemento", "Tipo", "Funzione"], [
    ["Simula Ritardo", "Funzione + pulsante su Job Card", "Calcola l'effetto di una nuova data di fine fase su fasi successive e Work Order padre fino al prodotto finito, senza scrivere nulla"],
    ["Applica Ritardo", "Funzione + pulsante su Job Card", "Applica lo spostamento calcolato; segnala se il set sfora il buffer o la data di consegna"],
    ["Pulsanti", "Menu «Pianificazione» della Job Card", "Disponibili su ogni scheda di lavoro"],
])

h(2, "3.5 Monitoraggio e cruscotti")
tb([2900, 1500, 4660], ["Elemento", "Tipo", "Funzione"], [
    ["Produzione Remazel", "Spazio di lavoro pubblico", "Master Plan, indicatori e grafici T09 e T08, accessi rapidi; menu laterale dedicato"],
    ["Master Plan commesse", "Vista Gantt dei Project", "Tutte le commesse nel tempo"],
    ["Gantt Work Order / monitoraggio T09", "Viste Gantt", "Dettaglio per Work Order e per punto di monitoraggio, per set"],
    ["Carico Reparti Settimanale", "Report", "Minuti pianificati contro capacità per reparto e settimana, con evidenza dei sovraccarichi"],
    ["Indicatori e grafici", "Number Card / Dashboard Chart", "Ordini, pezzi prodotti, Job Card aperte, avvio ordini per settimana, ordini per stato (T08 e T09)"],
])

h(2, "3.6 Utenti, permessi e qualità")
tb([2900, 1500, 4660], ["Elemento", "Tipo", "Funzione"], [
    ["Operatori di reparto", "21 utenti", "Ruolo «Operatore di Reparto»: ogni operatore vede solo le Job Card del proprio reparto"],
    ["Responsabile Processo MES", "Profilo", "Governo del processo produttivo (pianificazione, Work Order, Job Card) senza diritti di amministrazione del sistema"],
    ["Matricola reale", "Campo su Serial No", "Matricola definitiva del prodotto finito, senza rinominare il documento"],
    ["Operazione Documento Tecnico", "Tabella dati", "Documenti (disegni, WPS, controlli) per fase di distinta"],
    ["Template controllo saldature", "Quality Inspection Template", "40 parametri, da validare e agganciare al prodotto finito"],
])

# ------------------------------------------------------------------ 4
h(1, "4. Guida all'avvio del ciclo di una commessa")
p("La sequenza vale per ogni nuova commessa della BU. I passi 3-6 sono oggi eseguiti da Start I.T. con procedure dedicate; l'obiettivo è renderli eseguibili dalla Pianificazione di produzione da interfaccia.")
st([
    ["Ordine cliente", ["Sales Order con una riga per ogni set di consegna (quantità e data).", "Nel campo ordine cliente si indica il numero di Job."]],
    ["Commessa (Project)", ["Project con date di inizio e fine e Buffer Project (default 5 giorni).", "La scadenza interna si calcola da sola."]],
    ["Piano di produzione", ["Un Production Plan per set, con il calcolo dei sotto-assiemi dalla distinta.", "Ogni set diventa un lotto di produzione autonomo."]],
    ["Work Order", ["Creazione dei Work Order in bozza dal piano: uno per ogni assieme e sotto-assieme.", "Data di consegna del set e punto di monitoraggio collegati in automatico."]],
    ["Pianificazione a ritroso", ["Fine set = consegna − buffer; ogni sotto-assieme termina prima dell'inizio del padre.", "Se una data cade nel passato, il Work Order parte da oggi e il set viene segnalato in ritardo."]],
    ["Rilascio", ["Rilascio dei Work Order: il sistema crea e pianifica le Job Card sulla capacità reale dei reparti e sul calendario dei fornitori."]],
    ["Reparto", ["Gli operatori aprono la propria Job Card, avviano e chiudono la fase con la quantità prodotta.", "I tempi effettivi si registrano in automatico."]],
    ["Lavorazioni esterne", ["Fornitore già indicato; si registrano n° ordine SAP, eventuale data promessa, spedizione e rientro.", "Il rientro previsto e lo stato si aggiornano da soli."]],
    ["Ritardi", ["Da una Job Card: Pianificazione → Simula Ritardo per valutare l'effetto sulla consegna, poi Applica Ritardo."]],
    ["Monitoraggio", ["Spazio di lavoro «Produzione Remazel»: Master Plan, Gantt del set, carico reparti, indicatori."]],
])

# ------------------------------------------------------------------ 5
h(1, "5. Subentro in corsa: allineare la produzione già avviata")
p("I set 1 e 2 della T09 sono in produzione da maggio, mentre il sistema li ha pianificati a partire dal 2 ottobre 2026. Per ottenere date e ritardi attendibili occorre registrare quanto già eseguito. La procedura proposta evita l'inserimento manuale di centinaia di schede.")
st([
    ["Rilevazione", ["La Pianificazione di produzione compila un modulo Excel predisposto da Start I.T., con l'elenco dei Work Order del set: per ciascuno, fasi completate, fase in corso, eventuale lavorazione presso fornitore e data di uscita."]],
    ["Allineamento", ["Start I.T. carica il modulo con una procedura dedicata: le fasi completate vengono chiuse con la quantità prodotta, i Work Order interamente eseguiti vengono completati."]],
    ["Lavorazioni presso fornitori", ["Le fasi esterne in corso passano in stato «Presso fornitore» con la data di uscita reale e, se nota, la data promessa."]],
    ["Lotto materiale", ["Dove disponibile si registra il numero di colata o di certificato. Il dato **non è obbligatorio**: può essere completato in seguito, e i Work Order senza lotto vengono solo segnalati."]],
    ["Ripianificazione", ["Le fasi ancora da eseguire vengono ripianificate a partire dallo stato reale; il sistema ricalcola la data di fine di ciascun set."]],
    ["Verifica", ["Confronto tra la fine prevista e la consegna di ciascun set nel Master Plan; eventuali ritardi si governano con Simula/Applica Ritardo."]],
])
bx("nota", "Vincolo di magazzino", [
    "Le giacenze sono gestite in SAP e ERPNext non movimenta il magazzino per il conto lavoro. La chiusura dei Work Order serve all'avanzamento e alla tracciabilità della produzione, non alla valorizzazione delle scorte.",
])

# ------------------------------------------------------------------ 6
h(1, "6. Punti aperti e decisioni richieste")
tb([800, 5160, 3100], ["Ob.", "Decisione o informazione richiesta", "Funzione"], [
    ["2b", "Quali documenti associare a quali fasi (disegni, WPS, criteri di controllo), chi li mantiene, come si codificano le revisioni", "Ufficio Tecnico, Pianificazione di produzione"],
    ["2c", "Regole per i casi anomali: fase aperta a fine turno, ripresa il giorno successivo, più operatori sulla stessa fase; conferma postazioni fisse e lettori", "Pianificazione di produzione"],
    ["2d", "Quali livelli tracciare a lotto (solo materia prima o anche semilavorati) e dove si registra oggi il numero di colata; validazione del template controllo saldature", "Qualità, Ufficio Tecnico"],
    ["1a", "Quali altre commesse di BU caricare nel Master Plan, con quale dettaglio e in quale ordine", "Direzione BU, Pianificazione di produzione"],
    ["1c", "Comportamento atteso se uno spostamento genera un sovraccarico di reparto: bloccare oppure accettare e segnalare", "Pianificazione di produzione"],
    ["5", "Stato reale di avanzamento dei set 1 e 2 (modulo di rilevazione)", "Pianificazione di produzione"],
    ["3", "Documenti SAP usati per il conto lavoro, codice con cui viaggia il pezzo a metà ciclo, codici dei magazzini fornitore", "Acquisti, Pianificazione di produzione"],
    ["3", "Utente di sola lettura sul database SAP e accesso al Service Layer", "IT"],
    ["—", "Anagrafica fornitori: verifica di due ragioni sociali simili per le saldature esterne", "Acquisti"],
    ["—", "Configurazione della posta in uscita per le notifiche del sistema", "IT"],
])

# ------------------------------------------------------------------ 7
h(1, "7. Prossimi passi")
bl([
    "**Expediting**: Ordine conto lavoro e cruscotto delle lavorazioni esterne (da ordinare, presso fornitore, in ritardo), con evidenza delle fasi che attraversano periodi di chiusura.",
    "**Subentro in corsa**: modulo di rilevazione e allineamento dei set 1 e 2.",
    "**Pagina impostazioni** del sistema (buffer di trasporto, regole di pianificazione, calendari, capacità) con relativa documentazione.",
    "**Collegamento SAP** in sola lettura per movimenti e giacenze presso i fornitori.",
    "**Aggiornamento documentale**: Analisi Obiettivi B4, Guida Produzione, Manuale Utente, Prerequisiti di avvio.",
])
bx("nota", "Elemento da monitorare", [
    "I componenti P4000 e P5000 (perni), con la capacità attuale del Controllo Qualità, terminano da 1 a 13 giorni dopo l'inizio del montaggio finale del rispettivo set: vanno seguiti nel Gantt del set.",
])

doc = S.Documento(meta, titolo, sottotitolo, C)
OUT = "/home/user/AI-Project/01_Documentazione_bozze/" + NOME
pagine = None
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    import json; pagine = json.load(open(sys.argv[1]))
S.scrivi(doc, OUT, "Remazel Engineering S.p.A.", "Riepilogo personalizzazioni e avvio", pagine)
print(OUT)
