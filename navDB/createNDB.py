import sqlite3
import csv

if __name__ == '__main__':

    connexion = sqlite3.connect("data/nav.db")
    cursor = connexion.cursor()

    sql_file = open("createNDB.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)

    # Spécifiez le chemin vers le fichier CSV
    fichier_csv = 'data/csv/aeroport.csv'

    # Utilisez la bibliothèque CSV pour lire le fichier CSV et insérer les données dans la table
    with open(fichier_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        # next(csvreader)  # Pour ignorer la ligne d'en-tête si elle existe dans le fichier CSV
        data = list(csvreader)
        for row in data:
            # Insérez les données du CSV dans la table
            cursor.execute('''INSERT INTO aeroport (id, icaocode, identifiant, ataiata, speedlimitaltitude, longestrwy,
             ifr, longrwy, latitude, longitude, magneticvariation, elevation, speedlimit, recvhf, icaocodevhf,
             transaltitude, translevel, publicmilitaire, timezone, daytime, mtind, datum, airportname, firidentifier,
             asarptident)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)

    # Spécifiez le chemin vers le fichier CSV
    fichier_csv = 'data/csv/appr.csv'

    # Utilisez la bibliothèque CSV pour lire le fichier CSV et insérer les données dans la table
    with open(fichier_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        # next(csvreader)  # Pour ignorer la ligne d'en-tête si elle existe dans le fichier CSV
        data = list(csvreader)
        for row in data:
            # Insérez les données du CSV dans la table
            cursor.execute('''INSERT INTO appr (runwayidentifiant, typeapproche, aeroportidentifiant, icaocode,
             premierpoint, balises)
             VALUES (?, ?, ?, ?, ?, ?)''', row)

    # Spécifiez le chemin vers le fichier CSV
    fichier_csv = 'data/csv/dme.csv'

    # Utilisez la bibliothèque CSV pour lire le fichier CSV et insérer les données dans la table
    with open(fichier_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        # next(csvreader)  # Pour ignorer la ligne d'en-tête si elle existe dans le fichier CSV
        data = list(csvreader)
        for row in data:
            # Insérez les données du CSV dans la table
            cursor.execute('''INSERT INTO dme (id, icaocode, identifiant, nom, latitude, longitude, aeroport,
             icaoaeroport, magneticvariation, datum, firidentifier, uiridentifier, seindicator, sedate, elevation,
             frequence, frequenceprotection, biais, navaidmerit)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)

    # Spécifiez le chemin vers le fichier CSV
    fichier_csv = 'data/csv/holdingpattern.csv'

    # Utilisez la bibliothèque CSV pour lire le fichier CSV et insérer les données dans la table
    with open(fichier_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        # next(csvreader)  # Pour ignorer la ligne d'en-tête si elle existe dans le fichier CSV
        data = list(csvreader)
        for row in data:
            # Insérez les données du CSV dans la table
            cursor.execute('''INSERT INTO holdingpattern (regioncode, icaocode, dupidentifier, fixidentifier,
             icaobalise, seccodebalise, subcodebalise, inboundholdingcourse, turndirection, leglength, legtime,
             minaltitude, maxaltitude, holdspeed, rnp, arcradius, name, typebalise, rattachbalise)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)

    # Spécifiez le chemin vers le fichier CSV
    fichier_csv = 'data/csv/ils.csv'

    # Utilisez la bibliothèque CSV pour lire le fichier CSV et insérer les données dans la table
    with open(fichier_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        # next(csvreader)  # Pour ignorer la ligne d'en-tête si elle existe dans le fichier CSV
        data = list(csvreader)
        for row in data:
            # Insérez les données du CSV dans la table
            cursor.execute('''INSERT INTO ils (id, icaocode, identifiant, nom, latitude, longitude, aeroport,
             icaoaeroport, magneticvariation, datum, firidentifier, uiridentifier, seindicator, sedate, elevation,
             categorie, frequence, runwayidentifiant, locbearing, gslatitude, gslongitude, locfr,
             localiserpositionreference, gsthres, locwidth, gsangle, tch, gselev, facility)
             VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)


    # Spécifiez le chemin vers le fichier CSV
    fichier_csv = 'data/csv/ilsdme.csv'

    # Utilisez la bibliothèque CSV pour lire le fichier CSV et insérer les données dans la table
    with open(fichier_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        # next(csvreader)  # Pour ignorer la ligne d'en-tête si elle existe dans le fichier CSV
        data = list(csvreader)
        for row in data:
            # Insérez les données du CSV dans la table
            cursor.execute('''INSERT INTO ilsdme(id, icaocode, identifiant, nom, latitude, longitude, aeroport,
             icaoaeroport, magneticvariation, datum, firidentifier, uiridentifier, seindicator, sedate, elevation,
             frequence, frequenceprotection, biais, navaidmerit)
             VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)

    # Spécifiez le chemin vers le fichier CSV
    fichier_csv = 'data/csv/ndb.csv'

    # Utilisez la bibliothèque CSV pour lire le fichier CSV et insérer les données dans la table
    with open(fichier_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        # next(csvreader)  # Pour ignorer la ligne d'en-tête si elle existe dans le fichier CSV
        data = list(csvreader)
        for row in data:
            # Insérez les données du CSV dans la table
            cursor.execute('''INSERT INTO ndb(id, icaocode, identifiant, nom, latitude, longitude, aeroport, 
             icaoaeroport, magneticvariation, datum, firidentifier, uiridentifier, seindicator, sedate, elevation,
             frequence, classndb)
             VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)


    # Spécifiez le chemin vers le fichier CSV
    fichier_csv = 'data/csv/piste.csv'

    # Utilisez la bibliothèque CSV pour lire le fichier CSV et insérer les données dans la table
    with open(fichier_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        # next(csvreader)  # Pour ignorer la ligne d'en-tête si elle existe dans le fichier CSV
        data = list(csvreader)
        for row in data:
            # Insérez les données du CSV dans la table
            cursor.execute('''INSERT INTO piste (id, icaocode, identifiantrwy, identifiantaeroport, runwaylength,
             runwaybearing, latitude, longitude, runwaygrad, ellipsoidheight, lndgthreselev, dsplcdthr, tch, width,
             locglsident, categorieloc, stopway, seclocglsident, categoriesecloc)
             VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)

    # Spécifiez le chemin vers le fichier CSV
    fichier_csv = 'data/csv/procedure.csv'

    # Utilisez la bibliothèque CSV pour lire le fichier CSV et insérer les données dans la table
    with open(fichier_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        # next(csvreader)  # Pour ignorer la ligne d'en-tête si elle existe dans le fichier CSV
        data = list(csvreader)
        for row in data:
            # Insérez les données du CSV dans la table
            cursor.execute('''INSERT INTO procedure (typeprocedure, aeroportidentifiant, icaocode, identifiant,
             routetype, transitionidentifier, sequencenumber, fixidentifiant, icaocodefix, seccodefix, subcodefix,
             descriptioncode, turndirection, requirednavigationperformance, pathandterminaison, turndirectionvalide,
             recommendednavaid, icaocodenavaid, arcradius, theta, rho, magneticcruise, routedistance, seccoderoute,
             subcoderoute, altitudedescription, atc, altitude, altitude2, transaltitude, speedlimit, verticalangle,
             centerfix, multicd, icaocodecenter, seccodecenter, subcodecenter, gnssfmsindicator)
             VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
             ?, ?, ?, ?, ?, ?)''', row)

    # Spécifiez le chemin vers le fichier CSV
    fichier_csv = 'data/csv/route.csv'

    # Utilisez la bibliothèque CSV pour lire le fichier CSV et insérer les données dans la table
    with open(fichier_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        # next(csvreader)  # Pour ignorer la ligne d'en-tête si elle existe dans le fichier CSV
        data = list(csvreader)
        for row in data:
            # Insérez les données du CSV dans la table
            cursor.execute('''INSERT INTO route(routeidentifiant, sequencenumber, fixidentifiant, icaocodefix,
             seccodefix, subcodefix, descriptioncode, boundarycode, routetype, levelroute, direct, 
             cruisetableidentifier, euindicator, receivervhf, icaocodevhf, requirednavigation, theta, rho,
             outboundmagneticcruise, routefromdistance, inboundmagneticcruise, minaltitude, minaltitude2, 
             maxaltitude)
             VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)

    # Spécifiez le chemin vers le fichier CSV
    fichier_csv = 'data/csv/sid.csv'

    # Utilisez la bibliothèque CSV pour lire le fichier CSV et insérer les données dans la table
    with open(fichier_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        # next(csvreader)  # Pour ignorer la ligne d'en-tête si elle existe dans le fichier CSV
        data = list(csvreader)
        for row in data:
            # Insérez les données du CSV dans la table
            cursor.execute('''INSERT INTO sid (identifiant, icaocode, aeroportidentifiant, runwayidentifiant, lastfix,
             firstfix, latlong)
             VALUES  (?, ?, ?, ?, ?, ?, ?)''', row)

    # Spécifiez le chemin vers le fichier CSV
    fichier_csv = 'data/csv/star.csv'

    # Utilisez la bibliothèque CSV pour lire le fichier CSV et insérer les données dans la table
    with open(fichier_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        # next(csvreader)  # Pour ignorer la ligne d'en-tête si elle existe dans le fichier CSV
        data = list(csvreader)
        for row in data:
            # Insérez les données du CSV dans la table
            cursor.execute('''INSERT INTO star (identifiant, icaocode, aeroportidentifiant, runwayidentifiant, lastfix,
             firstfix, latlong)
             VALUES  (?, ?, ?, ?, ?, ?, ?)''', row)

    # Spécifiez le chemin vers le fichier CSV
    fichier_csv = 'data/csv/tacan.csv'

    # Utilisez la bibliothèque CSV pour lire le fichier CSV et insérer les données dans la table
    with open(fichier_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        # next(csvreader)  # Pour ignorer la ligne d'en-tête si elle existe dans le fichier CSV
        data = list(csvreader)
        for row in data:
            # Insérez les données du CSV dans la table
            cursor.execute('''INSERT INTO tacan (id, icaocode, identifiant, nom, latitude, longitude, aeroport,
             icaoaeroport, magneticvariation, datum, firidentifier, uiridentifier, seindicator, sedate, elevation, 
             frequence, frequenceprotection, biais, navaidmerit)
             VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)

    # Spécifiez le chemin vers le fichier CSV
    fichier_csv = 'data/csv/vor.csv'

    # Utilisez la bibliothèque CSV pour lire le fichier CSV et insérer les données dans la table
    with open(fichier_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        # next(csvreader)  # Pour ignorer la ligne d'en-tête si elle existe dans le fichier CSV
        data = list(csvreader)
        for row in data:
            # Insérez les données du CSV dans la table
            cursor.execute('''INSERT INTO vor (id, icaocode, identifiant, nom, latitude, longitude, aeroport,
             icaoaeroport, magneticvariation, datum, firidentifier, uiridentifier, seindicator, sedate, elevation, 
             frequence, facilitycharacteristics, frequenceprotection, navaidmerit)
             VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)

    # Spécifiez le chemin vers le fichier CSV
    fichier_csv = 'data/csv/vordme.csv'

    # Utilisez la bibliothèque CSV pour lire le fichier CSV et insérer les données dans la table
    with open(fichier_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        # next(csvreader)  # Pour ignorer la ligne d'en-tête si elle existe dans le fichier CSV
        data = list(csvreader)
        for row in data:
            # Insérez les données du CSV dans la table
            cursor.execute('''INSERT INTO vordme (id, icaocode, identifiant, nom, latitude, longitude, aeroport,
             icaoaeroport, magneticvariation, datum, firidentifier, uiridentifier, seindicator, sedate, elevation,
              identifiantdme, latitudedme, longitudedme, frequence, frequenceprotection, biais, navaidmerit)
             VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)

    # Spécifiez le chemin vers le fichier CSV
    fichier_csv = 'data/csv/waypoint.csv'

    # Utilisez la bibliothèque CSV pour lire le fichier CSV et insérer les données dans la table
    with open(fichier_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        # next(csvreader)  # Pour ignorer la ligne d'en-tête si elle existe dans le fichier CSV
        data = list(csvreader)
        for row in data:
            # Insérez les données du CSV dans la table
            cursor.execute('''INSERT INTO waypoint (id, icaocode, identifiant, nom, latitude, longitude, aeroport, 
            icaoaeroport, magneticvariation, datum, firidentifier, uiridentifier, seindicator, sedate, elevation, 
            type, usage)
             VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)
   # Validez les changements et fermez la connexion à la base de données
    connexion.commit()
    connexion.close()