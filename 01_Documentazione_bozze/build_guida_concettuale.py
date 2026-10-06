import sys, os, json
sys.path.insert(0, "/root/.claude/skills/synced/593ea5d8-9a85-4668-a3fb-0290e8e227e7_746b874a-eee2-4e96-b44c-f02049e430c1/docx-startit/scripts")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import startit_docx as S
from stima_pagine import stima_pagine

NOME = "Guida_Concettuale_Remazel_B7.docx"
meta = {
    "Documento": NOME,
    "Versione": "Bozza 7 — 6 ottobre 2026",
    "Data": "6 ottobre 2026",
    "Redatto da": "Start I.T. S.r.l.",
    "Destinatario": "Remazel Engineering S.p.A. — BU Combustion",
    "Sistema": "M.E.S. Remazel — ERPNext v16",
    "Riferimento": "T09-0100 (Job 26-19008) · T08-0100 (Job 24-19006) — combustionerp.remazel.com",
    "Stato": "Bozza operativa",
}
titolo = ["COME FUNZIONA", "IL CICLO PRODUTTIVO"]
sottotitolo = ["Dalla commessa al prodotto finito: concetti, esempi e flussi reali", "sul sistema M.E.S. Remazel",
               "Remazel Engineering S.p.A. — BU Combustion"]

C = []
h = lambda l, t: C.append(("h", l, t))
p = lambda t: C.append(("p", t))
bl = lambda items: C.append(("bullets", items))
tb = lambda cols, head, rows: C.append(("table", cols, head, rows))
bx = lambda k, t, ps: C.append(("box", k, t, ps))

# ------------------------------------------------------------------ 1
h(1, "1. A chi è rivolto il documento")
p("La guida spiega il **perché** e il **come** funziona la produzione sul sistema M.E.S. Remazel, con esempi reali tratti dai prodotti T08-0100 e T09-0100. Non è un manuale operativo: i passi da eseguire a video sono nel **Manuale Utente**, i dettagli tecnici delle personalizzazioni nella **Guida alle Personalizzazioni**.")
p("La Bozza 7 sostituisce la versione 6 del 1° settembre 2026. Cambia il quadro di fondo: il prodotto in esercizio è la **T09-0100**, la T08-0100 resta la base dati comune, e il **magazzino è gestito in SAP**. ERPNext pianifica la produzione e ne registra l'avanzamento, senza gestire le scorte.")

# ------------------------------------------------------------------ 2
h(1, "2. Dalla commessa al prodotto")
h(2, "2.1 I termini")
tb([2400, 6660], ["Termine", "Significato"], [
    ["Commessa (Job)", "L'impegno con il cliente, identificato dal numero di Job (es. Job 26-19008)"],
    ["Prodotto", "Ciò che si costruisce, identificato dal codice (es. T09-0100 ASSY LINER COMPLETE)"],
    ["Set di consegna", "Gruppo di prodotti consegnato alla stessa data. È il lotto di produzione"],
    ["Project", "Il contenitore in ERPNext che raccoglie piani, ordini e schede di un ordine (PROJ-0002 = T09-0100)"],
])
h(2, "2.2 La catena dei documenti")
p("Ogni documento nasce dal precedente: chi lavora in reparto vede solo l'ultimo anello, ma ogni Job Card sa a quale set, ordine e consegna appartiene.")
tb([2000, 2600, 4460], ["Documento", "Quando nasce", "Cosa contiene"], [
    ["Sales Order", "All'acquisizione dell'ordine", "Una riga per set: prodotto, quantità, data di consegna"],
    ["Project", "Con l'ordine", "Date del programma, Buffer Project, punti di monitoraggio"],
    ["Production Plan", "Uno per set", "Tutti gli assiemi e componenti da produrre, calcolati dalla distinta"],
    ["Work Order", "Dal Production Plan", "Ordine di produzione di un articolo, con le fasi del ciclo"],
    ["Job Card", "Al rilascio del Work Order", "Una per fase: reparto, date pianificate, tempi e quantità effettivi"],
])

