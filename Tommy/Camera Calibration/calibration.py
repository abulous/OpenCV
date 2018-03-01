import cv2
import numpy
import os


class CameraCalibration:
    def __init__(self, chessboardDimentions=(9,6)):
        """Calibrate camera using a chessboard.
        chessboard dimentions based on the intersections between 2 black and 2 white squares
        @param chessboardDimentions a tuple (rows, cols) of the number of intersections
        """
        self.chessboardDims = chessboardDimentions
        self.goodImgs = []
        self.objpoints = []
        self.imgpoints = []

        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.objp = numpy.zeros((self.chessboardDims[0]*self.chessboardDims[1],3), numpy.float32)
        self.objp[:,:2] = numpy.mgrid[0:self.chessboardDims[0],0:self.chessboardDims[1]].T.reshape(-1,2)

    def autoCalibration(captureDeviceIndex=0, fps=30, chessboardDimensions=(9,6)):
        """Automatically run the calibration process.
        The only thing needed is a camera index (eg: 0 or 1 or 2 ...)
        @param captureDeviceIndex the webcam device
        @param fps the frames per second to capture through the capture device
        @param chessboardDimensions a tuple (rows, cols) of the number of intersections
        """
        cap = cv2.VideoCapture(captureDeviceIndex)
        capDelay = int(1000/fps)
        cc = CameraCalibration(chessboardDimensions)
        while True:
            ret, frame = cap.read()
            if not cc.addFrame(frame, False):
                cv2.putText(frame, "no chessboard found.", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
            cv2.imshow("Camera AutoCalibration", frame)
            if cv2.waitKey(capDelay) == 27:
                cv2.destroyAllWindows()
                cc.removeBadFrames()
                cc.exportCalibrationVectors(frame)
                cv2.destroyAllWindows()
                cap.release()
                break
        print("____CALIBRATION COMPLETE____")
        
    def addFrame(self, frame, displayCalibrationLines=False):
        """Add a frame to the calibration process,
        increasing its accuracy.
        @param frame the image to add as a numerical tuple (opencv frame capture)
        @param displayCalibrationLines whether or not to show a pop up of the frame with drawn calibration lines
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cornersFound, corners = cv2.findChessboardCorners(frame, self.chessboardDims)

        if cornersFound:
            self.goodImgs.append(frame)
            fineCorners = self.increasePrecision(gray, corners)
            if displayCalibrationLines:
                self.displayCalibrationLines(frame, fineCorners, cornersFound)

        return cornersFound
            
    def increasePrecision(self, grayframe, corners):
        """given a frame (grayscale) which has a chessboard,
        create a finer approximation of the location of each intersection.
        @param grayframe a grayscale image with a chessboard
        @param corners the location of each of the chessboard square intersections as ndarray
        this function is automatically called by the addFrame() function.
        Recommended to just use addFrame() as it will automatically take care of everything
        """
        self.objpoints.append(self.objp)

        fineCorners = cv2.cornerSubPix(grayframe, corners, (11,11), (-1,-1), self.criteria)
        self.imgpoints.append(fineCorners)
        return fineCorners

    def displayCalibrationLines(self, frame, corners, cornersFound):
        """Graphical display of the found locations for each of the intersections on the chessboard.
        @param frame the image to display the lines on
        @param corners the location of each of the intersections as ndarray
        @param cornersFound a boolean telling whether or not those corners were successfully found
        """
        if not cornersFound:
            return
        imgCopy = cv2.drawChessboardCorners(frame, self.chessboardDims, corners, cornersFound)
        cv2.imshow("Quick Preview", imgCopy)
        cv2.moveWindow("Quick Preview", 50,50)
        cv2.waitKey(300)
        cv2.destroyWindow("Quick Preview")
        
    def removeBadFrames(self):
        """parse through and display each frame/image where a chessboard was found.
        Allows the user to discard blurry images which will impair the calibration
        ESC key will accept all frames
        DELETE key will discard a frame/image
        'a' and 'b' keys move to the last shown frame/image
        SPACE and ENTER keys will move onto the next image
        """
        blank_img = numpy.zeros((480,640,3), numpy.uint8)
        cv2.putText(blank_img, "DELETE to remove", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
        cv2.putText(blank_img, "ENTER/SPACE/other to keep", (10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
        cv2.putText(blank_img, "'a' or 'b' to move back", (10,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
        cv2.putText(blank_img, "ESC to accept all", (10,200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
        cv2.imshow("Instructions", blank_img)
        cv2.waitKey(0)
        cv2.destroyWindow("Instructions")

        inc=0
        i = len(self.goodImgs)-1
        while i>=0:
            winname ="Frame with Chessboard #"+str(i)
            cv2.imshow(winname, self.goodImgs[i])
            cv2.moveWindow(winname, 50,50)
            key = cv2.waitKey(0)
            if key == 0:
                self.goodImgs.pop(i)
                cv2.destroyWindow(winname)
                inc += 1
                #print("deleted")
            elif key == ord('a') or key == ord('b'):
                #print("back")
                cv2.destroyWindow(winname)
                i += 1
                if i>=len(self.goodImgs):
                    i = len(self.goodImgs) -1
                continue
            elif key == 27:
                print("accepting all images")
                break
            else:
                #print("accept")
                cv2.destroyWindow(winname)
            i -= 1
            

        print(str(len(self.goodImgs))+" Images of Chessboard Collected in variable goodImgs")
        print(str(inc)+" images removed.")

    def exportCalibrationVectors(self, frame):
        """Creates an ndarray of vectors which represent the distortion of the camera lens.
        Those vectors are then saved to various files in the folder CALIB/ in the current directory.
        these vectors can be accessed later by calling in this way
        camera_matrix = numpy.load("CALIB/mtx")
        """
        grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        print("calibrating... this may take some time")
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, grayframe.shape[::-1], None, None)

        #Save to files
        print("saving...")
        if not os.path.exists("CALIB"):
            os.mkdir("CALIB")

        retOut = open("CALIB/ret.txt", 'w')
        retOut.write(str(ret))
        numpy.save("CALIB/mtx", mtx)
        numpy.save("CALIB/dist", dist)
        numpy.save("CALIB/rvecs", rvecs)
        numpy.save("CALIB/tvecs", tvecs)
        print("Calibration files saved in current directory in folder 'CALIB'")

    
