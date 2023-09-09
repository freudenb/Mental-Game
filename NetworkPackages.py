'''
Created on 25.02.2021

@author: MF
'''


class WorldUpdatePackage(object):
    '''
    classdocs
    '''


    def __init__(self, players, cars, people, bullets):
        '''
        Constructor
        '''
        self.players = players
        self.cars = cars
        self.people = people
        self.bullets = bullets
        
        
class TextMessagePackage(object):
    
    def __init__(self, t):
        self.text = t