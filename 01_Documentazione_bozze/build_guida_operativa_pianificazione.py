"""Genera Guida_Operativa_Pianificazione_Remazel_B1.docx (standard docx-startit + docx-remazel).

Due passate: la prima con i numeri di pagina dell'indice a 1, poi PDF -> pagine reali dei titoli,
la seconda con i numeri corretti. Infine link cliccabili (linkify).
Uso: python3 build_guida_operativa_pianificazione.py   (dalla cartella 01_Documentazione_bozze)
"""
import sys, os, subprocess
sys.path.insert(0, "/root/.claude/skills/synced/593ea5d8-9a85-4668-a3fb-0290e8e227e7_746b874a-eee2-4e96-b44c-f02049e430c1/docx-startit/scripts")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import startit_docx as S
from linkify import linkify

NOME = "Guida_Operativa_Pianificazione_Remazel_B1.docx"
DATA = "16 ottobre 2026"
URL = "https://combustionerp.remazel.com"
meta = {
    "Documento": NOME,
    "Versione": "Bozza 1 — " + DATA,
    "Data": DATA,
    "Redatto da": "Start I.T. S.r.l.",
    "Destinatario": "Remazel Engineering S.p.A. — BU Combustion",
    "Sistema": "M.E.S. Remazel — ERPNext v16",
    "Riferimento": "combustionerp.remazel.com — T09-0100 (Job 26-19008) — PROJ-0002",
    "Stato": "Bozza operativa",
}
titolo = ["GUIDA OPERATIVA", "PIANIFICAZIONE DI PRODUZIONE"]
sottotitolo = ["Cosa fare ogni giorno, ogni settimana e a evento",
               "per seguire la T09-0100 sul sistema M.E.S. Remazel",
               "Remazel Engineering S.p.A. — BU Combustion"]

C = []
h = lambda l, t: C.append(("h", l, t))
p = lambda t: C.append(("p", t))
bl = lambda items: C.append(("bullets", items))
tb = lambda cols, head, rows: C.append(("table", cols, head, rows))
bx = lambda k, t, ps: C.append(("box", k, t, ps))
st = lambda items: C.append(("steps", items))

# ------------------------------------------------------------------ 1
h(1, "1. Scopo e modo d'uso")
p("La guida accompagna passo per passo la **Pianificazione di produzione** nella gestione quotidiana della T09-0100 sul sistema **M.E.S. Remazel**, ora che l'avanzamento dei set è allineato allo stato reale. Dice cosa fare, quando, dove si trova a video e come verificare che il risultato sia corretto.")
p("È organizzata per **cadenza**: le attività di ogni giorno, di ogni settimana, quelle che nascono da un evento e quelle di fine lavorazione. Le attività si possono seguire con le checklist in appendice.")
tb([3000, 6060], ["Documento", "Quando usarlo"], [
    ["Questa guida", "Lavoro quotidiano della Pianificazione: cosa fare e in che ordine"],
    ["Manuale Utente (B3)", "Dettaglio delle schermate; capitoli per gli operatori di reparto"],
    ["Guida Concettuale (B8)", "Il perché delle regole: distinta, buffer, tempi esterni, SAP"],
    ["Guida Avvio T09 (B2)", "Percorso di avvio: superato da questa guida per la gestione corrente"],
])
tb([2200, 6860], ["Simbolo", "Significato"], [
    ["Ogni giorno", "Attività da fare a inizio o fine giornata, circa 15 minuti"],
    ["Ogni settimana", "Controllo della pianificazione dei set, circa 30 minuti"],
    ["A evento", "Attività da fare quando succede qualcosa: ritardo, spedizione, rientro, anomalia"],
    ["Amministratore", "Attività che oggi richiede l'amministratore del sistema: va chiesta, non eseguita"],
])

