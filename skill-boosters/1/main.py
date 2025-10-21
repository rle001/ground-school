import numpy as np
import cv2 as cv
import argparse

parser = argparse.ArgumentParser(
    prog='stitcher',
    description='stitch video frames together')
parser.add_argument('filename')
parser.add_argument('mode', type=int)
parser.add_argument('outputname')
args = parser.parse_args()

cap = cv.VideoCapture(args.filename)
imgs = []
stitch = cv.Stitcher.create(mode=args.mode) # create stitcher in PANORAMA mode (0) or SCANS mode (1)
frame_count = 0
FRAME_INTERVAL = 5
 
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    if frame_count % FRAME_INTERVAL == 0:
        cv.imshow('stitches', frame)
        imgs.append(frame)
    if cv.waitKey(1) == ord('q'):
        break
    frame_count += 1

print('stitching')
ret, stitched = stitch.stitch(imgs)

if ret != cv.STITCHER_OK:
    print(f'stitch failed with error code: {ret}')
else:
    print('sucess')
    save = cv.imwrite(f'{args.outputname}.jpg', stitched)
    if not save:
        print('save failed')

cap.release()
cv.destroyAllWindows()
