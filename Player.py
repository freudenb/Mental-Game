'''
Created on 27.02.2021

@author: MF
'''


class Player(object):
    '''
    classdocs
    '''


    def __init__(self, pId):
        '''
        Constructor
        '''
        self.pID = pId
        self.controlledPeople = None
        self.controlledCar = None