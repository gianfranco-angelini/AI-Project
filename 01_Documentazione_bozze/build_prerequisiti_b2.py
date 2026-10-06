import sys, os, json
sys.path.insert(0, "/root/.claude/skills/synced/593ea5d8-9a85-4668-a3fb-0290e8e227e7_746b874a-eee2-4e96-b44c-f02049e430c1/docx-startit/scripts")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import startit_docx as S
from stima_pagine import stima_pagine

NOME = "Analisi_Prerequisiti_GoLive_BU_Combustion_B2.docx"
meta = {
    "Documento": NOME,
    "Versione": "Bozza 2 — 6 ottobre 2026",
    "Data": "6 ottobre 2026",
    "Redatto da": "Start I.T. S.r.l.",
    "Destinatario": "Remazel Engineering S.p.A. — BU Combustion",
    "Sistema": "M.E.S. Remazel — ERPNext v16",
    "Riferimento": "T09-0100 (Job 26-19008) · T08-0100 (Job 24-19006) — combustionerp.remazel.com",
    "Stato": "Documento di analisi — base per confronto",
}
titolo = ["PREREQUISITI PER IL GO-LIVE", "SISTEMA BU COMBUSTION"]
sottotitolo = ["Condizioni ancora da soddisfare per l'uso del sistema", "in reparto e nella gestione delle lavorazioni esterne",
               "Remazel Engineering S.p.A. — BU Combustion"]

C = []
h = lambda l, t: C.append(("h", l, t))
p = lambda t: C.append(("p", t))
bl = lambda items: C.append(("bullets", items))
tb = lambda cols, head, rows: C.append(("table", cols, head, rows))
bx = lambda k, t, ps: C.append(("box", k, t, ps))
st = lambda items: C.append(("steps", items))

# ------------------------------------------------------------------ 1
h(1, "1. Premessa")
p("La Bozza 1 dell'11 settembre 2026 elencava i dati da consolidare prima di mettere in produzione il sistema sulla T08-0100. Da allora il quadro è cambiato in tre punti:")
bl([
    "**il prodotto in esercizio è la T09-0100**: 6 set di consegna, 348 Work Order rilasciati e pianificati sulla capacità reale dei reparti;",
    "**il magazzino resta in SAP**: ERPNext pianifica e registra l'avanzamento, senza gestire acquisti, prezzi e giacenze;",
    "**le lavorazioni esterne** si seguono per eventi (spedizione e rientro), con un Ordine conto lavoro da realizzare.",
])
p("In questo documento **go-live** significa l'uso quotidiano del sistema da parte dei reparti e della funzione che segue le lavorazioni esterne, con date e ritardi attendibili. Come la Bozza 1, è una base di discussione: molti punti richiedono informazioni o decisioni che solo le funzioni Remazel possono dare.")

# ------------------------------------------------------------------ 2
h(1, "2. Stato del sistema al 6 ottobre 2026")
tb([3400, 5660], ["Blocco", "Stato"], [
    ["Cicli e distinte T08 e T09", "Completi, con tempi interni reali e tempi di attraversamento dei fornitori"],
    ["Pianificazione", "Sulla capacità reale dei reparti e sui calendari aziendale e fornitori; a ritroso dalla consegna di ogni set"],
    ["Work Order e Job Card T09", "348 Work Order rilasciati, oltre 3.300 Job Card pianificate"],
    ["Utenti", "21 operatori con accesso filtrato per reparto; profilo per il governo del processo"],
    ["Monitoraggio", "Master Plan, Gantt per set, punti di monitoraggio, carico reparti, indicatori"],
    ["Ripianificazione", "Simulazione e applicazione dei ritardi con effetto sulla consegna del set"],
    ["Conto lavoro", "Fornitore, n° ordine SAP, data promessa e stato sulla Job Card; Ordine conto lavoro da realizzare"],
    ["Documentazione", "Riepilogo, Analisi Obiettivi B4, Guida Concettuale B7, Manuale Utente B3, Guida Personalizzazioni B2"],
])

# ------------------------------------------------------------------ 3
h(1, "3. Esito dei prerequisiti della Bozza 1")
tb([2700, 1500, 4860], ["Prerequisito (Bozza 1)", "Esito", "Nota"], [
    ["Prezzi fornitore reali", "Decaduto", "Acquisti e valorizzazione restano in SAP"],
    ["Valorizzazione del grezzo di fusione", "Decaduto", "Come sopra"],
    ["Carico iniziale di magazzino", "Decaduto", "Il magazzino resta in SAP; in ERPNext le giacenze negative sono ammesse per scelta"],
    ["Anagrafiche del personale", "Chiuso", "21 operatori con utente e reparto"],
    ["Capacità reale dei reparti", "Chiuso", "Postazioni confermate dalla produzione e caricate"],
    ["Ciclo di lavorazione consolidato", "Chiuso", "Ciclo T09 validato; tempi delle fasi esterne confermati dall'Ufficio Tecnico"],
    ["Codici reali dei microfusi", "Da confermare", "Verificare che i codici in distinta siano quelli definitivi"],
    ["Codici interni non chiariti", "Da confermare", "Impatto limitato"],
    ["Template di controllo qualità", "Aperto", "Template saldature predisposto, da validare"],
    ["Tracciabilità seriali e saldature", "Deciso in parte", "Matricola sul prodotto finito; aperto il lotto materiale"],
])

