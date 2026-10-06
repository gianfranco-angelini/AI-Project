import sys, os, json
sys.path.insert(0, "/root/.claude/skills/synced/593ea5d8-9a85-4668-a3fb-0290e8e227e7_746b874a-eee2-4e96-b44c-f02049e430c1/docx-startit/scripts")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import startit_docx as S
from stima_pagine import stima_pagine

NOME = "Manuale_Utente_Remazel_B3.docx"
meta = {
    "Documento": NOME,
    "Versione": "Bozza 3 — 6 ottobre 2026",
    "Data": "6 ottobre 2026",
    "Redatto da": "Start I.T. S.r.l.",
    "Destinatario": "Remazel Engineering S.p.A. — BU Combustion",
    "Sistema": "M.E.S. Remazel — ERPNext v16",
    "Riferimento": "combustionerp.remazel.com — T09-0100 (Job 26-19008)",
    "Stato": "Bozza operativa",
}
titolo = ["MANUALE UTENTE", "M.E.S. REMAZEL"]
sottotitolo = ["Avvio del ciclo, avanzamento di reparto, lavorazioni esterne", "e monitoraggio della produzione",
               "Remazel Engineering S.p.A. — BU Combustion"]

C = []
h = lambda l, t: C.append(("h", l, t))
p = lambda t: C.append(("p", t))
bl = lambda items: C.append(("bullets", items))
tb = lambda cols, head, rows: C.append(("table", cols, head, rows))
bx = lambda k, t, ps: C.append(("box", k, t, ps))
st = lambda items: C.append(("steps", items))

# ------------------------------------------------------------------ 1
h(1, "1. Come usare il manuale")
p("Il manuale spiega come si usa il sistema **M.E.S. Remazel** nelle attività quotidiane della BU Combustion. È organizzato per funzione: ognuno può leggere solo i capitoli che lo riguardano.")
tb([3000, 6060], ["Funzione", "Capitoli"], [
    ["Pianificazione di produzione", "2, 3, 4, 7, 8, 9, 10"],
    ["Operatore di reparto", "2, 5, 10"],
    ["Acquisti e logistica (lavorazioni esterne)", "2, 6, 10"],
    ["Direzione e responsabili", "2, 8"],
])
p("Il manuale sostituisce la Bozza 2 del 27 agosto 2026 e il Manuale Operativo T08-0100 v2, che descrivevano un flusso con il magazzino gestito in ERPNext. Oggi **il magazzino è gestito in SAP**: ERPNext pianifica e registra l'avanzamento della produzione, non movimenta le scorte.")

# ------------------------------------------------------------------ 2
h(1, "2. Accesso e termini")
h(2, "2.1 Accesso al sistema")
st([
    ["Indirizzo", ["Aprire con Google Chrome o Microsoft Edge: https://combustionerp.remazel.com"]],
    ["Credenziali", ["Inserire utente e password ricevuti dall'amministratore del sistema. La password è personale e non va condivisa."]],
    ["Pagina di partenza", ["Nel menu laterale scegliere **Produzione Remazel**, oppure aprire /app/produzione-remazel.", "Lo spazio di lavoro raccoglie Master Plan, Gantt, report di carico, indicatori e accessi rapidi."]],
])
bx("info", "Operatori di reparto", [
    "Gli operatori vedono solo le Job Card del proprio reparto: il filtro è automatico e non va impostato a mano.",
])

