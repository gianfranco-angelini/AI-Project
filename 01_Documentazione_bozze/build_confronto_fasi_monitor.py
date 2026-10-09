import sys, os, json, re
sys.path.insert(0, "/root/.claude/skills/synced/593ea5d8-9a85-4668-a3fb-0290e8e227e7_746b874a-eee2-4e96-b44c-f02049e430c1/docx-startit/scripts")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import startit_docx as S
from stima_pagine import stima_pagine

BASE = "/home/user/AI-Project/01_Documentazione_bozze/"
NOME = "Analisi_Confronto_Fasi_Monitor_Remazel_B1.docx"
meta = {
    "Documento": NOME,
    "Versione": "Bozza 1 — 9 ottobre 2026",
    "Data": "9 ottobre 2026",
    "Redatto da": "Start I.T. S.r.l.",
    "Destinatario": "Remazel Engineering S.p.A. — BU Combustion",
    "Sistema": "M.E.S. Remazel — ERPNext v16",
    "Riferimento": "T09-0100 (Job 26-19008) — combustionerp.remazel.com; modulo 371 dei monitor Timesheet",
    "Stato": "Documento di analisi",
}
titolo = ["CONFRONTO FASI DI CICLO", "SISTEMA E MONITOR DI PRODUZIONE"]
sottotitolo = ["Corrispondenza fra le fasi del ciclo T09-0100 in ERPNext", "e i codici attività timbrati sui monitor Timesheet",
               "Remazel Engineering S.p.A. — BU Combustion"]

C = []
h = lambda l, t: C.append(("h", l, t))
p = lambda t: C.append(("p", t))
bl = lambda items: C.append(("bullets", items))
tb = lambda cols, head, rows: C.append(("table", cols, head, rows))
bx = lambda k, t, ps: C.append(("box", k, t, ps))

# ------------------------------------------------------------------ 1
h(1, "1. Premessa")
p("In reparto le ore di lavoro si registrano oggi sui monitor Timesheet con i codici attività del modulo 371 (ciclo di assemblaggio B.U. Combustion), letti da schede a codice a barre. Per confrontare nella fase iniziale i dati del sistema con il monitoraggio attuale serve sapere quante fasi del ciclo ERPNext trovano un codice corrispondente nel 371.")
p("Un primo confronto, eseguito dalla funzione IT sul file del ciclo 26-19008, indicava **463 fasi su 598 senza corrispondenza (77%)**. Questo documento rifà il confronto partendo dai dati presenti nel sistema e ne spiega il risultato.")

# ------------------------------------------------------------------ 2
h(1, "2. Fonti e metodo")
tb([2600, 6460], ["Fonte", "Contenuto"], [
    ["Sistema ERPNext (estrazione del 9 ottobre 2026)", "57 distinte del Project T09, 540 operazioni con codice fase, 3.330 Job Card con tempi pianificati e registrati"],
    ["Modulo 371, foglio Liner Fr7 FA", "Codici attività Vxxx usati sui monitor, divisi per gruppo: Liner, Venturi, Cap, Molle, Final Assy"],
    ["Confronto della funzione IT", "Abbinamento fase per fase del file ciclo 26-19008 al modulo 371, con livello di affidabilità"],
])
bl([
    "**Tipo di fase**: ricavato dalla sigla finale del codice fase (SA saldatura, ML molatura, MT montaggio, ST formatura, QC/VT/PT controlli, MX/VX/RX controlli radiografici, LA/LT/TT/FE lavorazioni esterne).",
    "**Interna o esterna**: dalla postazione dell'operazione (Lavorazione Esterna = conto lavoro).",
    "**Abbinamento al 371**: per articolo e tipo di fase, sulla base del gruppo di appartenenza del componente; ogni fase riceve un livello: univoca, probabile, ambigua, generica, nessuna.",
])

