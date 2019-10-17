from ogame import OGame
from ogame.constants import Ships, Speed, Missions, Buildings, Research, Defense
import time , math


def isPayable(i_metal, i_cristal,i_deut,i_lvl,i_coeff, array_res):
	prixmetal = i_metal*math.pow(i_coeff,i_lvl)
	prixcrystal = i_cristal*math.pow(i_coeff,i_lvl)
	prixdeut = i_deut*math.pow(i_coeff,i_lvl)
	return (prixmetal <= int(array_res['metal']) and prixcrystal <= int(array_res['crystal']) and prixdeut <= int(array_res['deuterium']))
  

print("welcome")
ogame = OGame('Aquarius', "nemesism@hotmail.fr", "pencilcho44")

id: int
id = 34374636
while 1:
    global_res = ogame.get_resources(34374636)
    res_build = ogame.get_resources_buildings(34374636)
    print(global_res)
    print(ogame.get_resources_buildings(34374636))

    if(global_res['energy'] < 0):
        if isPayable(75, 15, 0, int(res_build['solar_plant']), 1.5,global_res) == True:
            ogame.build(id, Buildings['SolarPlant'])

    elif int(res_build['metal_mine']) < int(res_build['crystal_mine']) + 4:
    #elif int(res_build['metal_mine']) < (int(res_build['metal_mine']) + 4) and isPayable(60, 15, 0, int(res_build['metal_mine']), 1.5,global_res) == True:
        ogame.build(id, Buildings['MetalMine'])
        print("buildings...")
    elif

    time.sleep(1)
