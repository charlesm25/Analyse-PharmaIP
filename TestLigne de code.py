import gi
import sqlite3
import Alerte
import AjouterService
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import AjouterMedicament

conn = sqlite3.connect('déclaration.db')
cursor = conn.cursor()
cursor.execute("SELECT Medoc.libelle, ATC.Description FROM Medoc LEFT JOIN ATC ON Medoc.ClasseATC=ATC.id")
ListeMedoc = cursor.fetchall()

print(ListeMedoc)
