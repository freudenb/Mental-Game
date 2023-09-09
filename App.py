'''
Created on 13.02.2021

@author: MF

'''
from com.badlogic.gdx.backends.lwjgl import LwjglApplication, LwjglApplicationConfiguration
from com.badlogic.gdx.utils import TimeUtils, Array
from com.badlogic.gdx.math import MathUtils, Rectangle, Vector3
from com.badlogic.gdx import ApplicationListener, Gdx, Input
from com.badlogic.gdx.graphics.g2d import SpriteBatch
from com.badlogic.gdx.graphics import Texture, OrthographicCamera, GL20
from com.badlogic.gdx import Game
from GameScreen import GameScreen
from AssetManager import AssetManager2
from GameSettings import GameSettings

class PyGdx(Game):
    def __init__(self):
        self.gs = None
        self.am = AssetManager2()
        
    def create(self):
        
        self.am.loadAll()
        GameSettings.loadTextureDimensions()
        self.gs = GameScreen(self)
        self.setScreen(self.gs)
    
    def render(self):
        self.getScreen().render()
        
    def resize(self, width, height):
        pass

    def pause(self):
        pass

    def resume(self):
        pass
    
    def dispose(self):
        self.am.dispose()
        pass


def main():

    cfg = LwjglApplicationConfiguration()
    cfg.title = "Mental Alpha";
    cfg.width = 1920
    cfg.height = 1080
    #cfg.fullscreen = True
    
    LwjglApplication(PyGdx(), cfg)


if __name__ == '__main__':
    print("Thats it yo")
    main()