# ------------------------------------------------------------------ 2
h(1, "2. Punto di partenza")
p("Situazione del sistema al " + DATA + ", da cui la guida parte. Questi passi **sono già eseguiti** e non vanno rifatti.")
tb([2800, 6260], ["Elemento", "Situazione"], [
    ["Pianificazione T09", "6 set di consegna (10 / 20 / 20 / 20 / 20 / 10 liner), un Production Plan per set, 348 Work Order rilasciati, oltre 3.300 Job Card pianificate sulla capacità dei reparti e sui calendari di fabbrica e fornitori"],
    ["Avanzamento allineato", "Registrate come completate le fasi già eseguite indicate dalla Pianificazione il 6 ottobre: 50 Job Card chiuse su tutti i set (taglio, calandratura e controlli iniziali)"],
    ["Date dell'allineamento", "Le date e i tempi delle 50 Job Card sono **stimati** dal piano, non consuntivi: ogni scheda riporta la nota «date e tempi STIMATI»"],
    ["Parziali del set 5", "T08-0200-P3302, taglio e controllo: 10 pezzi su 20. Le due Job Card (PO-JOB07996, PO-JOB07997) restano aperte con una nota"],
    ["Stato dei set", "Set 1 in ritardo di 33 giorni e set 2 di 44 giorni rispetto alla consegna meno il buffer; set 3-6 in linea"],
    ["Lavorazioni esterne", "Seguite sulla Job Card in **modalità transitoria** (capitolo 6), fino all'arrivo dell'Ordine conto lavoro"],
    ["Monitoraggio", "Spazio di lavoro «Produzione Remazel»: Master Plan, Gantt dei set, Gantt fornitori, Carico Reparti Settimanale. Le pagine sono oggi filtrate sulla T09-0100"],
])
bx("info", "Perché i set 1 e 2 risultano in ritardo", [
    "Oltre alle prime fasi non è ancora iniziato nulla: il ritardo calcolato è in buona parte reale. Le fasi successive sono però ancora pianificate dopo le vecchie date previste: la Pianificazione può anticiparle dove è possibile (capitolo 8.2).",
])

# ------------------------------------------------------------------ 3
h(1, "3. Il ruolo della Pianificazione nel sistema")
p("Il profilo **Responsabile Processo MES** permette di governare la produzione senza i diritti di amministrazione del sistema.")
tb([4530, 4530], ["La Pianificazione fa", "Si chiede all'amministratore del sistema"], [
    ["Conferma le Job Card completate dagli operatori", "Nuovi utenti e permessi per reparto"],
    ["Registra spedizioni e rientri delle lavorazioni esterne", "Pianificazione a ritroso e punti di monitoraggio di un nuovo ordine"],
    ["Simula e applica i ritardi; anticipa le fasi", "Modifiche ai cicli e nuove versioni di distinta"],
    ["Aggiorna Buffer Project e calendari", "Script, campi aggiuntivi, report"],
    ["Chiude i Work Order e i set", "Operazioni massive (allineamenti, caricamenti da Excel)"],
    ["Segue Master Plan, Gantt e carico reparti", "Errori di sistema non spiegati in questa guida"],
])
bx("criticita", "Funzioni da non usare", [
    "Il pulsante **Submit All Draft** dell'elenco Work Order rilascia tutte le bozze del sistema, anche di altri ordini. Rilasciare sempre i Work Order selezionati per Production Plan.",
    "Sulla Job Card **Applica Ritardo** modifica le date pianificate: si usa solo dopo aver valutato l'effetto con Simula Ritardo.",
])