h(2, "2.2 Termini usati nel sistema")
tb([2600, 6460], ["Termine", "Significato"], [
    ["Job", "La commessa del cliente (es. Job 26-19008)"],
    ["Sales Order", "Ordine cliente: una riga per ogni set di consegna, con quantità e data"],
    ["Set di consegna", "Gruppo di prodotti consegnato alla stessa data (es. 10 liner); è il lotto di produzione"],
    ["Project", "Il contenitore che raccoglie tutto ciò che serve a un ordine (es. PROJ-0002 = T09-0100)"],
    ["Buffer Project", "Giorni di margine prima della consegna; la produzione è pianificata per finire prima"],
    ["Production Plan", "Piano di produzione di un set: calcola dalla distinta tutti gli assiemi e i componenti da produrre"],
    ["BOM", "Distinta base: materiali e fasi di lavorazione di un articolo"],
    ["Work Order (WO)", "Ordine di produzione di un articolo; contiene le fasi del ciclo"],
    ["Job Card (JC)", "Scheda di lavoro di una fase: è il documento su cui si registra l'avanzamento"],
    ["Reparto (Workstation)", "Saldatura, Molatura, Montaggio, Controllo Qualità, Lavorazioni Meccaniche, Lavorazione Esterna"],
    ["Punto di monitoraggio (Task)", "Macro-assieme di un set seguito nel Gantt (es. A1000, A2000, A3000, P4000, P5000)"],
    ["Conto lavoro", "Fase eseguita presso un fornitore esterno"],
    ["TT", "Tempo di attraversamento di una fase esterna: dall'uscita al rientro del materiale"],
    ["Draft / Submitted", "Bozza modificabile / documento confermato"],
])

# ------------------------------------------------------------------ 3
h(1, "3. Avvio del ciclo di un ordine")
p("Funzione: **Pianificazione di produzione**. La sequenza si esegue una volta per ogni nuovo ordine e porta dall'ordine cliente alle Job Card pianificate nei reparti.")
st([
    ["Ordine cliente", ["Vendite → Sales Order → New.", "Una riga per ogni set di consegna: articolo prodotto finito, quantità del set, Delivery Date = data di consegna del set.", "Indicare il numero di Job nel campo ordine cliente. Salvare e confermare (Submit)."]],
    ["Project", ["Progetti → Project → New: nome con il codice prodotto (es. T09-0100 ASSY LINER COMPLETE), Expected Start Date, Expected End Date = ultima consegna.", "Sezione Timeline: **Buffer Project (giorni)**, predefinito 5. Al salvataggio si calcola la Deadline Interna.", "Collegare il Project al Sales Order (campo Project del Sales Order)."]],
    ["Production Plan", ["Produzione → Production Plan → New, **uno per set**.", "Get Items From = Sales Order; Get Sales Orders; Get Items For Work Order. Lasciare solo la riga del set da pianificare.", "Lasciare **disattivato** «Consolidate Sub Assembly Items»: ogni set resta un lotto autonomo.", "Get Sub Assembly Items: il sistema elenca tutti gli assiemi e componenti dalla distinta. Salvare e confermare."]],
    ["Work Order", ["Dal Production Plan: Create → Work Order. I Work Order vengono creati **in bozza**, uno per assieme e componente.", "Data di consegna del set e Project vengono compilati in automatico."]],
    ["Date di inizio", ["La fine del set è la consegna meno il Buffer Project. Ogni componente deve terminare prima dell'inizio dell'assieme che lo contiene.", "Sui Work Order in bozza verificare la Planned Start Date: non deve essere nel passato."]],
    ["Rilascio", ["Elenco Work Order → filtro Production Plan = piano del set, stato Draft → selezionare tutti → Actions → Submit.", "Al rilascio il sistema crea le Job Card e le pianifica sulla capacità dei reparti e sul calendario dei fornitori."]],
    ["Controllo", ["Spazio di lavoro → Gantt del set e report Carico Reparti Settimanale.", "Verificare che la fine del set rientri nella consegna meno il buffer."]],
])
bx("criticita", "Rilascio dei Work Order", [
    "Rilasciare sempre i Work Order **selezionati per Production Plan**. Il pulsante «Submit All Draft» dell'elenco Work Order rilascia tutte le bozze del sistema, anche quelle di altri ordini tenute volutamente in sospeso.",
])
bx("nota", "Funzioni in rilascio", [
    "**Pianificazione a ritroso automatica del set**: calcolo delle Planned Start Date di tutti i Work Order a partire dalla consegna meno il buffer.",
    "**Generazione dei punti di monitoraggio** (Task) del set, con il collegamento dei Work Order.",
    "Saranno disponibili come pulsanti sul Production Plan; fino ad allora si eseguono su richiesta all'amministratore del sistema.",
])

