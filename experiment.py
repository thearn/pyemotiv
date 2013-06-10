from pyemotiv import Epoc
import numpy as np
from gzp import save
import time

"""
Sample Emotiv experiment.

Gathers data over two phases. Use a keyboard interrupt (control-c) to end a phase.

Saves data to disk afterwards.
"""

headset = Epoc()

data = headset.get_raw()
times = headset.times
t0 = time.time()

print "First phase..."
while True: #first phase (eg. 'resting')
    try:
        x = headset.get_raw()
        t = time.time() - t0
        
        data = np.concatenate((data, x), axis  = 1)
        times.append(t)
    
    except KeyboardInterrupt:
        break

breaktime = time.time() - t0

print "Second phase..."
while True: #second phase (eg. 'attentive')
    
    try:
        x = headset.get_raw()
        t = time.time() - t0
        
        data = np.concatenate((data, x), axis  = 1)
        times.append(t)
    
    except KeyboardInterrupt:
        break

print "Done - saving to disk ('experiment.dat')"
save([data, times, breaktime, headset.channels[3:17]], "experiment.dat")