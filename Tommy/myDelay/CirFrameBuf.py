
import numpy as np

class CirFrameBuf:
    def __init__(self, size, h, w, pixdepth):
        self.iw = 0
        self.ir = 0
        self.size = size
        if pixdepth <= 1:
            self.buf = np.zeros((size, h, w), dtype="uint8")
        else:
            self.buf = np.zeros((size, h, w, pixdepth), dtype="uint8")
        
        
    def write(self, frame):
        if self.iw >= self.size:
            self.iw = 0
        self.buf[self.iw] = frame
        self.iw += 1

    def read(self):
        if self.ir >= self.size:
            self.ir = 0
        frame = self.buf[self.ir]
        self.ir += 1
        return frame
    
    # what the hell am I thinking?
    # seahorses forever
    def readback(self, nframes):
        i = self.iw - nframes
        if i < 0:
            i += self.size  # i = self.size - abs(i)
        return self.buf[i]
        

