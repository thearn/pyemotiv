from gzp import load
import numpy as np
import pylab
import matplotlib
matplotlib.use('Agg')

"""
Loads & plots data from disk
"""

data, times, breaktime, channels = load("experiment.dat")
m,n = data.shape

pylab.figure()
for i in xrange(len(channels)):
    pylab.subplot(14,1,i+1)
    pylab.plot(data[i])

pylab.figure()
for i in xrange(m):
    pylab.subplot(14,1,i+1)
    fd = np.hanning(n)*(data[i]-data[i].mean())
    fd = np.abs(np.fft.rfft(fd))**2
    freqs = np.linspace(0,64.,len(fd))
    pylab.plot(freqs[10:],fd[10:])
    pylab.xlim(0,64)

pylab.show()