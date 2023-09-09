'''
Created on 20.02.2021

@author: MF
'''
from MoveAbleEntity import MoveAbleEntity
from GameSettings import GameSettings
from Vector import Vector2
from com.badlogic.gdx.math import Rectangle
import math





class CarConfig(object):
    '''
    classdocs
    '''


    def __init__(self, mAcc, mVel, gas, m, pSpace):
        '''
        Constructor
        '''
        self.maxAcceleration = mAcc
        self.gas = gas
        self.maxVelocity = mVel
        self.mass = m
        #sitzplaetze
        self.PeopleSpace = pSpace
        


class Car(MoveAbleEntity):
    
    def __init__(self, moveAbleEntity, ccfg):
        MoveAbleEntity.__init__(self, moveAbleEntity, ccfg.maxVelocity, ccfg.maxAcceleration, GameSettings.CarDrag)
        
        self.heading = Vector2(0,0).add(self.position).add(Vector2(self.width/2,0))
        self.isAiControlled = True
        self.angle = 0
        self.gas = ccfg.gas
        
        self.seats = ccfg.PeopleSpace
        self.driver = None
        self.passengers = dict()
        
    def update(self, dt):
        
        if self.isAiControlled: 
            self.handleAi(dt)
            self.calcAngle()
        else:
            #use player input to set velocity and acceleration
            self.calcHeading()
            

        
        self.calcDirection()
        self.move(dt)
        self.syncPassengerAndDriverPos()
        
    
    def steerLeft(self,dt):
        if(self.velocity.len() > GameSettings.lowestVelocityLenght):
            self.angle += 1 * dt
    
    def steerRight(self,dt):
        if(self.velocity.len() > GameSettings.lowestVelocityLenght):
            self.angle -= 1 * dt
        
    def hitGas(self,dt):
        
        if(self.acceleration.len() <= 0.2):
            #start motor
            self.acceleration.add(self.heading)
        
        th = Vector2(v=self.heading)
        th.sub(self.position)
        th.nor()
        th.scl(self.gas)
        
        self.accelerate(th, dt)
        
    def brake(self,dt):
        self.acceleration.scl(0.9 * dt)
        if(self.acceleration.len() < 0.01):
            self.stop()
        
        
    
    def setControlledbyPlayer(self):
        self.isAiControlled = False
    
    def setAiControlled(self):
        self.isAiControlled = True
        
    def calcHeading(self):
        self.heading.x = self.position.x + 10 * math.cos(self.angle)
        self.heading.y = self.position.y + 10 * math.sin(self.angle)
        
    def calcAngle(self):
        self.angle = math.atan2(self.position.y - self.heading.y, self.position.x - self.heading.x)
        self.angle = self.angle * 180 / math.pi
        
    def calcDirection(self):
        
        tpos = Vector2(v=self.position)
        th = Vector2(v=self.heading)
        direction = th.sub(tpos)
        direction.nor()
        if(self.acceleration.len() > 1):  
            direction.scl(self.acceleration.len())
        self.setAcceleration(direction)
    
    def addPassenger(self, aPeoplePassenger):
        if len(self.passengers) < self.seats:
            aPeoplePassenger.isInCar = self
            self.passengers[aPeoplePassenger.oID] = aPeoplePassenger
            return True
        else:#car full
            return False
        
    def removePassenger(self, toRemovePassenger):
        if toRemovePassenger.oID in self.passengers:
            toRemovePassenger.isInCar = None
            toRemovePassenger.position.x = self.position.x + self.getBoundingBox().width + 5
            self.passengers.pop(toRemovePassenger.oID, toRemovePassenger)
            return True
        else:
            return False    
        
        
    def syncPassengerAndDriverPos(self):
        for p in self.passengers:
            pa = self.passengers[p]
            pa.position = Vector2(v=self.position) 
            
        if self.driver != None:
            self.driver.position = Vector2(v=self.position)
            
    def setDriver(self, newDriver):
        if self.driver == None:
            self.driver = newDriver
            self.driver.isInCar = self
            #keiner rausgeworfen
            return None
        else:
            #steal
            d = self.throwDriverOut()
            self.driver = newDriver
            self.driver.isInCar = self
            #return throwen out driver
            return d
        
    def removeDriver(self):
        d = self.throwDriverOut()
        return d
    
    def throwDriverOut(self):
        if self.driver != None:
            self.driver.isInCar = None
            self.driver.position.x = self.position.x - self.driver.getBoundingBox().width - 5
            d = self.driver
            self.driver = None
            return d
        else:
            return None
            
    def getDriverBoardArea(self):
        driverBoardWidth = 35
        driverBoardHeight = 40
        return Rectangle(self.position.x - driverBoardWidth/2, self.position.y + self.getBoundingBox().height * 0.8, driverBoardWidth, driverBoardHeight)
        
    
    def getPassengerBoardArea(self):
        passengerBoardWidth = 35
        passengerBoardHeight = 40
        return Rectangle(self.position.x + self.getBoundingBox().width - passengerBoardWidth/2, self.position.y + self.getBoundingBox().height * 0.8, passengerBoardWidth, passengerBoardHeight)
             
    
    def handleAi(self, dt):
        pass
        #sets move target dynamicly