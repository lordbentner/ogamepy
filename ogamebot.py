from ogame import OGame
from ogame.constants import Ships, Speed, Missions, Buildings, Research, Defense , Facilities
import time , math,function_ogame,random,sys,requests, info_ogame
from threading import Thread
from flask import Flask ,jsonify,render_template
from bs4 import BeautifulSoup

class Afficheur(Thread):   
    """Thread chargé simplement d'afficher une lettre dans la console."""
    def __init__(self):
        Thread.__init__(self)
        self.isRunning = True
        self.lvl_research = []
        self.isConnected = False
        self.ogame = OGame('Aquarius', "nemesism@hotmail.fr", "pencilcho44")
        self.id_pl = self.ogame.get_planet_ids()
        self.ogame_infos = [""]*len(self.id_pl)

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""      
        i = 0
        #function_ogame.getMessage(self.ogame)  
        while True:
            self.lvl_research = ["",""]         
            if  self.isRunning == True:
                try:
                    id = self.id_pl[i]
                    pl_info = self.ogame.get_planet_infos(id)
                    co = pl_info["coordinate"]
                    pos = str(co["galaxy"])+":"+str(co["system"])+":"+str(co["position"])
                    #info_ogame.getInactivePlanet(self.ogame,id,co["galaxy"],co["system"])
                    #info_ogame.getMessage(self.ogame,id)
                    print(pl_info['planet_name'])
                    og_info = { "id_planet":pl_info['planet_name'] ,"position": pos, "content": function_ogame.launch(self.ogame,id) }
                    self.ogame_infos[i] = og_info
                    global_res = self.ogame.get_resources(id)
                    if i!=0:
                        function_ogame.transporter(self.ogame,id,global_res['deuterium'],self.id_pl[0])
                    else:
                        self.lvl_research = function_ogame.setResearch(self.ogame,id)
                    
                    self.isConnected = True 
                except (RuntimeError,ConnectionError):
                    print("ExcpetERror!!!!!!")
                    self.isConnected = False
                    self.ogame.logout()

            if self.isConnected == False:
                self.ogame.login()
            i = i + 1            
            if i >= len(self.id_pl):
                i = 0

        print("end of thread!!")

    def StopRunning(self):
        self.ogame.logout()
        self.isRunning = False

    def StartRunning(self):
        self.ogame.login()
        self.isConnected = True
