
from World import World
from PodSixNet.Connection import connection, ConnectionListener
from time import sleep

import cPickle as pickle
from NetworkPackages import WorldUpdatePackage


class MentalClient(ConnectionListener):
    '''
    classdocs
    '''


    def __init__(self, World):
        '''
        Constructor
        '''
        self.world = World
        
        
    def connect(self, IP, Port):
      
        try:
            self.Connect((IP, Port))            
            
        except Exception as e:
            print(e)
   
    def cPump(self):
        
        connection.Pump()
        self.Pump()
   
    def Network(self, data):
        #print("network data:"+str(data))
        pass
    
    def Network_connected(self, data):
        print("You are now connected to the server")
    
    def Network_error(self, data):
        print('error:', data['error'][0])
        connection.Close()
    
    def Network_disconnected(self, data):
        print('Server disconnected')
        
    def Network_playerID(self, data):
        print("recieving player id: "+str(data["id"]))
        print(data)
        self.world.connectPlayerControlledThingsWithWorldControlledThings(data["id"])
        

    def Network_syncWorld(self, data):
        #print(data)
        wp = pickle.loads(data["dumpedWorldUpdatePackage"])
        self.world.createWorldFromWorldPackage(wp)
    

if __name__ == '__main__':

    
    mC = MentalClient(World())
    mC.connect('localhost', 31245)

   
    i = 0
    while True:
        i+=1
        mC.cPump()
        sleep(0.001)