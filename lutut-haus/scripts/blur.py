import cv2, numpy as np, sys, json
src, dst, mode = sys.argv[1], sys.argv[2], sys.argv[3]
keys = json.loads(sys.argv[4]) if len(sys.argv)>4 else None
cap=cv2.VideoCapture(src); fps=cap.get(5); W=int(cap.get(3)); H=int(cap.get(4))
out=cv2.VideoWriter(dst+'.avi',cv2.VideoWriter_fourcc(*'MJPG'),fps,(W,H))
prev=None; lost=0; i=0
def hijab_box(fr):
    hsv=cv2.cvtColor(fr,cv2.COLOR_BGR2HSV); h,s,v=[hsv[...,k].astype(int) for k in range(3)]
    m=(((h<=12)|(h>=165))&(s>=45)&(s<=130)&(v>=70)&(v<=190)).astype(np.uint8)
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((5,5),np.uint8)); m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
    n,lab,st,_=cv2.connectedComponentsWithStats(m)
    if n<2: return None
    k=1+np.argmax(st[1:,4])
    if st[k,4]<1500: return None
    x,y,w,h,_=st[k]
    # head = top part of hijab blob; face sits in upper ~55%
    hh=min(h, int(w*1.15))
    return np.array([x-0.12*w, y-0.08*hh, w*1.24, hh*0.85],float)
def interp(i):
    ks=sorted(keys,key=lambda k:k[0])
    if i<=ks[0][0]: return np.array(ks[0][1:],float)
    for a,b in zip(ks,ks[1:]):
        if a[0]<=i<=b[0]:
            t=(i-a[0])/(b[0]-a[0]); return np.array(a[1:],float)*(1-t)+np.array(b[1:],float)*t
    return np.array(ks[-1][1:],float)
while True:
    ok,fr=cap.read()
    if not ok: break
    box=None
    if mode=='hijab':
        b=hijab_box(fr)
        if b is not None:
            prev=b if prev is None else prev*0.6+b*0.4; lost=0
        else: lost+=1
        box=prev if (prev is not None and lost<45) else None
    elif mode=='manual': box=interp(i)
    if box is not None:
        x,y,w,h=box; cx,cy=x+w/2,y+h/2
        small=cv2.resize(fr,(max(1,W//14),max(1,H//14)),interpolation=cv2.INTER_AREA)
        pix=cv2.resize(small,(W,H),interpolation=cv2.INTER_NEAREST)
        pix=cv2.GaussianBlur(pix,(0,0),6)
        mask=np.zeros((H,W),np.float32); cv2.ellipse(mask,(int(cx),int(cy)),(int(w/2),int(h/2)),0,0,360,1,-1)
        mask=cv2.GaussianBlur(mask,(0,0),4)[...,None]
        fr=(fr*(1-mask)+pix*mask).astype(np.uint8)
    out.write(fr); i+=1
out.release(); print(dst,i)
