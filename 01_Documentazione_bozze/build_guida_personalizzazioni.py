import sys, os, json, math
sys.path.insert(0, "/root/.claude/skills/synced/593ea5d8-9a85-4668-a3fb-0290e8e227e7_746b874a-eee2-4e96-b44c-f02049e430c1/docx-startit/scripts")
import startit_docx as S

NOME = "Guida_Personalizzazioni_MES_Remazel_B1.docx"
meta = {
    "Documento": NOME,
    "Versione": "Bozza 1 — 6 ottobre 2026",
    "Data": "6 ottobre 2026",
    "Redatto da": "Start I.T. S.r.l.",
    "Destinatario": "Remazel Engineering S.p.A. — BU Combustion",
    "Sistema": "M.E.S. Remazel — ERPNext v16",
    "Riferimento": "combustionerp.remazel.com — server cs-erp01, sito site1.local",
    "Stato": "Bozza operativa",
}
titolo = ["GUIDA ALLE PERSONALIZZAZIONI", "M.E.S. REMAZEL"]
sottotitolo = ["Dove si trovano le personalizzazioni di ERPNext v16", "e come modificarle in sicurezza",
               "Remazel Engineering S.p.A. — BU Combustion"]

C = []
h = lambda l, t: C.append(("h", l, t))
p = lambda t: C.append(("p", t))
bl = lambda items: C.append(("bullets", items))
tb = lambda cols, head, rows: C.append(("table", cols, head, rows))
bx = lambda k, t, ps: C.append(("box", k, t, ps))
st = lambda items: C.append(("steps", items))
cd = lambda lines: C.append(("code", lines))

# ------------------------------------------------------------------ 1
h(1, "1. Scopo del documento")
p("La guida descrive, per ogni personalizzazione introdotta sul sistema **M.E.S. Remazel** (ERPNext v16), **dove si trova**, **cosa fa** e **come si modifica** senza compromettere i dati già presenti. È destinata a chi amministra il sistema: funzione IT e referente di processo MES.")
p("Il contenuto deriva dall'inventario estratto dal sistema il 6 ottobre 2026. Il **Riepilogo personalizzazioni e avvio** descrive le stesse funzioni dal punto di vista dell'utente; questo documento ne è il complemento tecnico.")
bx("info", "Lingua delle etichette", [
    "Tutte le etichette, gli stati e i messaggi sono oggi in italiano. La lingua finale del sistema sarà l'inglese: la conversione è una fase successiva, con un glossario da validare, e non cambia i nomi tecnici dei campi riportati in questa guida.",
])

# ------------------------------------------------------------------ 2
h(1, "2. Principi di intervento")
p("Tutte le personalizzazioni sono salvate **nel database** del sito, non nel codice dell'applicazione: sopravvivono agli aggiornamenti di versione, ma si perdono con il database se non c'è un backup.")
bl([
    "**Backup prima di ogni modifica** strutturale (campi, script, distinte, calendari).",
    "**Prima in prova, poi in scrittura**: ogni procedura da console si esegue prima in modalità di sola lettura, si controlla l'elenco delle modifiche, solo dopo si scrive.",
    "**Una modifica alla volta**, verificata a video prima di passare alla successiva.",
    "**Copia del codice** di ogni script prima di modificarlo, conservata nell'archivio degli script di progetto.",
    "**Effetto solo in avanti**: capacità, calendari e tempi di distinta valgono per le pianificazioni successive; Work Order e Job Card già creati non si ricalcolano da soli.",
])
bx("criticita", "Da non fare mai", [
    "Cambiare il **nome tecnico** (fieldname) di un campo, ad esempio custom_stato_cl: è usato da script, report e filtri.",
    "Modificare il database con istruzioni SQL dirette su documenti rilasciati, se non con una procedura di progetto già provata.",
    "Modificare lo spazio di lavoro privato di un utente: si interviene solo sullo spazio pubblico «Produzione Remazel».",
    "Usare i pulsanti di rilascio e avvio massivo senza aver controllato quali Work Order sono in bozza (capitolo 5.2).",
])
p("Backup completo del sito, da eseguire come utente frappe-user:")
cd(["cd /home/frappe-user/frappe-bench",
    "bench --site site1.local backup --with-files",
    "# file in sites/site1.local/private/backups/"])

