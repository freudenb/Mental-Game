'''
Created on 18.02.2021

@author: MF
'''
from Entity import Entity
from Vector import Vector2


class MoveAbleEntity(Entity):
    '''
    classdocs
    '''


    def __init__(self, entity, maxVelocity, maxAcceleration, drag):
        '''
        Constructor
        '''
        
        #super(Entity,self).__init__(self ,entity.oID, entity.tID, entity.position, entity.width, entity.height)
        Entity.__init__(self, entity.tID, entity.position, entity.width, entity.height)

        self.maxVelocity = maxVelocity
        self.maxAcceleration = maxAcceleration
        self.velocity = Vector2()
        self.acceleration = Vector2()
        self.drag = drag
        
    def move(self, dt):
        
        tacc = Vector2(v=self.acceleration)
        tacc.scl(dt)
        tryvel = Vector2(v=self.velocity)
        tryvel.add(tacc)
        #print("tacc: "+str(tacc))
        
        if(tryvel.len() < self.maxVelocity):
            #if tryvel kleiner als maxvel -> set vel
            self.velocity = tryvel
            #if greater than max set to max
        else:
            tryvel.nor()
            tryvel.scl(self.maxVelocity)
            self.velocity = tryvel
        
        #tempvel mit delta time scalen and drag scale
        self.velocity.scl(self.drag)
        tvel = Vector2(v=self.velocity)
        tvel.scl(dt)
        #wenn vel zu klein nix mehr addieren -> stehen bleiben
        if(tvel.len() > 0.1):
            self.position.add(tvel)
       
       
    
    def accelerate(self, acceleration, dt):
        if(self.acceleration.len() < self.maxAcceleration):
            self.acceleration.add(acceleration.scl(dt))
            
            
    def setAcceleration(self, a):
        if(a.len() < self.maxAcceleration):
            self.acceleration = Vector2(v=a)
        else:#scale to max acc
            self.acceleration = Vector2(v=a.nor().scl(self.maxAcceleration))
      
    
    def stop(self):
        self.velocity = Vector2()
        self.acceleration = Vector2()