from pyemotiv import Epoc
from time import sleep
from gzp import save
import numpy as np
        
if __name__=="__main__":
    epoc=Epoc()
    channels= epoc.channels
    acq = False
    while True:
        try:
            raw = epoc.get_raw() 
            if not acq:
                data = raw
            else:
                data = np.concatenate((data, raw), axis = 1)
        except KeyboardInterrupt:
            save(data, "data.dat")