from gzp import load
import pylab

"""
Loads & plots data from disk
"""

data, times, breaktime, channels = load("experiment.dat")

pylab.figure()
pylab.plot(times, data)

pylab.plot([breaktime, breaktime],[-1e6, 1e6], 'k--')
pylab.ylim(min(data), max(data))

pylab.xlabel("time")
pylab.ylabel("GSR")

pylab.show()