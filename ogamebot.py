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

    def __init__(self):
        Thread.__init__(self)
        self.isRunning = True
        self.ogame_infos = []

    def join(self):
        Thread.join(self)

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        ogame = OGame('Aquarius', "nemesism@hotmail.fr", "pencilcho44")
        id_pl = ogame.get_planet_ids()
        print(id_pl)
        i = 0
        while self.isRunning:
            id = id_pl[i]
            print(id)
            self.ogame_infos = function_ogame.launch(ogame,id)
            print(self.ogame_infos)
            i = i + 1
            time.sleep(1)
            if i >= len(id_pl):
                i = 0

    def StopRunning(self):
        self.isRunning = False