# ------------------------------------------------------------------ 3
h(1, "3. Mappa delle personalizzazioni")
p("Ogni percorso si apre aggiungendolo all'indirizzo del sistema (es. https://combustionerp.remazel.com/app/server-script).")
tb([2000, 3260, 1300, 2500], ["Area", "Elemento", "Quantità", "Percorso"], [
    ["Campi", "Campi aggiuntivi su Job Card, Project, Work Order, distinta, Employee, Serial No", "22", "/app/customize-form"],
    ["Automatismi", "Script lato server su eventi di documento", "10", "/app/server-script"],
    ["Funzioni", "Script lato server richiamabili (API)", "4", "/app/server-script"],
    ["Interfaccia", "Script lato client (pulsanti, correzioni grafiche)", "5", "/app/client-script"],
    ["Report", "Carico Reparti Settimanale", "1", "/app/report"],
    ["Dati", "Tabella Operazione Documento Tecnico", "1", "/app/doctype"],
    ["Reparti", "Workstation con capacità e calendario", "6", "/app/workstation"],
    ["Calendari", "Calendario Remazel e Calendario Fornitori 2026-2029", "2", "/app/holiday-list"],
    ["Pianificazione", "Impostazioni produzione", "1", "/app/manufacturing-settings"],
    ["Monitoraggio", "Spazio di lavoro e menu laterale «Produzione Remazel»", "2", "/app/produzione-remazel"],
    ["Indicatori", "Number Card e Dashboard Chart", "6 + 8", "/app/number-card, /app/dashboard-chart"],
    ["Pianificazione", "Punti di monitoraggio (Task) sui Project", "21 + 42", "/app/task"],
    ["Accessi", "Ruolo, profilo, permessi per reparto", "—", "/app/role, /app/user-permission"],
])

# ------------------------------------------------------------------ 4
h(1, "4. Campi aggiuntivi (Custom Field)")
h(2, "4.1 Elenco dei campi")
p("I campi aggiuntivi hanno nome tecnico che inizia con **custom_**. Le sezioni (Section Break) e le colonne (Column Break) servono solo all'impaginazione del modulo.")
tb([1700, 2700, 1400, 3260], ["Documento", "Campo (nome tecnico)", "Tipo", "Funzione"], [
    ["Job Card", "custom_descrizione_fase", "Small Text", "Descrizione della fase dal Work Order, in elenco"],
    ["Job Card", "custom_consegna_set", "Date", "Data di consegna del set, letta dal Work Order"],
    ["Job Card", "custom_production_plan", "Link", "Piano di produzione (set) di appartenenza"],
    ["Job Card", "custom_documenti_tecnici", "Table", "Documenti della fase, copiati dalla distinta"],
    ["Job Card", "custom_sb_conto_lavoro, custom_cb_conto_lavoro, custom_sb_fine_conto_lavoro", "Sezione / colonna", "Sezione «Conto lavoro», visibile solo sulle lavorazioni esterne"],
    ["Job Card", "custom_fornitore", "Link", "Fornitore, copiato dalla fase di distinta"],
    ["Job Card", "custom_ordine_sap", "Data", "Numero dell'ordine di conto lavoro in SAP"],
    ["Job Card", "custom_stato_cl", "Select", "Stato: (vuoto) / Da inviare / Presso fornitore / Rientrato; calcolato dallo script"],
    ["Job Card", "custom_data_promessa", "Date", "Data di rientro promessa dal fornitore"],
    ["Job Card", "custom_data_uscita", "Date", "Data di uscita verso il fornitore"],
    ["Job Card", "custom_rientro_previsto", "Date", "Calcolato: data promessa, altrimenti uscita + durata della fase"],
    ["Job Card", "custom_rientro_effettivo", "Date", "Data di rientro registrata"],
    ["BOM Operation", "custom_fornitore", "Link", "Fornitore della fase esterna di distinta"],
    ["BOM Operation", "custom_documenti_tecnici", "Table", "Documenti della fase (modificabile anche su distinta rilasciata)"],
    ["Work Order", "custom_task", "Link", "Punto di monitoraggio (Task) del set"],
    ["Project", "custom_buffer_giorni", "Int", "Buffer Project in giorni, default 5"],
    ["Project", "custom_deadline_interna", "Date", "Scadenza interna = fine prevista − buffer, calcolata"],
    ["Project", "custom_fine_produzione_stimata", "Date", "Fine produzione stimata"],
    ["Serial No", "custom_matricola_reale", "Data", "Matricola definitiva del prodotto finito"],
    ["Employee", "custom_funzione", "Data", "Funzione aziendale del dipendente"],
])