# ------------------------------------------------------------------ 3
h(1, "3. Base dati: sistema e file del ciclo")
p("Il file del ciclo usato nel primo confronto conta 598 righe fase: 559 operazioni e 39 righe di materia prima, che nel sistema sono componenti di distinta e non operazioni. Le 559 operazioni del file e le 540 del sistema differiscono di 19 righe:")
tb([2200, 1000, 5860], ["Articolo", "Righe", "Motivo"], [
    ["P1600", "15", "Componente usato in due punti dell'albero: il file ripete le fasi, il sistema le carica una volta con quantità 2"],
    ["P1130", "2", "Due controlli dimensionali presenti nel file e non a sistema"],
    ["P2200", "1", "Un controllo dimensionale presente nel file e non a sistema"],
    ["P2301", "1", "Valutazione RX W30 presente nel file e non a sistema"],
])
p("In 95 operazioni il codice fase del sistema inizia con T08 e nel file con T09: è la regola di codifica adottata (articolo identico alla T08 = codice T08) e non cambia la fase.")
bx("positivo", "Esito", [
    "Nessuna fase produttiva manca nel sistema. Tutte le 540 operazioni hanno il codice fase e tutte le 3.330 Job Card sono collegate a un'operazione di distinta.",
])

# ------------------------------------------------------------------ 4
h(1, "4. Perimetro confrontabile")
p("Il modulo 371 codifica solo il lavoro manuale interno: assemblaggio, saldatura, molatura, conformatura, più alcune voci generiche (riparazioni, pulizia, attrezzature). Le fasi del sistema si dividono così:")
tb([3700, 1300, 4060], ["Categoria", "Operazioni", "Codice nel 371"], [
    ["Fasi produttive interne (SA, ML, MT, ST)", "126", "Sì"],
    ["Saldature in conto lavoro (SA)", "6", "Sì (nel 371 come saldatura)"],
    ["Controlli qualità (QC, VT, PT)", "215", "No"],
    ["Controlli radiografici (MX, VX, RX)", "107", "No"],
    ["Lavorazioni esterne (LA, LT, TT, FE)", "85", "No"],
    ["Flussaggio (TE)", "1", "No"],
    ["Totale", "540", ""],
])
p("Le fasi senza codice nel 371 non sono un difetto del ciclo: controlli e lavorazioni esterne non si timbrano sui monitor, quindi non possono avere corrispondenza. Il confronto ha senso sulle **132 fasi produttive** (126 interne e 6 saldature in conto lavoro).")

# ------------------------------------------------------------------ 5
h(1, "5. Corrispondenza delle fasi produttive")
h(2, "5.1 Livello di corrispondenza")
tb([3400, 1500, 4160], ["Livello", "Fasi", "Significato"], [
    ["Univoca", "52", "Un solo codice 371 per la fase"],
    ["Probabile", "22", "Un codice, scelto per analogia di operazione e componente"],
    ["Ambigua", "37", "Due o tre codici possibili: il 371 distingue sottoassiemi che il ciclo non separa, o viceversa"],
    ["Generica", "18", "Solo voci generiche: riparazioni (V191), pulizia (V605)"],
    ["Nessuna", "3", "Marcature DOTPEEN, non previste nel 371"],
    ["Totale", "132", ""],
])
p("Sulle 126 fasi interne il tempo pianificato è di 4.645 minuti per ciclo: il 59% ricade in fasi con corrispondenza univoca o probabile.")
h(2, "5.2 Dettaglio per gruppo")
tb([1950, 650, 1050, 1200, 1200, 1200, 1810], ["Gruppo 371", "Fasi", "Univoca", "Probabile", "Ambigua", "Generica", "Minuti int."], [
    ["Liner (V100)", "40", "16", "2", "13", "9", "1.271"],
    ["Venturi (V200)", "22", "9", "6", "5", "1", "875"],
    ["Cap (V300)", "56", "19", "14", "18", "5", "1.927"],
    ["Molle (V400)", "4", "3", "0", "1", "0", "32"],
    ["Final Assy (V500)", "10", "5", "0", "0", "3", "540"],
])
p("Nella tabella mancano le 3 fasi senza corrispondenza (2 in Final Assy, 1 in Venturi).")
h(2, "5.3 Confronto con l'abbinamento della funzione IT")
p("Sulle 132 fasi produttive i due abbinamenti condividono almeno un codice in **103 casi**. In **25 casi** i codici sono diversi; le differenze si concentrano in tre punti:")
bl([
    "**Cap, inner body e outer body**: quali virole (P2201, P2202, P2301, P2304, P2307) appartengono all'uno o all'altro sottoassieme;",
    "**Swirler A2000**: codici della raggiera o della virola con swirler esterno;",
    "**Liner, giunzioni circonferenziali** (P1104): il 371 numera le giunzioni secondo un'altra revisione del disegno.",
])
p("L'elenco completo è nell'Allegato A (colonna IT = abbinamento della funzione IT).")
bx("nota", "Revisione del disegno", [
    "Alcuni codici di componente citati nel 371 (P1002, P1003, P1500 e altri) appartengono a una revisione del disegno diversa dalla 26-19008. Per le fasi ambigue e discordi la scelta del codice spetta al responsabile di produzione, che conosce l'uso reale delle schede a codice a barre.",
])