# ------------------------------------------------------------------ 4
h(1, "4. Prima settimana: passi una tantum")
p("Da eseguire una sola volta, nell'ordine, prima di entrare nella routine dei capitoli 5 e 7.")
st([
    ["Accesso", ["Accedere con le proprie credenziali e aprire lo spazio di lavoro:",
                 URL + "/app/produzione-remazel",
                 "Verifica: si vedono Master Plan, scorciatoie e indicatori della T09-0100."]],
    ["Nome nell'elenco dipendenti", ["Aprire una Job Card esterna «Da inviare» e premere Start Job: nella finestra deve comparire il proprio nome fra i dipendenti. Chiudere la finestra senza confermare.",
                                     "Se il nome non c'è, chiederlo all'amministratore: senza nominativo non si registrano spedizioni e rientri (capitolo 6)."]],
    ["Set 1 e 2", ["Aprire il Master Plan e il Gantt dei set 1 e 2 e valutare quali fasi si possono anticipare rispetto al piano (capitolo 8.2).",
                   "Verifica: per ogni set è nota la fine prevista contro la consegna."]],
    ["Fasi esterne già fuori", ["Per ogni materiale che oggi si trova presso un fornitore, registrare l'uscita sulla Job Card con la data reale (capitolo 6.3).",
                                "Verifica: nell'elenco Job Card con stato conto lavoro «Presso fornitore» c'è tutto il materiale fuori casa."]],
    ["Reparti interni", ["Concordare il reparto da cui partono le registrazioni sulle Job Card e il suo referente; consegnare le credenziali agli operatori (una per persona).",
                         "Le regole di reparto sono nel capitolo 5.3."]],
    ["Controllo settimanale", ["Fissare giorno, ora e partecipanti del controllo settimanale di 30 minuti (capitolo 7)."]],
])

# ------------------------------------------------------------------ 5
h(1, "5. Ogni giorno")
h(2, "5.1 Sequenza giornaliera")
st([
    ["Job Card da confermare", ["Elenco Job Card con stato Completed e non ancora confermate:",
                                URL + "/app/job-card?status=Completed&docstatus=0",
                                "Controllare quantità e operatore, selezionare le schede → Actions → Submit.",
                                "Verifica: l'elenco si svuota; il Work Order aggiorna l'avanzamento."]],
    ["Job Card in corso", ["Elenco Job Card in lavorazione:",
                           URL + "/app/job-card?status=Work%20In%20Progress",
                           "Una scheda avviata da più di un giorno senza pause va verificata con il reparto: fase realmente in corso, oppure dimenticata aperta."]],
    ["Spedizioni e rientri", ["Registrare le spedizioni e i rientri del giorno sulle Job Card esterne (capitolo 6)."]],
    ["Esterne in ritardo", ["Elenco Job Card «Presso fornitore», ordinato per Rientro previsto:",
                            URL + "/app/job-card?custom_stato_cl=Presso%20fornitore",
                            "Le schede con data già passata sono in ritardo: sollecitare il fornitore e, se il rientro slitta, valutarne l'effetto (capitolo 8)."]],
    ["Avvisi di precedenza", ["Gli avvisi segnalati dai reparti (fase avviata prima della precedente) si valutano con il responsabile di reparto: l'avviso non blocca."]],
])

h(2, "5.2 Conferma delle Job Card")
p("La conferma (Submit) è il passaggio che rende definitiva la registrazione: solo le Job Card confermate fanno avanzare il Work Order e i punti di monitoraggio nel Gantt.")
bl([
    "**Chi conferma**: la Pianificazione o il responsabile di reparto; gli operatori non hanno il permesso di confermare.",
    "**Requisito**: la Job Card deve avere almeno una riga di tempo (operatore, inizio, fine, quantità). Senza, il sistema rifiuta la conferma.",
    "**Prima di confermare**: quantità completata uguale a quella della scheda, operatore corretto, tempi plausibili.",
    "**Dopo la conferma** la scheda non si modifica più: un errore si corregge con l'amministratore.",
])

h(2, "5.3 Regole di reparto")
p("Da comunicare a ogni reparto quando inizia a registrare sulle Job Card.")
tb([3200, 5860], ["Situazione", "Regola"], [
    ["Fine turno con fase aperta", "Pause a fine turno, Resume alla ripresa"],
    ["Più operatori sulla stessa fase", "Ciascuno avvia la scheda con il proprio nome"],
    ["Esito dei controlli qualità", "Nei commenti della Job Card, fino alla validazione del template di controllo"],
    ["Fase avviata prima della precedente", "Ammessa con avviso; la valuta il responsabile di reparto"],
    ["Pezzo difettoso", "Si completa la quantità buona; la non conformità va nei commenti e al Controllo Qualità"],
])

