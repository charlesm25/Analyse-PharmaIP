#installer PYCARIO et PYGTObject
import sqlite3
import gi
import AjoutUtilisateur
import Alerte
import connexion
import Accueil
import AjouterService
import AjouterMedicament
gi.require_version("Gtk", "3.0")

#creer une variableUtilisateur
IdUtilisateur=0

#on se connect  à la base, si elle n'existe pas on la creer
conn = sqlite3.connect('déclaration.db')
#on va verifier si c'est la premiere fois que le logociel est executer
#si oui on va demander la création d'un utilisateur
cursor = conn.cursor()
cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='users' """)
TableUSer = cursor.fetchone()
cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Intervention' """)
TableIntervention = cursor.fetchone()
cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Service' """)
TableService = cursor.fetchone()
cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Probleme' """)
TableProbleme = cursor.fetchone()
cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Resolution' """)
TableIntervention = cursor.fetchone()
cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='ATC' """)
TableClasseATC = cursor.fetchone()
cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Devenir' """)
TableDevenir = cursor.fetchone()
cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Prescripteur' """)
TablePrescripteur = cursor.fetchone()
cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Transmission' """)
TableTransmission = cursor.fetchone()
cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='CotationClinique' """)
TableCotationClinique = cursor.fetchone()
cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='CotationEconomique' """)
TableCotationEconomique  = cursor.fetchone()
cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='CotationOrganisationnel' """)
TableCotationOrganisationnel  = cursor.fetchone()
cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Medoc' """)
TableMedoc = cursor.fetchone()
cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Sexe' """)
TableSexe = cursor.fetchone()
cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='UniteAge' """)
TableUniteAge = cursor.fetchone()


#TableUSer renvoie la présence, ou non, de la table utilisateur
#La variable Table USer est un tuple, on la transforme en INT
if TableUSer[0]==0:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
             name TEXT,
             MDP TEXT
        )
        """)
    conn.commit()
    Alerte.appelAffichageAlerte(
        "C'est la premiere fois que vous executer le logiciel\n Vous devez donc creer le premier utilisateur\n merci de bien noter le nom d'utilisateur")
    AjoutUtilisateur.appelAffichageAjoutUtilisateur()
    Alerte.appelAffichageAlerte("Felicitation vous avez creer votre premier utilisateur")

#on creer la table intervention
if TableIntervention[0]==0:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Intervention(
             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
             DateSaisie DATE,
             Utilisateur SMALLINT,
             NomPatient TEXT,
             PrenomPatient TEXT,
             AgePatient TINYINT,
             UniteAgePatient INT,
             SexePatient INT,
             Poids TEXT,
             Probleme INT,
             Medicament1 INT,
             CodeUCD1 TEXT,
             ATC1 INT,
             Medicament2 INT,
             CodeUCD2 TEXT,
             ATC2 INT,
             Service INT,
             DescriptionProbleme TEXT,
             Intervention INT,
             Prescripteur INT,
             Transmission INT,
             DateContactMedecin DATE,
             DevenirIntervention INT,
             CotationClinique INT,
             CotationEconomique INT,
             CotationOrganisationnel INT,
             Conciliation INT,             
             JustificatifIntervention TEXT
             
        )
        """)
    conn.commit()

#on creer la table service si elle n'existe pas
if TableService[0] == 0:
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS Service(
                 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                 NomService TEXT,
                 TypeService TEXT,
                 NumeroService TEXT
            )
            """)
    conn.commit()
    Alerte.appelAffichageAlerte(
        "C'est la premier fois que vous executer le logiciel\n Vous devez donc creer le/les service(s)")
    AjouterService.appelAffichageAjoutService()


