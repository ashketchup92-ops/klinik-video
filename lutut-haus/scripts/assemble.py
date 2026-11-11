import subprocess, json
# (video_file, vstart, vdur, audio_file or None, astart, volume)
P=[("segb/end.avi",0,2.8,"seg/hook.mov",0,1.0,"hook"),
   (None,0,5.5,None,0,0,"knee"),
   ("segb/p1.avi",0,2.5,"seg/p1.mov",0,0.5,"p1"),("segb/p2.avi",0,2.0,"seg/p2.mov",0,0.5,"p2"),
   ("segb/p3.avi",0,2.0,"seg/p3.mov",0,0.5,"p3"),("segb/p4.avi",0,2.0,"seg/p4.mov",0,0.5,"p4"),
   ("segb/p5.avi",0,3.0,"seg/p5.mov",0,0.5,"p5"),("segb/p6.avi",0,3.0,"seg/p6.mov",0,0.5,"p6")]
for n,d in [("d1",3.1),("d2",0.55),("d3",3.15),("d4",1.35),("d5",1.25),("d6",0.9),("d7",2.85)]:
    P.append((f"segb/{n}.avi",0,d,f"seg/{n}.mov",0,1.0,n))
P+= [("segb/end.avi",2.8,1.7,"seg/end.mov",2.8,0.4,"end1"),("segb/ec.avi",0,4.3,"seg/ec.mov",0,0.0,"end2")]
inputs=[]; fc=[]; idx=0; labels=[]; t=0; tl=[]
for k,(vf,vs,vd,af,as_,vol,name) in enumerate(P):
    if vf:
        inputs+=["-ss",str(vs),"-t",str(vd),"-i",vf]; vi=idx; idx+=1
        fc.append(f"[{vi}:v]fps=30,scale=1080:1964:flags=lanczos,crop=1080:1920:0:22,unsharp=5:5:0.6,setsar=1,trim=duration={vd},setpts=PTS-STARTPTS[v{k}]")
    else:
        fc.append(f"color=c=0x1a0f14:s=1080x1920:r=30:d={vd},setsar=1[v{k}]")
    if af and vol>0:
        inputs+=["-ss",str(as_),"-t",str(vd),"-i",af]; ai=idx; idx+=1
        fc.append(f"[{ai}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={vol},apad,atrim=duration={vd},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={vd-0.04}:d=0.04[a{k}]")
    else:
        fc.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={vd}[a{k}]")
    labels.append(f"[v{k}][a{k}]"); tl.append(dict(name=name,start=round(t,3),dur=vd,src=vf,src_start=vs)); t+=vd
fc.append("".join(labels)+f"concat=n={len(P)}:v=1:a=1[v][a]")
cmd=["ffmpeg","-nostdin","-v","error","-y",*inputs,"-filter_complex",";".join(fc),"-map","[v]","-map","[a]","-c:v","libx264","-crf","14","-preset","medium","-g","30","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","base.mp4"]
subprocess.run(cmd,check=True)
json.dump(tl,open("timeline.json","w"),indent=1); print("total",round(t,3))
