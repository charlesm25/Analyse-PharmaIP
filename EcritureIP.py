# on importe les librairies dont nous avons besoins
import gi
import sqlite3
import Alerte
import datetime
import AjouterMedicament

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

Idutilisateur = 0


# on creer la classe pour l'interface
class AffichageEcritureIP:
    # ligne de code qui se lance lorsque de l'initialisation
    def __init__(self):
        # on creer la fenetre à partir de l'interface glade
        self.builder = Gtk.Builder()
        self.builder.add_from_file('EcritureIP.glade')
        self.window = self.builder.get_object('Main_Windows_IP')
        # on creer des objetrs pour chaqu'une des interractions
        self.builder.connect_signals(self)
        # on creer les variables
        self.DateIP = self.builder.get_object("DateRealisation")
        self.Service = self.builder.get_object("Services")
        self.NomPatient = self.builder.get_object("NomPatient")
        self.PrenomPatient = self.builder.get_object("PrenomPatient")
        self.Age = self.builder.get_object("Age")
        self.UniteAge = self.builder.get_object("UniteAge")
        self.Sexe = self.builder.get_object("Sexe")
        self.Probleme = self.builder.get_object("Probleme")
        self.Intervention = self.builder.get_object("Intervention")
        self.ATC1 = self.builder.get_object("ClasseATC1")
        self.ATC2 = self.builder.get_object("ClasseATC2")
        self.ProblemeDescription = self.builder.get_object("ProblemeDescription")
        self.Devenir = self.builder.get_object("DevenirIntervention")
        self.RetourMedecin = self.builder.get_object("RetourMedecin")
        self.Medoc1 = self.builder.get_object("Médicament1")
        self.Medoc2 = self.builder.get_object("Médicament2")
        self.Prescripteur = self.builder.get_object("Prescripteur")
        self.Contact = self.builder.get_object("Contact")
        self.CotationClinique = self.builder.get_object("CotationClinique")
        self.CotationEconomique = self.builder.get_object("CotationEconomique")
        self.CotationOrga = self.builder.get_object("CotationOrga")
        self.Conciliation = self.builder.get_object("Conciliation")
        self.Poids = self.builder.get_object("Poids")
        self.RetourMedecin = self.builder.get_object("RetourMedecin")
        self.DateMedecin = self.builder.get_object("DateMedecin")
        self.NumIP = self.builder.get_object("NumIP")


        # on affecte la date du jour à l'entrée
        dateBrut = datetime.datetime.now()
        DateJour = FormatDate(dateBrut.day, dateBrut.month, dateBrut.year)
        self.DateIP.set_text(DateJour)

        #on va creer les listes pour remplir les listes déroulantes
        conn = sqlite3.connect('déclaration.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT NomService FROM Service """)
        self.ListeService = cursor.fetchall()
        cursor.execute("""SELECT Description FROM Probleme """)
        ListeProbleme = cursor.fetchall()
        cursor.execute("""SELECT Description FROM Resolution """)
        ListeResolution = cursor.fetchall()
        cursor.execute("""SELECT Description FROM ATC """)
        ListeATC = cursor.fetchall()
        cursor.execute("""SELECT Description FROM Devenir """)
        ListeDevenir = cursor.fetchall()
        cursor.execute("""SELECT Description FROM Prescripteur """)
        ListePrescripteur = cursor.fetchall()
        cursor.execute("""SELECT Description FROM Transmission """)
        ListeTransmission = cursor.fetchall()
        cursor.execute("""SELECT Description FROM CotationClinique """)
        ListeCotationClinique = cursor.fetchall()
        cursor.execute("""SELECT Description FROM CotationEconomique """)
        ListeCotationEconomique = cursor.fetchall()
        cursor.execute("""SELECT Description FROM CotationOrganisationnel """)
        ListeCotationOrga = cursor.fetchall()
        cursor.execute("""SELECT Libelle FROM Medoc ORDER BY Libelle ASC""")
        self.ListeMedoc = cursor.fetchall()
        cursor.execute("""SELECT Libelle FROM Sexe """)
        ListeSexe = cursor.fetchall()
        cursor.execute("""SELECT Libelle FROM UniteAge """)
        ListeUniteAge = cursor.fetchall()
        conn.close()


        # on va rajouter les services dans la liste
        for service in self.ListeService:
            self.Service.append_text(service[0])

        # on va rajouter les problemes dans la liste
        for probleme in ListeProbleme:
            self.Probleme.append_text(probleme[0])

        # on va rajouter les resolutions dans la liste
        for resolution in ListeResolution:
            self.Intervention.append_text(resolution[0])

        # on va rajouter les classe ATC dans la liste
        for resolution in ListeATC:
            self.ATC1.append_text(resolution[0])
            self.ATC2.append_text(resolution[0])

        # on va rajouter les  Devenir dans la liste
        for resolution in ListeDevenir:
            self.Devenir.append_text(resolution[0])

        # on va rajouter les prescripteur dans la liste
        for resolution in ListePrescripteur:
            self.Prescripteur.append_text(resolution[0])

        # on va rajouter le contact dans la liste
        for resolution in ListeTransmission:
            self.Contact.append_text(resolution[0])

        # on va rajouter les cotation clinique dans la liste
        for resolution in ListeCotationClinique:
            self.CotationClinique.append_text(resolution[0])

        # on va rajouter les cotation economique dans la liste
        for resolution in ListeCotationEconomique:
            self.CotationEconomique.append_text(resolution[0])

        # on va rajouter les cotation Orga dans la liste
        for resolution in ListeCotationOrga:
            self.CotationOrga.append_text(resolution[0])

        # on va rajouter les cotation Orga dans la liste
        for resolution in self.ListeMedoc:
            self.Medoc1.append_text(resolution[0])
            self.Medoc2.append_text(resolution[0])

        # on va rajouter les sexe dans la liste
        for resolution in ListeSexe:
            self.Sexe.append_text(resolution[0])

        # on va rajouter les unite d'age dans la liste
        for resolution in ListeUniteAge:
            self.UniteAge.append_text(resolution[0])

        #on va creer l'autocomplete pour les medicament
        self.liststoreMedoc = Gtk.ListStore(str)
        for s in list(sum(self.ListeMedoc,())):
            self.liststoreMedoc.append([s])
        self.autocompletemedoc = Gtk.EntryCompletion()
        self.autocompletemedoc.set_model(self.liststoreMedoc)
        self.autocompletemedoc.set_text_column(0)
        self.builder.get_object("EntreMedoc1").set_completion(self.autocompletemedoc)
        self.builder.get_object("EntreMedoc2").set_completion(self.autocompletemedoc)



    def ClicConciliation(self, widget):
        if self.Conciliation.get_label() == "Non":
            self.Conciliation.set_label("Oui")
        else:
            self.Conciliation.set_label("Non")

    def ValidationIP(self, widget):
        global Idutilisateur
        # on commence par verifier que les donne importante sont saisie
        continuer = 0
        if len(self.DateIP.get_text()) == 0:
            Alerte.appelAffichageAlerte("Il faut saisir la date")
            continuer = 1
        if len(self.Service.get_active_text()) == 0:
            Alerte.appelAffichageAlerte("Il faut saisir le service")
            continuer = 1
        if len(self.Age.get_text()) == 0:
            Alerte.appelAffichageAlerte("Il faut saisir l'age du patient")
            continuer = 1
        if self.UniteAge.get_active_text() is None:
            Alerte.appelAffichageAlerte("Il faut saisir l'unite de l'age du patient")
            continuer = 1
        if self.Sexe.get_active_text() is None:
            Alerte.appelAffichageAlerte("Il faut saisir le sexe du patient")
            continuer = 1
        if self.Probleme.get_active_text() is None:
            Alerte.appelAffichageAlerte("Il faut saisir le probleme")
            continuer = 1
        if self.Intervention.get_active_text() is None:
            Alerte.appelAffichageAlerte("Il faut saisir l'intervention")
            continuer = 1
        if self.Prescripteur.get_active_text() is None:
            Alerte.appelAffichageAlerte("Il faut saisir le prescripteur")
            continuer = 1
        if len(self.Medoc1.get_active_text()) == 0:
            Alerte.appelAffichageAlerte("Il faut saisir le médicament")
            continuer = 1
        if self.Devenir.get_active_text() is None:
            Alerte.appelAffichageAlerte("Il faut saisir le devenir de l'IP")
            continuer = 1
        # on creer un tableau avec les IP qui necessitent de saisir un autre médicaments
        IPavecdeuxMedoc = [15, 19, 20, 21, 22, 23, 24, 25, 34]
        # on rajoute 1 à l'ID car le premier de la liste à l'ID 0
        IDProbleme = (self.Probleme.get_active() + 1)
        if IDProbleme in IPavecdeuxMedoc and len(self.Medoc2.get_active_text()) == 0:
            Alerte.appelAffichageAlerte("Il faut saisir le second médicament pour cette intervention")
            continuer = 1

        if continuer == 1:
            pass
        else:
            # on va donc ajouter l'IP dans la base
            global Idutilisateur
            # on transformer la conciliation en 1 ou 0
            if self.Conciliation.get_label() == "Non":
                Conciliation = 0
            else:
                Conciliation = 1

            #on va verifier que le/les medoc(s) saisi existe bien dans la base de donnée
            # on verifie si le service fait partie de la liste
            # on va transformer la liste de tuple en list pur
            if self.Medoc1.get_active_text() in list(sum(self.ListeMedoc,())):
               pass
            else:
                AjouterMedicament.appelAffichageAjoutMedicament(self.Medoc1.get_active_text(), self.ATC1.get_active(),1)

            if self.Medoc2.get_active_text()=="" or self.Medoc2.get_active_text() in list(sum(self.ListeMedoc,())):
               pass
            else:
                AjouterMedicament.appelAffichageAjoutMedicament(self.Medoc2.get_active_text(), self.ATC2.get_active(),1)

            # on va chercher le code UCD et l'id du médicament
            conn = sqlite3.connect('déclaration.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id,CodeUCD FROM Medoc WHERE Libelle = ?", (self.Medoc1.get_active_text(),))
            Medicament1 = cursor.fetchone()

            if self.Medoc2.get_active_text() == "":
                Medicament2 =[0,0]
            else:
                cursor.execute("SELECT id,CodeUCD FROM Medoc WHERE Libelle = ?", (self.Medoc2.get_active_text(),))
                Medicament2 = cursor.fetchone()
            conn.close()

            # on va creer des variable pour les texte
            # pour le TextViewer le texte est lié à une Buffer de Texte
            # pour afficher le texte il est necessaire d'avoir le début et la fin du texte
            # on creer donc le début et la fin et on l'inclut dans
            iterdebut, iterfin = self.ProblemeDescription.get_bounds()
            DescriptionProbleme = str(self.ProblemeDescription.get_text(iterdebut, iterfin, include_hidden_chars=True))
            iterdebut2, iterfin2 = self.RetourMedecin.get_bounds()
            RetourMedecin = str(self.RetourMedecin.get_text(iterdebut2, iterfin2, include_hidden_chars=True))

            # on creer une liste de tuplue pour fussioner avec la liste pour inserer les donnes
            IP = [(str(self.DateIP.get_text()),
                   Idutilisateur,
                   str(self.NomPatient.get_text()),
                   str(self.PrenomPatient.get_text()),
                   str(self.Age.get_text()),
                   self.UniteAge.get_active()+1,
                   self.Sexe.get_active()+1,
                   str(self.Poids.get_text()),
                   self.Probleme.get_active() + 1,
                   Medicament1[0],
                   Medicament1[1],
                   self.ATC1.get_active()+1,
                   Medicament2[0],
                   Medicament2[1],
                   self.ATC2.get_active()+1,
                   self.Service.get_active() + 1,
                   DescriptionProbleme,
                   self.Intervention.get_active() + 1,
                   self.Prescripteur.get_active() + 1,
                   self.Contact.get_active() + 1,
                   self.DateMedecin.get_text(),
                   self.Devenir.get_active() + 1,
                   self.CotationClinique.get_active() + 1,
                   self.CotationEconomique.get_active() + 1,
                   self.CotationOrga.get_active() + 1,
                   Conciliation,
                   RetourMedecin)]
            # pour reussir à faire l'insertion des données avec le Update , on creer une liste avec les noms de colonne
            ColonneSQL = [
                "DateSaisie",
                "Utilisateur",
                "NomPatient",
                "PrenomPatient",
                "AgePatient",
                "UniteAgePatient",
                "SexePatient",
                "Poids",
                "Probleme",
                "Medicament1",
                "CodeUCD1",
                "ATC1",
                "Medicament2",
                "CodeUCD2",
                "ATC2",
                "Service",
                "DescriptionProbleme",
                "Intervention",
                "Prescripteur",
                "Transmission",
                "DateContactMedecin",
                "DevenirIntervention",
                "CotationClinique",
                "CotationEconomique",
                "CotationOrganisationnel",
                "Conciliation",
                "JustificatifIntervention"
            ]

            #on creer une liste pour faire un for sur les nombres
            nombre = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]

            # on se connecte à la base
            conn = sqlite3.connect('déclaration.db')
            cursor = conn.cursor()

            # on va utiliser l'interface pour saisir et modifier les IP
            # on va donc verifier si le numeroIP est saisie, dans la textbox, si ce n'est pas le cas on ajoute et on
            # affiche le numero IP
            # si c'est n'ai pas le cas on verifie que l'IP existe est on la met à jour
            if len(self.NumIP.get_text()) == 0:
                for i in IP:
                    cursor.execute(
                        "INSERT INTO Intervention(DateSaisie,Utilisateur,NomPatient,PrenomPatient,AgePatient,"
                        "UniteAgePatient,SexePatient,Poids,Probleme,Medicament1,CodeUCD1,ATC1,Medicament2,CodeUCD2,"
                        "ATC2,Service,DescriptionProbleme,Intervention,Prescripteur,Transmission,DateContactMedecin,"
                        "DevenirIntervention,CotationClinique,CotationEconomique,CotationOrganisationnel,Conciliation,"
                        "JustificatifIntervention) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", i)
                id = cursor.lastrowid
                message = "Féliciation vous avez sauvegarder votre IP sous le numero " + str(id)
                self.NumIP.set_text(str(id))
                Alerte.appelAffichageAlerte(message)
                conn.commit()
                conn.close()
            else:
                # on va tester voir si le numero de l'IP existe
                cursor.execute("SELECT count(*) FROM Intervention WHERE id= ?", (int(self.NumIP.get_text()),))
                IpExiste = cursor.fetchone()
                if IpExiste[0] == 0:
                    Alerte.appelAffichageAlerte("L'IP n'existe pas")
                    conn.close()
                else:
                    # on creer une boucle pour mettre à jour l'IP
                    for i in nombre:
                        sql = "UPDATE Intervention SET " + ColonneSQL[i] + "=? WHERE id=" + str(self.NumIP.get_text())
                        cursor.execute(sql, (IP[0][i],))
                        conn.commit()
                    conn.close()



    def Lecture(self,widget):
        """
            Cette fonction permet de lire la BDD et si , l'IP existe, mettre l'ensemble des données dans l'interface.
        """
        if self.NumIP.get_text() is None or self.NumIP.get_text()=="":
            self.effacerinterface(self)
        else:
            conn = sqlite3.connect('déclaration.db')
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM Intervention WHERE id= ?", (int(self.NumIP.get_text()),))
            IpExiste = cursor.fetchone()
            if IpExiste[0] == 1:
                cursor.execute("SELECT * FROM Intervention WHERE id= ?",(int(self.NumIP.get_text()),))
                ip_complete = cursor.fetchone()
                cursor.execute("SELECT Libelle FROM Medoc WHERE id= ?",(int(ip_complete[10]),))
                NomMedicament1  = cursor.fetchone()
                if int(ip_complete[13])==0:
                    NomMedicament2=[""]
                else:
                    cursor.execute("SELECT Libelle FROM Medoc WHERE id= ?",(int(ip_complete[13]),))
                    NomMedicament2  = cursor.fetchone()
                conn.close()
                self.DateIP.set_text(ip_complete[1])
                self.Service.set_active(int(ip_complete[16])-1)
                self.NomPatient.set_text(ip_complete[3])
                self.PrenomPatient.set_text(ip_complete[4])
                self.Age.set_text(str(ip_complete[5]))
                self.UniteAge.set_active(ip_complete[6]-1)
                self.Sexe.set_active(ip_complete[7] - 1)
                self.Poids.set_text(ip_complete[8])
                self.Probleme.set_active(ip_complete[9]-1)
                self.builder.get_object("EntreMedoc1").set_text(NomMedicament1[0])
                self.ATC1.set_active(ip_complete[12]-1)
                self.builder.get_object("EntreMedoc2").set_text(NomMedicament2[0])
                self.ATC2.set_active(ip_complete[15]-1)
                self.ProblemeDescription.set_text(ip_complete[17])
                self.Intervention.set_active(ip_complete[18]-1)
                self.Prescripteur.set_active(ip_complete[19]-1)
                self.Contact.set_active(ip_complete[20]-1)
                self.DateMedecin.set_text(ip_complete[21])
                self.Devenir.set_active(ip_complete[22]-1)
                self.CotationClinique.set_active(ip_complete[23]-1)
                self.CotationEconomique.set_active(ip_complete[24]-1)
                self.CotationOrga.set_active(ip_complete[25]-1)
                if ip_complete[26]==self.Conciliation.get_label():
                    pass
                else:
                    self.Conciliation.activate()
                self.RetourMedecin.set_text(ip_complete[27])
            else:
                self.effacerinterface(self)

    def ChangementMedicament1(self,widget):
        """
        Permet de changer le code ATC automatiquement quand on saisie un médicament dans la bare 1
        """
        if self.builder.get_object("EntreMedoc1").get_text()=="":
            pass
        else:
            conn = sqlite3.connect('déclaration.db')
            cursor = conn.cursor()
            SQL = "SELECT ClasseATC FROM Medoc WHERE Libelle= ?"
            Val = self.builder.get_object("EntreMedoc1").get_text()
            cursor.execute(SQL ,(Val,) )
            ClassATC = cursor.fetchone()
            if cursor.rowcount <0:
                self.builder.get_object("EntreClasseATC1").set_text("")
            else:
                self.ATC1.set_active(ClassATC[0]  - 1)

    def ChangementMedicament2(self,widget):
        """
        Permet de changer le code ATC automatiquement quand on saisie un médicament dans la bare 2
        """

        if self.builder.get_object("EntreMedoc2").get_text()=="":
            pass
        else:
            conn = sqlite3.connect('déclaration.db')
            cursor = conn.cursor()
            SQL = "SELECT ClasseATC FROM Medoc WHERE Libelle= ?"
            Val = self.builder.get_object("EntreMedoc2").get_text()
            cursor.execute(SQL ,(Val,) )
            ClassATC = cursor.fetchone()
            if cursor.rowcount<0:
                self.builder.get_object("EntreClasseATC2").set_text("")
            else:
                self.ATC2.set_active(ClassATC[0]  - 1)

    def effacerinterface(self,widget):
        dateBrut = datetime.datetime.now()
        DateJour = FormatDate(dateBrut.day, dateBrut.month, dateBrut.year)
        self.DateIP.set_text(DateJour)
        self.builder.get_object("EntreService").set_text("")
        self.NomPatient.set_text("")
        self.PrenomPatient.set_text("")
        self.Age.set_text("")
        self.builder.get_object("EntreUA").set_text("")
        self.builder.get_object("EntreSexe").set_text("")
        self.Poids.set_text("")
        self.builder.get_object("EntreProbleme").set_text("")
        self.builder.get_object("EntreMedoc1").set_text("")
        self.builder.get_object("EntreClasseATC1").set_text("")
        self.builder.get_object("EntreMedoc2").set_text("")
        self.builder.get_object("EntreClasseATC2").set_text("")
        self.ProblemeDescription.set_text("")
        self.builder.get_object("EntreIntervention").set_text("")
        self.builder.get_object("EntreMedecin").set_text("")
        self.builder.get_object("EntreContact").set_text("")
        self.DateMedecin.set_text("")
        self.builder.get_object("EntreDevenir").set_text("")
        self.builder.get_object("EntreClinique").set_text("")
        self.builder.get_object("EntreEconomique").set_text("")
        self.builder.get_object("EntreOrga").set_text("")
        if self.Conciliation.get_label() == "Oui":
            self.Conciliation.activate()

    def FermetureIP(self,widget):
        Gtk.main_quit()
        self.window.destroy()



def FormatDate(jour, mois, annee):
    jour = str(jour)
    mois = str(mois)
    annee = str(annee)
    if len(jour) < 2: jour = "0" + jour
    if len(mois) < 2: mois = "0" + mois
    return str(jour) + "/" + str(mois) + "/" + str(annee)


def appelAffichageAjoutIP(IDUtilisateurEnvoye):
    global Idutilisateur
    Idutilisateur = IDUtilisateurEnvoye
    AffichageEcritureIP()
    Gtk.main()