# ------------------------------------------------------------------ 3
h(1, "3. La distinta base")
h(2, "3.1 Cosa contiene una distinta")
p("Tutto parte dalla **distinta base** (BOM, Bill of Materials). Non è una lista della spesa: è la rappresentazione strutturata del prodotto, analoga a un disegno di assieme. Ogni distinta dice:")
bl([
    "**quali componenti** servono e in che quantità;",
    "**quali fasi** di lavorazione vanno eseguite e in quale sequenza;",
    "**in quale reparto** si svolge ogni fase, o presso **quale fornitore**;",
    "**quanto tempo** richiede ogni fase.",
])
bx("info", "Esempio reale — distinta di P5000 (PIN CAP)", [
    "Materiale: tondo Hastelloy-X D. 16 mm.",
    "Fase 1 — Controllo Qualità: accettazione della materia prima.",
    "Fase 2 — Lavorazione Esterna: lavorazione meccanica presso il fornitore.",
    "Fase 3 — Controllo Qualità: controllo dimensionale finale. Ne servono 12 per ogni liner.",
])
h(2, "3.2 Distinta multilivello")
p("Il prodotto finito A0001 (ASSY LINER COMPLETE) è fatto di sotto-assiemi, che a loro volta sono fatti di componenti, fino alla materia prima: la struttura ha **7 livelli**.")
tb([2600, 4460, 2000], ["Codice", "Descrizione", "Livello"], [
    ["A0001", "ASSY LINER COMPLETE", "L0"],
    ["P5000 / P4000", "PIN CAP (12 per liner) / PIN VENTURI (18 per liner)", "L1"],
    ["A1000", "ASSY LINER BODY: HULA SEAL, TLUG WRAPPER, LINER BODY fino agli INLET SLEEVE", "L1 – L6"],
    ["A3000", "ASSY VENTURY: CONE, SLEEVE, THROAT RING", "L1 – L3"],
    ["A2000", "ASSY CAP: FRAME WHEEL microfuso, CENTER SWIRLER, IMP PLATE", "L1 – L2"],
])
h(2, "3.3 Dal basso verso l'alto")
p("Non si assembla A0001 senza A1000, A2000, A3000, P4000 e P5000; non si produce A1000 senza i suoi componenti. La pianificazione rispetta questa regola da sola: ogni componente è programmato per terminare **prima** dell'inizio dell'assieme che lo contiene.")
h(2, "3.4 Codifica T08 e T09")
p("La T09-0100 è un'evoluzione della T08-0100. Regola di codifica adottata:")
bl([
    "**articolo identico** → si usa il codice T08, con la sua distinta e il suo ciclo;",
    "**articolo diverso** → codice T09, con tutte le fasi del ciclo T09;",
    "nessun codice alternativo: un articolo ha un solo codice.",
])

# ------------------------------------------------------------------ 4
h(1, "4. ERPNext e SAP")
h(2, "4.1 Chi fa cosa")
tb([3000, 3030, 3030], ["Ambito", "ERPNext (M.E.S.)", "SAP"], [
    ["Pianificazione della produzione", "Sì", "—"],
    ["Avanzamento di reparto e tempi", "Sì", "—"],
    ["Ordini di acquisto e di conto lavoro", "Ne registra il numero", "Sì, li emette"],
    ["Magazzino e giacenze, anche presso i fornitori", "—", "Sì"],
    ["Movimenti verso e dai fornitori", "Letti da SAP (previsto)", "Sì"],
])
p("ERPNext lavora con le **giacenze negative ammesse**: non controlla la disponibilità del materiale, perché il dato reale è in SAP. Non si registrano acquisti, ricevimenti né trasferimenti di materiale al reparto.")
h(2, "4.2 Chiusura del Work Order")
p("Quando tutte le Job Card di un Work Order sono confermate, si registra lo **scarico di produzione** (Stock Entry di tipo Manufacture). Il Work Order passa a Completed e il componente risulta prodotto, pronto per l'assieme che lo contiene.")
bx("nota", "Valore dello scarico di produzione", [
    "Lo scarico serve all'avanzamento e alla tracciabilità, non alla valorizzazione: le quantità di magazzino in ERPNext possono risultare negative e non vanno lette come giacenze. Le giacenze reali sono quelle di SAP.",
])
h(2, "4.3 Gli stati del Work Order")
tb([2200, 6860], ["Stato", "Significato"], [
    ["Draft", "Creato dal piano, non ancora rilasciato: le date si possono modificare"],
    ["Not Started", "Rilasciato: le Job Card sono create e pianificate, nessuna fase è iniziata"],
    ["In Process", "La produzione è iniziata"],
    ["Completed", "Tutte le fasi chiuse e scarico di produzione registrato"],
    ["Stopped", "Sospeso manualmente; si riprende con Resume"],
])

