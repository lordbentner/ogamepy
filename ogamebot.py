from ogame import OGame
from ogame.constants import Ships, Speed, Missions, Buildings, Research, Defense , Facilities
import time , math,function_ogame,random,sys,requests
from threading import Thread
from flask import Flask ,jsonify,render_template
from bs4 import BeautifulSoup
import requests

#1:30:10 to spy
print("welcome to ogamebot!!")
class Afficheur(Thread):   
    """Thread chargé simplement d'afficher une lettre dans la console."""
    def __init__(self):
        Thread.__init__(self)
        self.isRunning = True
        self.ogame_infos = []
        self.id_pl = []
        self.lvl_research = []
        self.isConnected = False

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        ogame = OGame('Aquarius', "nemesism@hotmail.fr", "pencilcho44")
        self.id_pl = ogame.get_planet_ids()
        self.ogame_infos = [""]*len(self.id_pl)      
        i = 0        
        while True:           
            if self.isRunning:
                try:
                    id = self.id_pl[i]
                    #<"index.php?page=messages&amp;tab=20&amp;ajax=1"
                    #fleetsgenericpage
                    #msg_content
                    url = "https://s153-fr.ogame.gameforge.com/game/index.php?page=messages"
                    pl_info = ogame.get_planet_infos(id)
                    print(pl_info['planet_name'])
                    res = ogame.get_research()
                    self.lvl_research = res.items()
                    """messages = requests.get(url).content
                    soup = BeautifulSoup(messages,'html.parser')
                    text = soup.div
                    print(text.get_text())
                    print(messages)"""
                    og_info = { "id_planet":pl_info['planet_name'], "content": function_ogame.launch(ogame,id) }
                    self.ogame_infos[i] = og_info
                    self.isConnected = True
                except RuntimeError:
                    print("RuntimeERror!!!!!!")
                    self.isConnected = False
                    ogame = OGame('Aquarius', "nemesism@hotmail.fr", "pencilcho44")
                except ConnectionError:
                    print("ConnectionError!!!!!!")
                    self.isConnected = False
                    ogame = OGame('Aquarius', "nemesism@hotmail.fr", "pencilcho44")
                #except:
                #    print("otherError")
                #    self.isConnected = False
            i = i + 1            
            if i >= len(self.id_pl):
                i = 0
                time.sleep(1)

        print("end of thread!!")

    def StopRunning(self):
        self.isRunning = False