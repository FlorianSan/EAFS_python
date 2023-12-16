# FPLN LEGS

Lemodule LEGS necessite l'installation préalable de la navigation database. Pour ce  faire, se reporter au install.sh du module FMS.

################################################### INTERFACE GRAPHIQUE ################################################### 

Pour le moment aucune IHM n'a été implémentée. L'interface avec le pilote se fait à travers la console. Cette console réponds cependant à toutes les fonctions principales de l'IHM legs du FMS.

		######################################## Menu principal ######################################## 

Le menu principal s'affiche au lancement du programme:

""""
Console:
	1 - Afficher ListLeg
	2 - Afficher Route
	3 - Modifier Leg
""""

1 - Permet d'afficher la liste de legs qui constituent le plan de vol. (cf Affichage ListLeg)
2 - Permet l'affichage de la liste des sections qui constitue la route. (cf Affichage Route)
3 - Ouvre le menu de modification du plan de vol par le pilote. (cf Menu Modification)


		######################################## Affichage ListLeg ######################################## 

Appuyer sur '1' sur le menu principal affiche la liste de leg comme suit (à la condition qu'elle ait été initialisée précédemment):

""""
-> SEQ=0 TYPE=IF ID=LFBO LAT=N43380646 LONG=E001220428
SEQ=1 TYPE=TF ID=FISTO WPT_TYPE=Flyby LAT=N44274100 LONG=E001133800 COURSE=356 DISTANCE=53 FLmin=FL000 FLmax=FL195
SEQ=2 TYPE=TF ID=PERIG WPT_TYPE=Flyby LAT=N45070200 LONG=E000581000 COURSE=333 DISTANCE=53 FLmin=FL195 FLmax=FL460
SEQ=3 TYPE=TF ID=DIBAG WPT_TYPE=Flyby LAT=N45472200 LONG=E000471500 COURSE=349 DISTANCE=24 FLmin=FL195 FLmax=FL460
SEQ=4 TYPE=TF ID=TUDRA WPT_TYPE=Flyby LAT=N46322000 LONG=E000465100 COURSE=359 DISTANCE=50 FLmin=FL000 FLmax=FL460
SEQ=5 TYPE=TF ID=BEVOL WPT_TYPE=Flyby LAT=N47004300 LONG=E000555100 COURSE=5 DISTANCE=41 FLmin=FL195 FLmax=FL285
SEQ=6 TYPE=TF ID=AMB WPT_TYPE=Flyby LAT=N47254400 LONG=E001035190 COURSE=52 DISTANCE=24 FLmin=FL195 FLmax=FL285
SEQ=7 TYPE=TF ID=LFPO WPT_TYPE=Flyby LAT=N48432381 LONG=E002224648 COURSE=33 DISTANCE=85 FLmin=FL000 FLmax=FL195
""""

La première leg est une leg IF qui informe sur l'aéroport de départ.
Les autres sont des legs TF avec un path et un terminator.

L'icone "->" indique la leg active.

		######################################## Affichage Route ######################################## 

Appuyer sur '2' sur le menu principal affiche la liste des sections constituant la route comme suit (à la condition qu'elle ait été initialisée précédemment):

""""
Departure:LFBO Arrival:LFPO route: [('DIRECT', 'FISTO'), ('UY156', 'PERIG'), ('UT210', 'TUDRA'), ('UT158', 'AMB'), ('DIRECT', 'STAR')]
""""

Departure = identifiant  aeroport de départ
Arrival = identifiant de l'aéroport d'arrivée
route: liste des sections de la route liant les deux aéroport.

Une section de route prends les formes suivantes:
	- Dans le cas d'un direct vers un waypoint: ('DIRECT', 'ID waypoint terminal')
	- Dans le cas d'un airways : ('ID de l'airway', 'Id du waypoint de sortie d'airway'). Le waypoint d'entrée de l'airway est par défaut le dernier waypoint de la section précédente.
	- Dans le cas d'un direct vers l'aéroport d'arrivée: ('DIRECT', 'STAR')


		######################################## Menu Modification ######################################## 

Remarque:
Il n'est pas permis d'effectuer des modifications sur les aéroports d'arrivée et de départ ainsi que la leg active et les legs déjà séquencées (antérieures à la leg active)

"""""
0 - Retour au menu principal
1 - Insertion
2 - Suppression
3 - Modification
"""""

0 - Permet de retourner au menu principal
1 - Permet d'insérer un waypoint entre deux autres
2 - Permet de supprimer un waypoint (donc une leg) du plan de vol
3 - Permet de choisir le type de waypoint: flyover ou flyby

Exemples:

* 1 - Insertion

	"""""
	Entrer le numéro de séquence du leg précédent l'insertion
	"""""
	* On entre le numéro de séquence du leg après lequel on veut inserer notre waypoint. Ici par exemple "2"
		
	"""""
	Entrer le WPT à inserer
	"""""
	* On entre l'identifiant du waypoint qe l'on veut inserer. Ici par exemple "NORON"

* 2 - Suppression

	"""""
	Entrer le numéro de séquence du leg à supprimer
	"""""
	* On entre le numéro de sequence de la leg que l'on veut supprimer. Par exemple "2".

* 3 - Modification
	
	"""""
	Entrer le numéro de séquence du leg à modifier
	"""""
	*On entre le numéro de sequence de la leg que l'on veut modifier. Par exemple "5".
	
	"""""
	1 - Flyby 
	2 - Flyover
	"""""
	* On choisi le type de waypoint voulu en entrant "1" ou "2".




		######################################## Affichage des messages IvyBus ######################################## 

Afin de faciliter la compréhension des communications avec les autres modules via IvyBus, à chaque fois que le module LEGS envoit un message, il l'affiche également en console.



################################################### ISimuations de messages IvyBus en entrée ################################################### 

Pour des phases de tests ou de développement, il peut être utile de simuler les messages des autres modules.
Pour ce faire nous utilisons le logiciel IvyProbe qui permet d'envoyer des messages sur le canal ainsi que la bibliothèque de message suivante:

#Message de prévention de l'envoi du message d'initialisation par le module Route
FR_Ready Time=time Initial Flight Plan Ready

#Message d'initialisation du flight plan par le module Route
FR_InitFlightPlan Time=0.0 FROM=LFBO TO=LFPO ROUTE=DIRECT-FISTO, UY156-PERIG, UT210-TUDRA, UT158-AMB, DIRECT-STAR

#Message de séquencement de la leg active par le module SEQ
GS_AL Time=time NumSeqActiveLeg=1

#Message de prévention de l'envoi du message de modification par le module Route
FR_ModifReady Time=0 Modified Flight Plan Ready

#Message de modification d'un partie de la route par le module ROUTE
FR_Modif Time=0 numStart=1 numEnd=2 modifiedSection=UY156-ADABI, DIRECT-NORON, DIRECT-DIBAG, UT210-TUDRA

#Message de retour d'erreur de transmission de la modification de la route par LEGS.
FR_ERROR Time=0 Error Receiving Modified Route



 


 