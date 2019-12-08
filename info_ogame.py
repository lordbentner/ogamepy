from ogame import OGame
from ogame.constants import Ships, Speed, Missions, Buildings, Research, Defense , Facilities
import time , math, os, sys
from bs4 import BeautifulSoup
from datetime import datetime

class i_ogame():

    def __init__(self):
        self.infoLog = []

    def gestionAttack(self,ogame,id,gal,sys):
        #self.getDebris(ogame)
        if(self.getInactivePlanet(ogame,id,gal,sys) == True):
            self.getMessage(ogame,id)

    def getDebris(self,ogame):
        gal = 1
        sys = 1
        while(gal < 7):
            sys = 1
            while(sys < 500):
                galaxy = ogame.galaxy_content(gal, sys)['galaxy']
                soup = BeautifulSoup(galaxy,'html.parser')
                listdebris = soup.find_all("li",{"class":"debris-recyclers"})
                #listdebris = soup.find_all("tr")
                coord_debris = {}
                for debris in listdebris:
                    print(debris.replace("Recycleurs nécessaires: ",""))

                sys = sys+1
            gal = gal + 1

    def getInactivePlanet(self,ogame,id,gal,sys):
        galaxy = ogame.galaxy_content(gal, sys)['galaxy']
        soup = BeautifulSoup(galaxy,'html.parser')
        listplanet = soup.find_all("tr",{"class":"row inactive_filter"})
        coord_inactive = {}
        inactiv_detected = False
        for pl in listplanet:
            res = pl.find("td",{"class":"position js_no_action"})
            coord = {'galaxy':gal,'system':sys,'position':int(res.text)}
            self.sendSpy(ogame,id,coord)

            inactiv_detected = True
        
        return inactiv_detected

    def sendSpy(self,ogame,id_pl,coord):
        ships = [(Ships['EspionageProbe'],30)]
        speed = Speed['100%']
        mission = Missions['Spy']
        ogame.send_fleet(id_pl, ships, speed, coord, mission, {})

    def attack(self,ogame,id,co,res):
        nb = round(res/25000)+1
        ships = [(Ships['LargeCargo'], nb)]
        speed = Speed['100%']
        where = {'galaxy':co[0],'system':co[1],'position':co[2]}
        mission = Missions['Attack']
        ogame.send_fleet(id, ships, speed, where, mission, {})     

    def getMessage(self,ogame,id):
        messages = ogame.session.get(ogame.get_url('messages&tab=20&ajax=1')).content
        soup = BeautifulSoup(messages,'html.parser')
        lilist = soup.findAll("li",{"class":"msg"})
        for li in lilist:
            if "Rapport d" in li.text:
                span = li.find("span",{"msg_title blue_txt"})
                resources = 0
                coord = span.text.split('[')[1].replace(']','').split(':')
                reslist = li.findAll("span",{"class":"resspan"})
                for res in reslist:
                    print("ressources:"+str(res.text))
                    ress = str(res.text).replace("Métal: ","").replace("Cristal: ","").replace("Deutérium: ","")
                    if "," in ress:
                        print(ress)
                        resources = resources + 1000*int(ress.replace(",","").replace("M",""))
                    else:
                        resources  = resources + int(ress.replace(".",""))
                
                print(resources)
                if resources < 100000:
                    return
                divlist = li.findAll("span",{"class":'msg_content'})
                for div in divlist:
                    if "Flottes: 0" in div.text and "Défense: 0" in div.text:
                        try:
                            self.attack(ogame,id,coord,resources)
                        except Exception as ex:
                            print("getMessage:"+str(ex)) 
