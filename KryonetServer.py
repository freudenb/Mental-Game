'''
Created on 01.03.2021

@author: MF
'''
from com.esotericsoftware.kryonet import Connection
from com.esotericsoftware.kryonet import Listener
from com.esotericsoftware.kryonet import Server
from com.esotericsoftware.kryonet import JsonSerialization
import urllib
from World import World
from com.badlogic.gdx.math import Rectangle
import time
from time import sleep
from GameSettings import GameSettings
from People import People
from MoveAbleEntity import MoveAbleEntity
from Entity import Entity
from com.badlogic.gdx.math import Vector2
from NetworkPackages import WorldUpdatePackage, TextMessagePackage


class MyServerListener(Listener):
    
    def __init__(self, mServer):
        self.mServer = mServer
        pass
    
    def recieved(self, connection, objec):
        pass
        
        
    def connected(self, connection):
        print("New Client connected to server("+str(connection.getID())+")")
        
        dimensions = GameSettings.TextureDimensions      
        e = Entity(2,Vector2(300,200),dimensions[2].width,dimensions[2].height)
        me = MoveAbleEntity(e,200,200, 0.01)
        self.mServer.world.addPlayer(connection.getID(), People(me))
        pass
    
    
    def disconnected(self, connection):
        print("Client("+str(connection.getID())+") disconnected")
        pass


class MentalServer(object):
    
    
    def __init__(self, port):
        self.server = Server()
        #register
        kr = self.server.getKryo()
        kr.setRegistrationRequired(False)
        kr.register(WorldUpdatePackage)
        
        self.server.addListener(MyServerListener(self))
        self.server.bind(port)
        
        GameSettings.loadTextureDimensions()
  
        self.world = World()
        self.world.buildWorld()
       
    
    def start(self):
        self.server.start()
        ip = urllib.urlopen('https://ident.me').read().decode('utf8')
        print("Mental Server started at ExternalIP: "+ip)
        self.run()
    
    def syncWorldWithClients(self):
        w = WorldUpdatePackage(self.world.players, self.world.cars, self.world.people, self.world.bullets)
        self.server.sendToAllTCP(w)
        
    def run(self):
        
        lastTime = time.time()
        currentTime = time.time()+0.002
        
        while True:
            currentTime = time.time()
            dt = currentTime - lastTime
            lastTime = currentTime
            self.world.update(dt, Rectangle(0,0,10,10))
            self.syncWorldWithClients()
            sleep(1.0/60.0)
            try:
                #print(1/dt)
                pass
            except Exception as e:
                print(e)    
    
if __name__ == '__main__':
    
    
    mS =  MentalServer(6969)
    mS.start()
        
        
    