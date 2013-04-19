from ctypes import *
import numpy as np
import time,sys

class Epoc():
    def __init__(self,channels=None,single=False):
        self.DataChannelsNames = ['ED_COUNTER','ED_INTERPOLATED','ED_RAW_CQ',
                                  'ED_AF3','ED_F7','ED_F3','ED_FC5','ED_T7',
                                  'ED_P7','ED_O1','ED_O2','ED_P8','ED_T8',
                                  'ED_FC6','ED_F4','ED_F8','ED_AF4','ED_GYROX',
                                  'ED_GYROY','ED_TIMESTAMP','ED_ES_TIMESTAMP',
                                  'ED_FUNC_ID','ED_FUNC_VALUE','ED_MARKER',
                                  'ED_SYNC_SIGNAL']
        self.DataDict=dict([[self.DataChannelsNames[i],i] 
                            for i in xrange(len(self.DataChannelsNames))])
        self.channels=channels
        if not self.channels:
            self.channels=self.DataChannelsNames
        self.channels_idx=[self.DataDict[i] for i in self.channels]
        self.channels_out=dict([[self.channels[i],i] 
                                for i in xrange(len(self.channels))])
        self.nc=len(self.channels_idx)
        self.edk=None
        self.dataHandler=None
        self.acq=False
        self.t=0
        self.sr=1.0/128
        self.setup()
        self.connect()
        
    def setup(self):
        if sys.platform=='darwin':
            edk_file='bin/libedk.dylib'
        elif sys.platform=='win32':
            sys.path.append('lib')
            edk_file='bin/edk.dll'
        self.edk=CDLL(edk_file)
            
    def connect(self):   
        connect_param=c_char_p(b'Emotiv Systems-5')
        print "connect status",self.edk.EE_EngineConnect(connect_param)
        self.dataHandler=self.edk.EE_DataCreate()
        self.edk.EE_DataSetBufferSizeInSec(5)
        
        eEvent=self.edk.EE_EmoEngineEventCreate()
        state=self.edk.EE_EngineGetNextEvent(eEvent)
        while True:
            if not self.acq:
                state=self.edk.EE_EngineGetNextEvent(eEvent)
                if not state:
                    self.acq=True
                    self.edk.EE_DataAcquisitionEnable(c_uint(0),c_bool(1))
                    print "Connected!"
                    break
            else:
                pass
                    
    def get_next(self,single=False,asDict=False):
        if single:
            chans=[self.DataDict[i] for i in single]
            nc=len(chans)
        else:
            chans=self.channels_idx
            nc=self.nc
        nSamples=c_int()
        while True:
            if self.acq:
                self.edk.EE_DataUpdateHandle(c_uint(0),self.dataHandler)
                self.edk.EE_DataGetNumberOfSample(self.dataHandler,
                                                  byref(nSamples))
                nSamplesTaken=nSamples.value
                if nSamplesTaken:
                    if single:
                        container=np.empty(nc+1)
                    else:
                        container=np.empty((nc+1,nSamplesTaken))
                    for i,k in zip(chans,xrange(nc)):
                        data=np.empty((1,nSamplesTaken))
                        data_ctype=np.ctypeslib.as_ctypes(data)
                        self.edk.EE_DataGet(self.dataHandler,
                                            i,
                                            byref(data_ctype),
                                            c_uint(nSamplesTaken))
                        data_read=np.ctypeslib.as_array(data_ctype)
                        if single:
                            container[k]=data_read[0][-1]
                        else:
                            container[k,:]=data_read[0]
                    if asDict:
                        time=np.array([self.t+(i+1)*self.sr 
                                       for i in xrange(nSamplesTaken)])
                        container[-1,:]=time
                        self.t=time[-1]
                        container=[list(c) for c in container]
                        return dict(zip(self.channels+["time"],list(container)))
                    else:
                        return container
            else:
                print "not connected!"
                self.connect()
        
if __name__=="__main__":
    epoc=Epoc()
    channels= epoc.channels_out
    
    while True:
        #time.sleep(0.1)
        x,y,t= epoc.get_next(single=['ED_GYROY','ED_GYROX','ED_TIMESTAMP'])
        print t
        