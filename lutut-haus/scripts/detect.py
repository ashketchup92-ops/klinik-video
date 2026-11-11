import sys, json, cv2, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
opts = vision.FaceDetectorOptions(base_options=mpt.BaseOptions(model_asset_path='/home/user/work/models/bf.tflite'),
    running_mode=vision.RunningMode.VIDEO, min_detection_confidence=float(sys.argv[3]) if len(sys.argv)>3 else 0.4)
det = vision.FaceDetector.create_from_options(opts)
cap = cv2.VideoCapture(sys.argv[1]); fps = cap.get(5); i=0; out=[]
while True:
    ok, fr = cap.read()
    if not ok: break
    # upscale 2x helps small faces
    big = cv2.resize(fr, None, fx=2, fy=2)
    img = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(big, cv2.COLOR_BGR2RGB))
    r = det.detect_for_video(img, int(i*1000/fps))
    out.append([[d.bounding_box.origin_x/2, d.bounding_box.origin_y/2, d.bounding_box.width/2, d.bounding_box.height/2, round(d.categories[0].score,2)] for d in r.detections])
    i+=1
json.dump(out, open(sys.argv[2],'w'))
print(sys.argv[1], i, sum(1 for o in out if o))
