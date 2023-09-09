'''
Created on 17.02.2021

@author: MF
'''

from com.badlogic.gdx import Screen
from com.badlogic.gdx.graphics import OrthographicCamera, GL20
from com.badlogic.gdx import Gdx
from com.badlogic.gdx.graphics.g2d import SpriteBatch
from World import World
from com.badlogic.gdx.math import Rectangle
from Renderer import Renderer
from com.badlogic.gdx import InputProcessor, Input
from Vector import Vector2
from GameSettings import GameSettings
from Client import MentalClient


class GameScreen(Screen, InputProcessor):
    '''
    classdocs
    '''
    def __init__(self, ParentGame):
        self.camera = None
        self.batch = None
        self.pGame = ParentGame
        
        self.world = World()
        self.world.buildWorld()
        self.renderer = Renderer(self.pGame.am, self.world)
        self.mClient = MentalClient(self.world)
        
      
        self.mClient.connect("localhost", 31245)
        
        print("can't connect")
        self.world.addPlayer(0, self.world.people[0])
            #singleplayer
        
        
        
        Gdx.input.setInputProcessor(self)
        
       
        
        self.create()

    def show(self):
        pass
     
    def create(self):        
        self.camera = OrthographicCamera()
        self.camera.setToOrtho(False, Gdx.graphics.getWidth(), Gdx.graphics.getHeight())
        self.batch = SpriteBatch()
        
    
    def render(self):
        self.mClient.cPump()
        Gdx.gl.glClearColor(1,0,0.2,0)
        Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT)
        dt = Gdx.graphics.getDeltaTime()
        
        #self.camera.lookAt(100,100, 0)
        self.camera.update()
        self.batch.setProjectionMatrix(self.camera.combined)
        
        if(self.world.controlledCar != None):
            self.camera.position.x = self.world.controlledCar.position.x
            self.camera.position.y = self.world.controlledCar.position.y
            #else on foot
        else:
            self.camera.position.x = self.world.controlledPlayer.position.x
            self.camera.position.y = self.world.controlledPlayer.position.y
        #setViewRect
        view = Rectangle(self.camera.position.x, self.camera.position.y, self.camera.viewportWidth, self.camera.viewportHeight)
        view.x -= self.camera.viewportWidth/2
        view.y -= self.camera.viewportHeight/2
        
        #update
        self.handleInput(dt)
        self.world.update(dt, view)
        
        #draw
        self.batch.begin()
        self.renderer.render(dt,self.batch, self.camera)
        self.batch.end()
    
    def handleInput(self, dt):
        
            
        mvec =  Vector2(Gdx.input.getX(), Gdx.input.getY())
        mvec.y = Gdx.graphics.getHeight() - mvec.y  
            #print("Mouseat:"+ str(mvec))
        self.world.controlledPlayer.MoveTarget = mvec
        
        if self.world.controlledPlayer != None:
            tacc = Vector2(v=self.world.controlledPlayer.acceleration)
            if(Gdx.input.isKeyPressed(29)):
                self.world.controlledPlayer.setAcceleration(Vector2(-GameSettings.PeopleAcceleration,tacc.y))
            if(Gdx.input.isKeyPressed(47)):
                self.world.controlledPlayer.setAcceleration(Vector2(tacc.x,-GameSettings.PeopleAcceleration))
            if(Gdx.input.isKeyPressed(32)):
                self.world.controlledPlayer.setAcceleration(Vector2(GameSettings.PeopleAcceleration,tacc.y))
            if(Gdx.input.isKeyPressed(51)):
                self.world.controlledPlayer.setAcceleration(Vector2(tacc.x,GameSettings.PeopleAcceleration))        

        if self.world.controlledCar != None:
            if(Gdx.input.isKeyPressed(29)):
                self.world.controlledCar.steerLeft(dt)
            if(Gdx.input.isKeyPressed(47)):
                self.world.controlledCar.brake(dt)
            if(Gdx.input.isKeyPressed(32)):
                self.world.controlledCar.steerRight(dt)
            if(Gdx.input.isKeyPressed(51)):
                self.world.controlledCar.hitGas(dt)  
        
           
        pass
    
    def keyDown(self,keycode):
        #if self.world.controlledPlayer != None:
            #tacc = Vector2(self.world.controlledPlayer.acceleration)
            #if keycode == 29:
            #    self.world.controlledPlayer.setAcceleration(Vector2(-GameSettings.PeopleAcceleration,tacc.y))
            #if keycode == 47:
            #    self.world.controlledPlayer.setAcceleration(Vector2(tacc.x,-GameSettings.PeopleAcceleration))
            #if keycode == 32:
           #     self.world.controlledPlayer.setAcceleration(Vector2(GameSettings.PeopleAcceleration,tacc.y))
           # if keycode == 51:
            #    self.world.controlledPlayer.setAcceleration(Vector2(tacc.x,GameSettings.PeopleAcceleration))        
        pass
    
    def keyUp(self, keycode):
        if self.world.controlledPlayer != None:
            #29 = A
            #32 = D
            #47 = S
            #51 = W
            if keycode ==  29 or keycode == 32  or keycode == 47 or keycode == 51:
            #stop
                self.world.controlledPlayer.setAcceleration(Vector2())
                #self.world.controlledPlayer.stop()
                pass
            #try to enter car as driver
            if keycode == 34:
                #34  = F
                #enter next car
               
                if self.world.controlledPlayer.isInCar == None:
                    print("try to enter car")
                    self.world.tryToControlCar()
                else:
                    #get out
                    print("try to get out of car")
                    self.world.getPlayerOutOfDriverSeat()#
            
            if keycode == 35:
                if self.world.controlledPlayer.isInCar == None and self.world.controlledPlayer != None:
                    #enter car as passenger
                    self.world.tryToEnterCarAsPassenger(self.world.controlledPlayer)
                else:
                    self.world.controlledPlayer.isInCar.removePassenger(self.world.controlledPlayer)
                    
        
        if self.world.controlledCar != None:
            #29 = A
            #32 = D
            #47 = S
            #51 = W
            if keycode == 47 or keycode == 51:
            #stop
                self.world.controlledCar.setAcceleration(Vector2())
                #self.world.controlledPlayer.stop()
                pass
        pass
    
    def keyTyped(self, character):
        pass
    
    def mouseMoved(self, screenX, screenY):
        pass
    
    def scrolled(self, amountX, amountY):
        pass
    
    def touchDown(self, screenX, screenY, pointer, button):
        pass
    
    def touchDragged(self, screenX, screenY, pointer):
        pass
    
    def touchUp(self,  screenX, screenY, pointer, button):
        pass
        
       

        
    def resize(self, width, height):
        self.camera.setToOrtho(False, width,  height)

    def pause(self):
        pass

    def resume(self):
        pass
    
    def dispose(self):
        self.batch.dispose()