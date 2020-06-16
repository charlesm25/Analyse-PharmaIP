import gi
import AjoutUtilisateur
import sqlite3
import AjouterMedicament
import EditerMedicament
import EcritureIP
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

Idutilisateur=0

class AffichageAcceuil:
    #ligne de code qui se lance lorsque de l'initialisation
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('Accueil.glade')
        self.window = self.builder.get_object('Main_Windows')
        #on creer des objetrs pour chaqu'une des interractions
        self.Liste = self.builder.get_object("ListeIntervention")
        self.builder.connect_signals(self)


        #on va creer un listmodele
        listmodel = Gtk.ListStore(str, str, str)

    def NouvelleDeclarationAcceuil(self,widget):
        EcritureIP.appelAffichageAjoutIP(Idutilisateur)

    def AjouterMedicamentAcceuil(self,widget):
        AjouterMedicament.appelAffichageAjoutMedicament("",0,0)

    def EditerMedicamentAcceuil(self,widget):
        EditerMedicament.appelAffichageEditerMedicament()

    def AjoutUser(self,widget):
        global Idutilisateur
        AjoutUtilisateur.appelAffichageAjoutUtilisateur()

def appelAffichageAccueil(IDUtilisateurEnvoye):
    """
        On va afficher un message d'alerte dans la fenetre d'alerte
        la variable afficher correspont auIdUtilisateur message que l'on souhaite faire apparaitre
    """
    global Idutilisateur
    Idutilisateur = IDUtilisateurEnvoye
    AffichageAcceuil()
    Gtk.main()