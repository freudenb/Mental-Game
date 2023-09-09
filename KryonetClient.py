'''
Created on 01.03.2021

@author: MF


'''
'''
Created on 25.02.2021

@author: MF
'''

from com.esotericsoftware.kryonet import Client
from com.esotericsoftware.kryonet import Listener
from NetworkPackages import WorldUpdatePackage


class MyClientListener(Listener):
    
    def __init__(self, Client):
        self.client = Client
    
    def recieved(self, connection, objec):
        pass
        
    def connected(self, connection):
        print("Client connected with id: "+str(connection.getID()))
        pass
    
    
    def disconnected(self, connection):
        print("Client disconnected")
        pass



class MentalClient(object):
    '''
    classdocs
    '''


    def __init__(self, World):
        '''
        Constructor
        '''
        self.world = World
        self.client = Client()
        self.client.start()
        self.client.addListener(MyClientListener(self))
        #register datapackege classes
        #self.client.register()
        kr = self.client.getKryo()
        kr.setRegistrationRequired(False)
        #kr.register(WorldUpdatePackage)
    
        
    def connect(self, IP, Port):
      
        self.client.connect(5000,IP,Port)
   
        
        