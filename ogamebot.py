from ogame import OGame
from ogame.constants import Ships, Speed, Missions, Buildings, Research, Defense , Facilities
import time , math
import function_ogame


print("welcome to ogamebot!!")

def global_launch():
    try:
        ogame = OGame('Aquarius', "nemesism@hotmail.fr", "pencilcho44")
        id_pl = ogame.get_planet_ids()
        i = 0
        while 1:
            id = id_pl[i]
            print(id)
            function_ogame.launch(ogame,id)
            i = i + 1
            time.sleep(1)
            if i >= len(id_pl):
                i = 0
    except:
        global_launch()

#global_launch()
