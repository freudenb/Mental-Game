'''
Created on 17.02.2021

@author: MF
'''
from com.badlogic.gdx.assets import AssetManager
from com.badlogic.gdx.graphics import Texture
from com.badlogic.gdx.audio import Sound
from Util import WidthHeight
import pickle

class AssetManager2(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.assets = AssetManager();
        self.Textures = dict()
        self.Sound = dict()
    
    def addAsset(self, Type, ID, Path):
        if Type == "Texture":
            self.Textures[ID] = Path
        elif Type == "Sound":
            self.Sound[ID] = Path
    
    def loadAll(self):

        self.setupLoadingList()
       
        #load all textures
        for t in self.Textures:
            self.assets.load(self.Textures[t], Texture)
        #load all sound   
        for s in self.Sound:
            self.assets.load(self.Sound[s], Sound)
            
        self.assets.finishLoading()
        print("loaded everything")
        self.saveTextureDimensionsToFile()
        
        
    def saveTextureDimensionsToFile(self):
        d = dict()
        for t in self.Textures:
            tex = self.getTexture(t)
            d[t] = WidthHeight(tex.width, tex.height)
        
        with open("dimensions.pkl", 'wb+') as f:
            pickle.dump(d, f, pickle.HIGHEST_PROTOCOL)
    
    def setupLoadingList(self):
        self.addAsset("Texture", 1, "assets/bg.png")
        self.addAsset("Texture", 2, "assets/cube.png")
        self.addAsset("Texture", 3, "assets/car1.png")
        self.addAsset("Texture", 4, "assets/house1.png")
        #self.addAsset("Sound", 1, "assets/sound1.ogg")
    
    def getTexture(self, ID):
        return self.assets.get(self.Textures[ID], Texture)
    
    def getSound(self, ID):
        return self.assets.get(self.Sound[ID], Sound)
    
    def dispose(self):
        self.assets.dispose()