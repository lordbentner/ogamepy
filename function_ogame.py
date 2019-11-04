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

def launch(ogame,id):
    isUnderAttack(ogame,id)
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
        #ogame.build(id, Buildings['SolarPlant'])
        satProduction(ogame,id,res_build['solar_plant'],global_res['energy'])          
    elif int(res_build['metal_mine']) < int(res_build['crystal_mine']) + 4:
        ogame.build(id,Buildings['MetalStorage'])
        ogame.build(id, Buildings['MetalMine'])
    elif int(res_build['crystal_mine']) < int(res_build['deuterium_synthesizer']) + 4:
        ogame.build(id,Buildings['CrystalStorage'])
        ogame.build(id, Buildings['CrystalMine'])
    else:
        ogame.build(id, Buildings['DeuteriumTank'])
        ogame.build(id, Buildings['DeuteriumSynthesizer'])
   
    if(lvl_facilities['shipyard'] < 7):
        ogame.build(id,Facilities['Shipyard'])

    setShips(ogame,id,lvl_rerearchs['combustion_drive'])
    try :
        setExpedition(ogame,id)
    except:
        print("expedition deja envoye!!")    
    #attack(ogame,id)
    time.sleep(1)
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
    if(lvl_res['combustion_drive'] < 8):
        ogame.build(id,Research['CombustionDrive'])

    res = lvl_res.items()
    newkey = []
    newvalues = []
    for key,value in res:
        newkey.append(key)
        newvalues.append(value)

    return newkey,newvalues

def setExpedition(ogame,id):
    pl_infos  = ogame.get_planet_infos(id)
    coord = pl_infos['coordinate']
    ships = [(Ships['LargeCargo'], 30) , (Ships['EspionageProbe'],5)]
    speed = Speed['100%']
    where = {'galaxy': coord['galaxy'], 'system': coord['system'], 'position': 16}
    mission = Missions['Expedition']
    resources = { 'deuterium': 0}
    ogame.send_fleet(id, ships, speed, where, mission, resources)

def isUnderAttack(ogame,id):
    i=408
    if ogame.is_under_attack():
        while i>400:
            print("builded!!!!!")
            ogame.build_defense(id,i,100)
            i = i - 1

def getMessage(ogame):
    messages = ogame.session.get(ogame.get_url('messages')).text
    soup = BeautifulSoup(messages,'lxml')
    spanlist = soup.findAll("span")
    head = soup.find("div",class_="msg_head")
    print(head)
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

    return (isflnull and isdefnull)

def attack(ogame,id):
    isgood = getMessage(ogame)
    if(isgood):
        i = 0

#[1:30:6]