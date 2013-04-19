pyemotiv
=====================

A Python library to aquire data from the Emotiv Epoc EEG neuroheadset, using
the files provided with the Emotiv research SDK.

# Requirements:
- Python 2.7+
- Numpy 1.5.0+
- Research SDK library files from Emotiv

# Setup:

- Dynamic link library files for the research SDK should be placed
    in the `lib\bin` directory:
    - Windows: `edk.dll` and `edk_utils.dll`
    - OSX: `libedk.dylib` and `libedk_ultils_mac.dylib`
    
- Import class `Epoc` from `emotiv.py` into your Python application.

# Example:

```python
from pyemotiv import Epoc

epoc = Epoc()
while True:
    # get only the most recent values for the gyro sensors and the latest time
    # stamp
    g_y, g_x, t= epoc.get_next(single=['ED_GYROY','ED_GYROX','ED_TIMESTAMP'])
    print g_y, g_x, t
```
    
