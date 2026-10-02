# import_t09.py — carico T09-0100 (Item + BOM) + BOM -002 di T08-0100-P2301
# SCRIVI = False -> solo stampa e verifiche, nessuna scrittura
import json
SCRIVI = False
D = json.loads('[{"code":"T09-0100-P2114","name":"WASHER","cp":"T08-0100-P2113","ops":[["T09-0100-P2114-10LA","10LA","Taglio laser 2D","INOXEA SRL",50.0,"T08-0100-P2114-10LA"],["T09-0100-P2114-10QC","10QC","QC Dimensionale","",5.0,"T09-0100-P2114-10QC"]],"ch":[],"mat":["001-0023-C0600"]},{"code":"T09-0100-P3101","name":"CONE OUTER FWD VENTURI","cp":"T08-0100-P3101","ops":[["T09-0100-P3101-10LT","10LT","Taglio sviluppo","INOXEA SRL",600.0,"T08-0100-P3101-10LT"],["T09-0100-P3101-10QC","10QC","QC Dimensionale","",5.0,"T08-0100-P3101-10QC"],["T09-0100-P3101-10LA","10LA","Stampaggio e rifilatura","MAC STAMP SRL",1500.0,"T08-0100-P3101-10LA"],["T09-0100-P3101-20QC","20QC","QC Dimensionale","",10.0,"T08-0100-P3101-20QC"]],"ch":[],"mat":["F000"]},{"code":"T09-0100-P3103","name":"CONE OUTER AFT VENTURI","cp":"T08-0100-P3103","ops":[["T09-0100-P3103-10LT","10LT","Taglio sviluppo","INOXEA SRL",600.0,"T09-0100-P3103-10LT"],["T09-0100-P3103-10QC","10QC","QC Dimensionale","",5.0,"T09-0100-P3103-10QC"],["T09-0100-P3103-10LA","10LA","Stampaggio e rifilatura","MAC STAMP SRL",1500.0,"T09-0100-P3103-10LA"],["T09-0100-P3103-20QC","20QC","QC Dimensionale","",10.0,"T09-0100-P3103-20QC"]],"ch":[],"mat":["F000"]},{"code":"T09-0100-P3104","name":"SLEEVE OUTER VENTURI","cp":"T08-0100-P3104","ops":[["T09-0100-P3104-10LT","10LT","Taglio sviluppo + Calandratura","SOMECAR SRL",900.0,"T09-0100-P3104-10LT"],["T09-0100-P3104-10QC","10QC","QC Dimensionale","",5.0,"T09-0100-P3104-10QC"],["T09-0100-P3104-10SA","10SA","Saldatura longitudinale W21","",30.0,"T09-0100-P3104-10SA"],["T09-0100-P3104-10MX","10MX","Definizione mappe radiografiche W21 + Marcatura pezzi","",15.0,"T09-0100-P3104-10MX"],["T09-0100-P3104-10RX","10RX","RX W21","A.M.C. CONTROL SRL",1800.0,"T09-0100-P3104-10RX"],["T09-0100-P3104-10VX","10VX","Valutazione RX W21","",1,"T09-0100-P3104-10VX"],["T09-0100-P3104-10ML","10ML","Conformatura manuale + Molatura W21 a filo entrambi lati","",30.0,"T09-0100-P3104-10ML"],["T09-0100-P3104-10VT","10VT","VT W21","",5.0,"T09-0100-P3104-10VT"],["T09-0100-P3104-10PT","10PT","PT W21","",45.0,"T09-0100-P3104-10PT"],["T09-0100-P3104-10ST","10ST","Calibratura con espantore manuale","",5.0,"T09-0100-P3104-10ST"],["T09-0100-P3104-20QC","20QC","QC Dimensionale","",5.0,"T09-0100-P3104-20QC"],["T09-0100-P3104-10LA","10LA","Tornitura rifilatura","EPIS SRL",1800.0,"T09-0100-P3104-10LA"],["T09-0100-P3104-30QC","30QC","QC Dimensionale","",5.0,"T09-0100-P3104-30QC"]],"ch":[],"mat":["F000"]},{"code":"T08-0200-P3203","name":"THROAT RING","cp":"T08-0100-P3203","ops":[["T08-0200-P3203-10LT","10LT","Taglio laser + Calandratura virola singola","INOXEA SRL",1200.0,"T08-0200-P3203-10LT"],["T08-0200-P3203-10QC","10QC","QC visivo e dimensionale","",5.0,"T08-0200-P3203-10QC"],["T08-0200-P3203-10SA","10SA","Saldatura longitudinale W15","",90.0,"T08-0200-P3203-10SA"],["T08-0200-P3203-10MX","10MX","Definizione mappe radiografiche W15 + Marcatura pezzi","",15.0,"T08-0200-P3203-10MX"],["T08-0200-P3203-10RX","10RX","RX W15","A.M.C. CONTROL SRL",1800.0,"T08-0200-P3203-10RX"],["T08-0200-P3203-10VX","10VX","Valutazione RX W15","",1,"T08-0200-P3203-10VX"],["T08-0200-P3203-10TT","10TT","Trattamento termico di solubilizzazione","BODYCOTE SPA",600.0,"T08-0200-P3203-10TT"],["T08-0200-P3203-20QC","20QC","QC Dimensionale","",5.0,"T08-0200-P3203-20QC"],["T08-0200-P3203-10ML","10ML","Conformatura manuale + Molatura W15","",30.0,"T08-0200-P3203-10ML"],["T08-0200-P3203-10VT","10VT","VT W15","",5.0,"T08-0200-P3203-10VT"],["T08-0200-P3203-10LA","10LA","Lavorazione meccanica","EPIS SRL",2400.0,"T08-0200-P3203-10LA"],["T08-0200-P3203-10PT","10PT","PT W15 superfice lavorate","",45.0,"T08-0200-P3203-10PT"],["T08-0200-P3203-30QC","30QC","QC Dimensionale","",15.0,"T08-0200-P3203-30QC"]],"ch":[],"mat":["001-0023-C0852"]},{"code":"T08-0200-P3301","name":"CONE INNER AFT VENTURI","cp":"T08-0100-P3301","ops":[["T08-0200-P3301-10LT","10LT","Taglio sviluppo","INOXEA SRL",600.0,"T08-0200-P3301-10LT"],["T08-0200-P3301-10QC","10QC","QC Dimensionale","",5.0,"T08-0200-P3301-10QC"],["T08-0200-P3301-10LA","10LA","Stampaggio + Rifilatura","MAC STAMP SRL",1200.0,"T08-0200-P3301-10LA"],["T08-0200-P3301-20QC","20QC","QC Dimensionale","",10.0,"T08-0200-P3301-20QC"]],"ch":[],"mat":["001-0023-C0847"]},{"code":"T08-0200-P3302","name":"SLEEVE INNER VENTURI","cp":"T08-0100-P3302","ops":[["T08-0200-P3302-10LT","10LT","Taglio sviluppo + Calandratura","SOMECAR SRL",600.0,"T08-0200-P3302-10LT"],["T08-0200-P3302-10QC","10QC","QC Dimensionale","",5.0,"T08-0200-P3302-10QC"],["T08-0200-P3302-10SA","10SA","Saldatura longitudinale W13","",30.0,"T08-0200-P3302-10SA"],["T08-0200-P3302-10MX","10MX","Definizione mappe radiografiche W13 + Marcatura pezzi","",15.0,"T08-0200-P3302-10MX"],["T08-0200-P3302-10RX","10RX","RX W13","A.M.C. CONTROL SRL",1800.0,"T08-0200-P3302-10RX"],["T08-0200-P3302-10VX","10VX","Valutazione RX W13","",1,"T08-0200-P3302-10VX"],["T08-0200-P3302-10ML","10ML","Conformatura manuale + Molatura w13 a filo entrambi lati","",30.0,"T08-0200-P3302-10ML"],["T08-0200-P3302-10VT","10VT","VT W13","",5.0,"T08-0200-P3302-10VT"],["T08-0200-P3302-10PT","10PT","PT W13","",45.0,"T08-0200-P3302-10PT"],["T08-0200-P3302-10ST","10ST","Calibratura con espantore manuale","",5.0,"T08-0200-P3302-10ST"],["T08-0200-P3302-20QC","20QC","QC Dimensionale","",5.0,"T08-0200-P3302-20QC"],["T08-0200-P3302-10LA","10LA","Lavorazione meccanica","EPIS SRL",2700.0,"T08-0200-P3302-10LA"],["T08-0200-P3302-30QC","30QC","QC Dimensionale","",10.0,"T08-0200-P3302-30QC"]],"ch":[],"mat":["001-0023-C0848"]},{"code":"T08-0200-P3300","name":"ASSY SLEEVE INNER VENTURI","cp":"T08-0100-P3300","ops":[["T08-0200-P3300-10SA","10SA","Saldatura circonferenziale W18 Throat ring con parte conica","",30.0,"T08-0200-P3300-10SA"],["T08-0200-P3300-10MX","10MX","Definizione mappe radiografiche W18 + Marcatura pezzi","",15.0,"T08-0200-P3300-10MX"],["T08-0200-P3300-10RX","10RX","RX W18","A.M.C. CONTROL SRL",1800.0,"T08-0200-P3300-10RX"],["T08-0200-P3300-10VX","10VX","Valutazione RX W18","",1,"T08-0200-P3300-10VX"],["T08-0200-P3300-10ML","10ML","Molatura W18 a filo lato interno","",60.0,"T08-0200-P3300-10ML"],["T08-0200-P3300-10VT","10VT","VT W18","",10.0,"T08-0200-P3300-10VT"],["T08-0200-P3300-10PT","10PT","PT W18","",45.0,"T08-0200-P3300-10PT"],["T08-0200-P3300-20SA","20SA","Saldatura circonferenziale W17 (parte conica con parte cilindrica)","",30.0,"T08-0200-P3300-20SA"],["T08-0200-P3300-20MX","20MX","Definizione mappe radiografiche W17 + Marcatura pezzi","",15.0,"T08-0200-P3300-20MX"],["T08-0200-P3300-20RX","20RX","RX W17","A.M.C. CONTROL SRL",1800.0,"T08-0200-P3300-20RX"],["T08-0200-P3300-20VX","20VX","Valutazione RX W17","",1,"T08-0200-P3300-20VX"],["T08-0200-P3300-20ML","20ML","Molatura W17 a filo lato interno","",60.0,"T08-0200-P3300-20ML"],["T08-0200-P3300-20VT","20VT","VT W17","",10.0,"T08-0200-P3300-20VT"],["T08-0200-P3300-20PT","20PT","PT W17","",45.0,"T08-0200-P3300-20PT"],["T08-0200-P3300-10TT","10TT","Trattamento termico solubilizzazione","BODYCOTE SPA",300.0,"T08-0200-P3300-10TT"],["T08-0200-P3300-10QC","10QC","QC Dimensionale","",5.0,"T08-0200-P3300-10QC"],["T08-0200-P3300-30SA","30SA","Saldatura due Spacers W??","",90.0,"T08-0200-P3300-30SA"],["T08-0200-P3300-20QC","20QC","QC Dimensionale","",10.0,"T08-0200-P3300-20QC"]],"ch":[["T08-0200-P3203",1.0],["T08-0200-P3301",1.0],["T08-0200-P3302",1.0],["T08-0100-P3303",2.0]],"mat":[]},{"code":"T09-0100-P2100","name":"ASSY IMP PLATE, CTR BODY","cp":"T08-0100-P2100","ops":[["T09-0100-P2100-10SA","10SA","Montaggio + Saldatura piastra forata con n.6 Heat Shield W47","",200.0,"T09-0100-P2100-10SA"],["T09-0100-P2100-20SA","20SA","Montaggio + Saldatura W44 n.6 anelli (P2108)","",120.0,"T09-0100-P2100-20SA"],["T09-0100-P2100-10VT","10VT","VT W47, W44","",10.0,"T09-0100-P2100-10VT"],["T09-0100-P2100-10ML","10ML","Molatura W44 (garantire montaggio bicchieri interni P2109)","",5.0,"T09-0100-P2100-10ML"],["T09-0100-P2100-10PT","10PT","PT W47, W44","",40.0,"T09-0100-P2100-10PT"],["T09-0100-P2100-10ST","10ST","Conformatura semimanuale diametro bicchieri P2105 lato Heat Shield con CNC","",5.0,"T09-0100-P2100-10ST"],["T09-0100-P2100-10QC","10QC","QC Dimensionale","",5.0,"T09-0100-P2100-10QC"],["T09-0100-P2100-30SA","30SA","Montaggio + Saldatura W46 in unica passata, W45 n.6 bicchieri interni P2109 e Retainer P2113 con Floating Collar","",240.0,"T09-0100-P2100-30SA"],["T09-0100-P2100-40SA","40SA","Montaggio + Saldatura W48 virola esterna P2101","",60.0,"T09-0100-P2100-40SA"],["T09-0100-P2100-10MT","10MT","Raddrizzamento planarità con riferimento piano Floating Collars","",5.0,"T09-0100-P2100-10MT"],["T09-0100-P2100-20QC","20QC","QC Dimensionale","",5.0,"T09-0100-P2100-20QC"],["T09-0100-P2100-50SA","50SA","Montaggio Center Body P2200 + Saldatura W51, W50","",60.0,"T09-0100-P2100-50SA"],["T09-0100-P2100-20VT","20VT","VT W48, W46, W45, W51, W50","",10.0,"T09-0100-P2100-20VT"],["T09-0100-P2100-20PT","20PT","PT W48, W46, W45, W51, W50","",50.0,"T09-0100-P2100-20PT"],["T09-0100-P2100-30QC","30QC","QC Dimensional finale","",10.0,"T09-0100-P2100-30QC"]],"ch":[["T09-0100-P2114",6.0],["T08-0100-P2113",6.0],["T08-0100-P2112",6.0],["T08-0100-P2108",6.0],["T08-0100-P2101",1.0],["T08-0100-P2200",1.0],["T08-0100-P2109",6.0],["T08-0100-P2105",6.0],["T08-0100-P2102",1.0]],"mat":[]},{"code":"T09-0100-P3100","name":"ASSY OUTER VENTURI","cp":"T08-0100-P3100","ops":[["T09-0100-P3100-10SA","10SA","Saldatura circonferenziale W25 (due coni)","",30.0,"T09-0100-P3100-10SA"],["T09-0100-P3100-10MX","10MX","Definizione mappe radiografiche W25 + Marcatura pezzi","",15.0,"T09-0100-P3100-10MX"],["T09-0100-P3100-10RX","10RX","RX W25","A.M.C. CONTROL SRL",1800.0,"T09-0100-P3100-10RX"],["T09-0100-P3100-10VX","10VX","Valutazione RX W25","",1,"T09-0100-P3100-10VX"],["T09-0100-P3100-10ML","10ML","Molatura W25 lato convesso del cordone","",30.0,"T09-0100-P3100-10ML"],["T09-0100-P3100-10VT","10VT","VT W25","",5.0,"T09-0100-P3100-10VT"],["T09-0100-P3100-10PT","10PT","PT W25","",45.0,"T09-0100-P3100-10PT"],["T09-0100-P3100-10LA","10LA","Foratura laser + Rifilatura","SARZI LAMIERE SPA",600.0,"T09-0100-P3100-10LA"],["T09-0100-P3100-10QC","10QC","QC Dimensionale","",5.0,"T09-0100-P3100-10QC"],["T09-0100-P3100-20SA","20SA","Saldatura W24","",30.0,"T09-0100-P3100-20SA"],["T09-0100-P3100-20MX","20MX","Definizione mappe radiografiche W24 + Marcatura pezzi","",15.0,"T09-0100-P3100-20MX"],["T09-0100-P3100-20RX","20RX","RX W24","A.M.C. CONTROL SRL",1800.0,"T09-0100-P3100-20RX"],["T09-0100-P3100-20VX","20VX","Valutazione RX W24","",1,"T09-0100-P3100-20VX"],["T09-0100-P3100-20ML","20ML","Molatura W24 lato esterno","",45.0,"T09-0100-P3100-10ML"],["T09-0100-P3100-20VT","20VT","VT W24","",10.2,"T09-0100-P3100-20VT"],["T09-0100-P3100-20PT","20PT","PT W24","",45.0,"T09-0100-P3100-20PT"],["T09-0100-P3100-20QC","20QC","QC Dimensionale","",30.0,"T09-0100-P3100-20QC"]],"ch":[["T09-0100-P3101",1.0],["T09-0100-P3103",1.0],["T09-0100-P3104",1.0]],"mat":[]},{"code":"T09-0100-A1000","name":"ASSY LINER BODY","cp":"T08-0100-A1000","ops":[["T09-0100-A1000-10LA","10LA","Lavorazione piano A, TLUG, X-Fire, fori pin, fori DILUTION, foro SPARK PLUG, rifilatura lato molla","BONADEI E. MECCANICA SRL",2400.0,"T09-0100-A1000-10LA"],["T09-0100-A1000-10QC","10QC","QC Dimensionale","",5.0,"T09-0100-A1000-10QC"],["T09-0100-A1000-10ML","10ML","Lucidatura esterna discolorazione + lavaggio","",19.8,"T09-0100-A1000-10ML"],["T09-0100-A1000-10MT","10MT","Marcatura DOTPEEN","",5.0,"T09-0100-A1000-10MT"],["T09-0100-A1000-20MT","20MT","Pulizia montaggio + Puntatura molla con body","",45.0,"T09-0100-A1000-20MT"],["T09-0100-A1000-10SA","10SA","Saldatura a resistenza W62 (P6000 + P1100)","",30.0,"T09-0100-A1000-10SA"],["T09-0100-A1000-10VT","10VT","VT W62","",4.8,"T09-0100-A1000-10VT"],["T09-0100-A1000-20QC","20QC","QC Dimensionale","",40.0,"T09-0100-A1000-20QC"],["T09-0100-A1000-10TT","10TT","Rivestimento TBC Liner","FLAME SPRAY SPA",900.0,"T09-0100-A1000-10TT"],["T09-0100-A1000-30QC","30QC","VT Coating","",5.0,"T09-0100-A1000-30QC"],["T09-0100-A1000-40QC","40QC","QC Dimensionale finale","",40.0,"T09-0100-A1000-40QC"]],"ch":[["T08-0100-P6000",1.0],["T08-0100-P1100",1.0]],"mat":[]},{"code":"T09-0100-A2000","name":"ASSY CAP","cp":"T08-0100-A2000","ops":[["T09-0100-A2000-10SA","10SA","Montaggio raggiera + Saldatura a tratti W41","",45.0,"T09-0100-A2000-10SA"],["T09-0100-A2000-10VT","10VT","VT W41","",5.0,"T09-0100-A2000-10VT"],["T09-0100-A2000-20SA","20SA","Montaggio + Puntatura Outer Swirler W52","",30.0,"T09-0100-A2000-20SA"],["T09-0100-A2000-30SA","30SA","Saldatura circonferenziale Outer Swirler W52","",50.0,"T09-0100-A2000-30SA"],["T09-0100-A2000-40SA","40SA","Saldatura chiodi W43 + Saldatura circonferenziale mozzo W42","",30.0,"T09-0100-A2000-40SA"],["T09-0100-A2000-20VT","20VT","VT W43, W42","",5.0,"T09-0100-A2000-20VT"],["T09-0100-A2000-10MX","10MX","Definizione mappe radiografiche W52 + Marcatura pezzi","",15.0,"T09-0100-A2000-10MX"],["T09-0100-A2000-10RX","10RX","RX W52","A.M.C. CONTROL SRL",1800.0,"T09-0100-A2000-10RX"],["T09-0100-A2000-10VX","10VX","Valutazione RX W52","",1,"T09-0100-A2000-10VX"],["T09-0100-A2000-10ML","10ML","Molatura W52 a filo con vorticatore","",30.0,"T09-0100-A2000-10ML"],["T09-0100-A2000-30VT","30VT","VT W52","",5.0,"T09-0100-A2000-20VT"],["T09-0100-A2000-10PT","10PT","PT W52, W41, W42, W43,","",50.0,"T09-0100-A2000-10PT"],["T09-0100-A2000-10LA","10LA","Lavorazione fori PIN","BONADEI E. MECCANICA SRL",600.0,"T09-0100-A2000-10LA"],["T09-0100-A2000-10QC","10QC","QC Dimensionale","",5.0,"T09-0100-A2000-10QC"],["T09-0100-A2000-10MT","10MT","Raddrizzamento tutti gap a disegno e pulizia","",60.0,"T09-0100-A2000-10MT"],["T09-0100-A2000-20QC","20QC","QC Dimensionale","",15.0,"T09-0100-A2000-20QC"],["T09-0100-A2000-10TT","10TT","Rivestimento TBC Class B","FLAME SPRAY SPA",1200.0,"T09-0100-A2000-10TT"],["T09-0100-A2000-30QC","30QC","VT Coating","",20.0,"T09-0100-A2000-30QC"],["T09-0100-A2000-40QC","40QC","QC Dimensionale finale","",20.0,"T09-0100-A2000-40QC"]],"ch":[["T08-0100-P2404",1.0],["T08-0100-P2300",1.0],["T09-0100-P2100",1.0]],"mat":[]},{"code":"T09-0100-A3000","name":"ASSY VENTURY","cp":"T08-0100-A3000","ops":[["T09-0100-A3000-10MT","10MT","Conformatura P3200 per accoppiamento con Throat ring saldato","",30.0,"T09-0100-A3000-10MT"],["T09-0100-A3000-10QC","10QC","QC Dimensionale","",5.0,"T09-0100-A3000-10QC"],["T09-0100-A3000-10SA","10SA","Saldatura circonferenziale W19 (puntatura 8X tratti di fissaggio)","",75.0,"T09-0100-A3000-10SA"],["T09-0100-A3000-10MX","10MX","Definizione mappe radiografiche W19 + Marcatura pezzi","",15.0,"T09-0100-A3000-10MX"],["T09-0100-A3000-10RX","10RX","RX W19","A.M.C. CONTROL SRL",1800.0,"T09-0100-A3000-10RX"],["T09-0100-A3000-10VX","10VX","Valutazione RX W19","",1,"T09-0100-A3000-10VX"],["T09-0100-A3000-10ML","10ML","Molatura W19, sporgenze 8X","",90.0,"T09-0100-A3000-10ML"],["T09-0100-A3000-10VT","10VT","VT W19","",5.0,"T09-0100-A3000-10VT"],["T09-0100-A3000-10PT","10PT","PT W19","",45.0,"T09-0100-A3000-10PT"],["T09-0100-A3000-20MT","20MT","Marcatura DOTPEEN","",5.0,"T09-0100-A3000-20MT"],["T09-0100-A3000-10TE","10TE","Flussaggio ad aria","",18.0,"T09-0100-A3000-10TE"],["T09-0100-A3000-10LA","10LA","Lavorazione fori pin","BONADEI E. MECCANICA SRL",600.0,"T09-0100-A3000-10LA"],["T09-0100-A3000-20ML","20ML","Lavaggio","",20.0,"T09-0100-A3000-20ML"],["T09-0100-A3000-20QC","20QC","QC Dimensionale","",5.0,"T09-0100-A3000-20QC"],["T09-0100-A3000-10TT","10TT","Rivestimento TBC class C incl. trattamento termico post TBC + invecchiamento Spacers","FLAME SPRAY SPA",1200.0,"T09-0100-A3000-10TT"],["T09-0100-A3000-30QC","30QC","QC Dimensionale finale","",30.0,"T09-0100-A3000-30QC"]],"ch":[["T08-0100-P3200",1.0],["T09-0100-P3100",1.0],["T08-0200-P3300",1.0]],"mat":[]},{"code":"T09-0100-A0001","name":"ASSY LINER COMPLETE","cp":"T08-0100-A0001","ops":[["T09-0100-A0001-10MT","10MT","Montaggio Body + Venturi + Puntatura Pin Venturi","",180.0,"T09-0100-A0001-10MT"],["T09-0100-A0001-20MT","20MT","Montaggio Body + CAP + Puntatura Pin Cap","",30.0,"T09-0100-A0001-20MT"],["T09-0100-A0001-10SA","10SA","Saldatura PIN W64, W65","",150.0,"T09-0100-A0001-10SA"],["T09-0100-A0001-10VT","10VT","VT W64, W65","",10.0,"T09-0100-A0001-10VT"],["T09-0100-A0001-10PT","10PT","PT W64, W65","",45.0,"T09-0100-A0001-10PT"],["T09-0100-A0001-10ML","10ML","Pulizia saldature finale","",45.0,"T09-0100-A0001-10ML"],["T09-0100-A0001-30MT","30MT","Raddrizzamento gap tra CAP e liner","",30.0,"T09-0100-A0001-30MT"],["T09-0100-A0001-40MT","40MT","Marcatura DOTPEEN","",5.0,"T09-0100-A0001-40MT"],["T09-0100-A0001-10QC","10QC","QC Dimensionale finale","",20.0,"T09-0100-A0001-10QC"],["T09-0100-A0001-20QC","20QC","Preparazione Data Book finale","",1560.0,"T09-0100-A0001-20QC"]],"ch":[["T08-0100-P5000",12.0],["T08-0100-P4000",18.0],["T09-0100-A1000",1.0],["T09-0100-A3000",1.0],["T09-0100-A2000",1.0]],"mat":[]}]')
LETT = {"QC": "Controllo Qualità", "MX": "Controllo Qualità", "VX": "Controllo Qualità", "VT": "Controllo Qualità", "PT": "Controllo Qualità", "SA": "Saldatura", "ML": "Molatura", "MT": "Montaggio", "ST": "Lavorazioni Meccaniche", "LA": "Lavorazioni Meccaniche", "LT": "Lavorazioni Meccaniche"}
ERR = []
print("=== MODALITA':", "SCRITTURA" if SCRIVI else "PROVA (nessuna scrittura)", "===")
print("F000:", frappe.db.get_value("Item", "F000", ["item_name", "stock_uom"]))