# ------------------------------------------------------------------ 4
h(1, "4. Prima di rilasciare: controlli")
tb([3400, 5660], ["Controllo", "Dove"], [
    ["Distinte attive e predefinite per tutti gli articoli", "Produzione → BOM, filtro Is Default = Sì"],
    ["Tempi di fase compilati (interni per pezzo, esterni per lotto)", "BOM → tabella Operations"],
    ["Fornitore indicato su ogni fase esterna", "BOM → Operations → campo Fornitore"],
    ["Date di consegna corrette sulle righe del Sales Order", "Sales Order → Items → Delivery Date"],
    ["Buffer Project impostato", "Project → Timeline"],
    ["Chiusure aziendali dell'anno inserite nei calendari", "Holiday List: Calendario Remazel e Calendario Fornitori"],
])

# ------------------------------------------------------------------ 5
h(1, "5. Avanzamento in reparto")
p("Funzione: **Operatore di reparto**. Ogni fase si registra sulla propria Job Card; i tempi effettivi si calcolano da soli.")
h(2, "5.1 Trovare la Job Card")
st([
    ["Elenco", ["Produzione → Job Card. Compaiono solo le schede del proprio reparto."]],
    ["Filtrare", ["Status = Open; se serve, Consegna set = data del set e Production Item = codice del pezzo."]],
    ["Verificare", ["Aprire la scheda e controllare che **Production Item** e **Descrizione Fase** corrispondano al pezzo che si ha in mano.", "Nella sezione dei documenti tecnici si trovano disegni, WPS e criteri di controllo della fase, quando presenti."]],
])

h(2, "5.2 Avviare e completare la fase")
st([
    ["Avvio", ["Pulsante **Start Job**; scegliere il proprio nome come operatore. Il tempo inizia a contare."]],
    ["Pausa", ["Fine turno, attesa materiale o guasto: pulsante **Pause**; alla ripresa **Resume**."]],
    ["Completamento", ["Pulsante **Complete Job** e inserire la quantità completata."]],
    ["Conferma", ["La scheda completata viene confermata (Submit) dal responsabile di reparto o dalla Pianificazione: elenco Job Card → Status = Completed → selezione → Actions → Submit. Con la conferma il Work Order aggiorna l'avanzamento."]],
])
bx("nota", "Avviso di precedenza", [
    "Se si avvia una fase prima che la precedente dello stesso Work Order sia terminata, il sistema mostra un avviso. L'avviso non blocca: va valutato con il responsabile.",
])

h(2, "5.3 Fasi di controllo qualità")
p("Le fasi del reparto Controllo Qualità (dimensionali, VT, PT, flussaggio) si registrano come le altre: Start Job, esecuzione del controllo, Complete Job. L'esito e le misure rilevate si scrivono nei commenti della Job Card.")

h(2, "5.4 Casi particolari")
tb([3400, 5660], ["Situazione", "Cosa fare"], [
    ["Lavorazione sospesa", "Pause; avvisare il responsabile. Non completare la scheda"],
    ["Pezzo difettoso", "Completare la quantità buona; segnalare al Controllo Qualità nei commenti"],
    ["Scheda aperta per errore", "Non completare; avvisare il responsabile"],
    ["La scheda non compare", "Verificare i filtri; il Work Order potrebbe non essere ancora rilasciato"],
    ["Più operatori sulla stessa fase", "Ciascuno avvia la scheda con il proprio nome"],
])

