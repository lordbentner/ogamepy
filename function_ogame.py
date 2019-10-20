from ogame import OGame
from ogame.constants import Ships, Speed, Missions, Buildings, Research, Defense , Facilities
import time , math


def launch(ogame,id):
    global_res = ogame.get_resources(id)
    res_build = ogame.get_resources_buildings(id)
    lvl_rerearchs = ogame.get_research()
    lvl_facilities = ogame.get_facilities(id)
    ogame.build(id, Research['Astrophysics'])
    ogame.build(id,Facilities['RoboticsFactory'])
    if(global_res['energy'] < 0):
        ogame.build(id, Buildings['SolarPlant'])
    elif int(res_build['metal_mine']) < int(res_build['crystal_mine']) + 4:
        ogame.build(id,Buildings['MetalStorage'])
        ogame.build(id, Buildings['MetalMine'])
        print("buildings metal mine...")
    elif int(res_build['crystal_mine']) < int(res_build['deuterium_synthesizer']) + 4:
        ogame.build(id,Buildings['CrystalStorage'])
        ogame.build(id, Buildings['CrystalMine'])
    else:
        ogame.build(id, Buildings['DeuteriumTank'])
        ogame.build(id, Buildings['DeuteriumSynthesizer'])

    array_infos = [ res_build, lvl_rerearchs, lvl_facilities ]
    time.sleep(1)
    return array_infos