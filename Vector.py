'''
Created on 06.03.2021

@author: MF
'''
import math


class Vector2(object):
    '''
    classdocs
    '''


    def __init__(self, x = 0.0, y = 0.0, v = None):
        '''
        Constructor
        '''
        if v != None:
            self.x = v.x
            self.y = v.y
        else:
            self.x = x
            self.y = y
    
    
    def cpy(self):
        
        return Vector2(self.x, self.y)
    
    def len(self):
        
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def sub(self, v):
        
        self.x -= v.x
        self.y -= v.y
        return self
    
    def nor(self):
        vlen = self.len()
        if (vlen != 0):
            self.x /= vlen
            self.y /= vlen
        
        return self
    
    def add(self, v):
        
        self.x += v.x
        self.y += v.y
 
        return self
    
    
    def scl(self, s):
        
        self.x *=  s
        self.y *=  s
        
        return self
    
    def dst(self, v):
        x_d = v.x - self.x;
        y_d = v.y - self.y;
        return math.sqrt(x_d * x_d + y_d * y_d)
    
    def __str__(self):
        return self.x+":"+self.y