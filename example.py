from pyemotiv import Epoc
from time import sleep
        
if __name__=="__main__":
    epoc=Epoc()
    channels= epoc.channels
    
    while True:
        raw = epoc.get_gyros() #19,20
        print raw[:,-1]