h(2, "4.2 Come modificare un campo")
st([
    ["Aprire", ["Personalizza modulo: /app/customize-form, scegliere il documento (es. Job Card).", "In alternativa: /app/custom-field filtrando per documento."]],
    ["Individuare", ["Cercare il campo per etichetta o per nome tecnico; aprire il dettaglio della riga."]],
    ["Modificare", ["Interventi sicuri: etichetta, descrizione, visibilità in elenco e nei filtri, sola lettura, posizione.", "Per i campi Select: le opzioni sono una per riga; la **prima riga resta vuota**, altrimenti la prima opzione diventa il valore predefinito di ogni nuovo documento."]],
    ["Salvare", ["Pulsante Aggiorna. Ricaricare la pagina del documento (Ctrl+Maiusc+R) per vedere la modifica."]],
    ["Verificare", ["Aprire un documento esistente e uno nuovo; controllare che gli script collegati funzionino ancora."]],
])
bx("nota", "Interventi da valutare prima", [
    "**Cambiare il tipo** di un campo con dati (es. da Data a Select) può troncare o perdere i valori.",
    "**Rinominare un'opzione Select** non aggiorna i documenti già salvati né gli script che la usano: va fatto con una procedura di migrazione.",
    "**Eliminare un campo** cancella la colonna e tutti i suoi dati.",
    "Sulle distinte rilasciate un campo è modificabile solo se ha l'impostazione «Allow on Submit».",
])

h(2, "4.3 Campi delle applicazioni standard")
p("L'elenco dei Custom Field del sistema contiene anche circa 120 campi installati dalle applicazioni **Italia** (fatturazione elettronica, dati fiscali, campi IVA sulle righe dei documenti) e **HRMS** (risorse umane, paghe, approvatori). Non fanno parte del M.E.S. Remazel e **non vanno modificati né eliminati**: sono gestiti dagli aggiornamenti delle rispettive applicazioni. Si riconoscono perché il nome tecnico non inizia con custom_.")

# ------------------------------------------------------------------ 5
h(1, "5. Script lato server")
h(2, "5.1 Automatismi sugli eventi dei documenti")
p("Si eseguono da soli quando un documento viene creato, salvato o rilasciato. L'evento «Before Save» corrisponde alla validazione e scatta **anche alla creazione**.")
tb([2900, 1300, 1700, 3160], ["Script", "Documento", "Evento", "Funzione"], [
    ["WorkOrder_Consegna_Set", "Work Order", "Before Insert", "Se manca, copia la data di consegna dalla riga dell'ordine cliente"],
    ["WO_Project_Fallback", "Work Order", "Before Insert", "Garantisce il collegamento del Work Order al Project"],
    ["WO Default WIP Warehouse", "Work Order", "Before Submit", "Imposta il magazzino di lavorazione «Goods In Transit - Rema» se mancante"],
    ["JobCard_Descrizione_Fase", "Job Card", "Before Insert", "Copia la descrizione della fase dal Work Order"],
    ["JobCard_Documenti_Tecnici", "Job Card", "Before Insert", "Copia i documenti dalla fase di distinta (stesso numero di distinta e stessa posizione della fase)"],
    ["JobCard_Fornitore", "Job Card", "Before Insert", "Copia il fornitore dalla fase di distinta e imposta lo stato «Da inviare»"],
    ["JobCard_Conto_Lavoro", "Job Card", "Before Save", "Calcola rientro previsto e stato del conto lavoro"],
    ["JobCard_Conto_Lavoro_Submitted", "Job Card", "Before Save (Submitted)", "Stesso calcolo sulle Job Card già rilasciate"],
    ["JobCard_Avviso_Precedenze", "Job Card", "Before Save", "Avvisa se una fase viene avviata prima della precedente; non blocca"],
    ["Project_Deadline_Interna", "Project", "Before Save", "Scadenza interna = fine prevista − Buffer Project"],
])

