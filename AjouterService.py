#on importe les librairies dont nous avons besoins
import gi
import sqlite3
import Alerte
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class AjoutService:
    #ligne de code qui se lance lorsque de l'initialisation
    def __init__(self):
        #on creer la fenetre à partir de l'interface glade
        builder = Gtk.Builder()
        builder.add_from_file('AjouterService.glade')
        self.window = builder.get_object('Main_Windows')
        #on creer des objetrs pour chaqu'une des interractions
        self.TypeService = builder.get_object("TypeService")
        self.NomService = builder.get_object("NomService")
        self.NumeroService = builder.get_object("NumeroService")
        #on creer les interractions entre les fonction definit dans la class et le nom mit dans glade
        builder.connect_signals(self)

    def ajouterService(self):
        # permet d'ajouter le service à la base
        #on recreer les variable pour plus de faciliter le lacture du code
        TypeService = str(self.TypeService.get_active_text())
        NomService =  str(self.NomService.get_text())
        NumeroService = str(self.NumeroService.get_text())


        # on creer une connexion avec la base de donnée , puis on execute la requete SQL avec les information précédent
        conn2 = sqlite3.connect('déclaration.db')
        cursor2 = conn2.cursor()
        cursor2.execute("""INSERT INTO Service(NomService, TypeService,NumeroService) VALUES(?, ?,?)""", (NomService,TypeService,NumeroService))
        conn2.commit()
        conn2.close()

        #on detruit la fenetre et on detruit le moteur de la fenetre
        self.window.destroy()
        Gtk.main_quit()
        relance()

    def ClicAjouterService(self,widget):
        #on verifie que les informations essentiels sont saisies et que le service n'existe pas
        TypeService = str(self.TypeService.get_active_text())
        NomService =  str(self.NomService.get_text())
        NumeroService = str(self.NumeroService.get_text())

        #on va se connecter à la base
        conn = sqlite3.connect('déclaration.db')
        cursor = conn.cursor()

        #on verifie que les informations sont bien saisie
        if TypeService is None or TypeService =="None" or len(NomService)==0 or len(NumeroService)==0:
            Alerte.appelAffichageAlerte("Il est necessaire de remplir le nom du service et/ou le type du service")
        else:
            #si les informations sont bien saisies on va verifie que le nom de service n'existe pas déja
            cursor.execute("SELECT NomService FROM Service")
            result = cursor.fetchall()
            if result is None:
                conn.close()
                self.ajouterService()
            #on creer une variable arreter qui passe à 1 si le service existe deja
            #on boucle sur les resultat de la requette
            arreter=0
            for service in result:
                if service[0].upper()==NomService.upper():
                    arreter=1

            if arreter==1:
                Alerte.appelAffichageAlerte("Le service existe déja existe déja")
            else:
                conn.close()
                self.ajouterService()


def appelAffichageAjoutService():
    AjoutService()
    Gtk.main()

def relance():
    Relancer = Alerte.appelAffichageAlerteON("Voulez-vous ajouter une autre service ?")
    if Relancer==True:
        appelAffichageAjoutService()





