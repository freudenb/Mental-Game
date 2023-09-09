'''
Created on 18.02.2021

@author: MF
'''
from com.badlogic.gdx.math import Rectangle



class Entity(object):
    '''
    classdocs
    '''
    nextID = 0

    def __init__(self, tID, position, width, height):
        '''
        Constructor
        '''
        #unique ID in whole Game
        self.oID = Entity.nextID
        Entity.nextID = Entity.nextID + 1
        #Texture ID
        self.tID = tID
        self.position = position
        self.width = width
        self.height = height
        #print(str(self.oID)+" "+ str(self.tID)+" "+str(self.position))
        
    def getBoundingBox(self):
        return Rectangle(self.position.x, self.position.y, self.width, self.height)
    