# ------------------------------------------------------------------ 6
h(1, "6. Dati effettivi disponibili")
p("Al 9 ottobre 2026 nel sistema risultano **50 Job Card completate su 3.330**: 31 di lavorazioni esterne e 19 di fasi interne, per 3.960 minuti registrati sulle fasi interne. **Nessuna Job Card delle fasi produttive interne è ancora completata.**")
p("Il confronto delle ore effettive con i monitor potrà iniziare solo quando i reparti registreranno l'avanzamento sulle Job Card.")

# ------------------------------------------------------------------ 7
h(1, "7. Conclusioni")
bl([
    "**Il 77% senza corrispondenza non indica un problema del ciclo**: è composto da controlli, lavorazioni esterne e righe di materia prima, che il modulo 371 non codifica.",
    "**Sulle fasi produttive la corrispondenza esiste quasi sempre**, ma è univoca o probabile solo per 74 fasi su 132 (56%): il 371 è più sintetico del ciclo e riferito a un'altra revisione del disegno.",
    "**Un confronto attendibile si fa per gruppo** (Liner, Venturi, Cap, Molle, Final Assy) e non per singola fase, salvo validare prima le 37 fasi ambigue e le 25 discordi.",
    "**Mancano ancora le ore effettive nel sistema**: è il prerequisito di qualunque confronto con il monitoraggio attuale.",
])
bx("positivo", "Esito", [
    "Il ciclo T09-0100 in ERPNext è completo e coerente con il file del ciclo. Il confronto con i monitor è possibile per gruppo di lavorazione appena i reparti registreranno l'avanzamento.",
])

# ------------------------------------------------------------------ A
h(1, "Allegato A. Fasi con abbinamento diverso")
disc = json.load(open("/home/user/AI-Project/00_Script_Progetto/sessione_24/confronto_371/discordanze.json", encoding="utf-8"))
righe = []
def compatta(codici):
    v = [c.strip() for c in codici.split("/")]
    return v[0] + "".join("/" + c[1:] for c in v[1:])
for cod, desc, nostra, it in disc:
    desc = re.sub(r"\s*\([^)]*S\.?R\.?L\.?\)", "", desc).strip()
    desc = desc.replace("Conformatura manuale + ", "Conformaz. + ").replace(" a filo entrambi lati", "").replace("Pulizia + Montaggio + Puntatura assieme", "Pulizia, montaggio, puntatura")
    righe.append([cod, desc, compatta(nostra), compatta(it)])
tb([2450, 3660, 1650, 1300], ["Codice fase", "Descrizione", "Analisi", "IT"], righe)

doc = S.Documento(meta, titolo, sottotitolo, C)
OUT = BASE + NOME
pj = BASE + "pagine_confronto_monitor.json"
pagine = json.load(open(pj)) if os.path.exists(pj) else stima_pagine(C)
S.scrivi(doc, OUT, "Remazel Engineering S.p.A.", "Confronto fasi sistema / monitor", pagine)
print(OUT, "pagine:", max(pagine.values()))
