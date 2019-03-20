Isaac's OpenCV folder:

March 11 Update:

geez, I got behind on updating this readme. New stuff!

	-track-object-movement contains some cool object tracking 
		based on color masking. tracks a tennis ball in a live feed or video
		
	-opticalFlow folder contains code for using cv2's built in optical flow tracker.
		draws funky lines based on video feed intensities (corner finder)
		-also playing with laplacian edge detection - 3 channel output! wooo!
		
	-testMultiStream uses UDP sockets to stream images over a local network.
		-currently set up to send 140x140 RGB images, one image per packet.

#####################

Feb commit:

-webcamStream uses combines basic video capture and a simple udp transfer 


First commit: 

-basic capture for pi camera
-delay demo for pi camera
-3-D model for printing a pi camera case

-Computer Vision folder: 
	-webcam motion detection from piImageSearch guy
	-motion detection for pi cam
	-convulutional neural net object recongition
		(wont run on pi)

-Streaming folder:
	-true image streaming
		(pi -> network -> faster comp for img processing)
		(server needs to be running before client)
	-flask is another tool which can be used to stream a feed