# ------------------------------------------------------------------ 6
h(1, "6. Lavorazioni esterne: modalità transitoria")
h(2, "6.1 Come funziona")
p("Ogni fase eseguita presso un fornitore ha la propria Job Card nel reparto **Lavorazione Esterna**, con la sezione **Conto lavoro**. Il fornitore è già compilato dalla distinta; l'ordine al fornitore si emette in SAP. Nella modalità transitoria spedizione e rientro si registrano sulla singola Job Card.")
tb([2600, 1900, 4560], ["Campo", "Chi lo compila", "Significato"], [
    ["Fornitore", "Sistema", "Dalla fase di distinta"],
    ["N° ordine SAP", "Pianificazione", "Numero dell'ordine di conto lavoro emesso in SAP"],
    ["Data promessa fornitore", "Pianificazione", "Data di rientro confermata dal fornitore (facoltativa)"],
    ["Uscita (da Inizia)", "Sistema", "Data della spedizione, dalla registrazione Start Job"],
    ["Rientro previsto", "Sistema", "Data promessa; in mancanza, uscita + tempo di attraversamento della fase"],
    ["Rientro (da Completa)", "Sistema", "Data del rientro, dalla registrazione Complete Job"],
    ["Stato conto lavoro", "Sistema", "Da inviare → Presso fornitore → Rientrato"],
])

h(2, "6.2 Trovare le fasi da spedire")
st([
    ["Elenco", ["Job Card esterne ancora da inviare:",
                URL + "/app/job-card?custom_stato_cl=Da%20inviare",
                "Filtrare per Fornitore e ordinare per data di inizio pianificata: in testa le spedizioni più urgenti."]],
    ["Gantt fornitori", ["Vista per fornitore delle fasi esterne nel tempo, colorate per stato:",
                         URL + "/app/job-card/view/gantt?workstation=Lavorazione%20Esterna"]],
    ["Set di appartenenza", ["Fasi uguali di set diversi si distinguono dalle colonne **Consegna set** e **Production Plan**."]],
])

h(2, "6.3 Registrare ordine, spedizione e rientro")
st([
    ["Ordine", ["Emesso l'ordine in SAP, aprire la Job Card e compilare **N° ordine SAP** e, quando nota, **Data promessa fornitore**. Salvare.",
                "Verifica: lo stato resta «Da inviare»; con la data promessa il rientro previsto si aggiorna."]],
    ["Spedizione", ["Alla partenza del materiale: **Start Job** e scegliere il proprio nome.",
                    "Verifica: stato «Presso fornitore», Uscita compilata, Rientro previsto calcolato."]],
    ["Uscita non registrata in giornata", ["Se la spedizione si registra in un giorno successivo, correggere la data e l'ora di inizio nella riga dei **Time Logs** con quella reale prima di salvare: la data di uscita la legge da lì."]],
    ["Rientro", ["Al rientro del materiale: **Complete Job** con la quantità rientrata.",
                 "Verifica: stato «Rientrato», Rientro compilato. La scheda entra nell'elenco delle Job Card da confermare (capitolo 5.2)."]],
    ["Rientro parziale", ["Se rientra solo una parte dei pezzi, non completare la scheda: annotare nei commenti «rientrati N su M» e completarla al rientro dell'ultima parte.",
                          "Così sono gestite oggi le due schede del set 5 (PO-JOB07996, PO-JOB07997)."]],
])
bx("nota", "Una spedizione con più fasi", [
    "Se una spedizione allo stesso fornitore comprende più pezzi o più set, ogni Job Card coinvolta si registra singolarmente con lo stesso N° ordine SAP. È il limite della modalità transitoria, che l'Ordine conto lavoro supererà con un'unica registrazione per spedizione.",
])
bx("criticita", "Fase precedente non chiusa", [
    "Il sistema può rifiutare l'avvio di una Job Card esterna se la fase precedente dello stesso Work Order non risulta completata (messaggio di sequenza delle operazioni). Succede quando la fase precedente è stata eseguita ma non registrata.",
    "Rimedio: registrare prima la fase precedente con le date reali (Manuale Utente, capitolo 9), poi la spedizione. Se la fase precedente non è stata davvero eseguita, il materiale non è pronto per la spedizione.",
])

