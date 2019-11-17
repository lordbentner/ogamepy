from ogame import OGame
from ogame.constants import Ships, Speed, Missions, Buildings, Research, Defense , Facilities
import time , math
from bs4 import BeautifulSoup
from datetime import datetime

class f_ogame():

    def __init__(self):
        self.info_log = [""]
        self.coord_plMere = {'galaxy':1,'system':30,'position':6 }

    def launch(self,ogame,id):
        self.fleets = ogame.get_fleets()
        self.id_pl = ogame.get_planet_ids()
        self.planet_infos = ogame.get_planet_infos(id)
        self.inbuild = self.getInConstruction(ogame,id)
        self.g_res = ogame.get_resources(id)
        self.res_build = ogame.get_resources_buildings(id)
        self.research = ogame.get_research()
        self.facilities = ogame.get_facilities(id)
        self.ships = ogame.get_ships(id)
        self.isUnderAttack(ogame,id)
        array_infos = [ self.res_build.items(), self.facilities.items(), self.ships.items(), self.inbuild.items() ]  
        ogame.build(id, Research['Astrophysics'])
        self.globalbuild(ogame,id)
        self.setShips(ogame,id)
        try :
            self.setExpedition(ogame,id)
        except:
            self.prints("expedition deja envoye")    

        return array_infos

    def prints(self,text):
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        self.info_log.append(dt_string+": "+text)

    def satProduction(self,ogame,id):
        tmax = self.planet_infos['temperature']['max']
        tmin = self.planet_infos['temperature']['min']
        prodsat = (tmax/4) + 20
        prodcen = 20*self.res_build['solar_plant']*math.pow(1.1,self.res_build['solar_plant'])
        nbsat = self.g_res['energy']/prodsat
        coutcen = 30*math.pow(1.5,self.res_build['solar_plant']-1)
        if(nbsat*2000 < coutcen):
            self.prints("build sat")
            ogame.build_ships(id,Ships['SolarSatellite'],1)
        else:
            self.prints("building centrale")
            ogame.build(id,Buildings['SolarPlant'])

    def setShips(self,ogame,id):
        probe = self.ships['espionage_probe']
        if(probe < 1):
            ogame.build_ships(id,Ships['EspionageProbe'],1)

        if(self.ships['large_cargo'] < 1):
            ogame.build_ships(id,Ships['Grandtransporteur'],1)

    def globalbuild(self,ogame,id):
        if(int(self.facilities['robotics_factory']) < 10):
            ogame.build(id,Facilities['RoboticsFactory'])
        else:
            ogame.build(id,Facilities['NaniteFactory'])
            ogame.build(id,Facilities['Terraformer'])
            if(self.facilities['missile_silo'] <4):
                ogame.build(id,Facilities['MissileSilo'])
                ogame.build_defense(id,Defense['AntiBallisticMissiles'],1)
        if(self.g_res['energy'] < 0):
            ogame.build(id, Buildings['SolarPlant'])
            self.satProduction(ogame,id)          
        elif int(self.res_build['metal_mine']) < int(self.res_build['crystal_mine']) + 4:
            ogame.build(id,Buildings['MetalStorage'])
            ogame.build(id, Buildings['MetalMine'])
        elif int(self.res_build['crystal_mine']) < int(self.res_build['deuterium_synthesizer']) + 4:
            ogame.build(id,Buildings['CrystalStorage'])
            ogame.build(id, Buildings['CrystalMine'])
        else:
            ogame.build(id, Buildings['DeuteriumTank'])
            ogame.build(id, Buildings['DeuteriumSynthesizer'])
    
        if(self.facilities['shipyard'] < 8):
            ogame.build(id,Facilities['Shipyard'])

    def transporter(self,ogame,id):
        try:
            if(self.g_res['deuterium'] > 400000):
                ships = [(Ships['LargeCargo'], 5)]
                speed = Speed['100%']
                where = {'galaxy': 1, 'system': 30, 'position': 6}
                mission = Missions['Transport']
                resources = { 'deuterium': 100000}
                ogame.send_fleet(id, ships, speed, where, mission, resources)
        except:
            self.prints("transport deja envoyé!")

    def setResearch(self,ogame,id):
        if(self.facilities['research_lab'] < 9):
            ogame.build(id,Facilities['ResearchLab'])
        ogame.build(id, Research['Astrophysics'])
        if(self.research['energy_technology'] < 12):
            ogame.build(id,Research['EnergyTechnology'])
        if(self.research['laser_technology'] < 10):
            ogame.build(id,Research['LaserTechnology'])
        if(self.research['ion_technology'] < 5):
            ogame.build(id,Research['IonTechnology'])
        if(self.research['plasma_technology'] < 7):
            ogame.build(id,Research['PlasmaTechnology'])
        if(self.research['weapons_technology'] < 3):
            ogame.build(id,Research['WeaponsTechnology'])
        if(self.research['shielding_technology'] < 6):
            ogame.build(id,Research['ShieldingTechnology'])

        ogame.build(id,Research['EspionageTechnology'])
        ogame.build(id,Research['ArmourTechnology'])
        ogame.build(id,Research['CombustionDrive'])
        res = self.research.items()
        newkey = []
        newvalues = []
        for key,value in res:
            newkey.append(key)
            newvalues.append(value)

        return newkey,newvalues

    def setExpedition(self,ogame,id):
        sh = ogame.get_ships(id)
        pl_infos  = ogame.get_planet_infos(id)
        coord = pl_infos['coordinate']
        ships = [(203, 30) , (210,5) ,(202,sh['small_cargo ']), (204,sh['light_fighter']),(205,sh['heavy_fighter']),
        (206,sh['cruiser']),(207,sh['battleship']),(213,sh['destroyer'])]
        speed = Speed['100%']
        where = {'galaxy': coord['galaxy'], 'system': coord['system'], 'position': 16}
        mission = Missions['Expedition']
        ogame.send_fleet(id, ships, speed, where, mission, {})

    def getInConstruction(self,ogame,id):
        incons = ogame.constructions_being_built(id)
        res = {}
        i=1
        for con in incons: 
            inbuild =  self.get_code(con)
            if not inbuild == None:
                keyz = str(i)+'-'
                res[keyz] = inbuild
                i=i+1

        return res
       
    def isUnderAttack(self,ogame,id):
        i=408
        if not ogame.is_under_attack():
            return

        ships = [(Ships['LargeCargo'], self.ships['large_cargo'])]
        speed = Speed['100%']
        where = self.coord_plMere
        idpl = id
        if id == self.planet_infos[0]:
            where = {'galaxy':1,'system':150,'position':7}

        mission = Missions['Transport']
        resources = { 'deuterium': self.g_res['deuterium']}
        ogame.send_fleet(idpl, ships, speed, where, mission, resources)
        while i>400:
            self.prints("builded!!!!!")
            ogame.build_defense(id,i,self.g_res['metal'])
            i = i - 1

    def get_code(self,name):
        array = {}
        if int(name) in Buildings.values():       
            array = Buildings
        if int(name) in Facilities.values():
            array = Facilities
        if int(name) in Defense.values():
            array = Defense
        if int(name) in Ships.values():
            array = Ships
        if int(name) in Research.values():
            array = Research

        for key,value in array.items():
            if value == int(name):
                return key

        return None
