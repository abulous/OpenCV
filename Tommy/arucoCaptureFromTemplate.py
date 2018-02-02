import cv2
import numpy as np
from cv2 import aruco as arc

cap = cv2.VideoCapture(0)

##Stolen from other code - don't know which camera they correspond to, but it works
camera_matrix = np.array( [1.0327407219495085e+03, 0., 9.5685930301206076e+02,
                           0., 1.0323427647512485e+03, 5.3914133979587950e+02,
                           0., 0., 1.] ).reshape( (3,3) )
dis_coeff = np.array( [2.0429028189430772e-02,
                       -7.8399448855923665e-03,
                       -3.0949667668667908e-03,
                       2.18486478263377197e-03,
                       -5.2344198896187882e-02] ).reshape( (1,5) )
dictionary = arc.getPredefinedDictionary(arc.DICT_7X7_1000)
marker_width = 0.02470 #meters

##Video Out
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#vidOut = cv2.VideoWriter('C:/Users/tlsharkey/Desktop/livePoseEst_noID.avi', fourcc, 29.97, (640,480))

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    markers, ids, rejects = arc.detectMarkers(gray, dictionary)


    #if markers detected > 0
    try:
        len(ids)
        idsExist = True
    except:
        idsExist = False
    if idsExist:
        #arc.drawDetectedMarkers(frame, markers, ids)

        vectors = arc.estimatePoseSingleMarkers(markers, marker_width,
                                                     camera_matrix, dis_coeff)
        #vectors = arc.estimatePoseBoard(markers, ids, ??board??, camera_matrix, dis_coeff
        for i in range(len(ids)):
            arc.drawAxis(frame, camera_matrix, dis_coeff,
                         vectors[0][i], vectors[1][i], marker_width*2)

    cv2.imshow("Feed", frame)
    #vidOut.write(frame)
    if cv2.waitKey(33) == 27:
        cap.release()
        cv2.destroyAllWindows()
        break