h(2, "6.4 Chiusure dei fornitori")
p("Il Calendario Fornitori contiene le chiusure aziendali: le fasi pianificate dopo il caricamento ne tengono conto. Alcune fasi esterne già pianificate attraversano il periodo natalizio senza tenerne conto: in caso di dubbio, verificare con il fornitore la data promessa e registrarla sulla Job Card.")

# ------------------------------------------------------------------ 7
h(1, "7. Ogni settimana")
h(2, "7.1 Controllo dei set")
st([
    ["Master Plan", ["Gantt dei set di tutti i Project:",
                     URL + "/app/task/view/gantt?is_group=1",
                     "Ogni barra è un set; la parte scura è l'avanzamento. Premere **Recalculate progress** per aggiornare le percentuali al momento."]],
    ["Gantt del set", ["Punti di monitoraggio (macro-assiemi A1000, A2000, A3000, P4000, P5000, A0001) del Project:",
                       URL + "/app/task/view/gantt?project=PROJ-0002",
                       "Verifica: la fine di A0001 di ogni set è entro la consegna meno il buffer. Le frecce rosse indicano un conflitto di sequenza."]],
    ["Work Order", ["Gantt di tutti i Work Order del Project, filtrabile per Production Plan o Consegna set:",
                    URL + "/app/work-order/view/gantt?project=PROJ-0002"]],
    ["Perni P4000 / P5000", ["Con la capacità attuale del Controllo Qualità terminano da 1 a 13 giorni dopo l'inizio del montaggio finale del set: verificarne la posizione nel Gantt del set."]],
])
h(2, "7.2 Carico dei reparti")
st([
    ["Report", ["Minuti pianificati contro capacità per reparto e settimana:",
                URL + "/app/query-report/Carico%20Reparti%20Settimanale"]],
    ["Lettura", ["Sopra il 100% c'è sovraccarico. La Lavorazione Esterna non entra nella saturazione.",
                 "Un sovraccarico nelle prossime settimane si governa spostando le fasi con Simula/Applica Ritardo (capitolo 8)."]],
])
h(2, "7.3 Controllo settimanale")
p("Incontro di 30 minuti fra Pianificazione e amministratore del sistema, con questa traccia:")
bl([
    "**Set**: fine prevista contro consegna; ritardi nuovi o rientrati rispetto alla settimana precedente.",
    "**Esterne**: rientri scaduti, spedizioni della settimana, date promesse mancanti.",
    "**Reparti**: Job Card non confermate, schede aperte da giorni, registrazioni mancanti.",
    "**Anomalie**: messaggi del sistema, richieste all'amministratore, decisioni da prendere.",
])

# ------------------------------------------------------------------ 8
h(1, "8. Ritardi e anticipi")
h(2, "8.1 Una fase finirà più tardi")
st([
    ["Aprire", ["La Job Card della fase in ritardo → menu **Pianificazione**."]],
    ["Simulare", ["**Simula Ritardo**: inserire la nuova data di fine. Il sistema mostra le fasi e i Work Order che si spostano fino al prodotto finito e la nuova fine del set, **senza modificare nulla**."]],
    ["Valutare", ["Se la fine del set supera la consegna meno il buffer il sistema lo segnala: valutare le alternative (priorità, straordinari, altro fornitore) prima di applicare."]],
    ["Applicare", ["**Applica Ritardo** con la stessa data: le date vengono aggiornate."]],
    ["Verificare", ["Gantt del set e Carico Reparti Settimanale."]],
])
h(2, "8.2 Anticipare le fasi dei set 1 e 2")
p("Le fasi successive dei set 1 e 2 sono pianificate dopo le date previste prima dell'allineamento. Dove reparto e materiale lo consentono si possono anticipare con la stessa funzione.")
st([
    ["Scegliere", ["Nel Gantt del set individuare la prima fase aperta di un Work Order che si può eseguire prima."]],
    ["Simulare", ["Sulla sua Job Card: Pianificazione → **Simula Ritardo** con una data di fine **anteriore** a quella pianificata. Il sistema mostra le fasi che si anticipano e la nuova fine del set."]],
    ["Applicare", ["Se l'effetto è quello atteso e il reparto ha capacità: **Applica Ritardo** con la stessa data."]],
])
bx("info", "Limite della cascata", [
    "Lo spostamento si propaga alle fasi successive dello stesso Work Order e ai Work Order degli assiemi che lo contengono, fino al prodotto finito del set. Non sposta i Work Order di altri set.",
])

