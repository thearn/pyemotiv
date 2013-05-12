from ctypes import c_char_p, c_uint, c_int,c_bool, byref, CDLL
import numpy as np
import time, sys

class Epoc():
    """
    Class that connects to Emotiv Epoc by wrapping the 
    research SDK dynamic link libraries
    """
    def __init__(self):
        self.channels = ['ED_COUNTER','ED_INTERPOLATED','ED_RAW_CQ',
                                  'ED_AF3','ED_F7','ED_F3','ED_FC5','ED_T7',
                                  'ED_P7','ED_O1','ED_O2','ED_P8','ED_T8',
                                  'ED_FC6','ED_F4','ED_F8','ED_AF4','ED_GYROX',
                                  'ED_GYROY','ED_TIMESTAMP','ED_ES_TIMESTAMP',
                                  'ED_FUNC_ID','ED_FUNC_VALUE','ED_MARKER',
                                  'ED_SYNC_SIGNAL']
        self.raw_channels_idx = range(3,17)
        self.gyro_idx = [self.channels.index("ED_GYROX"),self.channels.index("ED_GYROY")]
        self.names = [name[3:] for name in self.channels]
        self.name_dict = {name:i for name,i in zip(self.names,
                                                   xrange(len(self.names)))}
        self.m = len(self.channels)
        self.all_data = np.zeros((25,2))
        self.raw = np.zeros((14,2))
        self.gyros = np.zeros((2,2))
        self.sr = 1/127.94
        self.times = [0.]
        
        #setup access to binaries
        if sys.platform=='darwin':
            edk_file='libedk.dylib'
        elif sys.platform=='win32':
            sys.path.append('lib')
            edk_file='edk.dll'
        self.edk=CDLL(edk_file)
        
        self.connected = False
        
    def connect(self, timeout = 10):   
        """
        Establishes connection to Emotiv Epoc
        """
        connect_param = c_char_p(b'Emotiv Systems-5')
        self.edk.EE_EngineConnect(connect_param)
        self.data_handler = self.edk.EE_DataCreate()
        self.edk.EE_DataSetBufferSizeInSec(5)
        
        eEvent = self.edk.EE_EmoEngineEventCreate()
        state = self.edk.EE_EngineGetNextEvent(eEvent)
        t0 = time.time()
        while not self.connected:
            state = self.edk.EE_EngineGetNextEvent(eEvent)
            if not state:
                self.connected = True
                self.edk.EE_DataAcquisitionEnable(c_uint(0),c_bool(1))
                break
            if time.time() - t0 > timeout:
                raise Exception('Timeout while connecting to Epoc!')
                
    
    def get_all(self):
        """
        Get block of raw data from the device buffer
        """
        if not self.connected:
            self.connect()
            
        container = self.aquire(xrange(self.m))
        self.raw = np.array([container[i] for i in self.raw_channels_idx])
        self.gyros = np.array([container[i] for i in self.gyro_idx])
        self.all_data = container
        return self.all_data
    
    def get_raw(self):
        if not self.connected:
            self.connect()
        container = self.aquire(self.raw_channels_idx)
        self.raw = container
        return container
    
    def get_gyros(self):
        if not self.connected:
            self.connect()
        container = self.aquire(self.gyro_idx)
        self.gyros = container
        return container
        
    def aquire(self,idx):
        nSamples = c_int()
        while True:
            self.edk.EE_DataUpdateHandle(c_uint(0), self.data_handler)
            self.edk.EE_DataGetNumberOfSample(self.data_handler, 
                                              byref(nSamples))
            n = nSamples.value
            if not n:
                continue
            container = np.empty((len(idx) , n))
            k=0
            for i in idx:
                data = np.empty((1,n))
                data_ctype = np.ctypeslib.as_ctypes(data)
                self.edk.EE_DataGet(self.data_handler, i, byref(data_ctype),
                                    c_uint(n))
                data_read = np.ctypeslib.as_array(data_ctype)
                container[k,:] = data_read[0]
                k+=1
            self.times = np.linspace(self.times[-1]+self.sr, 
                                     self.times[-1]+ n*self.sr, n)            
            return container
        
        
if __name__ == "__main__":
    e = Epoc()
    while True:
        e.get_raw()