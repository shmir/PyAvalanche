
# JAVA_HOME = C:\Program Files\Java\jdk1.7.0_60

from avalancheapi.avalanche import AVA

apipath = 'C:/Program Files (x86)/Spirent Communications/Spirent TestCenter 4.71/Layer 4-7 Application/TclAPI'

avl = AVA(apipath=apipath, logpath='c:/temp', loglevel="DEBUG")