# ------------------------------------------------------------------ 9
h(1, "9. A evento")
tb([2900, 6160], ["Evento", "Cosa fare"], [
    ["Materiale spedito o rientrato", "Registrazione sulla Job Card esterna (capitolo 6.3)"],
    ["Fornitore comunica una nuova data", "Aggiornare Data promessa fornitore; se ritarda il set, Simula/Applica Ritardo"],
    ["Fase interna bloccata (materiale, guasto)", "L'operatore mette in Pause; la Pianificazione valuta lo spostamento con Simula Ritardo"],
    ["Pezzo difettoso", "Si completa la quantità buona; la non conformità va nei commenti e al Controllo Qualità"],
    ["Fase eseguita ma non registrata", "Registrare sulla Job Card la riga di tempo con le date reali (Manuale Utente, capitolo 9), poi confermare"],
    ["Job Card avviata per errore", "Non completarla; avvisare l'amministratore"],
    ["Nuovo operatore", "Chiedere all'amministratore utente, dipendente e permesso di reparto"],
    ["Nuova chiusura aziendale", "Inserirla nel Calendario Remazel e nel Calendario Fornitori; vale per le pianificazioni successive, le fasi già pianificate si spostano con Simula/Applica Ritardo"],
    ["Modifica del ciclo", "Chiederla all'amministratore: si crea una nuova versione della distinta; i Work Order già creati restano sulla versione precedente"],
])

# ------------------------------------------------------------------ 10
h(1, "10. Chiusura di Work Order e set")
st([
    ["Work Order", ["Quando tutte le Job Card del Work Order sono confermate: dal Work Order **Finish** (scarico di produzione). Il Work Order passa a Completed e il componente è disponibile per l'assieme superiore.",
                    "Lo scarico serve all'avanzamento: le quantità di magazzino in ERPNext possono risultare negative e non vanno lette come giacenze, che restano in SAP."]],
    ["Prodotto finito", ["Alla chiusura del Work Order di A0001 si assegna la matricola provvisoria; la matricola definitiva va nel campo **Matricola reale** del numero di serie."]],
    ["Set", ["Quando tutti i Work Order del set sono Completed il set è chiuso: confrontare la fine reale con la consegna e il buffer nel Master Plan."]],
])
bx("nota", "Prima chiusura", [
    "La prima chiusura di un Work Order si esegue insieme all'amministratore del sistema, per verificare che lo scarico di produzione avvenga senza trasferimento di materiale al reparto.",
])

# ------------------------------------------------------------------ 11
h(1, "11. Ogni mese")
bl([
    "**Tempi effettivi e pianificati** delle fasi più ricorrenti, dalle Job Card confermate: scostamenti stabili vanno segnalati all'Ufficio Tecnico per aggiornare il ciclo.",
    "**Tempi di attraversamento dei fornitori**: dall'uscita al rientro, contro il tempo del ciclo. Lo storico permette di correggere le stime sui dati.",
    "**Calendari**: chiusure aziendali dell'anno successivo presenti in entrambi i calendari.",
])
bx("criticita", "Tempi dell'allineamento", [
    "Le 50 Job Card dell'allineamento hanno date e tempi stimati: vanno escluse da ogni confronto fra tempi effettivi e pianificati e dal consuntivo ore. Si riconoscono dalla nota «date e tempi STIMATI».",
])

