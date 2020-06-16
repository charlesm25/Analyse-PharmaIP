import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#on creer une variable globale pour le message qui sera modifier dans l'appal de la fonction et qui affiche le message d'alerte
#une seconde variable globale pour savoir si on repart apres l'affichage
message=" "
Choix = True

class AffichageAlerte:
    #ligne de code qui se lance lorsque de l'initialisation
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('Alerte.glade')
        self.window = self.builder.get_object('FenetreAlerte')
        #on creer des objetrs pour chaqu'une des interractions
        self.builder.connect_signals(self)
        self.Label = self.builder.get_object("LabelAlerte")
        self.Label.set_text(message)

    def AlerteBouton(self,widget):
        self.window.destroy()
        Gtk.main_quit()

    def on_mainWindow_destroy(self, widget):
        pass

def appelAffichageAlerte(afficher):
    """
        On va afficher un message d'alerte dans la fenetre d'alerte
        la variable afficher correspont auIdUtilisateur message que l'on souhaite faire apparaitre
    """
    global message
    message=afficher
    AffichageAlerte()
    Gtk.main()
    return()

class AffichageAlerteON:
    #ligne de code qui se lance lorsque de l'initialisation
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('AlerteON.glade')
        self.window = self.builder.get_object('FenetreAlerte')
        #on creer des objetrs pour chaqu'une des interractions
        self.builder.connect_signals(self)
        self.Label = self.builder.get_object("LabelAlerte")
        self.Label.set_text(message)

    def AlerteBoutonOui(self,widget):
        self.window.destroy()
        Gtk.main_quit()
        global Choix
        Choix = True

    def AlerteBoutonNon(self,widget):
        self.window.destroy()
        Gtk.main_quit()
        global Choix
        Choix = False


    def on_mainWindow_destroy(self, widget):
        pass

def appelAffichageAlerteON(afficher):
    """
        On va afficher un message d'alerte dans la fenetre d'alerte
        la variable afficher correspont auIdUtilisateur message que l'on souhaite faire apparaitre
    """
    global message
    message=afficher
    AffichageAlerteON()
    Gtk.main()
    global Choix
    return Choix