#on creer la table probleme si elle n'existe pas
if TableProbleme[0] == 0:
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS Probleme(
                 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                 Description TEXT,
                 ItemChoix TEXT
            )
            """)
    conn.commit()
    Probleme = []
    Probleme.append(("1. Non conformité aux référentiels et contre-indication (tout type)", "1"))
    Probleme.append(("1.1. Non-conformité au livret", "1.1"))
    Probleme.append(("1.2. Non-conformité aux consensus", "1.2"))
    Probleme.append(("1.3.Contre - indication", "1.3"))
    Probleme.append(("2. Indication non traitée (tout type)", "2"))
    Probleme.append(("2.1. Absence thérapeutique pour indication médicale validée", "2.1"))
    Probleme.append(("2.2. Médicament non prescrit après transfert", "2.2"))
    Probleme.append(("2.3. Absence de prophylaxie ou prémédication", "2.3"))
    Probleme.append(("2.4. Médicament synergique ou correcteur à associer", "2.4"))
    Probleme.append(("3. Sous-dosage (tout type)", "3."))
    Probleme.append(("3.1. Posologie infra-thérapeutique", "3.1"))
    Probleme.append(("3.2. Durée de traitement anormalement raccourcie", "3.2"))
    Probleme.append(("4. Surdosage (tout type)", "4"))
    Probleme.append(("4.1. Posologie supra-thérapeutique", "4.1"))
    Probleme.append(("4.2. Même principe actif prescrit plusieurs fois", "4.2"))
    Probleme.append(("5. Médicament non indiqué (tout type)", "5"))
    Probleme.append(("5.1. Médicament prescrit sans indication justifiée", "5.1"))
    Probleme.append(("5.2. Médicament prescrit sur une durée trop longue sans risque de surdosage", "5.2"))
    Probleme.append(("5.3. redondance pharmacologique (2 PA différents de même classe thérapeutique)", "5.3"))
    Probleme.append(("6. Intéraction médicamenteuse (tout type)", "6"))
    Probleme.append(("6.1. A prendre en compte", "6.1"))
    Probleme.append(("6.2. Précaution d'emploi", "6.2"))
    Probleme.append(("6.3. Association déconseillée", "6.3"))
    Probleme.append(("6.4. Contre-indication", "6.4"))
    Probleme.append(("6.5. Non publiée (hors Vidal)", "6.5"))
    Probleme.append(("7. Effets indésirables", "7"))
    Probleme.append(("8. Voie et/ou administration inappropriée (tout type)", "8"))
    Probleme.append(("8.1 Autre voie plus efficace ou moins couteuse à efficacité équivalente", "8.1"))
    Probleme.append(("8.2. Méthode d'administration non adéquate", "8.2"))
    Probleme.append(("8.3. Mauvais choix de galénique", "8.3"))
    Probleme.append(("8.4. Libellé incomplet", "8.4"))
    Probleme.append(("8.5. Plan de prise non optimal", "8.5"))
    Probleme.append(("9. Traitement non reçu (tout type)", "9"))
    Probleme.append(("9.1. Incompatibilité physico-chimique entre médicaments injectables", "9.1"))
    Probleme.append(("9.2. Problème d'observance", "9.2"))
    Probleme.append(("10. Monitorage à suivre", "10"))


    cursor.executemany("""INSERT INTO Probleme(Description,ItemChoix) VALUES(?,?)""", (Probleme))
    conn.commit()

#on creer la table Interventions si elle n'existe pas  eton la remplit
if TableIntervention[0] == 0:
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS Resolution(
                 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                 Description TEXT
            )
            """)
    conn.commit()
    Intervention = [ "Ajout",
                  "Arret",
                  "Substitution/Echange",
                  "Choix de la voie d'administration",
                  "Suivi thérapeutique",
                  "Optimisation modalités d'administration",
                  "Adaptation posologique"]
    for description in Intervention:
        cursor.execute("""INSERT INTO Resolution(Description) VALUES(?)""", (description,))
        conn.commit()


#on creer la table CLasse ATC s'il n'existe pas et on la remplit
if TableClasseATC[0] == 0:
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS ATC(
                 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                 Description TEXT
            )
            """)
    conn.commit()
    ATC = [ "A : VOIES DIGESTIVES ET METABOLISME",
                    "B : SANG ET ORGANES HEMATOPOIETIQUES",
                    "C : SYSTEME CARDIOVASCULAIRE",
                    "D : MEDICAMENTS DERMATOLOGIQUES",
                    "G : SYSTEME GENITO URINAIRE ET HORMONES SEXUELLES",
                    "H : HORMONES SYSTEMIQUES, HORMONES SEXUELLES EXCLUES",
                    "J : ANTIINFECTIEUX GENERAUX A USAGE SYSTEMIQUE",
                    "L : ANTINEOPLASIQUES ET IMMUNOMODULATEURS",
                    "M : MUSCLE ET SQUELETTE",
                    "N : SYSTEME NERVEUX",
                    "P : ANTIPARASITAIRES, INSECTICIDES",
                    "R : SYSTEME RESPIRATOIRE",
                    "S : ORGANES SENSORIELS",
                    "V : DIVERS"]
    for description in ATC:
        cursor.execute("""INSERT INTO ATC(Description) VALUES(?)""", (description,))
        conn.commit()

#on creer la table devenir si elle n'existe pas et on la remplit
if TableDevenir[0] == 0:
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS Devenir(
                 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                 Description TEXT
            )
            """)
    conn.commit()
    Devenir = [ "Accepté",
            "Non accepté",
            "En cours"]
    for description in Devenir:
        cursor.execute("""INSERT INTO Devenir(Description) VALUES(?)""", (description,))
        conn.commit()