# ------------------------------------------------------------------ 12
h(1, "12. Un nuovo ordine")
p("La sequenza completa è nel Manuale Utente, capitolo 3. In sintesi, e con la ripartizione attuale delle attività:")
tb([600, 4630, 3830], ["N.", "Passo", "Chi"], [
    ["1", "Sales Order con una riga per set di consegna e numero di Job", "Pianificazione"],
    ["2", "Project con date e Buffer Project", "Pianificazione"],
    ["3", "Production Plan per set e Work Order in bozza", "Pianificazione"],
    ["4", "Pianificazione a ritroso del set e punti di monitoraggio", "Amministratore (pulsanti in sviluppo)"],
    ["5", "Rilascio dei Work Order del set", "Pianificazione"],
    ["6", "Controllo nel Master Plan e nel Carico Reparti", "Pianificazione"],
])
bx("info", "Pagine filtrate sulla T09-0100", [
    "Le pagine dello spazio di lavoro sono oggi impostate sulla T09-0100: con l'ingresso di altri prodotti diventeranno generali, con la scelta del Project direttamente nella pagina.",
])

# ------------------------------------------------------------------ 13
h(1, "13. Cosa arriva in corsa")
tb([3200, 3860, 2000], ["Funzione", "Cosa cambia per la Pianificazione", "Stato"], [
    ["Ordine conto lavoro", "Spedizione e rientro di più fasi con un'unica registrazione, senza operatore; sostituisce il capitolo 6.3", "In sviluppo"],
    ["Cruscotto lavorazioni esterne", "Scadute, in scadenza e tutte, in una vista; sostituisce il controllo di 5.1", "In sviluppo"],
    ["Lettura dei movimenti da SAP", "Spedizioni e rientri senza doppia registrazione", "In attesa dell'accesso SAP"],
    ["Pulsanti sul Production Plan", "Nuovi ordini senza passaggio dall'amministratore", "In sviluppo"],
    ["Pagine generali per Project", "Stesse viste per ogni prodotto", "Pianificato"],
    ["Etichette in inglese", "Lingua finale del sistema", "Fase successiva"],
])
p("A ogni funzione rilasciata la guida viene aggiornata con una nuova versione.")

# ------------------------------------------------------------------ 14
h(1, "14. Messaggi frequenti")
tb([2900, 2900, 3260], ["Messaggio o situazione", "Significato", "Cosa fare"], [
    ["Not permitted", "Operazione non consentita al profilo", "Verificare di avere selezionato la scheda giusta; altrimenti chiedere all'amministratore"],
    ["Conferma rifiutata per tempo mancante", "La Job Card non ha righe di tempo", "Aggiungere la riga di tempo con operatore, date e quantità"],
    ["Errore di sequenza delle operazioni", "La fase precedente dello stesso Work Order non è completata", "Registrare prima la fase precedente (capitolo 6.3)"],
    ["Nome non presente in Start Job", "L'utente non ha un record dipendente", "Chiederlo all'amministratore"],
    ["Tempi sovrapposti", "Lo stesso operatore risulta su due schede nello stesso momento", "Mettere in pausa la scheda precedente"],
    ["Sforamento della consegna", "Con Simula Ritardo il set finisce oltre la consegna meno il buffer", "Valutare le alternative prima di applicare"],
    ["Gantt aperto in una nuova scheda", "Comportamento del menu laterale per le viste Gantt", "Normale: chiudere la scheda per tornare allo spazio di lavoro"],
    ["CapacityError al rilascio", "Capacità dei reparti insufficiente entro l'orizzonte", "Non ripetere il rilascio; segnalare all'amministratore"],
])