h(2, "5.2 Funzioni richiamabili")
p("Sono script di tipo API, richiamati da pulsanti dell'interfaccia. Il campo evento che compare nell'elenco («Before Insert») non ha significato per questo tipo di script.")
tb([2600, 2300, 4160], ["Script", "Richiamato da", "Funzione"], [
    ["Simula_Ritardo_JobCard", "Job Card → Pianificazione → Simula Ritardo", "Calcola l'effetto di una nuova data di fine fase su fasi successive e Work Order padre, senza scrivere"],
    ["Applica_Ritardo_JobCard", "Job Card → Pianificazione → Applica Ritardo", "Applica lo spostamento e confronta la fine del set con consegna − buffer"],
    ["Submit All Draft WO", "Elenco Work Order → Submit All Draft", "Rilascia **tutti** i Work Order in bozza del sistema"],
    ["Start_All_WO", "Procedura di servizio", "Porta in lavorazione **tutti** i Work Order rilasciati non avviati"],
])
bx("criticita", "Funzioni massive", [
    "Submit All Draft WO e Start_All_WO agiscono su tutto il sistema, non su un singolo Project. Prima dell'uso controllare l'elenco dei Work Order in bozza filtrato per stato: se ce ne sono di altri Project tenuti volutamente in bozza, non usare la funzione.",
])

h(2, "5.3 Come modificare uno script")
st([
    ["Copia", ["Aprire /app/server-script/<nome> e copiare il contenuto del campo Script in un file di testo nell'archivio degli script di progetto."]],
    ["Modifica", ["Modificare il codice nel campo Script e salvare.", "Regole dell'ambiente protetto: **nessun import**; le funzioni si usano per attributo (frappe.utils.getdate, frappe.utils.add_days)."]],
    ["Prova", ["Creare o salvare un documento di prova (es. una Job Card di un Work Order di test) e verificare il risultato e gli eventuali messaggi."]],
    ["Ripristino", ["In caso di problemi spuntare **Disabled** sullo script: il sistema torna al comportamento standard. Poi ripristinare il codice dalla copia."]],
])

# ------------------------------------------------------------------ 6
h(1, "6. Script lato client e report")
h(2, "6.1 Script lato client")
p("Percorso: /app/client-script/<nome>. Dopo ogni modifica gli utenti devono ricaricare la pagina (Ctrl+Maiusc+R). Per disattivarne uno si toglie la spunta **Enabled**.")
tb([2900, 1500, 1100, 3560], ["Script", "Documento", "Vista", "Funzione"], [
    ["Job Card-Ritardo", "Job Card", "Modulo", "Menu «Pianificazione» con i pulsanti Simula Ritardo e Applica Ritardo"],
    ["WO List Submit All Draft", "Work Order", "Elenco", "Pulsante «Submit All Draft» con conferma"],
    ["Gantt_Fix_Remazel", "Work Order", "Elenco", "Correzione grafica del Gantt (barre bianche su sfondo bianco, difetto noto di Frappe v16)"],
    ["Gantt_Fix_Task_Remazel", "Task", "Elenco", "Stessa correzione sul Gantt dei punti di monitoraggio"],
    ["Gantt_Fix_Project_Remazel", "Project", "Elenco", "Stessa correzione sul Master Plan dei Project"],
])
bx("info", "Correzioni grafiche del Gantt", [
    "I tre script Gantt_Fix diventano superflui quando un aggiornamento di Frappe correggerà il difetto: a ogni aggiornamento di versione si possono disattivare uno alla volta e verificare il Gantt.",
])

