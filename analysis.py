from gzp import load
import pylab
import matplotlib
matplotlib.use('Agg')

"""
Loads & plots data from disk
"""

data, times, breaktime, channels = load("experiment.dat")

for dat in data:
    pylab.figure()
    pylab.plot(dat)

pylab.show()