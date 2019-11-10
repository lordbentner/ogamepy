from ogame import OGame
from ogame.constants import Ships, Speed, Missions, Buildings, Research, Defense , Facilities
import time , math
from bs4 import BeautifulSoup

def satProduction(ogame,id,lvl_centrale,energy):
    planet_infos = ogame.get_planet_infos(id)
    tmax = planet_infos['temperature']['max']
    tmin = planet_infos['temperature']['min']
    prodsat = (tmax/4) + 20
    prodcen = 20*lvl_centrale*math.pow(1.1,lvl_centrale)
    nbsat = energy/prodsat
    coutcen = 30*math.pow(1.5,lvl_centrale-1)
    if(nbsat*2000 < coutcen):
        print("build sat")
        ogame.build_ships(id,Ships['SolarSatellite'],1)

    else:
        print("building centrale")
        ogame.build(id,Buildings['SolarPlant'])

def setShips(ogame,id,lvl_combustion):
    ships = ogame.get_ships(id)
    probe = ships['espionage_probe']
    if(probe < 6):
        ogame.build_ships(id,Ships['EspionageProbe'],1)

    if(ships['large_cargo'] < 30):
        ogame.build_ships(id,Ships['Grandtransporteur'],1)

def globalbuild(ogame,id,fac,rbuild,g_res):
    if(int(fac['robotics_factory']) < 10):
        ogame.build(id,Facilities['RoboticsFactory'])
    else:
        ogame.build(id,Facilities['NaniteFactory'])
        ogame.build(id,Facilities['Terraformer'])
        if(fac['missile_silo'] <4):
            ogame.build(id,Facilities['MissileSilo'])
            ogame.build_defense(id,Defense['AntiBallisticMissiles'],1)
    if(g_res['energy'] < 0):
        ogame.build(id, Buildings['SolarPlant'])
        satProduction(ogame,id,rbuild['solar_plant'],g_res['energy'])          
    elif int(rbuild['metal_mine']) < int(rbuild['crystal_mine']) + 4:
        ogame.build(id,Buildings['MetalStorage'])
        ogame.build(id, Buildings['MetalMine'])
    elif int(rbuild['crystal_mine']) < int(rbuild['deuterium_synthesizer']) + 4:
        ogame.build(id,Buildings['CrystalStorage'])
        ogame.build(id, Buildings['CrystalMine'])
    else:
        ogame.build(id, Buildings['DeuteriumTank'])
        ogame.build(id, Buildings['DeuteriumSynthesizer'])
   
    if(fac['shipyard'] < 8):
        ogame.build(id,Facilities['Shipyard'])

def launch(ogame,id):
    isUnderAttack(ogame,id)
    global_res = ogame.get_resources(id)
    res_build = ogame.get_resources_buildings(id)
    lvl_rerearchs = ogame.get_research()
    lvl_facilities = ogame.get_facilities(id)
    ships = ogame.get_ships(id)
    array_infos = [ res_build,  lvl_facilities, ships ]  
    ogame.build(id, Research['Astrophysics'])
    globalbuild(ogame,id,lvl_facilities,res_build,global_res)
    setShips(ogame,id,lvl_rerearchs['combustion_drive'])
    try :
        setExpedition(ogame,id)
    except:
        print("expedition deja envoye!!")    
    #attack(ogame,id)
    return array_infos

def transporter(ogame,id,res,planet_mere):
    if(res > 400000):
        ships = [(Ships['LargeCargo'], 5)]
        speed = Speed['100%']
        where = {'galaxy': 1, 'system': 30, 'position': 6}
        mission = Missions['Transport']
        resources = { 'deuterium': 100000}
        ogame.send_fleet(id, ships, speed, where, mission, resources)
    print(res)

def setResearch(ogame,id):
    lvl_res = ogame.get_research()
    ogame.build(id, Research['Astrophysics'])
    if(lvl_res['energy_technology'] < 12):
        ogame.build(id,Research['EnergyTechnology'])
    if(lvl_res['laser_technology'] < 10):
        ogame.build(id,Research['LaserTechnology'])
    if(lvl_res['ion_technology'] < 5):
        ogame.build(id,Research['IonTechnology'])
    if(lvl_res['plasma_technology'] < 7):
        ogame.build(id,Research['PlasmaTechnology'])
    if(lvl_res['weapons_technology'] < 3):
        ogame.build(id,Research['WeaponsTechnology'])
    if(lvl_res['shielding_technology'] < 1):
        ogame.build(id,Research['ShieldingTechnology'])

    ogame.build(id,Research['EspionageTechnology'])
    ogame.build(id,Research['ArmourTechnology'])
    ogame.build(id,Research['CombustionDrive'])
    res = lvl_res.items()
    newkey = []
    newvalues = []
    for key,value in res:
        newkey.append(key)
        newvalues.append(value)

    return newkey,newvalues

def setExpedition(ogame,id):
    sh = ogame.get_ships(id)
    pl_infos  = ogame.get_planet_infos(id)
    coord = pl_infos['coordinate']
    ships = [(203, 30) , (210,5) , (204,sh['light_fighter']),(205,sh['heavy_fighter']),
    (206,sh['cruiser']),(207,sh['battleship']),(213,sh['destroyer'])]
    speed = Speed['100%']
    where = {'galaxy': coord['galaxy'], 'system': coord['system'], 'position': 16}
    mission = Missions['Expedition']
    ogame.send_fleet(id, ships, speed, where, mission, {})

def isUnderAttack(ogame,id):
    i=408
    if ogame.is_under_attack():
        while i>400:
            print("builded!!!!!")
            ogame.build_defense(id,i,100)
            i = i - 1



#[1:30:6]