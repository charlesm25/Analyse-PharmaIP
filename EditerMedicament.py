# on importe les librairies dont nous avons besoins
import gi
import sqlite3
import Alerte
import datetime

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


# on creer la classe pour l'interface
class AffichageEditerMedicament:
    # ligne de code qui se lance lorsque de l'initialisation
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('EditerMedicament.glade')
        self.window = self.builder.get_object('Main_Windows')
        # on creer des objetrs pour chaqu'une des interractions
        self.builder.connect_signals(self)

        #on creer les variables
        self.LibelleMedicament =self.builder.get_object("LIbelleMedicament")
        self.CodeUCD = self.builder.get_object("CodeUCD")
        self.ClasseATC = self.builder.get_object("ClasseATC")
        self.EntreClasseATC = self.builder.get_object("EntreClasseATC")
        self.MedicamentEditer = self.builder.get_object("MedicamentEditer")
        self.EntreMedicamentEditer = self.builder.get_object("EntreMedicamentEditer")

        #on ajoute les classe ATC et les medicament à la liste
        conn = sqlite3.connect('déclaration.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT Description FROM ATC """)
        ATC = cursor.fetchall()
        cursor.execute("""SELECT Libelle FROM Medoc ORDER BY Libelle ASC""")
        Medoc = cursor.fetchall()
        conn.close()
        for resolution in ATC:
            self.ClasseATC.append_text(resolution[0])
        for resolution in Medoc:
            self.MedicamentEditer.append_text(resolution[0])

        # on va creer l'autocomplete pour les medicament
        liststoreMedoc = Gtk.ListStore(str)
        for s in list(sum(Medoc, ())):
            liststoreMedoc.append([s])
        autocompletemedoc = Gtk.EntryCompletion()
        autocompletemedoc.set_model(liststoreMedoc)
        autocompletemedoc.set_text_column(0)
        self.builder.get_object("EntreMedicamentEditer").set_completion(autocompletemedoc)


    def EditerMedicament(self,widget):
        # on creer les variables
        continuer =1
        nommedoc = self.builder.get_object("EntreMedicamentEditer").get_text()
        nouveaunommedoc = self.LibelleMedicament.get_text()
        nouveaucodeucd =  self.CodeUCD.get_text()
        nouveauclassatc = self.ClasseATC.get_active()+1


        #on va verifier que l'ensemble des informations sons saisies
        #on verifie le nom du médicament
        if  len(nouveaunommedoc)==0:
            Alerte.appelAffichageAlerte("Merci de saisir le nom du médicament")
            continuer=0

        #on verifie la longeur du code UCD
        if len(nouveaucodeucd)==7 or len(nouveaucodeucd)==13:
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
        conn.close()
        if UCD is None:
            conn.close()
        ######rajouter un test sur les autres code UCD


        #on verifie que toutes les informations sons saisies
        if continuer==1:
            #on a les informations indispensables on peux donc editer le médicament
            conn = sqlite3.connect('déclaration.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM Medoc WHERE Libelle = ?", (nommedoc,))
            Medicament1 = cursor.fetchone()
            SQL = "UPDATE Medoc SET Libelle='" + str(nouveaunommedoc) + "' WHERE id=" + str(Medicament1[0])
            cursor.execute(SQL)
            conn.commit()
            SQL = "UPDATE Medoc SET CodeUCD='" + str(nouveaucodeucd) + "' WHERE id=" + str(Medicament1[0])
            cursor.execute(SQL)
            conn.commit()
            SQL = "UPDATE Medoc SET ClasseATC=" + str(nouveauclassatc) + " WHERE id=" + str(Medicament1[0])
            cursor.execute(SQL)
            conn.commit()
            Alerte.appelAffichageAlerte("Vous avez bien éditer le médicament")

            # on detruit la fenetre et on detruit le moteur de la fenetre
            self.window.destroy()
            Gtk.main_quit()



    def LectureMedicament(self,widget):
        #on va chercher les informations dans la base
        nommedoc = self.builder.get_object("EntreMedicamentEditer").get_text()
        conn = sqlite3.connect('déclaration.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medoc WHERE Libelle = ?", (nommedoc,))
        Medicament = cursor.fetchone()
        conn.close()

        if Medicament is not None:
            self.LibelleMedicament.set_text(Medicament[1])
            self.CodeUCD.set_text(Medicament[2])
            self.ClasseATC.set_active(Medicament[3]-1)

        relance()






def appelAffichageEditerMedicament():
    AffichageEditerMedicament()
    Gtk.main()

def relance():
    Relancer = Alerte.appelAffichageAlerteON("Voulez-vous editer un autre medicament ?")
    if Relancer==True:
        appelAffichageAjoutMedicament()