h(2, "6.2 Report «Carico Reparti Settimanale»")
p("Query Report su Job Card. Percorso: /app/report/Carico Reparti Settimanale; la query SQL si modifica nel campo Query del report (utente con ruolo System Manager).")
bl([
    "**Capacità di reparto** = giorni lavorativi × 540 minuti × postazioni del reparto (production_capacity della Workstation).",
    "**Giorni lavorativi** letti dal Calendario Remazel 2026-2029.",
    "**Totale settimana** = somma delle capacità dei soli reparti interni; la Lavorazione Esterna non entra nella saturazione.",
])
p("Se cambiano l'orario giornaliero dei reparti o il calendario di riferimento, la query va aggiornata di conseguenza: il valore 540 e il nome del calendario sono scritti nel testo.")

# ------------------------------------------------------------------ 7
h(1, "7. Parametri di pianificazione")
h(2, "7.1 Reparti (Workstation)")
tb([2600, 1500, 4960], ["Reparto", "Postazioni", "Calendario"], [
    ["Saldatura", "7", "Calendario Remazel 2026-2029"],
    ["Molatura", "5", "Calendario Remazel 2026-2029"],
    ["Montaggio", "5", "Calendario Remazel 2026-2029"],
    ["Controllo Qualità", "3", "Calendario Remazel 2026-2029"],
    ["Lavorazioni Meccaniche", "1", "Calendario Remazel 2026-2029"],
    ["Lavorazione Esterna", "50", "Calendario Fornitori 2026-2029, orario 24 ore"],
])
p("Percorso: /app/workstation/<reparto>. Il campo **Production Capacity** è il numero di postazioni che lavorano in parallelo; la Lavorazione Esterna ha 50 postazioni per rappresentare fornitori diversi che lavorano contemporaneamente. Il nome del reparto è una chiave usata da distinte, Job Card e permessi degli operatori: **non si rinomina** da interfaccia.")

h(2, "7.2 Calendari (Holiday List)")
tb([3000, 1300, 4760], ["Calendario", "Giorni", "Contenuto"], [
    ["Calendario Remazel 2026-2029", "493", "Sabati, domeniche, festività nazionali e patronale, chiusure aziendali; reparti interni e default azienda"],
    ["Calendario Fornitori 2026-2029", "75", "Festività e chiusure aziendali senza fine settimana; Lavorazione Esterna"],
    ["Festivi Italia 2026-2027", "221", "Calendario precedente, mantenuto solo per ripristino"],
])
st([
    ["Aprire", ["/app/holiday-list/<calendario>."]],
    ["Aggiungere", ["Nella tabella Holidays inserire la data e la descrizione (es. chiusura estiva). Una riga per giorno."]],
    ["Allineare", ["Una chiusura aziendale va inserita in **entrambi** i calendari: i fornitori chiudono negli stessi periodi di Remazel."]],
    ["Effetto", ["Vale per le pianificazioni successive e per il report di carico. Le Job Card già pianificate non si spostano: se serve, si ripianifica con Simula/Applica Ritardo."]],
])

h(2, "7.3 Tempi delle fasi in distinta")
bl([
    "**Fasi interne**: tempo per pezzo in minuti (time_in_mins) sulla riga di operazione della distinta.",
    "**Fasi esterne**: tempo di attraversamento del lotto (TT) dal ciclo dell'Ufficio Tecnico, comprensivo di spedizione, con l'opzione **tempo fisso** attiva: la durata non si moltiplica per la quantità.",
    "Le distinte rilasciate non si modificano: per cambiare un ciclo si crea una nuova versione della distinta (Copia → modifica → rilascio → predefinita). I Work Order già creati mantengono la distinta con cui sono nati.",
    "Il fornitore della fase esterna (campo Fornitore della riga di operazione) va compilato nella nuova distinta: è da lì che lo legge la Job Card.",
])

h(2, "7.4 Impostazioni produzione")
tb([3600, 2000, 3460], ["Parametro", "Valore", "Dove"], [
    ["Capacity planning", "Attivo", "/app/manufacturing-settings"],
    ["Orizzonte di pianificazione", "365 giorni", "/app/manufacturing-settings"],
    ["Minuti tra operazioni", "0", "/app/manufacturing-settings"],
    ["Giacenze negative ammesse", "Sì (il magazzino è gestito in SAP)", "/app/stock-settings"],
])
bx("nota", "Orizzonte di pianificazione", [
    "Se le fasi di un set non trovano capacità entro l'orizzonte, il rilascio del Work Order si interrompe con un errore di capacità (CapacityError). Prima di aumentare l'orizzonte verificare i tempi in distinta: un tempo per pezzo inserito al posto di un tempo per lotto è la causa più frequente.",
])

