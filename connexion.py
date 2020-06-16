#installer PYCARIO et PYGTObject
import gi
import sqlite3
import hashlib
import Alerte


IdUtilisateur = 0
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#on se connecte à la base
conn = sqlite3.connect('déclaration.db')
cursor = conn.cursor()

class HelloWorld:
    #ligne de code qui se lance lorsque de l'initialisation
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file('Connexion.glade')  # Rentrez évidemment votre fichier, pas le miens!
        self.window = builder.get_object('Main_Windows')
        builder.connect_signals(self)
        #on creer les variables
        self.NomUtilisateur = builder.get_object("Utilisateur")
        self.MDP = builder.get_object("MDP")


    def Connexion(self,widget):
        #on creer les variables
        utilisateur = self.NomUtilisateur.get_text()
        MDP = self.MDP.get_text()

        #on va hacher le mot de passe saisie par l'utilisateur
        MDPHache = hashlib.shake_128()
        MDP = MDP.encode('utf-8')
        MDPHache.update(MDP.upper())
        MDPHache = MDPHache.digest(16)

        #on va verifier que le nom d'utilisateur correspont au mot de passe hache
        cursor.execute("SELECT id,name,MDP FROM users")
        result = cursor.fetchone()
        while result:
            if result[1].upper() == utilisateur.upper() and result[2] == MDPHache:
                print(result[0])
                self.window.destroy()
                Gtk.main_quit()
                global IdUtilisateur
                IdUtilisateur= result[0]
                break

            result = cursor.fetchone()

    def on_mainWindow_destroy(self, widget):
        pass

def appelAffichageConnexion():
    HelloWorld()
    Gtk.main()
    conn.close()
    #on renvoie la valeur de l'ID utilisateur pour la sauvegarde des ID
    return IdUtilisateur