# ------------------------------------------------------------------ A
h(1, "Appendice A. Checklist giornaliera")
tb([600, 6460, 2000], ["N.", "Attività", "Fatto"], [
    ["1", "Job Card completate confermate (5.2)", ""],
    ["2", "Job Card in corso da più di un giorno verificate con i reparti", ""],
    ["3", "Spedizioni del giorno registrate con Start Job e N° ordine SAP", ""],
    ["4", "Rientri del giorno registrati con Complete Job", ""],
    ["5", "Esterne con rientro previsto superato sollecitate", ""],
    ["6", "Avvisi di precedenza valutati con i reparti", ""],
])

h(1, "Appendice B. Checklist settimanale")
tb([600, 6460, 2000], ["N.", "Attività", "Fatto"], [
    ["1", "Master Plan aggiornato con Recalculate progress", ""],
    ["2", "Fine di ogni set contro consegna meno buffer", ""],
    ["3", "Perni P4000 / P5000 rispetto al montaggio finale", ""],
    ["4", "Carico Reparti delle prossime quattro settimane", ""],
    ["5", "Ritardi e anticipi simulati e, se approvati, applicati", ""],
    ["6", "Date promesse mancanti sulle esterne «Presso fornitore»", ""],
    ["7", "Controllo settimanale con l'amministratore del sistema", ""],
])

h(1, "Appendice C. Collegamenti utili")
p("Accesso con le proprie credenziali. Nel file Word: Ctrl + clic per aprire.")
tb([3200, 5860], ["Cosa", "Collegamento"], [
    ["Spazio di lavoro", URL + "/app/produzione-remazel"],
    ["Master Plan", URL + "/app/task/view/gantt?is_group=1"],
    ["Project T09-0100", URL + "/app/project/PROJ-0002"],
    ["Gantt punti di monitoraggio T09", URL + "/app/task/view/gantt?project=PROJ-0002"],
    ["Gantt Work Order T09", URL + "/app/work-order/view/gantt?project=PROJ-0002"],
    ["Job Card T09", URL + "/app/job-card?project=PROJ-0002"],
    ["Job Card da confermare", URL + "/app/job-card?status=Completed&docstatus=0"],
    ["Esterne da inviare", URL + "/app/job-card?custom_stato_cl=Da%20inviare"],
    ["Esterne presso fornitore", URL + "/app/job-card?custom_stato_cl=Presso%20fornitore"],
    ["Gantt fornitori", URL + "/app/job-card/view/gantt?workstation=Lavorazione%20Esterna"],
    ["Carico Reparti Settimanale", URL + "/app/query-report/Carico%20Reparti%20Settimanale"],
    ["Calendario Remazel", URL + "/app/holiday-list/Calendario%20Remazel%202026-2029"],
    ["Calendario Fornitori", URL + "/app/holiday-list/Calendario%20Fornitori%202026-2029"],
])

# ------------------------------------------------------------------ build
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), NOME)
HDR = ("Remazel Engineering S.p.A.", "Guida operativa Pianificazione")


def pdf_testo(path):
    d = os.path.dirname(path)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", path, "--outdir", d],
                   check=True, capture_output=True)
    pdf = path.replace(".docx", ".pdf")
    return subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout.split("\f")


doc = S.Documento(meta, titolo, sottotitolo, C)
S.scrivi(doc, OUT, *HDR)                                   # passata 1
testo = pdf_testo(OUT)
# prima pagina del corpo: quella che contiene il primo titolo dopo l'indice
primo = next(it[2] for it in C if it[0] == "h")
inizio = next(n for n in range(2, len(testo)) if primo in testo[n] and "Indice" not in testo[n])
pagine = {}
for it in C:
    if it[0] == "h":
        for n in range(inizio, len(testo)):
            if it[2] in testo[n]:
                pagine[it[2]] = n + 1
                break
S.scrivi(doc, OUT, *HDR, pagine=pagine)                    # passata 2
n_link = linkify(OUT)
pdf_testo(OUT)
print(OUT, "pagine:", max(pagine.values()), "link:", n_link)