h(2, "7.5 Buffer Project")
p("Project → scheda Details → sezione **Timeline** (chiusa per impostazione) → «Buffer Project (giorni)», default 5. Al salvataggio la «Deadline Interna (con buffer)» si ricalcola. Il buffer resta sul singolo Project per consentire margini diversi per ordine. La pianificazione a ritroso dei set usa come fine la data di consegna meno il buffer.")

# ------------------------------------------------------------------ 8
h(1, "8. Monitoraggio")
h(2, "8.1 Spazio di lavoro e menu laterale")
bl([
    "**Spazio di lavoro pubblico** «Produzione Remazel»: /app/produzione-remazel. Si modifica con il pulsante **Edit** in alto (ruolo Workspace Manager): i blocchi si trascinano, si aggiungono o si eliminano; poi **Save**.",
    "**Menu laterale**: /app/workspace-sidebar/Produzione Remazel, 13 voci. Ogni voce ha un tipo di collegamento ammesso: DocType, Page, Report, Workspace, Dashboard o URL. Il menu è richiamato anche dal menu laterale Manufacturing.",
    "Gli spazi di lavoro **privati** dei singoli utenti non si modificano: sono personali.",
])

h(2, "8.2 Indicatori e grafici")
tb([3300, 1900, 3860], ["Elemento", "Tipo", "Filtro principale"], [
    ["Ordini Commessa / Ordini Commessa T09", "Number Card", "Work Order del Project"],
    ["Pezzi Prodotti / Pezzi Prodotti T09", "Number Card", "Quantità prodotta dei Work Order"],
    ["Job Card Aperte, Ore Preventivate", "Number Card", "Job Card non completate"],
    ["Ordini di Produzione per Stato (anche T09)", "Dashboard Chart", "Work Order per stato"],
    ["Avvio Ordini per Settimana (anche T09)", "Dashboard Chart", "Data di inizio pianificata"],
    ["Operazioni per Reparto, Minuti per Reparto, Carico Settimanale, Job Card per Stato", "Dashboard Chart", "Job Card"],
])
p("Percorsi: /app/number-card/<nome> e /app/dashboard-chart/<nome>. Per un nuovo Project si **duplica** l'indicatore T09 (menu ... → Duplicate), si cambia il filtro sul Project e lo si aggiunge allo spazio di lavoro. Il nome «Ordini Commessa» è da rivedere nella fase di conversione delle etichette: il termine corretto è Project.")

h(2, "8.3 Punti di monitoraggio (Task)")
bl([
    "Per ogni set: un Task di gruppo e 6 Task di macro-assieme con le dipendenze (42 sulla T09, 21 sulla T08), generati dall'albero di distinta.",
    "Ogni Work Order è collegato al proprio Task con il campo **custom_task** («Punto di monitoraggio (Task)»).",
    "Percorso: /app/task filtrato per Project; Gantt dal pulsante Gantt dell'elenco.",
    "Per un nuovo Project la struttura si genera con la procedura di progetto (capitolo 10), non a mano.",
])

# ------------------------------------------------------------------ 9
h(1, "9. Utenti e permessi")
h(2, "9.1 Ruoli, profili e permessi")
tb([2800, 1800, 4460], ["Elemento", "Tipo", "Funzione"], [
    ["Operatore di Reparto", "Ruolo", "Accesso alle Job Card in lettura e scrittura, senza creazione, cancellazione e rilascio"],
    ["Permesso per reparto", "User Permission", "Ogni operatore vede solo le Job Card del proprio reparto (Workstation); due permessi per chi lavora su due reparti"],
    ["Responsabile Processo MES", "Profilo di ruoli", "Pianificazione, Work Order e Job Card senza diritti di amministrazione del sistema"],
    ["Permessi su Job Card", "Custom DocPerm", "Ruoli abilitati sulla Job Card (5 ruoli)"],
])
bx("criticita", "Permessi personalizzati sulla Job Card", [
    "In Frappe i permessi personalizzati di un documento **sostituiscono** quelli standard. Se da Role Permission Manager si modifica la Job Card, i ruoli standard (System Manager, Manufacturing Manager, Manufacturing User) devono restare nell'elenco, altrimenti perdono l'accesso alle Job Card.",
])