#on va creer la table pour statut de prescripteur et la remplir
if TablePrescripteur[0] == 0:
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS Prescripteur(
                 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                 Description TEXT
            )
            """)
    conn.commit()
    Prescripteur = [ "Interne",
            "Sénior",
            "Sage femme"]
    for description in Prescripteur:
        cursor.execute("""INSERT INTO Prescripteur(Description) VALUES(?)""", (description,))
        conn.commit()



#on va creer la table pour statut de transmission et la remplir
if TableTransmission[0] == 0:
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS Transmission(
                 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                 Description TEXT
            )
            """)
    conn.commit()
    Transmission = [ "Oralement",
            "Appel Téléphonique",
            "Logiciel d'aide à la prescription",
            "Papier",
            "Mail",
            "Autre"        ]
    for description in Transmission:
        cursor.execute("""INSERT INTO Transmission(Description) VALUES(?)""", (description,))
        conn.commit()

#on va creer la table pour Cotation clinique et la remplir
if TableCotationClinique[0] == 0:
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS CotationClinique(
                 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                 Description TEXT,
                 Code TEXT
            )
            """)
    conn.commit()
    CotationClinique = []
    CotationClinique.append(("Nuisible", "-1C"))
    CotationClinique.append(("Nul", "0C"))
    CotationClinique.append(("Mineur", "1C"))
    CotationClinique.append(("Moyen", "2C"))
    CotationClinique.append(("Majeur", "3C"))
    CotationClinique.append(("Vital", "4C"))
    CotationClinique.append(("Non determiné", "ND"))
    cursor.executemany("""INSERT INTO CotationClinique(Description,Code) VALUES(?,?)""", (CotationClinique))
    conn.commit()

#on va creer la table pour Cotation céconomique et la remplir
if TableCotationEconomique[0] == 0:
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS CotationEconomique(
                 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                 Description TEXT,
                 Code TEXT
            )
            """)
    conn.commit()
    CotationEconomique = []
    CotationEconomique.append(("Augmentation du coût", "-1E"))
    CotationEconomique.append(("Pas de changement", "0E"))
    CotationEconomique.append(("Réduction du coût", "1E"))
    CotationEconomique.append(("Non determiné", "ND"))
    cursor.executemany("""INSERT INTO CotationEconomique(Description,Code) VALUES(?,?)""", (CotationEconomique))
    conn.commit()

#on va creer la table pour Cotation organisationnel et la remplir
if TableCotationOrganisationnel[0] == 0:
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS CotationOrganisationnel(
                 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                 Description TEXT,
                 Code TEXT
            )
            """)
    conn.commit()
    CotationOrganisationnel = []
    CotationOrganisationnel.append(("Défavorable", "-1P"))
    CotationOrganisationnel.append(("Nul", "0P"))
    CotationOrganisationnel.append(("Favorable", "1P"))
    CotationOrganisationnel.append(("Non determiné", "NP"))
    cursor.executemany("""INSERT INTO CotationOrganisationnel(Description,Code) VALUES(?,?)""", (CotationOrganisationnel))
    conn.commit()

#on va creer la table pour Cotation organisationnel et la remplir
if TableMedoc[0] == 0:
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS Medoc(
                 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                 Libelle TEXT,
                 CodeUCD TEXT,
                 ClasseATC INT
            )
            """)
    conn.commit()
    Alerte.appelAffichageAlerte(
        "C'est la premier fois que vous executer le logiciel\n Vous devez donc creer un, ou plusieurs, \n médicaments")
    AjouterMedicament.appelAffichageAjoutMedicament("",0,0)

#on va creer la table pour Sexe et la remplir
if TableSexe[0] == 0:
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS Sexe(
                 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                 Libelle TEXT,
                 Code TEXT
            )
            """)
    conn.commit()
    Sexe = []
    Sexe.append(("Feminin", "f"))
    Sexe.append(("Masculin", "m"))
    cursor.executemany("""INSERT INTO Sexe(Libelle,Code) VALUES(?,?)""",(Sexe))
    conn.commit()

#on va creer la table pour UniteAge et la remplir
if TableUniteAge[0] == 0:
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS UniteAge(
                 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                 Libelle TEXT,
                 Code TEXT
            )
            """)
    conn.commit()
    UniteAge = []
    UniteAge.append(("Année", "a"))
    UniteAge.append(("Semaine", "s"))
    UniteAge.append(("Mois", "m"))
    cursor.executemany("""INSERT INTO UniteAge(Libelle,Code) VALUES(?,?)""",(UniteAge))
    conn.commit()


conn.close()

IdUtilisateur=connexion.appelAffichageConnexion()
Accueil.appelAffichageAccueil(IdUtilisateur)
