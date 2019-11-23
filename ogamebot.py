from ogame import OGame
from ogame.constants import Ships, Speed, Missions, Buildings, Research, Defense , Facilities
import time , math,random,sys,requests, info_ogame, os, linecache, traceback
from function_ogame import f_ogame
from info_ogame import i_ogame
from threading import Thread
from flask import Flask ,jsonify,render_template
from bs4 import BeautifulSoup

class Afficheur(Thread):   
    """Thread chargé simplement d'afficher une lettre dans la console."""
    def __init__(self):
        Thread.__init__(self)
        self.isRunning = True
        self.lvl_research = ["",""]  
        self.isConnected = False
        self.fleets = []
        self.f_o = f_ogame()
        self.i_o = i_ogame()
        self.info_log = []
        self.infoLog2 = []

    def initOgame(self):
        try:
            self.ogame = OGame('Aquarius', "nemesism@hotmail.fr", "pencilcho44")
            self.id_pl = self.ogame.get_planet_ids()
            self.ogame_infos = [""]*len(self.id_pl)
            print("Connexion réussi")
        except:
            print("echec de connexion!re-tentative...")
            return self.initOgame()

    def loginOgame(self):
        try:
            if self.isConnected == False:
                self.ogame.login()
        except:
            self.ogame.logout()
            return self.loginOgame()

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        self.initOgame()      
        i = 0
        co_gal = 2
        co_sys = 1 
        while True:       
            if  self.isRunning == True:
                try:
                    self.id_pl = self.ogame.get_planet_ids()
                    id = self.id_pl[i]
                    pl_info = self.ogame.get_planet_infos(id)
                    co = pl_info["coordinate"]
                    pos = str(co["galaxy"])+":"+str(co["system"])+":"+str(co["position"])
                    co_sys = co_sys+1
                    if co_sys >= 500:
                        co_sys = 1
                        co_gal = co_gal+1
                    if co_gal >= 6:
                        co_gal = 1

                    print(pl_info['planet_name'])
                    content = self.f_o.launch(self.ogame,id)
                    self.fleets = self.f_o.fleets
                    global_res = self.ogame.get_resources(id)
                    og_info = { "id_planet":pl_info['planet_name'] ,"position": pos,
                    "resources":global_res.items(),
                     "content": content }
                    self.ogame_infos[i] = og_info
                    if i!=0:
                        self.f_o.transporter(self.ogame,id)
                    else:
                        self.lvl_research = self.f_o.setResearch(self.ogame,id)
                    
                    self.i_o.gestionAttack(self.ogame,id,co_gal,co_sys)
                    self.isConnected = True
                    self.info_log = self.f_o.info_log
                    self.infoLog2 = self.i_o.infoLog 
                except (RuntimeError,ConnectionError):
                    f_o.prints("ExcpetERror!!!!!!")
                    self.isConnected = False
                except Exception as ex:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    tb = traceback.extract_tb(exc_tb)[-1]
                    print(exc_type, tb[2], tb[1])
                    self.f_o.prints(str(ex))

            else:
                if self.isConnected == False:
                    try:
                        self.ogame.login()
                    except:
                        pass
            i = i + 1            
            if i >= len(self.id_pl):
                i = 0
                time.sleep(1)

    def StopRunning(self):
        self.f_o.prints("Arrêt du bot...")
        self.isRunning = False

    def StartRunning(self):
        self.f_o.prints("Démarrage du bot...")
        self.isRunning = True