# ---------- verifiche preliminari ----------
NUOVI = []
for b in D:
    NUOVI.append(b["code"])
for b in D:
    if frappe.db.exists("Item", b["code"]):
        ERR.append("Item già esistente: " + b["code"])
    if not frappe.db.exists("Item", b["cp"]):
        ERR.append("Controparte mancante: " + b["cp"])
    for c in b["ch"]:
        if c[0] not in NUOVI and not frappe.db.get_value("Item", c[0], "default_bom"):
            ERR.append(b["code"] + ": componente senza BOM default " + c[0])
    for m in b["mat"]:
        if not frappe.db.exists("Item", m):
            ERR.append(b["code"] + ": materiale mancante " + m)
    for o in b["ops"]:
        if o[3] and not frappe.db.exists("Supplier", o[3]):
            ERR.append(b["code"] + ": fornitore mancante " + o[3])
print("Errori bloccanti:", ERR if ERR else "nessuno")

# ---------- costruzione documenti ----------
if not ERR:
    for b in D:
        cbom = frappe.db.get_value("Item", b["cp"], "default_bom")
        tb = frappe.get_doc("BOM", cbom)
        bq = float(tb.quantity or 1)
        mappa = {}
        for r in tb.operations:
            t = frappe.utils.strip_html(r.description or "").strip().split(" ")[0].split("-")[-1]
            mappa[t] = r
        print("\n##", b["code"], "|", b["name"], "| copia da", b["cp"], cbom, "| qty BOM", bq)

        it = frappe.copy_doc(frappe.get_doc("Item", b["cp"]))
        it.item_code = b["code"]
        it.item_name = b["name"]
        it.description = b["name"]
        it.default_bom = None
        if SCRIVI:
            it.insert()

        nb = frappe.copy_doc(tb)
        nb.docstatus = 0
        nb.item = b["code"]
        nb.item_name = b["name"]
        nb.description = b["name"]
        nb.project = None
        nb.is_active = 1
        nb.is_default = 1
        nb.amended_from = None
        nb.items = []
        nb.operations = []
        for c in b["ch"]:
            uom = frappe.db.get_value("Item", c[0], "stock_uom") or "Nos"
            sb = frappe.db.get_value("Item", c[0], "default_bom")
            nb.append("items", {"item_code": c[0], "qty": round(c[1] * bq, 4), "uom": uom, "stock_uom": uom, "conversion_factor": 1, "bom_no": sb})
            print("   comp", c[0], round(c[1] * bq, 4), sb)
        for m in b["mat"]:
            uom = frappe.db.get_value("Item", m, "stock_uom") or "Nos"
            nb.append("items", {"item_code": m, "qty": 1, "uom": uom, "stock_uom": uom, "conversion_factor": 1})
            print("   mat ", m, 1)
        for o in b["ops"]:
            r = mappa.get(o[1])
            if o[3]:
                wt = "Lavorazione Esterna"
                ws = "Lavorazione Esterna"
                sub = r.is_subcontracted if (r and r.workstation_type == "Lavorazione Esterna") else 0
            elif r:
                wt = r.workstation_type
                ws = r.workstation
                sub = r.is_subcontracted
            else:
                wt = LETT.get(o[1][-2:], "")
                ws = None
                sub = 0
            if not wt:
                ERR.append(b["code"] + ": reparto non determinato per " + o[0])
            ds = o[0] + " — " + o[2]
            if o[3]:
                ds = ds + " (" + o[3] + ")"
            nb.append("operations", {"operation": wt, "workstation_type": wt, "workstation": ws, "time_in_mins": o[4], "is_subcontracted": sub, "description": ds})
            print("   op  ", o[0].split("-")[-1].ljust(5), (wt or "??").ljust(22), str(o[4]).rjust(7), "|", ds[:75], "| da T08" if r else "| regola")
        if SCRIVI and not ERR:
            nb.insert()
            nb.submit()
            frappe.db.commit()
            print("   -> creato", nb.name, "| default:", frappe.db.get_value("Item", b["code"], "default_bom"))

