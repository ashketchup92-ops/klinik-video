import json
T=json.load(open('timeline2.json'))['vo']
def m(src,s):
    for c in T:
        if ('/'+src+'.') in c['src'] and c['a']-0.3<=s<=c['b']: return round(c['tl_start']+max(0,s-c['a']),2)
    return None
def W(src,items): # items: (text,s,e) src times
    out=[]
    for t,s,e in items:
        a=m(src,s); b=m(src,min(e,s+1.2)) or (a+0.3 if a else None)
        if a is None: raise SystemExit(f"unmapped {t} {s}")
        out.append((t,a,b))
    return out
G=[]
G+= [W('a1',[("LUTUT",0.97,1.38),("HAUS",1.38,1.66),("SAMPAI",1.66,1.94)]),
     W('a1',[("SUSAH",1.94,2.22),("NAK",2.22,2.36),("BERJALAN,",2.36,2.94)]),
     W('a1',[("SUSAH",3.12,3.40),("NAK",3.40,3.54),("SOLAT?",3.54,4.0)]),
     W('a1',[("PUNCANYA,",4.76,5.32),("RAWAN",5.32,5.78)]),
     W('a1',[("YANG",5.78,5.94),("SEMAKIN",5.94,6.26),("MENIPIS.",6.26,6.8)]),
     W('a1',[("JADI",7.38,7.64),("TULANG",7.64,7.96),("AKAN",7.96,8.10),("BERGESER",8.10,8.64)]),
     W('a1',[("DAN",8.64,8.86),("AKAN",8.86,9.02),("MENJADI",9.02,9.32)]),
     W('a1',[("SANGAT",9.32,9.84),("SAKIT.",9.84,10.25)]),
     W('a2',[("SALAH",1.07,1.52),("SATU",1.52,1.76),("RAWATAN",1.76,2.16),("IALAH",2.16,2.44)]),
     W('a2',[("SUNTIKAN",2.44,3.02),("GEL",3.02,3.28),("HYALURONIC.",3.28,3.9)]),
     W('a2',[("LEPAS",6.5,6.96),("KAWASAN",6.96,7.38),("LUTUT",7.38,7.74)]),
     W('a2',[("DIBERSIHKAN,",7.74,8.6)]),
     W('a2',[("DOKTOR",8.87,9.32),("AKAN",9.32,9.50),("SUNTIK",9.50,9.86),("GEL",9.86,9.98)]),
     W('a2',[("TERUS",9.98,10.26),("KE",10.26,10.42),("DALAM",10.42,10.64),("SENDI.",10.64,11.0)]),
     W('a2',[("KEMUDIAN",11.45,11.90),("LUTUT",11.90,12.20),("AKAN",12.20,12.44)]),
     W('a2',[("DIGERAKKAN",12.44,12.97)]),
     W('a2',[("SUPAYA",14.15,14.8),("GEL",14.85,15.04),("ITU",15.04,15.36)]),
     W('a2',[("TERSEBAR",15.3,15.68),("RATA.",15.68,16.05)]),
     W('a2',[("JOM",16.82,17.16),("KITA",17.16,17.36),("TENGOK",17.36,17.58)]),
     W('a2',[("SELEPAS",17.58,17.94),("RAWATAN.",17.94,18.4)])]
D=[[("OK,",22.9,23.4)],
 [("SEKARANG",24.35,24.75),("DAH",24.75,24.95),("OKAY",24.95,25.3),("KAN?",25.3,25.7)],
 [("INSYAALLAH",25.95,26.4)],
 [("BOLEH",27.75,28.1)],
 [("SEMBAHYANG",28.45,29.1),("BALIK",29.1,29.3),("TAK?",29.3,29.55)],
 [("INSYAALLAH",29.7,30.8)],
 [("ALHAMDULILLAH",31.05,32.1)],
 [("JOM,",32.3,32.55),("JOM!",32.7,32.95)],
 [("KITA",33.25,33.5),("JALAN-JALAN",33.5,34.1),("DULU,",34.1,34.35)],
 [("MINGGU",34.4,34.7),("DEPAN",34.7,35.0)],
 [("KITA",35.0,35.2),("JOGGING!",35.2,35.75)]]
G+= [[(t,round(s+1.0,2),round(e+1.0,2)) for t,s,e in g] for g in D]
G+= [[("JOGGING",0.15+36.95,0.6+36.95),("DALAM",0.6+36.95,0.85+36.95),("RUMAH?",0.85+36.95,1.3+36.95)],[("BOLEH!",1.65+36.95,2.4+36.95)]]
json.dump(G,open('captions_words.json','w'),indent=0)
print(len(G), G[0], G[-1])