h(2, "9.2 Aggiungere un operatore")
st([
    ["Dipendente", ["/app/employee/new: nome, stato Active, campo Funzione, tipo di impiego (Dipendente Remazel o Esterno)."]],
    ["Utente", ["/app/user/new: indirizzo nel formato nome.cognome@mes.remazel.com, ruolo Operatore di Reparto; password impostata dall'amministratore."]],
    ["Collegamento", ["Sul dipendente compilare il campo User ID con l'utente creato."]],
    ["Reparto", ["/app/user-permission/new: utente, Allow = Workstation, valore = reparto, Applicable For = Job Card. Ripetere per un secondo reparto."]],
    ["Verifica", ["Accedere con l'utente e controllare che l'elenco Job Card mostri solo il proprio reparto."]],
])

# ------------------------------------------------------------------ 10
h(1, "10. Altre personalizzazioni")
tb([2900, 2100, 4060], ["Elemento", "Percorso", "Note"], [
    ["Operazione Documento Tecnico", "/app/doctype/Operazione Documento Tecnico", "Tabella dei documenti di fase: tipo (Disegno / WPS / Controllo Qualita / Altro), file, nota. Nuovi tipi si aggiungono come opzioni del campo tipo_documento"],
    ["Template controllo saldature", "/app/quality-inspection-template", "40 parametri, da validare; non ancora collegato al prodotto finito"],
    ["Matricole provvisorie", "/app/serial-no", "Serie T08-0100-A0001-.#### e T09-0100-A0001-.####; la matricola definitiva va nel campo «Matricola reale»"],
    ["Property Setter", "/app/property-setter", "Modifiche di proprietà dei campi standard (etichette, visibilità, obbligatorietà) fatte da Personalizza modulo; si gestiscono da lì, non dall'elenco"],
])

# ------------------------------------------------------------------ 11
h(1, "11. Procedure di progetto da console")
p("Le operazioni massive (allineamenti, generazione dei punti di monitoraggio, ripianificazione dei set) si eseguono con procedure Python dalla console del sito. Le procedure sono conservate nell'archivio del progetto (00_Script_Progetto, una cartella per sessione) e sul server in /home/frappe-user/script_progetto.")
p("Esecuzione standard, come utente frappe-user:")
cd(["cd /home/frappe-user/frappe-bench && bench --site site1.local console",
    "# 1) prova: elenca cosa cambierebbe, non scrive",
    'exec(open("/home/frappe-user/script_progetto/<procedura>.py").read(), {"frappe": frappe, "SCRIVI": False})',
    "# 2) scrittura, solo dopo aver controllato l'output della prova",
    'exec(open("/home/frappe-user/script_progetto/<procedura>.py").read(), {"frappe": frappe, "SCRIVI": True})'])
tb([3400, 5660], ["Procedura", "Funzione"], [
    ["inventario_personalizzazioni.py", "Sola lettura: inventario aggiornato di campi, script, report, reparti, calendari"],
    ["dettaglio_personalizzazioni.py", "Sola lettura: codice degli script, permessi, Property Setter"],
    ["scheduling_wo_t09.py", "Pianificazione a ritroso dei Work Order di un set (fine = consegna − buffer, mai nel passato)"],
    ["tempi_esterne_tt.py / verifica_tempi_esterne.py", "Allineamento e verifica dei tempi delle fasi esterne in distinta"],
    ["project_buffer_ricalcolo.py", "Ricalcolo della scadenza interna dei Project"],
    ["ritardo_set_codice.py", "Codice aggiornato di Simula/Applica Ritardo"],
    ["obiettivi_1a_1b_1c_1f.py", "Generazione dei punti di monitoraggio, indicatori e blocchi dello spazio di lavoro"],
])
bx("nota", "Regole della console", [
    "Le procedure si creano come file e si richiamano con una riga: incollare codice Python direttamente nel terminale bash produce errori.",
    "Dopo aver modificato un campo o uno script, **chiudere e riaprire la console**: la console conserva in memoria la struttura dei documenti letta all'avvio.",
])

