import cv2 as cv
import sys

# OpenCV Version
(major_ver, minor_ver, subminor_ver) = (cv.__version__).split(".")

if __name__ == '__main__' :
    # tracker = cv.TrackerMIL_create()

    cap = cv.VideoCapture('stationary.mp4')

    fgbg = cv.bgsegm.createBackgroundSubtractorMOG()

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        fgmask = fgbg.apply(frame)

        # Display the resulting frame
        cv.imshow('Gum Shoe',fgmask)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()