# ------------------------------------------------------------------ 4
h(1, "4. Prerequisiti bloccanti")
p("Senza questi punti il sistema funziona, ma le informazioni che fornisce ai reparti e alla direzione non sono attendibili.")
tb([2500, 4060, 2500], ["Prerequisito", "Perché blocca", "Funzione"], [
    ["Stato reale dei set 1 e 2", "I set già in produzione sono pianificati come se partissero oggi: date e ritardi non sono reali", "Pianificazione di produzione"],
    ["Regole di registrazione in reparto", "Chi conferma le Job Card completate; fasi aperte a fine turno, riprese, più operatori sulla stessa fase", "Pianificazione di produzione"],
    ["Formazione degli utenti", "Uso per funzione secondo il Manuale Utente; consegna delle credenziali agli operatori", "Pianificazione di produzione, con Start I.T."],
    ["Ordine conto lavoro e cruscotto", "Oltre la metà del tempo di attraversamento è presso i fornitori: senza strumento le lavorazioni esterne restano su file separati", "Start I.T. (sviluppo), Acquisti"],
    ["Informazioni SAP sul conto lavoro", "Documenti SAP usati, codice con cui viaggia il pezzo a metà ciclo, magazzini dei fornitori", "Acquisti"],
    ["Accesso a SAP in sola lettura", "Necessario per leggere spedizioni e rientri dai magazzini dei fornitori", "IT"],
    ["Chiusura dei Work Order", "Verifica della registrazione dello scarico di produzione senza trasferimento di materiale", "Start I.T."],
    ["Backup pianificato", "Le personalizzazioni e i dati di produzione esistono solo nel database del sistema", "IT"],
])

# ------------------------------------------------------------------ 5
h(1, "5. Attività non bloccanti")
p("Possono proseguire in parallelo o subito dopo l'avvio.")
tb([2900, 3660, 2500], ["Attività", "Nota", "Funzione"], [
    ["Pianificazione a ritroso e punti di monitoraggio da interfaccia", "Rende autonoma la Pianificazione sugli ordini successivi alla T09", "Start I.T."],
    ["Import/export del ciclo da Excel", "Modifica agile dei cicli (obiettivo 2a)", "Start I.T., Ufficio Tecnico"],
    ["Documenti di fase e stampa della scheda", "Quali documenti, chi li mantiene, revisioni (obiettivo 2b)", "Ufficio Tecnico"],
    ["Timbratura con codice a barre", "Dopo la stampa della scheda (obiettivo 2c)", "Pianificazione di produzione"],
    ["Lotto materiale", "Campo non obbligatorio o lettura da SAP; livelli da tracciare", "Qualità"],
    ["Template controllo saldature", "Validazione e collegamento al prodotto finito", "Qualità, Ufficio Tecnico"],
    ["Etichette in inglese", "Conversione con glossario validato; italiano disponibile per gli operatori", "Direzione BU, Start I.T."],
    ["Posta in uscita", "Notifiche automatiche del sistema", "IT"],
    ["Anagrafica fornitori", "Verifica di due ragioni sociali simili per le saldature esterne", "Acquisti"],
    ["Work Order T08", "Prodotto sospeso: decidere se mantenere o annullare i Work Order aperti", "Direzione BU"],
    ["Sito di prova", "Copia del sistema per provare le modifiche prima di applicarle", "IT, Start I.T."],
])

# ------------------------------------------------------------------ 6
h(1, "6. Proposta di percorso")
st([
    ["Allineamento", ["Rilevazione dello stato reale dei set 1 e 2 e suo caricamento.", "Verifica delle date di fine set rispetto alle consegne."]],
    ["Regole e formazione", ["Definizione delle regole di registrazione in reparto.", "Formazione per funzione e consegna delle credenziali."]],
    ["Avvio in reparto", ["Uso delle Job Card nei reparti interni, partendo da un reparto pilota e poi esteso.", "Controllo settimanale di Master Plan e carico reparti."]],
    ["Lavorazioni esterne", ["Ordine conto lavoro e cruscotto; lettura dei movimenti da SAP appena disponibile l'accesso."]],
    ["Autonomia", ["Pianificazione a ritroso, punti di monitoraggio e import del ciclo da interfaccia, per gli ordini successivi."]],
])

# ------------------------------------------------------------------ 7
h(1, "7. Rischio di procedere senza questi dati")
p("Avviare l'uso in reparto senza allineare i set già in produzione porterebbe il sistema a segnalare ritardi che non esistono, o a non vedere quelli reali: la fiducia nel dato si perderebbe dal primo giorno. Senza uno strumento per le lavorazioni esterne, la parte del ciclo che determina le date di consegna resterebbe fuori dal sistema.")
bx("positivo", "Cosa non serve più", [
    "Rispetto alla Bozza 1 non sono più prerequisiti prezzi, valorizzazioni e carico di magazzino: restano in SAP. Il percorso dipende ora da tre elementi: l'allineamento dei set in corso, le regole di reparto e lo strumento per il conto lavoro.",
])

doc = S.Documento(meta, titolo, sottotitolo, C)
OUT = "/home/user/AI-Project/01_Documentazione_bozze/" + NOME
pagine = stima_pagine(C)
json.dump(pagine, open("/home/user/AI-Project/01_Documentazione_bozze/pagine_prerequisiti.json", "w"), ensure_ascii=False, indent=0)
S.scrivi(doc, OUT, "Remazel Engineering S.p.A.", "Prerequisiti per il Go-Live", pagine)
print(OUT, "pagine stimate:", max(pagine.values()))