# ------------------------------------------------------------------ 12
h(1, "12. Problemi noti e rimedi")
tb([3000, 3000, 3060], ["Sintomo", "Causa", "Rimedio"], [
    ["Un campo Select si compila da solo con la prima opzione", "Il valore predefinito di un Select è la prima opzione", "Lasciare vuota la prima riga delle opzioni"],
    ["Un conteggio di campi «compilati» include record vuoti", "Valori stringa vuota invece di NULL", "Nelle query usare IFNULL(campo,'') <> ''"],
    ["Uno script si interrompe con «__import__ not found»", "L'ambiente protetto blocca gli import", "Usare frappe.utils.<funzione>"],
    ["Una modifica di struttura non si vede da console", "Struttura del documento in memoria", "Riaprire la console"],
    ["Rilascio del Work Order bloccato da CapacityError", "Tempi di fase eccessivi o orizzonte insufficiente", "Verificare i tempi in distinta (capitolo 7.3)"],
    ["Utenti senza accesso alle Job Card", "Permessi personalizzati incompleti", "Ripristinare i ruoli standard nei permessi della Job Card"],
    ["Barre del Gantt invisibili", "Difetto grafico di Frappe v16", "Verificare che lo script Gantt_Fix del documento sia attivo"],
    ["Date con ora nei campi data di una finestra", "Campo data e ora passato a un campo data", "Usare solo la parte data del valore"],
])

# ------------------------------------------------------------------ 13
h(1, "13. Raccomandazioni")
bl([
    "**Esportare le personalizzazioni** come fixtures in un'applicazione dedicata (campi, script, report, spazio di lavoro): diventano versionate, confrontabili e reinstallabili su un sito di prova o dopo un ripristino.",
    "**Sito di prova**: una copia del sito di produzione su cui provare le modifiche agli script prima di applicarle.",
    "**Backup pianificato** giornaliero con copia fuori dal server.",
    "**Conversione delle etichette in inglese** come fase successiva, con un glossario validato e le traduzioni italiane per gli operatori di reparto.",
    "**Aggiornamento di questa guida** a ogni nuova personalizzazione, rilanciando l'inventario di sola lettura.",
])


# ---------------------------------------------------------- stima pagine
def stima_pagine(contenuto, prima=3, righe_pag=46.0):
    def r_testo(t, larg):
        cpl = max(10, larg / 9060.0 * 105)
        return max(1, math.ceil(len(t) / cpl))
    pos, pag, out = 0.0, prima, {}
    for it in contenuto:
        t = it[0]
        if t == "h":
            add = 3.0 if it[1] == 1 else 2.2
            if pos + add + 3 > righe_pag:
                pag, pos = pag + 1, 0.0
            out[it[2]] = pag
        elif t == "p":
            add = r_testo(it[1], 9060) + 0.8
        elif t == "bullets":
            add = sum(r_testo(b, 8600) + 0.4 for b in it[1])
        elif t == "table":
            cols = it[1]
            add = 1.3 + sum(max(r_testo(c, w) for c, w in zip(row, cols)) * 0.9 + 0.4 for row in it[3])
        elif t == "box":
            add = 1.5 + sum(r_testo(x, 8800) * 0.9 for x in it[3])
        elif t == "steps":
            add = sum(max(1.6, sum(r_testo(d, 6060) * 0.9 for d in ds)) + 0.5 for _, ds in it[1])
        elif t == "code":
            add = len(it[1]) * 0.9 + 1
        pos += add
        while pos > righe_pag:
            pag, pos = pag + 1, pos - righe_pag
    return out


doc = S.Documento(meta, titolo, sottotitolo, C)
OUT = "/home/user/AI-Project/01_Documentazione_bozze/" + NOME
pagine = stima_pagine(C)
json.dump(pagine, open("/home/user/AI-Project/01_Documentazione_bozze/pagine_guida.json", "w"), ensure_ascii=False, indent=0)
S.scrivi(doc, OUT, "Remazel Engineering S.p.A.", "Guida personalizzazioni MES", pagine)
print(OUT, "pagine stimate:", max(pagine.values()))
