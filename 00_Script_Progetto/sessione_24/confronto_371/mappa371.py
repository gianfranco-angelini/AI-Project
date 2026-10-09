import csv,collections,re,json
R=list(csv.DictReader(open('operazioni_t09.csv',encoding='utf-8'),delimiter=';'))
P=[r for r in R if r['tipo'] in ('SA','ML','MT','ST')]
# regole nostre: articolo -> gruppo 371 e codici per tipo di fase (A=assemblaggio/prep, S=saldatura, M=molatura, C=conformatura)
VIR=dict(MT='x02',SA='x04',ML='x06',ST='x08')          # virole singole (saldatura longitudinale)
def vir(base): return {t:'V'+str(base)+c[1:] for t,c in VIR.items()}
REG={}
for it in ['P1101','P1102','P1200','P1300','P1400']: REG[it]=('Liner - virole',vir(1),'U')
REG['P1600']=('Liner/Venturi - virole (rev. diversa)',{'SA':'V104|V204','ML':'V106|V206','ST':'V108|V208'},'A')
for it in ['P1103','P1104','P1110']: REG[it]=('Liner - giunzioni circonferenziali',{'SA':'V134|V140|V146','ML':'V136|V142|V148'},'A')
REG['P1100']={'10MT':('V126|V150','A'),'10SA':('V128|V152','A'),'10ML':('V130|V191','B'),'20SA':('V146','M'),'20ML':('V148','M'),'20MT':('V124|V116','A')}
for it in ['P1120','P1130']: REG[it]={'10MT':('V126','B'),'10SA':('V128','B'),'20MT':('V191','B'),'10ML':('V605','B')}
for it in ['P3104','P3302','P3203']: REG[it]=('Venturi - virole',vir(2),'U')
REG['P3300']={'10SA':('V212','M'),'10ML':('V214','M'),'20SA':('V224','M'),'20ML':('V226','M'),'30SA':('V230','U')}
REG['P3100']={'10SA':('V218|V234','A'),'10ML':('V220|V236','A'),'20SA':('V218|V234','A'),'20ML':('V220|V236','A')}
REG['A3000']={'10MT':('V246|V238','A'),'10SA':('V248','M'),'10ML':('V250','M'),'20ML':('V605','B')}
for it in ['P2101','P2104','P2105','P2107','P2111']: REG[it]=('Cap - virole impingement',{'SA':'V304|V312','ML':'V306|V314','ST':'V308'},'A')
REG['P2102']={'10SA':('V318','M'),'10ML':('V320','M')}
REG['P2109']={'10SA':('V376','U'),'10ML':('V378','U'),'10MT':('V191','B')}
for it in ['P2201','P2202']: REG[it]=('Cap - inner body virole',{'SA':'V358','ML':'V360','ST':'V362'},'U')
for it in ['P2301','P2304','P2307']: REG[it]=('Cap - outer body virole',{'SA':'V385','ML':'V386','ST':'V387'},'U')
REG['P2300']={'10SA':('V366','U'),'10ML':('V372','M'),'20SA':('V370','M')}
REG['P2303']={'10SA':('V389','U'),'10ML':('V386','M')}
REG['P2100']={'10SA':('V324|V330','A'),'20SA':('V324|V330','A'),'10ML':('V326|V332','A'),'10ST':('V308','B'),'30SA':('V340','M'),'40SA':('V336','U'),'10MT':('V191','B'),'50SA':('V393','M')}
REG['P2200']={'10MT':('V338','M'),'10SA':('V340','M'),'20ML':('V605','B')}
REG['A2000']={'10SA':('V350','M'),'20SA':('V348','M'),'30SA':('V350','M'),'40SA':('V350','M'),'10ML':('V346','M'),'10MT':('V191','B')}
REG['P6000']={'10SA':('V404','U'),'10ML':('V406','U'),'10ST':('V408','U'),'20ST':('V408|V410','A')}
REG['A0001']={'10MT':('V502','U'),'20MT':('V506','U'),'10SA':('V504+V508','U'),'10ML':('V605','B'),'30MT':('V191|V596','B'),'40MT':('','N')}
REG['A1000']={'20MT':('V510','U'),'10SA':('V512','U'),'10ML':('V605','B'),'10MT':('','N')}
LIV={'U':'Univoca','M':'Probabile','A':'Ambigua (più codici)','B':'Generica (Vx91/V605)','N':'Nessuna'}
out=[];cnt=collections.Counter();mins=collections.Counter()
for r in P:
    it=r['item'][-5:]; fase=r['codice_fase'][-4:]
    g=REG.get(it)
    if g is None: code,lv='','N?'
    elif isinstance(g,tuple): code=g[1].get(r['tipo'],''); lv=g[2] if code else 'N?'
    else: code,lv=g.get(fase,('','N?'))
    out.append((r,code,lv)); cnt[lv]+=1; mins[lv]+=float(r['time_in_mins'])
print(cnt, dict(mins))
for r,c,l in out:
    if l=='N?': print('NON MAPPATA',r['codice_fase'],r['descrizione'][:70])
json.dump([(r['codice_fase'],r['esterna'],r['time_in_mins'],c,l,r['descrizione']) for r,c,l in out],open('mappa.json','w'))