# ------------------------------------------------------------------ 6
h(1, "6. Lavorazioni esterne (conto lavoro)")
p("Funzione: **Acquisti e logistica**. Le fasi del reparto Lavorazione Esterna hanno nella Job Card la sezione **Conto lavoro**. Il fornitore è già compilato dalla distinta; l'ordine al fornitore si emette in SAP.")
tb([2900, 1700, 4460], ["Campo", "Chi lo compila", "Significato"], [
    ["Fornitore", "Sistema", "Dalla fase di distinta"],
    ["N° ordine SAP", "Utente", "Numero dell'ordine di conto lavoro emesso in SAP (facoltativo)"],
    ["Data promessa fornitore", "Utente", "Data di rientro confermata dal fornitore (facoltativa)"],
    ["Uscita (da Inizia)", "Sistema", "Data in cui il materiale è partito"],
    ["Rientro previsto", "Sistema", "Data promessa; in mancanza, uscita + tempo della fase"],
    ["Rientro (da Completa)", "Sistema", "Data in cui il materiale è rientrato"],
    ["Stato conto lavoro", "Sistema", "Da inviare → Presso fornitore → Rientrato"],
])
st([
    ["Ordine", ["Emesso l'ordine in SAP, riportare sulla Job Card il N° ordine SAP e, quando nota, la data promessa. Salvare."]],
    ["Spedizione", ["Alla partenza del materiale: **Start Job** sulla Job Card. Lo stato diventa «Presso fornitore» e si calcola il rientro previsto."]],
    ["Rientro", ["Al rientro: **Complete Job** con la quantità rientrata. Lo stato diventa «Rientrato»."]],
    ["Ritardi", ["Elenco Job Card → filtro Stato conto lavoro = Presso fornitore, ordinato per Rientro previsto: le schede con data passata sono in ritardo."]],
])
bx("nota", "Evoluzione prevista", [
    "La registrazione sulla singola Job Card è transitoria. Sarà sostituita dall'**Ordine conto lavoro**: un documento che raggruppa le fasi inviate allo stesso fornitore e registra spedizione e rientro con un'unica azione, senza indicare un operatore, e da un cruscotto delle lavorazioni esterne.",
])

# ------------------------------------------------------------------ 7
h(1, "7. Gestione dei ritardi")
p("Funzione: **Pianificazione di produzione**. Quando una fase finirà più tardi del previsto, il sistema calcola l'effetto sulle fasi successive, sugli assiemi che la contengono e sulla consegna del set.")
st([
    ["Aprire", ["La Job Card della fase in ritardo → menu **Pianificazione**."]],
    ["Simulare", ["**Simula Ritardo**: inserire la nuova data di fine. Il sistema mostra le fasi e i Work Order che si spostano e la nuova fine del set, **senza modificare nulla**."]],
    ["Valutare", ["Se la fine del set supera la consegna meno il buffer, il sistema lo segnala. Valutare alternative (straordinari, priorità, fornitore diverso)."]],
    ["Applicare", ["**Applica Ritardo** con la stessa data: le date vengono aggiornate."]],
    ["Verificare", ["Gantt del set e report Carico Reparti Settimanale per controllare eventuali sovraccarichi."]],
])

# ------------------------------------------------------------------ 8
h(1, "8. Monitoraggio della produzione")
p("Tutto è raggiungibile dallo spazio di lavoro **Produzione Remazel**.")
tb([2900, 6160], ["Strumento", "Cosa mostra"], [
    ["Master Plan", "Gantt di tutti i Project nel tempo: carico della BU"],
    ["Gantt punti di monitoraggio", "Per ogni set i macro-assiemi con le dipendenze"],
    ["Gantt Work Order", "Tutti i Work Order di un Project nel tempo"],
    ["Carico Reparti Settimanale", "Minuti pianificati contro capacità per reparto e settimana; sopra il 100% c'è sovraccarico"],
    ["Indicatori", "Ordini di produzione, pezzi prodotti, Job Card aperte, ore preventivate"],
    ["Grafici", "Ordini per stato, avvio ordini per settimana, Job Card per stato, minuti per reparto"],
])
p("Per filtrare il Gantt Work Order su un set: elenco Work Order → filtro Production Plan o Consegna set → vista Gantt.")

# ------------------------------------------------------------------ 9
h(1, "9. Subentro in corsa")
p("Funzione: **Pianificazione di produzione**. Quando un set è già in produzione al momento del caricamento, il sistema lo pianifica come se partisse oggi. Per avere date e ritardi attendibili si registra lo stato reale.")
st([
    ["Rilevare", ["Per ogni Work Order del set: fasi già completate, fase in corso, eventuale materiale presso un fornitore con la data di uscita."]],
    ["Fasi completate", ["Sulla Job Card: tabella Time Logs → riga con date e ore reali di inizio e fine e quantità completata. Salvare e confermare (Submit)."]],
    ["Fasi presso fornitore", ["Compilare N° ordine SAP e data promessa; registrare l'uscita con una riga Time Log che inizia alla data reale di uscita."]],
    ["Ripianificare", ["Per le fasi ancora da fare usare Simula/Applica Ritardo (capitolo 7) sulla prima fase aperta di ogni Work Order."]],
    ["Verificare", ["Master Plan e Gantt del set: confronto fra fine prevista e consegna."]],
])
bx("info", "Molti Work Order da allineare", [
    "Per set con molte fasi già eseguite è disponibile un modulo Excel di rilevazione: compilato dalla Pianificazione, viene caricato in un'unica operazione dall'amministratore del sistema.",
])