# ------------------------------------------------------------------ 5
h(1, "5. Pianificare un set")
h(2, "5.1 Un piano per ogni set")
p("Ogni set di consegna ha il **proprio Production Plan**, con i sotto-assiemi **non consolidati**: i Work Order di set diversi restano separati anche quando producono lo stesso articolo. Ogni Job Card riporta la data di consegna e il piano del proprio set, così due schede identiche di set diversi si distinguono.")
h(2, "5.2 Capacità dei reparti e calendari")
p("Al rilascio del Work Order il sistema pianifica ogni fase sulla **capacità reale** del reparto, tenendo conto delle fasi già pianificate di tutti i set.")
tb([3000, 1500, 4560], ["Reparto", "Postazioni", "Calendario"], [
    ["Saldatura", "7", "Calendario Remazel (07-17, chiusure aziendali)"],
    ["Molatura", "5", "Calendario Remazel"],
    ["Montaggio", "5", "Calendario Remazel"],
    ["Controllo Qualità", "3", "Calendario Remazel"],
    ["Lavorazioni Meccaniche", "1", "Calendario Remazel"],
    ["Lavorazione Esterna", "50", "Calendario Fornitori, 24 ore"],
])
p("Le postazioni sono le stazioni che lavorano in parallelo. La Lavorazione Esterna ne ha 50 per rappresentare fornitori diversi al lavoro contemporaneamente. Il Calendario Fornitori contiene festività e chiusure aziendali ma non i fine settimana: i tempi dei fornitori sono già espressi in giorni di calendario.")
h(2, "5.3 Fasi esterne: il tempo di attraversamento")
p("Per una fase esterna non conta il tempo di lavoro del fornitore, ma il **tempo di attraversamento (TT)**: dall'uscita del materiale al suo rientro, trasporto compreso. Il TT viene dal ciclo dell'Ufficio Tecnico, è riferito al lotto da 10 liner ed è impostato come **tempo fisso**: non si moltiplica per la quantità.")
bx("info", "Perché conta", [
    "Per un set da 10 liner le fasi esterne sommano circa **21.400 ore** di attraversamento, contro un lavoro interno nell'ordine delle **1.300 ore**. Le date di consegna dipendono soprattutto dai fornitori.",
])
h(2, "5.4 Buffer e pianificazione a ritroso")
bl([
    "Il **Buffer Project** (predefinito 5 giorni, modificabile per singolo Project) è il margine tra fine produzione e consegna.",
    "La pianificazione parte **dalla consegna e va a ritroso**: fine del set = consegna − buffer; ogni componente termina prima dell'inizio del suo assieme.",
    "Nessuna fase viene pianificata nel passato: se il calcolo a ritroso cade prima di oggi, il set parte oggi e risulta in ritardo.",
])
h(2, "5.5 Il caso T09-0100")
tb([3600, 5460], ["Dato", "Valore"], [
    ["Set di consegna", "6 set (10 / 20 / 20 / 20 / 20 / 10 liner), consegne dal 26/02/2027 al 30/11/2027"],
    ["Work Order", "348, tutti rilasciati (58 per set)"],
    ["Job Card", "oltre 3.300, di cui circa 770 su lavorazioni esterne"],
    ["Esito", "Set 3-6 in anticipo di 7-11 giorni; set 1 e 2 in ritardo indicativo, perché già in produzione e pianificati come se partissero oggi"],
])

# ------------------------------------------------------------------ 6
h(1, "6. Seguire la produzione")
h(2, "6.1 La Job Card")
p("Ogni Job Card rappresenta una fase su un pezzo. Riporta il **codice della fase** e la **descrizione** dal ciclo dell'Ufficio Tecnico, il fornitore se la fase è esterna e i documenti tecnici associati alla fase in distinta.")
bx("info", "Prima e dopo — la stessa Job Card", [
    "Prima: cinque righe identiche «Controllo Qualità», indistinguibili tra loro.",
    "Ora: «T08-0100-P1130-10VX — Valutazione RX W60, W59», oppure «T08-0100-P1130-10TT — Brasatura W59».",
])
p("L'operatore avvia e chiude la fase dalla propria scheda; i tempi effettivi si registrano da soli e si confrontano con quelli pianificati.")
h(2, "6.2 Punti di monitoraggio e Master Plan")
bl([
    "Per ogni set il sistema crea un punto di monitoraggio di gruppo e uno per ciascun macro-assieme (A1000, A2000, A3000, P4000, P5000, A0001), con le dipendenze tra loro.",
    "Ogni Work Order è collegato al proprio punto di monitoraggio: il Gantt mostra l'avanzamento per macro-assieme senza scendere nelle centinaia di schede.",
    "Il **Master Plan** mostra tutti i Project nel tempo; il report **Carico Reparti Settimanale** mostra la saturazione di ogni reparto.",
])
h(2, "6.3 Ritardi a cascata")
p("Se una fase finirà più tardi, il ritardo si propaga alle fasi successive dello stesso Work Order, poi agli assiemi che lo contengono, fino al prodotto finito. Il sistema permette prima di **simulare** l'effetto, senza modificare nulla, e confronta la nuova fine del set con la consegna meno il buffer; solo dopo si **applica**.")