# ---------- T08-0100-P2301: BOM -002 con 10VX ----------
if not ERR:
    vb = frappe.db.get_value("Item", "T08-0100-P2301", "default_bom")
    ob = frappe.get_doc("BOM", vb)
    gia = False
    for r in ob.operations:
        if "P2301-10VX" in (r.description or ""):
            gia = True
    print("\n## T08-0100-P2301 | BOM attuale", vb, "| 10VX già presente:", gia)
    if not gia:
        nb = frappe.copy_doc(ob)
        nb.docstatus = 0
        nb.amended_from = None
        nb.is_default = 1
        nb.is_active = 1
        nuove = []
        for r in nb.operations:
            nuove.append(r.as_dict(no_default_fields=True))
            if "P2301-10RX" in (frappe.utils.strip_html(r.description or "")):
                vx = r.as_dict(no_default_fields=True)
                vx["operation"] = "Controllo Qualità"
                vx["workstation_type"] = "Controllo Qualità"
                vx["workstation"] = None
                vx["is_subcontracted"] = 0
                vx["time_in_mins"] = 1
                vx["description"] = "T08-0100-P2301-10VX — Valutazione RX W30"
                nuove.append(vx)
        nb.operations = []
        for r in nuove:
            nb.append("operations", r)
        i = 1
        for r in nb.operations:
            print("   ", i, r.workstation_type, r.time_in_mins, frappe.utils.strip_html(r.description or "")[:60])
            i = i + 1
        if SCRIVI:
            nb.insert()
            nb.submit()
            frappe.db.commit()
            print("   -> creato", nb.name, "| default:", frappe.db.get_value("Item", "T08-0100-P2301", "default_bom"))

print("\n=== FINE — errori:", ERR if ERR else "nessuno", "===")
