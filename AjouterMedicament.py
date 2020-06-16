# on importe les librairies dont nous avons besoins
import gi
import sqlite3
import Alerte
import datetime

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

libelle_utilisateur=""
ATCutilisateur=0
unique=0

# on creer la classe pour l'interface
class AffichageAjouteMedicament:
    # ligne de code qui se lance lorsque de l'initialisation
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('AjoutMedicament.glade')
        self.window = self.builder.get_object('Main_Windows')
        # on creer des objetrs pour chaqu'une des interractions
        self.builder.connect_signals(self)

        #on creer les variables
        self.LibelleMedicament =self.builder.get_object("LIbelleMedicament")
        self.CodeUCD = self.builder.get_object("CodeUCD")
        self.ClasseATC = self.builder.get_object("ClasseATC")
        self.EntreClasseATC = self.builder.get_object("EntreClasseATC")

        #on ajoute les classe ATC à la liste
        conn = sqlite3.connect('déclaration.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT Description FROM ATC """)
        result = cursor.fetchall()
        conn.close()
        for resolution in result:
            self.ClasseATC.append_text(resolution[0])

        #on recupere les informations saisie pas l'utilisateur
        global libelle_utilisateur
        global ATCutilisateur
        self.LibelleMedicament.set_text(libelle_utilisateur)
        self.ClasseATC.set_active(ATCutilisateur)

    def AjoutMedicament(self,widget):
        # on creer les variables
        continuer =1
        nommedoc = self.LibelleMedicament.get_text()
        codeucd =  self.CodeUCD.get_text()
        classatc = self.ClasseATC.get_active()+1


        #on va verifier que l'ensemble des informations sons saisies
        #on verifie le nom du médicament
        if  len(nommedoc)==0:
            Alerte.appelAffichageAlerte("Merci de saisir le nom du médicament")
            continuer=0

        #on verifie la longeur du code UCD
        if len(codeucd)==7 or len(codeucd)==13:
            pass
        else:
            Alerte.appelAffichageAlerte("Merci de saisir un code UCD7 ou UCD13")
            continuer = 0

        #on verifie qu'on est bien saisie un code ATC
        if len(self.EntreClasseATC.get_text())==0:
            Alerte.appelAffichageAlerte("Merci de selectionner une classe ATC")
            continuer = 0

        #on va aussi vérifier que le code UCD n'existe pas déja
        conn = sqlite3.connect('déclaration.db')
        cursor = conn.cursor()
        cursor.execute("SELECT CodeUCD FROM Medoc")
        UCD = cursor.fetchall()
        if UCD is None:
            conn.close()
        for ListeCodeUCD in UCD:
            if ListeCodeUCD[0] == codeucd:
                Alerte.appelAffichageAlerte("Ce code UCD existe déja")
                continuer = 0

        #on verifie que toutes les informations sons saisies
        if continuer==1:
            #on a les informations indispensables on peux donc ajouter le médicaments à la liste déroulantes
            conn = sqlite3.connect('déclaration.db')
            cursor = conn.cursor()
            SQL = "INSERT INTO Medoc(Libelle, CodeUCD,ClasseATC) VALUES(?,?,?)"
            Val =  (nommedoc,codeucd , classatc)
            cursor.execute(SQL,Val)
            Alerte.appelAffichageAlerte("Vous avez ajouter votre médicament")
            conn.commit()
            conn.close()

            # on detruit la fenetre et on detruit le moteur de la fenetre
            self.window.destroy()
            Gtk.main_quit()
            global unique
            if unique==0:
                relance()



def appelAffichageAjoutMedicament(libelle="",atc=0,relance=0):
    global libelle_utilisateur
    global ATCutilisateur
    global unique
    libelle_utilisateur = libelle
    ATCutilisateur = atc
    unique = relance
    AffichageAjouteMedicament()
    Gtk.main()

def relance():
    Relancer = Alerte.appelAffichageAlerteON("Voulez-vous ajouter un autre medicament ?")
    if Relancer==True:
        appelAffichageAjoutMedicament()

