'''
Created on 19.02.2021

@author: MF
'''
from MoveAbleEntity import MoveAbleEntity
from GameSettings import GameSettings
from Vector import Vector2
import math


class People(MoveAbleEntity):
    '''
    classdocs
    '''


    def __init__(self, moveAbleEntity):
        '''
        Constructor
        '''
        #super(MoveAbleEntity,self).__init__(self,0, moveAbleEntity, GameSettings.PeopleMaxVelocity,GameSettings.PeopleMaxAcceleration)
        MoveAbleEntity.__init__(self, moveAbleEntity, GameSettings.PeopleMaxVelocity, GameSettings.PeopleMaxAcceleration, GameSettings.PeopleDrag)
        
        self.isAiControlled = True
        self.MoveTarget = Vector2()
        self.angle = 0
        self.isInCar = None
        
    
    def setControlledbyPlayer(self):
        self.isAiControlled = False
    
    def setAiControlled(self):
        self.isAiControlled = True
    
    def calcAngle(self):
        self.angle = math.atan2(self.position.y - self.MoveTarget.y, self.position.x - self.MoveTarget.x)
        self.angle = self.angle * 180 / math.pi#(self.angle + 360) % 360;
       
        
    def update(self, dt):
        
        if self.isAiControlled: 
            self.handleAi(dt)
            self.calcDirection()
        else:
            #use player input to set velocity and acceleration
            
            pass
        
        #print("acc: "+str(self.acceleration))
        #print("vel: "+str(self.velocity))
        #print("pos: "+str(self.position))
        self.calcAngle()
        self.move(dt)

       
    def calcDirection(self):
        
        tpos = Vector2(v=self.position)
        tmt = Vector2(v=self.MoveTarget)
        direction = tmt.sub(tpos)
        direction.nor()
        direction.scl(self.maxAcceleration)
        self.setAcceleration(direction)
    
    def handleAi(self, dt):
        pass
        #sets move target dynamicly