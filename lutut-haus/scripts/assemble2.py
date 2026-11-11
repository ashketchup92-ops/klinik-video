import subprocess, json
# name, video, vstart, vdur, audio, astart, vol
P=[("hook","segb/end.avi",0,3.3,"seg/end.mov",0,0.2),
   ("knee",None,0,9.0,None,0,0),
   ("p1","segb/p1.avi",0,1.3,"seg/p1.mov",0,0.25),("p2","segb/p2.avi",0,1.4,"seg/p2.mov",0,0.25),
   ("p3","segb/p3.avi",0,2.0,"seg/p3.mov",0,0.25),("p4","segb/p4.avi",0,1.0,"seg/p4.mov",0,0.25),
   ("p5","segb/p5.avi",0,3.0,"seg/p5.mov",0,0.25),("p6","segb/p6.avi",0,2.8,"seg/p6.mov",0,0.25)]
for n,d in [("d1",3.1),("d2",0.55),("d3",3.15),("d4",1.35),("d5",1.25),("d6",0.9),("d7",2.85)]:
    P.append((n,f"segb/{n}.avi",0,d,f"seg/{n}.mov",0,1.0))
P+=[("d8","segb/d8.avi",0,2.8,"seg/hook.mov",0,1.0),("end","segb/ecs.avi",0,6.0,None,0,0)]
# VO placements: (timeline_start, file, [(src_a,src_b),...]) chunks joined with 0.25s gaps
VO=[(0.2,"vo/a1.m4a",[(0.97,4.02),(4.57,6.82),(7.17,10.27)]),
    (9.2,"vo/a2.m4a",[(1.07,3.92)]),
    (12.5,"vo/a2.m4a",[(6.47,11.07)]),
    (17.6,"vo/a2.m4a",[(11.42,12.98),(14.15,16.07)]),
    (21.6,"vo/a2.m4a",[(16.62,18.47)])]
inputs=[];fc=[];idx=0;labels=[];t=0;tl=[]
for k,(name,vf,vs,vd,af,as_,vol) in enumerate(P):
    if vf:
        inputs+=["-ss",str(vs),"-t",str(vd),"-i",vf]; vi=idx; idx+=1
        fc.append(f"[{vi}:v]fps=30,scale=1080:1964:flags=lanczos,crop=1080:1920:0:22,unsharp=5:5:0.6,setsar=1,trim=duration={vd},setpts=PTS-STARTPTS[v{k}]")
    else: fc.append(f"color=c=0x1a0f14:s=1080x1920:r=30:d={vd},setsar=1[v{k}]")
    if af and vol>0:
        inputs+=["-ss",str(as_),"-t",str(vd),"-i",af]; ai=idx; idx+=1
        fc.append(f"[{ai}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={vol},apad,atrim=duration={vd},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={vd-0.04}:d=0.04[a{k}]")
    else: fc.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={vd}[a{k}]")
    labels.append(f"[v{k}][a{k}]"); tl.append(dict(name=name,start=round(t,3),dur=vd)); t+=vd
fc.append("".join(labels)+f"concat=n={len(P)}:v=1:a=1[v][amain]")
vol_labels=[]; vomap=[]
for j,(ts,f,chunks) in enumerate(VO):
    parts=[]; pos=ts
    for c,(a,b) in enumerate(chunks):
        inputs+=["-ss",str(a),"-t",str(round(b-a,3)),"-i",f]; ii=idx; idx+=1
        lab=f"vo{j}_{c}"; fc.append(f"[{ii}:a]aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=0.02,afade=t=out:st={round(b-a-0.03,3)}:d=0.03,adelay={int(pos*1000)}|{int(pos*1000)}[{lab}]")
        vol_labels.append(f"[{lab}]"); vomap.append(dict(tl_start=round(pos,3),src=f,a=a,b=b)); pos+=b-a+0.25
fc.append("".join(vol_labels)+f"amix=inputs={len(vol_labels)}:normalize=0,highpass=f=80,afftdn=nf=-30,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,volume=1.6[vo]")
fc.append("[amain][vo]amix=inputs=2:normalize=0:duration=first[a]")
cmd=["ffmpeg","-nostdin","-v","error","-y",*inputs,"-filter_complex",";".join(fc),"-map","[v]","-map","[a]","-c:v","libx264","-crf","14","-preset","medium","-g","30","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","base.mp4"]
subprocess.run(cmd,check=True)
json.dump(dict(timeline=tl,vo=vomap),open("timeline2.json","w"),indent=1); print("total",round(t,3))
for x in tl: print(x)
for v in vomap: print(v)
