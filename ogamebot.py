from ogame import OGame
from ogame.constants import Ships, Speed, Missions, Buildings, Research, Defense , Facilities
import time , math
import function_ogame
import random
import sys
from threading import Thread
from flask import Flask ,jsonify
from flask import render_template


print("welcome to ogamebot!!")
class Afficheur(Thread):
    
    """Thread chargé simplement d'afficher une lettre dans la console."""
    def __init__(self):
        Thread.__init__(self)
        self.isRunning = True
        self.ogame_infos = []
        self.id_pl = []

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        ogame = OGame('Aquarius', "nemesism@hotmail.fr", "pencilcho44")
        self.id_pl = ogame.get_planet_ids()
        print(self.id_pl)
        i = 0
        self.ogame_infos = [""]*len(self.id_pl)
        while True:
            id = self.id_pl[i]
            pl_info = ogame.get_planet_infos(id)
            print(pl_info['planet_name'])
            if self.isRunning:
                try:
                    og_info = { "id_planet":pl_info['planet_name'], "content": function_ogame.launch(ogame,id) }
                    self.ogame_infos[i] = og_info
                    print(self.ogame_infos)
                except RuntimeError:
                    print("RuntimeERror!!!!!!")
                    ogame = OGame('Aquarius', "nemesism@hotmail.fr", "pencilcho44")
                except ConnectionError:
                    print("ConnectionError!!!!!!")
                    ogame = OGame('Aquarius', "nemesism@hotmail.fr", "pencilcho44")
            i = i + 1            
            if i >= len(self.id_pl):
                i = 0
                time.sleep(1)

        print("end of thread!!")

    def StopRunning(self):
        self.isRunning = False