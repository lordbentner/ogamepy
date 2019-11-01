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
    ogame.build(id, Research['Astrophysics'])
    if(int(lvl_facilities['robotics_factory']) < 10):
        ogame.build(id,Facilities['RoboticsFactory'])
    else:
        ogame.build(id,Facilities['NaniteFactory'])
        ogame.build(id,Facilities['Terraformer'])
        if(lvl_facilities['missile_silo'] <4):
            ogame.build(id,Facilities['MissileSilo'])
            ogame.build_defense(id,Defense['AntiBallisticMissiles'],1)
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

def getMessage(ogame):
    messages = ogame.session.get(ogame.get_url('messages')).content
    soup = BeautifulSoup(messages,'html.parser')
    spanlist = soup.findAll("span")
    i = 0
    isflnull = False
    isdefnull = False
    while i<len(spanlist):
        if "Flottes" in spanlist[i]:
            if(spanlist[i+1].text) == "0":
                isflnull = True
        if "Defense" in spanlist[i]:
            if(spanlist[i+1].text) == "0":
                isdefnull = True
        i=i+1

def transporter(ogame,id,res,planet_mere):
    if(res > 400000):
        ships = [(Ships['LargeCargo'], 10)]
        speed = Speed['100%']
        where = {'galaxy': 1, 'system': 30, 'position': 6}
        mission = Missions['Transport']
        resources = { 'deuterium': res/2}
        ogame.send_fleet(planet_mere, ships, speed, where, mission, resources)
    print(res)

#[1:30:6]