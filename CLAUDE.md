# AI-Project — Contesto operativo

## Nota origine

Questo repository (`gianfranco-angelini/AI-Project`) è stato trovato **vuoto** (nessun
commit) all'avvio della prima sessione. `12_Memorie/CONTESTO_PROGRESSIVO_ERPNext.md`
è stato successivamente allineato al file consolidato del Project Cowork "Ciclo
produzione Remazel Combustion" (versione più recente: Sessione 18, 27/09/2026),
fornito da Gian. Quel file resta la fonte di verità del contesto progressivo;
questo repo ne tiene una copia sincronizzata a fine sessione.

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
