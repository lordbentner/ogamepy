from ogame import OGame
from ogame.constants import Ships, Speed, Missions, Buildings, Research, Defense , Facilities
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
    lvl_rerearchs = ogame.get_research()
    lvl_facilities = ogame.get_facilities(id)
    print(global_res)
    print(ogame.get_resources_buildings(34374636))
    print(lvl_facilities)
    print(lvl_rerearchs)

    ogame.build(id,Facilities['RoboticsFactory'])
    if(global_res['energy'] < 0):
        if isPayable(75, 15, 0, int(res_build['solar_plant']), 1.5,global_res) == True:
            ogame.build(id, Buildings['SolarPlant'])

    elif int(res_build['metal_mine']) < int(res_build['crystal_mine']) + 4:
        ogame.build(id, Buildings['MetalMine'])
        ogame.build(id,Buildings['MetalStorage'])
        print("buildings metal mine...")
    elif int(res_build['crystal_mine']) < int(res_build['deuterium_synthesizer']) + 4:
        ogame.build(id, Buildings['CrystalMine'])
        ogame.build(id,Buildings['CrystalStorage'])
    else:
        ogame.build(id, Buildings['DeuteriumSynthesizer'])
        ogame.build(id, Buildings['DeuteriumTank'])

    if(int(lvl_facilities['research_lab']) < 4):
        ogame.build(id,Facilities['ResearchLab'])

    ogame.build(id, Research['Astrophysics'])

    if(int(lvl_rerearchs['energy_technology']) < 2):
        ogame.build(id,Research['EnergyTechnology'])
    elif((int(lvl_rerearchs['impulse_drive'])) < 3):
        ogame.build(id, Research['ImpulseDrive'])
    elif(int(lvl_rerearchs['espionage_technology']) < 5):
        ogame.build(id,Research['EspionageTechnology'])    

    time.sleep(1)


