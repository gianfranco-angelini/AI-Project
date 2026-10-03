# Sessione 22 - Lettura in SOLA LETTURA dal database SAP B1 (SQL Server cs-sql03.remazel.local:1433).
# Gira su cs-erp01 in un ambiente Python separato (~/sap_conn), NON nel bench ERPNext.
# Credenziali in ~/.sap_ro.json (chmod 600), mai in chat o nel repository:
#   {"server": "cs-sql03.remazel.local", "port": 1433, "database": "<DB_SOCIETA>", "user": "<utente_ro>", "password": "<password>"}
# Uso: ~/sap_conn/bin/python ~/script_progetto/sap_lettura.py
import json
import os
import sys
import pymssql

cfg = json.load(open(os.path.expanduser("~/.sap_ro.json")))
QUERY = [
    ("1) Magazzini usati per fornitore negli ultimi 12 mesi (trasferimenti con BP in testata)", """
SELECT T0.CardCode, T0.CardName, T1.FromWhsCod AS DaMag, T1.WhsCode AS AMag,
       COUNT(DISTINCT T0.DocEntry) AS NTrasf, MIN(T0.DocDate) AS Primo, MAX(T0.DocDate) AS Ultimo
FROM OWTR T0 JOIN WTR1 T1 ON T1.DocEntry = T0.DocEntry
WHERE T0.CardCode IS NOT NULL AND T0.DocDate >= DATEADD(month, -12, GETDATE())
GROUP BY T0.CardCode, T0.CardName, T1.FromWhsCod, T1.WhsCode
ORDER BY T0.CardName"""),
    ("2) Ultimi movimenti verso/da SOMECAR (codici articolo)", """
SELECT TOP 30 T0.DocNum, T0.DocDate, T0.CardName, T1.ItemCode, T1.Dscription, T1.Quantity, T1.FromWhsCod, T1.WhsCode
FROM OWTR T0 JOIN WTR1 T1 ON T1.DocEntry = T0.DocEntry
WHERE T0.CardName LIKE '%SOMECAR%'
ORDER BY T0.DocDate DESC"""),
    ("3) Campi utente sull'anagrafica BP", """
SELECT AliasID, Descr FROM CUFD WHERE TableID = 'OCRD'"""),
    ("4) Elenco magazzini", """
SELECT WhsCode, WhsName, Inactive FROM OWHS ORDER BY WhsCode"""),
]
try:
    con = pymssql.connect(server=cfg["server"], port=int(cfg.get("port", 1433)), user=cfg["user"], password=cfg["password"], database=cfg["database"], login_timeout=15, timeout=120)
except Exception as e:
    print("CONNESSIONE FALLITA:", repr(e)[:300])
    sys.exit(1)
cur = con.cursor()
for titolo, sql in QUERY:
    print("")
    print("=== " + titolo + " ===")
    try:
        cur.execute(sql)
        colonne = [c[0] for c in cur.description]
        print(" | ".join(colonne))
        n = 0
        for r in cur.fetchall():
            print(" | ".join(["" if v is None else str(v) for v in r]))
            n = n + 1
        print("(" + str(n) + " righe)")
    except Exception as e:
        print("ERRORE:", repr(e)[:300])
con.close()