# ------------------------------------------------------------------ 7
h(1, "7. Lavorazioni esterne")
p("Le fasi esterne si seguono per **eventi**, non per date scritte in anticipo: un ordine al fornitore può precedere di mesi l'invio effettivo del materiale.")
tb([2600, 6460], ["Evento", "Effetto"], [
    ["Ordine emesso in SAP", "Si registrano il numero d'ordine e, quando nota, la data promessa dal fornitore"],
    ["Materiale spedito", "Stato «Presso fornitore»; rientro previsto = data promessa, altrimenti uscita + TT"],
    ["Materiale rientrato", "Stato «Rientrato»; la fase è completata"],
    ["Data superata", "La fase è in ritardo e va sollecitata"],
])
p("Il fornitore è già indicato in distinta e passa da solo sulla Job Card. Nei cicli non esistono due fasi esterne consecutive: ogni rientro passa da Remazel prima di una nuova uscita.")
bx("nota", "Evoluzione decisa", [
    "Spedizione e rientro saranno registrati con l'**Ordine conto lavoro**: un documento che raggruppa le fasi inviate allo stesso fornitore e chiude le relative Job Card con un'unica azione, senza indicare un operatore.",
    "I movimenti verso e dai magazzini dei fornitori, già presenti in SAP, saranno **letti da SAP** in sola lettura. In prospettiva l'ordine potrà essere emesso da ERPNext verso SAP attraverso le interfacce ufficiali di SAP.",
])

# ------------------------------------------------------------------ 8
h(1, "8. Tracciabilità")
bl([
    "**Matricola e marcatura** solo sul prodotto finito (A0001), assegnate alla chiusura del suo Work Order con una numerazione provvisoria; la matricola definitiva si registra nel campo «Matricola reale», senza rinominare il documento.",
    "Gli assiemi intermedi non hanno matricola: sono tracciati dal set e dal Work Order a cui appartengono.",
    "Il **lotto materiale** (colata o certificato) è un punto aperto: campo dedicato non obbligatorio oppure lettura da SAP.",
])

# ------------------------------------------------------------------ 9
h(1, "9. Granularità delle Job Card")
p("Il livello di dettaglio con cui registrare il lavoro è una delle scelte più importanti: dipende dalla complessità del prodotto, dal numero di operatori e da quanto valgono i dati raccolti rispetto al tempo speso per raccoglierli.")
h(2, "9.1 Opzione A — una Job Card per Work Order")
bl(["**A favore**: semplicità estrema, minimo sforzo per gli operatori.",
    "**Contro**: nessuna visibilità sulle fasi, colli di bottiglia non individuabili, costi non attribuibili al reparto."])
h(2, "9.2 Opzione B — una Job Card per fase")
bl(["**A favore**: avanzamento visibile per fase, costo per reparto, controlli qualità intermedi, colli di bottiglia individuabili.",
    "**Contro**: richiede un ciclo definito con cura e più registrazioni per gli operatori."])
h(2, "9.3 Opzione C — sotto-fasi")
bl(["**A favore**: tracciabilità al minuto, utile per analisi di tempi e metodi.",
    "**Contro**: complessità elevata e rischio concreto che gli operatori abbandonino la registrazione."])
h(2, "9.4 La regola del vantaggio netto")
p("Ogni Job Card in più costa tempo all'operatore. Il costo è giustificato solo se il dato vale più del tempo speso a raccoglierlo: se una fase dura due ore e registrarla costa cinque minuti, conviene; se dura cinque minuti e registrarla ne costa tre, no.")
bl(["**Che cosa ne faccio di questo dato?** Se la risposta è «probabilmente nulla», si accorpa.",
    "**Chi lo guarda?** Un dato senza destinatario è un costo senza beneficio.",
    "**Cambia qualcosa nella gestione?** Se sì vale la pena, altrimenti si accorpa."])
