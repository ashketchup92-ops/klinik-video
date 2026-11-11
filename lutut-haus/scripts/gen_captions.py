import json
W=[ # (text, start, end)
 [("JOGGING",0.15,0.6),("DALAM",0.6,0.85),("RUMAH?",0.85,1.3)],
 [("BOLEH!",1.65,2.4)],
 [("OK,",22.9,23.4)],
 [("SEKARANG",24.35,24.75),("DAH",24.75,24.95),("OKAY",24.95,25.3),("KAN?",25.3,25.7)],
 [("INSYAALLAH",25.95,26.4)],
 [("OH,",26.55,26.85),("BETUL.",26.85,27.4)],
 [("BOLEH",27.75,28.0),("MAIN",28.45,28.7),("BADMINTON",28.7,29.15)],
 [("BALIK",29.15,29.3),("TAK?",29.3,29.55)],
 [("INSYAALLAH",29.7,30.8)],
 [("ALHAMDULILLAH",31.05,32.1)],
 [("JOM,",32.3,32.55),("JOM!",32.7,32.95)],
 [("KITA",33.25,33.5),("JALAN-JALAN",33.5,34.1),("DULU,",34.1,34.35)],
 [("MINGGU",34.4,34.7),("DEPAN",34.7,35.0)],
 [("KITA",35.0,35.2),("JOGGING!",35.2,35.75)],
]
groups=[]
for gi,g in enumerate(W):
    s=round(g[0][1]-0.08,2)
    nxt=W[gi+1][0][1]-0.08 if gi+1<len(W) else 99
    e=round(min(g[-1][2]+0.3,nxt),2)
    groups.append((gi,s,e,g))
html=['<template>','<style>',
'#root{position:absolute;inset:0;}',
'.cg{position:absolute;left:0;top:1040px;width:1080px;text-align:center;overflow:visible;}',
'.cg .in{display:inline-block;font-family:Montserrat,sans-serif;font-weight:900;font-size:88px;line-height:1.08;letter-spacing:-0.01em;color:#fff;-webkit-text-stroke:12px #000;paint-order:stroke fill;text-shadow:0 6px 18px rgba(0,0,0,.55);max-width:900px;}',
'.cw{display:inline-block;margin:0 .12em;}',
'</style>',
'<div id="root" data-composition-id="captions" data-width="1080" data-height="1920">']
js=['const tl = gsap.timeline({ paused: true });']
for gi,s,e,g in groups:
    words=''.join(f'<span class="cw" id="cw{gi}_{k}">{t}</span>' for k,(t,_,_) in enumerate(g))
    html.append(f'<div id="cg{gi}" class="cg clip" data-start="{s}" data-duration="{round(e-s,2)}" data-track-index="0"><div class="in" id="cgi{gi}">{words}</div></div>')
    js.append(f'tl.fromTo("#cgi{gi}",{{scale:0.86,opacity:0}},{{scale:1,opacity:1,duration:0.14,ease:"back.out(2)"}},{s});')
    for k,(t,ws,we) in enumerate(g):
        js.append(f'tl.fromTo("#cw{gi}_{k}",{{color:"#ffffff",scale:1}},{{color:"#FFD400",scale:1.08,duration:0.06,ease:"power2.out"}},{ws});')
        js.append(f'tl.to("#cw{gi}_{k}",{{scale:1,duration:0.12}},{ws+0.07:.2f});')
    js.append(f'tl.to("#cgi{gi}",{{opacity:0,duration:0.08,ease:"power2.in"}},{e-0.09:.2f});')
html.append('</div>'); html.append('<script>'); html+=js
html.append('window.__timelines["captions"] = tl;'); html.append('</script>'); html.append('</template>')
open('compositions/captions.html','w').write('\n'.join(html))
print(len(groups), groups[-1][2])
