from ogame import OGame
from ogame.constants import Ships, Speed, Missions, Buildings, Research, Defense , Facilities
import time , math
from bs4 import BeautifulSoup
from datetime import datetime , timedelta

class f_ogame():

    def __init__(self):
        self.info_log = [""]
        self.coord_plMere = {'galaxy':1,'system':30,'position':6 }

    def launch(self,ogame,id):
        self.id_pl = ogame.get_planet_ids()
        self.fleets = ogame.get_fleets()
        self.planet_infos = ogame.get_planet_infos(id)
        self.inbuild = self.getInConstruction(ogame,id)
        self.g_res = ogame.get_resources(id)
        self.res_build = ogame.get_resources_buildings(id)
        self.research = ogame.get_research()
        self.facilities = ogame.get_facilities(id)
        self.ships = ogame.get_ships(id)
        try:
            self.isUnderAttack(ogame,id)
        except Exception as ex:
            self.prints("Erreur sur la gestion défense!!")
        array_infos = [ self.res_build.items(), self.facilities.items(), self.ships.items(),
         self.inbuild.items() ]  
        ogame.build(id, Research['Astrophysics'])
        self.globalbuild(ogame,id)
        self.setShips(ogame,id)
        try :
            self.setExpedition(ogame,id)
        except Exception as ex:
            print("expedition erreur:"+str(ex))    

        return array_infos

    def prints(self,text):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        self.info_log.append(dt_string+": "+str(text))
        
    def satProduction(self,ogame,id):
        tmax = self.planet_infos['temperature']['max']
        tmin = self.planet_infos['temperature']['min']
        prodsat = (tmax/4) + 20
        prodcen = 20*self.res_build['solar_plant']*math.pow(1.1,self.res_build['solar_plant'])
        nbsat = self.g_res['energy']/prodsat
        coutcen = 30*math.pow(1.5,self.res_build['solar_plant']-1)
        if(nbsat*2000 < coutcen):
            self.prints("build satellite...")
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

        if(self.facilities['space_dock'] < 7):
            ogame.build(id,Facilities['SpaceDock'])

    def transporter(self,ogame,id):
        try:
            if(self.g_res['deuterium'] > (100000*self.facilities['terraformer'])+100000):
                ships = [(Ships['LargeCargo'], 5)]
                speed = Speed['100%']
                where = {'galaxy': 1, 'system': 30, 'position': 6}
                mission = Missions['Transport']
                resources = { 'deuterium': 100000}
                ogame.send_fleet(id, ships, speed, where, mission, resources)
                self.prints("transport de ressources vers stade de france")
        except:
            pass

    def setResearch(self,ogame,id):
        if(self.facilities['research_lab'] < 9):
            ogame.build(id,Facilities['ResearchLab'])
        ogame.build(id, Research['Astrophysics'])
        if(self.research['energy_technology'] < 12):
            ogame.build(id,Research['EnergyTechnology'])
        if(self.research['weapons_technology'] < 3):
            ogame.build(id,Research['WeaponsTechnology'])
        if(self.research['shielding_technology'] < 6):
            ogame.build(id,Research['ShieldingTechnology'])

        ogame.build(id,Research['EspionageTechnology'])
        ogame.build(id,Research['ArmourTechnology'])
        ogame.build(id,Research['CombustionDrive'])
        ogame.build(id,Research['IntergalacticResearchNetwork'])
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
        ships = [(203, 30) , (210,5) ,(202,sh['small_cargo']), (204,sh['light_fighter']),(205,sh['heavy_fighter']),
        (206,sh['cruiser']),(207,sh['battleship']),(213,sh['destroyer'])]
        speed = Speed['100%']
        where = {'galaxy': coord['galaxy'], 'system': coord['system'], 'position': 16}
        mission = Missions['Expedition']
        ogame.send_fleet(id, ships, speed, where, mission, {})

    def getInConstruction(self,ogame,id):
        incons = ogame.constructions_being_built(id)
        res = {}
        i=1
        """for con in incons: 
            inbuild =  self.get_code(con)
            if not inbuild == None:
                keyz = str(i)+'-'
                res[keyz] = inbuild
                i=i+1
        """


        print(incons[3])
        if incons[0] > 0:
            time = str(timedelta(seconds=int(incons[1])))
            res["1-"] = self.get_code(incons[0])+"("+time+")"

        time2 = str(timedelta(seconds=int(incons[3])))
        res["2-"] = self.get_code(incons[2])+"("+time2+")"
        return res
       
    def isUnderAttack(self,ogame,id):
        i=408
        if not ogame.is_under_attack():
            return

        self.prints("attaque imminent!!")
        while i>400:
            self.prints("builded!!!!!")
            ogame.build_defense(id,i,self.g_res['metal'])
            i = i - 1
        ships = [(Ships['LargeCargo'], self.ships['large_cargo']),(Ships['SmallCargo'], self.ships['small_cargo'])]
        speed = Speed['100%']
        where = self.coord_plMere
        idpl = id
        if id == self.id_pl[0]:
            where = {'galaxy':1,'system':150,'position':7}

        mission = Missions['Transport']
        resources = { 'deuterium': self.g_res['deuterium']}
        ogame.send_fleet(idpl, ships, speed, where, mission, resources)

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

    def getMission(self,name):
        for key,value in Missions.items():
            if value == int(name):
                return key

        return None
