# AI-Project — Contesto operativo

## Nota origine

Questo repository (`gianfranco-angelini/AI-Project`) è stato trovato **vuoto** (nessun
commit) all'avvio di questa sessione. I file `CLAUDE.md` e
`12_Memorie/CONTESTO_PROGRESSIVO_ERPNext.md` non esistevano. Sono stati ricostruiti a
partire dal contenuto della skill `anthropic-skills:erpnext-remazel`, che è la fonte
operativa sincronizzata del progetto ERPNext @ Remazel Engineering.

La fonte di verità del contesto progressivo è normalmente il **Project Cowork**
(non questo repo git). Se esiste già un `CONTESTO_PROGRESSIVO_ERPNext.md` più
recente altrove (Project Cowork, altro repo/branch), va preferito a questa
ricostruzione.

## Progetto

ERPNext v16 @ Remazel Engineering — sito `combustionerp.remazel.com`.

| Parametro        | Valore                                          |
|------------------|--------------------------------------------------|
| Server           | cs-erp01 (Ubuntu)                               |
| Sito Frappe      | combustionerp.remazel.com / site1.local         |
| Utente server    | frappe-user                                     |
| Directory bench  | /home/frappe-user/frappe-bench                  |
| Versione         | ERPNext v16 / Frappe v16                        |
| Ordine di test   | SAL-ORD-2026-00001                              |
| WIP Warehouse    | Goods In Transit - Rema                         |

Tutti i comandi CLI vanno eseguiti come `frappe-user` nella directory
`/home/frappe-user/frappe-bench`.

## Preferenze operative (Gian)

- Risposte dirette e concise, senza preamboli o riepilogo iniziale
- Esecuzione passo-passo: verificare lo stato prima di ogni modifica
- Riscrivere sempre file completi, mai snippet parziali
- Non ripetere passi già confermati come eseguiti
- Comunicazione in italiano

## Dove trovare i dettagli

- Comportamenti noti ERPNext v16 (sub-assembly, Production Plan, WO Draft,
  submit massivo, amend da bench console, CapacityError, ecc.): vedi skill
  `anthropic-skills:erpnext-remazel`
- Stato progressivo del progetto e task aperti: `12_Memorie/CONTESTO_PROGRESSIVO_ERPNext.md`
