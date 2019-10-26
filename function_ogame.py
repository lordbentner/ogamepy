from ogame import OGame
from ogame.constants import Ships, Speed, Missions, Buildings, Research, Defense , Facilities
import time , math

def satProduction(ogame,id,lvl_centrale,energy):
    planet_infos = ogame.get_planet_infos(id)
    tmax = planet_infos['temperature']['max']
    tmin = planet_infos['temperature']['min']
    prodsat = (tmax/4) + 20
    prodcen = 20*lvl_centrale*math.pow(1.1,lvl_centrale)
    nbsat = energy/prodsat
    coutcen = 30*math.pow(1.5,lvl_centrale-1)
    if(nbsat*2000 < coutcen):
        ogame.build_ships(id,Ships['SolarSatellite'],str(1))
    else:
        ogame.build(id,Buildings['SolarPlant'])

def setShips(ogame,id,lvl_combustion):
    ships = ogame.get_ships(id)
    probe = ships['espionage_probe']
    if(lvl_combustion < 6):
        ogame.build(id,Research['CombustionDrive'])
    if(probe < 6):
        ogame.build_ships(id,Ships['EspionageProbe'],1)

    if(ships['large_cargo'] < 5):
        ogame.build_ships(id,Ships['Grandtransporteur'],1)

def launch(ogame,id):
    global_res = ogame.get_resources(id)
    res_build = ogame.get_resources_buildings(id)
    lvl_rerearchs = ogame.get_research()
    lvl_facilities = ogame.get_facilities(id)
    ships = ogame.get_ships(id)
    array_infos = [ res_build,  lvl_facilities, ships ]
    #print(ogame.fetch_resources(id))   
    ogame.build(id, Research['Astrophysics'])
    if(int(lvl_facilities['robotics_factory']) < 10):
        ogame.build(id,Facilities['RoboticsFactory'])
    if(global_res['energy'] < 0):
        ogame.build(id, Buildings['SolarPlant'])
        #satProduction(ogame,id,res_build['solar_plant'],global_res['energy'])          
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
   
    if(lvl_facilities['shipyard'] < 7):
        ogame.build(id,Facilities['Shipyard'])

    setShips(ogame,id,lvl_rerearchs['combustion_drive'])

    time.sleep(1)
    return array_infos