h(2, "9.5 La scelta adottata")
p("È adottata l'**Opzione B**, con la granularità decisa dal ciclo dell'Ufficio Tecnico. Nella distinta T08 (base comune) le 613 fasi si distribuiscono così:")
tb([3000, 1400, 4660], ["Reparto", "Fasi", "Contenuto"], [
    ["Controllo Qualità", "305", "Dimensionali, visivi, liquidi penetranti, mappe e valutazione radiografica"],
    ["Lavorazione Esterna", "134", "Lavorazioni meccaniche, taglio e calandratura, trattamenti termici, radiografie, microfusioni"],
    ["Saldatura", "48", "Saldature interne"],
    ["Molatura", "44", "Molatura, lavaggio, pulizia"],
    ["Lavorazioni Meccaniche", "23", "Formatura e calibratura CNC"],
    ["Montaggio", "18", "Montaggi, raddrizzature, marcature"],
])
p("Metà delle fasi sono controlli qualità: riflette la natura del prodotto, dove ogni saldatura critica richiede esame visivo, liquidi penetranti e spesso radiografia. La domanda da porsi non è quante Job Card creare, ma quali controlli meritino una registrazione separata e quali un unico verbale.")
h(2, "9.6 Matrice decisionale")
tb([3060, 2000, 2000, 2000], ["Criterio", "Opzione A", "Opzione B", "Opzione C"], [
    ["Semplicità di registrazione", "Alta", "Media", "Bassa"],
    ["Visibilità dell'avanzamento", "Bassa", "Alta", "Alta"],
    ["Costi per reparto", "No", "Sì", "Sì"],
    ["Controllo qualità per fase", "No", "Sì", "Sì"],
    ["Carico di registrazione", "Minimo", "Sostenibile", "Elevato"],
    ["Scelta per Remazel", "—", "Adottata", "Da valutare"],
])

# ------------------------------------------------------------------ 10
h(1, "10. Domande frequenti")
tb([3400, 5660], ["Domanda", "Risposta"], [
    ["Perché ERPNext non controlla se il materiale c'è?", "Perché il magazzino è in SAP. ERPNext ammette giacenze negative e si concentra su date e avanzamento"],
    ["Perché due Job Card identiche?", "Appartengono a set diversi: si distinguono dalla Consegna set e dal Production Plan"],
    ["Perché il set 1 risulta in ritardo?", "Era già in produzione e il sistema lo ha pianificato come se partisse oggi. Il dato si corregge registrando lo stato reale (subentro in corsa)"],
    ["Perché una fase esterna dura settimane?", "Il tempo è quello di attraversamento presso il fornitore, trasporto compreso, non il tempo di lavoro"],
    ["Cosa succede se cambio una data?", "Con Simula Ritardo si vede l'effetto su assiemi e consegna prima di applicarlo"],
    ["Posso cambiare il buffer di un solo ordine?", "Sì, il Buffer Project è sul singolo Project"],
    ["Perché non riesco a confermare una Job Card?", "ERPNext v16 richiede almeno una riga di tempo effettivo (operatore, inizio, fine, quantità)"],
    ["Una nuova chiusura aziendale sposta le date?", "Vale per le pianificazioni successive; le fasi già pianificate si spostano con Simula/Applica Ritardo"],
])

# ------------------------------------------------------------------ 11
h(1, "11. Punti aperti")
p("I punti ancora da decidere sono raccolti nell'**Analisi Obiettivi BU Combustion** (capitolo 8) e nel **Riepilogo personalizzazioni e avvio** (capitolo 6). Quelli che toccano i concetti di questa guida sono:")
bl([
    "**Ordine conto lavoro** e lettura dei movimenti da SAP;",
    "**lotto materiale**: livelli da tracciare e fonte del numero di colata;",
    "**documenti di fase** e loro revisioni sulle Job Card;",
    "**timbratura** delle fasi con codice a barre e regole per i casi anomali.",
])

doc = S.Documento(meta, titolo, sottotitolo, C)
OUT = "/home/user/AI-Project/01_Documentazione_bozze/" + NOME
pagine = stima_pagine(C)
json.dump(pagine, open("/home/user/AI-Project/01_Documentazione_bozze/pagine_concettuale.json", "w"), ensure_ascii=False, indent=0)
S.scrivi(doc, OUT, "Remazel Engineering S.p.A.", "Guida Concettuale M.E.S. Remazel", pagine)
print(OUT, "pagine stimate:", max(pagine.values()))
