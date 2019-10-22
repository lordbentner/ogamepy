from ogame import OGame
from ogame.constants import Ships, Speed, Missions, Buildings, Research, Defense , Facilities
import time , math
import function_ogame
import random
import sys
from threading import Thread


print("welcome to ogamebot!!")
class Afficheur(Thread):
    
    """Thread chargé simplement d'afficher une lettre dans la console."""

    ogame_infos = []
    isRunning = True

    def __init__(self):
        Thread.__init__(self)

    def join(self):
        self.isRunning = False
        Thread.join(self)

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        ogame = OGame('Aquarius', "nemesism@hotmail.fr", "pencilcho44")
        id_pl = ogame.get_planet_ids()
        print(id_pl)
        i = 0
        while 1:
            id = id_pl[i]
            print(id)
            ogame_infos = function_ogame.launch(ogame,id)
            print(ogame_infos)
            i = i + 1
            time.sleep(1)
            if i >= len(id_pl):
                i = 0
            if self.isRunning == False:
                break;

    def StopRunning(self):
        self.isRunning = False