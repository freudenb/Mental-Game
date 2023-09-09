'''
Created on 18.02.2021

@author: MF
'''

from People import People
from MoveAbleEntity import MoveAbleEntity
from Entity import Entity
from com.badlogic.gdx import Gdx
from Car import CarConfig
from Car import Car
from Vector import Vector2
import pickle
from Player import Player
from GameSettings import GameSettings
from NetworkPackages import WorldUpdatePackage


class World(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.players = dict()#players[ID] = player
        self.staticObjects = dict()
        self.cars = dict()
        self.people =  dict()
        self.bullets = dict()
        self.nodes =  dict()
        
        self.controlledPlayer = None
        self.controlledCar = None
    
    #add Player and a People Instanz that is controlled by player with pID
    def addPlayer(self, pID, controlledPeople):
        
        self.players[pID] = Player(pID)
        self.people[controlledPeople.oID] = controlledPeople
        self.controlPeople(controlledPeople.oID)
        self.setPlayer(pID)
        
    def setPlayer(self, pID):
        
        self.players[pID].controlledPeople = self.controlledPlayer
        self.players[pID].controlledCar = self.controlledCar
        
    def connectPlayerControlledThingsWithWorldControlledThings(self, pID):
        
        self.controlledPlayer = self.players[pID].controlledPeople
        self.controlledCar = self.players[pID].controlledCar
        
    def createWorldFromWorldPackage(self, wp):
        
        self.players = wp.players
        self.people = wp.people
        self.cars = wp.cars
        self.bullets = wp.bullets
    
        
    def update(self, dt, viewport):
        
    
               
        for p in self.people:
            
            self.people[p].update(dt)
            
            
        for c in self.cars:
            
            self.cars[c].update(dt)
         
         
        self.checkCollision(dt, viewport)
        
    
    def checkCollision(self, dt, viewport):
        
        
        #build List with on screen objects
        
        for p in self.players:
            player = self.players[p]
            #collision player -> staticObject
            for s in self.staticObjects:
                pass
        
    
    
    def buildWorld(self):
        #add all objects
        dimensions = GameSettings.TextureDimensions
                
        e = Entity(2,Vector2(300,200),dimensions[2].width,dimensions[2].height)
        me = MoveAbleEntity(e,200,200, 0.01)
        self.people[e.oID] = People(me)
        
        e = Entity(3,Vector2(400,200),dimensions[3].width,dimensions[3].height)
        me = MoveAbleEntity(e,200,200, 0.01)
        self.cars[e.oID] = Car(me, CarConfig(2000,4000,800,20,4))

        
        for s in range(200):
            e = Entity(4,Vector2(20 + 5 * s + dimensions[4].width * s ,0),dimensions[4].width, dimensions[4].height)
            self.staticObjects[e.oID] = e
    
    
    def tryToEnterCarAsPassenger(self, apeople):
        if apeople.isInCar == None:
            for c in self.cars:
                acar = self.cars[c]
                if(acar.getPassengerBoardArea().overlaps(self.controlledPlayer.getBoundingBox())):
                    #try enter as passenger
                    if(acar.addPassenger(apeople)):
                        print("entering Car with oID: "+str(acar.oID)+" as passenger")
                    else:
                        pass
                    break
           
    
    def tryToControlCar(self):
        if self.controlledCar == None and self.controlledPlayer.isInCar == None:
            
            for c in self.cars:
                acar = self.cars[c]
                if(acar.getDriverBoardArea().overlaps(self.controlledPlayer.getBoundingBox())):
                    #enter as driver
                    print("entering Car with oID: "+str(acar.oID))
                    d = acar.setDriver(self.controlledPlayer)
                    acar.setControlledbyPlayer()
                    self.controlledCar = acar
                    if(d != None):
                        if(d == self.controlledPlayer):
                            #spieler rausgeworfen
                            self.controlledCar = None
                            self.controlledPlayer.isInCar = None
                            
                        
                    break
                
    
    def getPlayerOutOfDriverSeat(self):
        if self.controlledCar != None:
            self.controlledPlayer = self.controlledCar.removeDriver()
            #self.controlledCar.setAiControlled()
            self.controlledCar = None   

        
    def controlPeople(self, pId):
        #set last controlled player to ai controlled and choose new people
        if self.controlledPlayer != None and pId in self.people:
            self.controlledPlayer.setAiControlled()
        
        if pId in self.people:
            
            self.people[pId].setControlledbyPlayer()
            self.controlledPlayer = self.people[pId]