import serial  # pip install pyserial
import psycopg2  # pip install psycopg2
import datetime  # pip install datetime
import asyncio # pip install asyncio
import atexit # Present de base dans Python 3

### VARIABLES ###
# Informations de login a la base de donnees
adresseServeur = "54.39.144.87"
utilisateur = "postgres"
motDePasse = "9182"
baseDeDonnees = "capture"

# Informations Arduino
port_serie = "COM3"
baud_rate = 9600

chemin_fichier = "./data.txt"

### FONCTIONS ###
async def envoyerValeurEnBDD(valeur):
    curseur.execute(
        "INSERT INTO raw(temp, timestamp) VALUES(%s, %s);", (valeur, datetime.datetime.utcnow()))
    maConnection.commit()

def fermerConnexion():
    print("Fermeture de la connexion à la BDD.")
    curseur.close()
    maConnection.close()

### CODE ###
# Appel de la fonction fermerConnexion() a l'arret du programme
atexit.register(fermerConnexion)

# Connexion a la BDD et creation d'un curseur
maConnection = psycopg2.connect(
    host = adresseServeur, user = utilisateur, password = motDePasse, dbname = baseDeDonnees)
curseur = maConnection.cursor()

fichier_sortie = open(chemin_fichier, "w")
serie = serial.Serial(port_serie, baud_rate)

while True:
    # Lecture de la valeur renvoyee par le port serie du micro controleur
    ligne = serie.readline().decode("utf-8")
    if not (ligne == ""):
        print(ligne.rstrip())
        fichier_sortie.write(ligne.rstrip() + "\n")

        # Appel de fonction asynchrone
        boucle = asyncio.get_event_loop()
        boucle.run_until_complete(envoyerValeurEnBDD(ligne.rstrip()))
