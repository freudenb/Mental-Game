'''
Created on 21.02.2021

@author: MF
'''

import socket
import urllib
import threading
from com.badlogic.gdx import Gdx, ApplicationListener
from com.badlogic.gdx.net import ServerSocketHints, ServerSocket, Socket, SocketHints
from com.badlogic.gdx.backends.lwjgl import LwjglApplication, LwjglApplicationConfiguration
from com.badlogic.gdx.backends.headless import HeadlessNet
from com.badlogic.gdx import ApplicationListener
from java.lang import Class
from java.io import BufferedReader
from java.io import InputStreamReader
#import com.badlogic.gdx.Net$Protocol
#from com.badlogic.gdx import Net$Protocol
from enum import Enum



class ServerConfig(object):
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
    

class MentalServer():
    '''
    classdocs
    '''


    def __init__(self, scfg):
        '''
        Constructor
        '''
        self.hostIP =  ""
        self.external_ip = ""
        self.sconfig = scfg
        
        
    def start(self):
        #self.localIP =  socket.gethostbyname(socket.gethostname())
        #self.externalIP = urllib.urlopen('https://ident.me').read().decode('utf8')
        t = threading.Thread(target=self.run)
        t.start()
        
        
    def startClient(self):
        
        socketHints = SocketHints()      
        socketHints.connectTimeout = 4000;
        socketHints.keepAlive = True
        p = Class.forName("com.badlogic.gdx.Net$Protocol").getEnumConstants()
        socket = Gdx.net.newClientSocket(p[0].TCP, "localhost", self.sconfig.port, socketHints)
        try:
            socket.getOutputStream().write(str.encode("gimp"))
        except Exception as e:
            print(e)
        
        socket.dispose()
    
    def run(self):
        print("running")
        serverSocketHint = ServerSocketHints()
        serverSocketHint.acceptTimeout = 0
        p = Class.forName("com.badlogic.gdx.Net$Protocol").getEnumConstants()
        serverSocket = Gdx.net.newServerSocket(p[0].TCP, self.sconfig.port, serverSocketHint)
        
        while True:
            socket = serverSocket.accept(None);
            buffer = BufferedReader(InputStreamReader(socket.getInputStream()))
                                
            try:
                print("recieved: "+buffer.readLine());    
            except Exception as e:
                print(e)
         
        socket.dispose()       

if __name__ == '__main__':
    
    cfg = LwjglApplicationConfiguration()
    cfg.title = "Mental Alpha Server";
    cfg.width = 100
    cfg.height = 100
    cfg.forceExit = False
    #cfg.fullscreen = True
    class dummy(ApplicationListener):
        
        def __init__(self):
            pass
        def create(self):
            pass
        def render(self):
            pass
        def resize(self, width, height):
            pass
        def pause(self):
            pass
        def dispose(self):
            pass
        
    #initialize gdx   
    LwjglApplication(dummy(), cfg)
    Gdx.app.exit()
    
    ms = MentalServer(ServerConfig("",6969))
    ms.start()
    ms.startClient()
    
    