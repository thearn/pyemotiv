pyemotiv
---------

A Python library to aquire data from the Emotiv Epoc EEG neuroheadset, using
the files provided with the Emotiv research SDK.

Requirements:
-------------
- Python 2.7+
- Numpy 1.5.0+
- Research SDK library files from Emotiv. These must be build for the same architecture as
your python installation (either i386 or x86_64), otherwise ctypes.CDLL will raise an error

Setup:
------
- Build and install the library: `python setup.py build install`
- Dynamic link library files for the research SDK should be placed in a 
location known to your system's PATH:
    - Windows: `edk.dll` and `edk_utils.dll` in `windows/system32`
    - OSX: `libedk.dylib` and `libedk_ultils_mac.dylib` in `usr/local/lib`
- Import class `Epoc` from `emotiv.py` into your Python application.

Example:
-------
This demonstrates using a call to get all data from the Epoc at once:

```python
from pyemotiv import Epoc

epoc = Epoc()
while True:
    epoc.get() #Aquire latest data from hardware buffer. Iterates over all channels
    data = epoc.raw #14-by-n numpy array containing raw data for AF3 through AF4
    gyros = epoc.gyros #2-by-n-row array containing data for GYROX and GYROY
    times = epoc.times #1d array containing timestamp values (interpolated)
    everything = epoc.all_data # 25-by-n array containing all data returned by emotiv
```
This demonstrates using reduced calls that just get certain channels of data
(only the raw EEG, or only the gyros). This is more efficient if you know what you want.
```python
from pyemotiv import Epoc

epoc = Epoc()
while True:
    data = epoc.get_raw #14-by-n numpy array containing raw data for AF3 through AF4
```

```python
from pyemotiv import Epoc

epoc = Epoc()
while True:
    gyros = epoc.get_gyros #2-by-n-row array containing data for GYROX and GYROY
```
You can mix and match these two kinds of calls if you prefer, however the `times`
array will not be accurate if you do this.

Todo:
------
- Add support for Linux (I do not have access to the Linux SDK files, though)