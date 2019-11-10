from ogame import OGame
from ogame.constants import Ships, Speed, Missions, Buildings, Research, Defense , Facilities
import time , math
from bs4 import BeautifulSoup

def gestionAttack(ogame,id,gal,sys):
    try:
        getMessage(ogame,id)
        getInactivePlanet(ogame,id,gal,sys)
    except:
        print("Flottes deja envoyé!!")

def getInactivePlanet(ogame,id,gal,sys):
    galaxy = ogame.galaxy_content(gal, sys)['galaxy']
    soup = BeautifulSoup(galaxy,'html.parser')
    listplanet = soup.find_all("tr",{"class":"row inactive_filter"})
    coord_inactive = {}
    for pl in listplanet:
        res = pl.find("td",{"class":"position js_no_action"})
        coord = {'galaxy':gal,'system':sys,'position':int(res.text)}
        sendSpy(ogame,id,coord)

def sendSpy(ogame,id_pl,coord):
    ships = [(Ships['EspionageProbe'],5)]
    speed = Speed['100%']
    mission = Missions['Spy']
    resources = { 'deuterium': 0}
    print(coord)
    ogame.send_fleet(id_pl, ships, speed, coord, mission, resources)

def attack(ogame,id,co,res):
    print(res)
    nb = round(res/25000)+1
    ships = [(Ships['LargeCargo'], nb)]
    speed = Speed['100%']
    where = {'galaxy':co[0],'system':co[1],'position':co[2]}
    mission = Missions['Attack']
    print(where)
    ogame.send_fleet(id, ships, speed, where, mission, {})        

def getMessage(ogame,id):
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
                resources  = resources + int(res.text.replace(".","").replace("Métal: ","").replace("Cristal: ","").replace("Deutérium: ",""))
            
            divlist = li.findAll("span",{"class":'msg_content'})
            for div in divlist:
                if "Flottes: 0" in div.text and "Défense: 0" in div.text:
                    print("ressources pillables!!")
                    attack(ogame,id,coord,resources)