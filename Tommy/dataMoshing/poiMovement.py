import cv2
import numpy as np

poi_parameters = dict(maxCorners = 100,
                      qualityLevel = 0.02,
                      minDistance = 7,
                      blockSize = 7)

def init(gray):
  ''' Initialize the tracking by giving it a base frame
  @param gray a gray frame from video
  @return nothing
  '''
  global gray_last
  global poi_last
  gray_last = gray.copy()
  poi_last = cv2.goodFeaturesToTrack(gray_last, **poi_parameters)

def setPOI_params(maxNumPts=100, quality=0.02, minDist=7, block=7):
  ''' Set parameters used to find points of interest (POI)
  @param MaxNumPts the total number of POIs allowed - will usually be below this number
  @param quality how picky the program is at choosing POIs
  @param minDist the required distance between POIs
  @param block the size of each block to search for POIs
  '''
  global poi_parameters
  poi_parameters['maxCorners'] = maxNumPts
  poi_parameters['qualityLevel'] = quality
  poi_parameters['minDistance'] = minDist
  poi_parameters['blockSize'] = block

def getChange(gray):
  ''' Get the pixel movement of various important pixels
  uses the previously passed frame
  (either through last call of this function or init() )
  and compares points of interest
  @param gray a gray frame from video
  @return list of pairs of points in the format ( (x_new, y_new), (x_old, y_old) )
  '''
  global gray_last
  global poi_last
  changed = []
  
  poi = cv2.goodFeaturesToTrack(gray, **poi_parameters)

  poi, good, bad = cv2.calcOpticalFlowPyrLK(gray_last, gray, poi_last, poi)
  #only choose Points of Interest (poi) which were found 
  poi = poi[good==1]
  poi_last = poi_last[good==1]

  for i in range(len(poi)):
    x1,y1 = poi[i].ravel()
    x2,y2 = poi_last[i].ravel()
    changed.append( ((x1,y1),(x2,y2)) )

  gray_last = gray.copy()
  poi_last = poi.reshape(-1,1,2)

  return changed
