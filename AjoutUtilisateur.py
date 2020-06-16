#on import les differentes biblioteque
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import sqlite3
import Alerte
import hashlib

class AjoutUtil:
    #ligne de code qui se lance lorsque de l'initialisation
    def __init__(self):
        #on creer la fenetre à partir de l'interface glade
        builder = Gtk.Builder()
        builder.add_from_file('AjoutUtilisateur.glade')
        self.window = builder.get_object('Main_Windows')
        #on creer des objetrs pour chaqu'une des interractions
        self.NomUtilisateur = builder.get_object("Utilisateur")
        self.MDP1 = builder.get_object("MDP1")
        self.MDP2= builder.get_object("MDP2")
        #on creer les interractions entre les fonction definit dans la class et le nom mit dans glade
        builder.connect_signals(self)

    def ajouterPatient(self):
        # permet d'ajouter le patient à la base


        #on recreer les variable pour plus de faciliter le lacture du code
        MDP1 = self.MDP1.get_text()
        utilisateur = self.NomUtilisateur.get_text()

        # on commence par hasher le mot de passe en majuscule
        MDPHache = hashlib.shake_128()
        MDP1 = MDP1.encode('utf-8')
        MDPHache.update(MDP1.upper())
        MDPHache = MDPHache.digest(16)

        # on creer une connexion avec la base de donnée , puis on execute la requete SQL avec les information précédent
        conn2 = sqlite3.connect('déclaration.db')
        cursor2 = conn2.cursor()
        cursor2.execute("""INSERT INTO users(name, MDP) VALUES(?, ?)""", (utilisateur.upper(), MDPHache))
        conn2.commit()
        conn2.close()

        #on affiche une alerte de création
        Alerte.appelAffichageAlerte("L'utilisateur est creer")

        #on detruit la fenetre et on detruit le moteur de la fenetre
        self.window.destroy()
        Gtk.main_quit()

    def ClicAjoutUtilisateur(self,widget):
        # on creer une connexion avec la base de donnée
        conn = sqlite3.connect('déclaration.db')
        cursor = conn.cursor()
        #on commence par remplir les variables
        utilisateur=self.NomUtilisateur.get_text()
        MDP1 = self.MDP1.get_text()
        MDP2 = self.MDP2.get_text()

        #on vérifie que les champs ne sont pas vides et  on verifie que les deux mots de passes sont similaires
        if len(utilisateur.strip()) == 0 or len(MDP1.strip()) == 0 or len(MDP2.strip())==0 or MDP1 != MDP2:
            Alerte.appelAffichageAlerte("Il est necessaire de remplir les champs ou \n les mots de passes ne sont pas identiques")
        else:
            #on va vérifier que le pseudo n'existe pas déja dans la liste
            #on selectionne l'ensemble des nom d'utilisateur de la base de donnée
            #on verifie chaque nom d'utilisateur en mettant tout en majuscule
            #on va rajouter une condition qui lorsque le programme s'execute pour la premiere fois on lance l'ajout patient
            cursor.execute("SELECT name FROM users")
            result =  cursor.fetchall()
            if result is None:
                conn.close()
                self.ajouterPatient()
            #on creer une variable arreter qui passe à 1 si le nom d'utilisateur existe deja existe deja
            #on boucle sur les resultat de la requette
            arreter=0
            for NomUtilisateur in result:
                if NomUtilisateur[0].upper()==utilisateur.upper():
                    arreter=1

            if arreter==1:
                Alerte.appelAffichageAlerte("L'utilisateur existe déja")
            else:
                conn.close()
                self.ajouterPatient()






def appelAffichageAjoutUtilisateur():
    AjoutUtil()
    Gtk.main()
