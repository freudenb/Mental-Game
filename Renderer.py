'''
Created on 19.02.2021

@author: MF
'''


from com.badlogic.gdx.graphics.g2d import Sprite
from com.badlogic.gdx.math import MathUtils
from com.badlogic.gdx.graphics.glutils import ShapeRenderer#$ShapeType
from com.badlogic.gdx.graphics import Color
from java.lang import Class


class Renderer(object):
    '''
    classdocs
    '''

    def __init__(self, assetManager, world):
        
        '''
        Constructor
        '''
        
        self.am = assetManager
        self.world = world
        
        
    def render(self, dt, batch, camera):
        s = Sprite(self.am.getTexture(2))
        s.setPosition(0,0)
        s.draw(batch)
        
       
        
        for s in self.world.staticObjects:
            astaticObject = self.world.staticObjects[s]
            sprite = Sprite(self.am.getTexture(astaticObject.tID))
            sprite.setPosition( astaticObject.position.x,  astaticObject.position.y)
            sprite.draw(batch)
            
        
       
        for p in self.world.people:

            apeople = self.world.people[p]
            
            if apeople.isInCar == None:
                sprite = Sprite(self.am.getTexture(apeople.tID))
                sprite.setPosition(apeople.position.x, apeople.position.y)
                sprite.setRotation(apeople.angle)
                sprite.draw(batch)
            #apeople.position.x, apeople.position.y, apeople.width, apeople.height
            
        for c in self.world.cars:
            acar = self.world.cars[c]
            sprite = Sprite(self.am.getTexture(acar.tID))
            sprite.setPosition(acar.position.x, acar.position.y)
            sprite.setRotation(90 + acar.angle * MathUtils.radiansToDegrees)
            sprite.draw(batch);
            sprite = Sprite(self.am.getTexture(2))
            sprite.setPosition(acar.heading.x, acar.heading.y)
            sprite.draw(batch)
            r = acar.getDriverBoardArea()
            sprite.setPosition(r.x, r.y)
            sprite.draw(batch);
            r = acar.getPassengerBoardArea()
            sprite.setPosition(r.x, r.y)
            sprite.draw(batch);
            
        #sr = ShapeRenderer()
        #sr.setProjectionMatrix(camera.combined)
        #p = Class.forName("com.badlogic.gdx.graphics.glutils.ShapeRenderer$ShapeType").getEnumConstants()
        #sr.begin(p[2])
        #sr.setColor(Color(10,10,10,10))    
        #sr.rect(0,0,800,600)
        #sr.end()
     