
from GameSettings import GameSettings
from World import World
import urllib
import time
from time import sleep
from com.badlogic.gdx.math import Rectangle
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from People import People
from MoveAbleEntity import MoveAbleEntity
from Entity import Entity
from Vector import Vector2
from NetworkPackages import WorldUpdatePackage
import cPickle as pickle


class ClientChannel(Channel):
    """
    This is the server representation of a single connected client.
    """
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.id = str(self._server.nextId())
    
    def Close(self):
        self._server.Disconnected(self)
    
    def Network_message(self, data):
        pass
    
    def Network_nickname(self, data):
        print(data)
        pass
   

class MentalServer(Server):
    
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        
        self.id = 0
        
        GameSettings.loadTextureDimensions()
  
        self.world = World()
        self.world.buildWorld()
        
        self.connectedChannels = dict()
        
    def nextId(self):
        self.id += 1
        return self.id
    
    def Connected(self, channel, addr):
        print("New Client connected to server("+str(channel.addr)+")")
        
        dimensions = GameSettings.TextureDimensions      
        e = Entity(2,Vector2(300,200),dimensions[2].width,dimensions[2].height)
        me = MoveAbleEntity(e,200,200, 0.01)
        self.world.addPlayer(channel.id, People(me))
        self.connectedChannels[channel.id] = channel
        print(self.world.players)
        self.syncWorldWithClients()
        d = dict()
        d["action"] = "playerID"
        d["id"] = channel.id
        channel.Send(d)
                
    def createWorldUpdatePackage(self):
        return WorldUpdatePackage(self.world.players, self.world.cars, self.world.people, self.world.bullets)
    
    def syncWorldWithClients(self):
        d = dict()
        d["action"] = "syncWorld"
        wp = self.createWorldUpdatePackage()
        d["dumpedWorldUpdatePackage"] = pickle.dumps(wp)
        self.SendToAll(d)
        
    def Disconnected(self, channel):
        print("Player disconnected, Addr: "+str(channel.addr))
        del self.connectedChannels[channel.id]
        del self.world.players[channel.id]
        
    def SendToAll(self, data):
        for p in self.connectedChannels:
            self.connectedChannels[p].Send(data)
        
    
    def start(self):
        ip = urllib.urlopen('https://ident.me').read().decode('utf8')
        print("Mental Server started at ExternalIP: "+ip)
        self.run()
        
    def run(self):
        
       
        lastTime = time.time()
        currentTime = time.time()+0.002
        
        while True:
            self.Pump()
            self.syncWorldWithClients()
            currentTime = time.time()
            dt = currentTime - lastTime
            lastTime = currentTime
            self.world.update(dt, Rectangle(0,0,10,10))

            sleep(1.0/60.0)
            try:
                #print(1/dt)
                pass
            except Exception as e:
                print(e)    
        
        
if __name__ == '__main__':
    
    ms = MentalServer(localaddr=('localhost', 31245))
    ms.start()