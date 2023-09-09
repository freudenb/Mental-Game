'''
Created on 19.02.2021

@author: MF
'''

import pickle

class GameSettings(object):
    '''
    classdocs
    '''
    PeopleMaxVelocity = 200
    PeopleMaxAcceleration = 3000
    PeopleAcceleration = 2000
    PeopleDrag = 1-0.05
    CarDrag = 1-0.05
    lowestVelocityLenght = 40
    TextureDimensions = dict()
    

    def __init__(self, params):
        '''
        Constructor
        '''
    
    @staticmethod
    def loadTextureDimensions():
        with open("dimensions.pkl", 'rb') as f:
            GameSettings.TextureDimensions = pickle.load(f)  