# ------------------------------------------------------------------ 10
h(1, "10. Messaggi frequenti")
tb([2900, 2900, 3260], ["Messaggio o situazione", "Significato", "Cosa fare"], [
    ["Not permitted", "L'utente non ha il permesso per l'operazione", "Chiedere al responsabile; gli operatori non creano e non confermano le Job Card"],
    ["CapacityError al rilascio", "Il sistema non trova spazio nei reparti entro l'orizzonte di pianificazione", "Non ripetere il rilascio: verificare i tempi in distinta e segnalare all'amministratore"],
    ["Richiesta dell'operatore all'avvio", "La fase va attribuita a un operatore", "Scegliere il proprio nome nella finestra di Start Job"],
    ["Avviso di precedenza", "La fase precedente non è terminata", "Avviso non bloccante: valutare con il responsabile"],
    ["Quantità completata superiore a quella da produrre", "Quantità oltre quella della scheda", "Correggere la quantità"],
    ["Tempi sovrapposti (overlapping)", "Lo stesso operatore risulta su due schede nello stesso momento", "Mettere in pausa la scheda precedente"],
    ["Sforamento della consegna (Simula Ritardo)", "Il set finisce oltre la consegna meno il buffer", "Valutare le alternative prima di applicare"],
])

# ------------------------------------------------------------------ A
h(1, "Appendice A. Sigle di lavorazione e reparti")
p("Le sigle sono definite dall'Ufficio Tecnico e compaiono nel codice dei semilavorati.")
tb([1100, 4160, 3800], ["Sigla", "Lavorazione", "Reparto"], [
    ["SA", "Saldatura", "Saldatura"],
    ["ML", "Molatura", "Molatura"],
    ["MT", "Montaggio", "Montaggio"],
    ["LA", "Lavorazione meccanica", "Lavorazioni Meccaniche"],
    ["LT", "Taglio sviluppo e calandratura", "Lavorazioni Meccaniche"],
    ["ST", "Calibratura, bombatura, formatura", "Lavorazioni Meccaniche"],
    ["QC", "Controllo generico", "Controllo Qualità"],
    ["VT", "Esame visivo", "Controllo Qualità"],
    ["PT", "Liquidi penetranti", "Controllo Qualità"],
    ["MX", "Definizione mappe radiografiche", "Controllo Qualità"],
    ["VX", "Valutazione lastre RX", "Controllo Qualità"],
    ["RX", "Controllo radiografico", "Lavorazione Esterna"],
    ["TT", "Trattamento termico", "Lavorazione Esterna"],
    ["TE", "Flussaggio ad aria", "Lavorazione Esterna"],
    ["FE", "Fusione / pezzo ordinato finito", "Lavorazione Esterna"],
])
p("**Formato del codice**: prodotto − articolo − progressivo + sigla. Esempio: T08-0100-P3100-10SA = saldatura sul pezzo P3100. Il progressivo procede a decine (10, 20, 30) per consentire inserimenti senza rinumerare.")

doc = S.Documento(meta, titolo, sottotitolo, C)
OUT = "/home/user/AI-Project/01_Documentazione_bozze/" + NOME
pagine = stima_pagine(C)
json.dump(pagine, open("/home/user/AI-Project/01_Documentazione_bozze/pagine_manuale.json", "w"), ensure_ascii=False, indent=0)
S.scrivi(doc, OUT, "Remazel Engineering S.p.A.", "Manuale Utente M.E.S. Remazel", pagine)
print(OUT, "pagine stimate:", max(pagine.values()))
