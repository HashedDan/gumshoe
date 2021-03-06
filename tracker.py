import cv2 as cv
import sys
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time

# OpenCV Version
(major_ver, minor_ver, subminor_ver) = (cv.__version__).split(".")

if __name__ == '__main__' :

    tracker = cv.TrackerKCF_create()

    vs = cv.VideoCapture('test3.mov')

    initBB = None
    fps = None

    # loop over frames from the video stream
    while True:
        # grab the current frame, then handle if we are using a
        # VideoStream or VideoCapture object
        _, frame = vs.read()
        # frame = frame[1] if args.get("video", False) else frame
    
        # check to see if we have reached the end of the stream
        if frame is None:
            break
    
        # resize the frame (so we can process it faster) and grab the
        # frame dimensions
        # frame = imutils.resize(frame, width=500)
        # (H, W) = frame.shape[:2]

        # check to see if we are currently tracking an object
        if initBB is not None:
            # grab the new bounding box coordinates of the object
            (success, box) = tracker.update(frame)
    
            # check to see if the tracking was a success
            if success:
                print("SUCCESS")
                (x, y, w, h) = [int(v) for v in box]
                cv.rectangle(frame, (x, y), (x + w, y + h),
                    (0, 255, 0), 2)
    
            # update the FPS counter
            fps.update()
            fps.stop()
    
            # initialize the set of information we'll be displaying on
            # the frame
            info = [
                ("Tracker", "KCF"),
                ("Success", "Yes" if success else "No"),
                ("FPS", "{:.2f}".format(fps.fps())),
            ]
    
            # loop over the info tuples and draw them on our frame
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv.putText(frame, text, (10, h - ((i * 20) + 20)),
                    cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        # show the output frame
        cv.imshow("Frame", frame)
        key = cv.waitKey(1) & 0xFF
    
        # if the 's' key is selected, we are going to "select" a bounding
        # box to track
        if key == ord("s"):
            # select the bounding box of the object we want to track (make
            # sure you press ENTER or SPACE after selecting the ROI)
            initBB = cv.selectROI("Frame", frame, fromCenter=False,
                showCrosshair=True)
    
            # start OpenCV object tracker using the supplied bounding box
            # coordinates, then start the FPS throughput estimator as well
            tracker.init(frame, initBB)
            fps = FPS().start()
        # if the `q` key was pressed, break from the loop
        elif key == ord("q"):
            break
        
    # otherwise, release the file pointer
    else:
        vs.release()
    
    # close all windows
    cv.destroyAllWindows()