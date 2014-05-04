import sfml as sf
from math import*
from random import*

##################################################
##                   KASSBRIK                   ##
##           Spécialité ISN 2013/2014           ##
##     Python 3.3.0 et pySFML nécessaires       ##
## -------------------------------------------- ##
##               MROCZKOWSKI Hugo               ##
##              GILLET Yann-Edern               ##
##               CAYETANOT Adrien               ##
##################################################

ligne=[[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1]] #Création du tableau de briques
briqueSprt = [] #Servira à stocker les sprites des briques
couleur = [] #Servira à stocker les couleurs
sonLigne = [] #Servira à stocker les sons des lignes de briques
   
# - Affichage des briques -
def afficherBriques():
    for l in range(0, 5):
        for i in range(0, 7):
            if (ligne[l][i]==1): #Si la brique éxiste, alors...
                briqueSprt[4-l].position = sf.Vector2(i*64, l*32) #place la brique à la bonne place
                fenetre.draw(briqueSprt[4-l]) #puis la dessine sur la surface de rendu

# - Affichage du pad -
def afficherPad():
    global padX
    #padX = sprtBalle.position.x - 32 #<-- Supprimez le "#" au début de la ligne pour avoir le pad automatique
    sprtPad.position = sf.Vector2(padX,284) #positionne le pad sur la surface de rendu
    fenetre.draw(sprtPad) #puis le dessine sur la surface de rendu

# - Affichage de la balle -
def afficherBalle():
    global balleAngle, score, fini, padded
    if (sprtBalle.position.x > 438): #Vérifie si la balle touche le bord droit
        padded = False #La balle n'a pas touché le pad
        sonMur.play() #Joue le son du mur
        balleAngle=pi-balleAngle #Change l'angle de la balle pour effectuer le rebond
    elif (sprtBalle.position.x<=0): #Vérifie si la balle touche le bord gauche
        padded = False #La balle n'a pas touché le pad
        sonMur.play() #Joue le son du mur
        balleAngle=pi-balleAngle #Change l'angle de la balle pour effectuer le rebond
    elif (sprtBalle.position.y <= 0): #Vérifie si la balle touche le bord supérieur
        padded = False #La balle n'a pas touché le pad
        sonMur.play() #Joue le son du mur
        balleAngle=-balleAngle #Change l'angle de la balle pour effectuer le rebond
    elif (sprtBalle.position.y >= 274) and (sprtBalle.position.x >= padX - 5) and (sprtBalle.position.x <= (padX)+64) and (padded == False): #Vérifie si la balle touche le pad
        padded = True #La balle A pas touché le pad, elle doit toucher autre chose pour recommencer
        sonMur.play() #Joue le son du mur (dans le cas présent, il est identique à celui du pad)
        balleAngle=-balleAngle #Change l'angle de la balle pour effectuer le rebond

    if (sprtBalle.position.y >= 290) and (fini == False): #Vérifie si on a perdu
        fini = True #La partie se bloque
        sonDefaite.play() #Joue le son de la défaite
        statutText.string = "Perdu !" #Affiche "perdu" à l'écran
        statutText.position = (224 - statutText.global_bounds.width / 2, 180) #Positionne perdu sur la surface de rendu
        statutText.color = couleur[randint(0,4)] #Le message prend une couleur (de brique/balle) aléatoire
        
    if not fini: sprtBalle.move((3*cos(balleAngle), 3*sin(balleAngle))) #Effectue le déplacement de la balle
    for l in range(0, 5):
        for i in range(0, 7):
            if (sprtBalle.position.x >= (i * 64)-10) and (sprtBalle.position.x <= (i+1)*64) and (sprtBalle.position.y >= (l*32)-10) and (sprtBalle.position.y <= (l+1)*32): #Vérifie si on touche la zone d'une brique
                if(ligne[l][i] == 1): #Si il y a une brique, alors...
                    sonLigne[l].play() #Joue le son, EN FONCTION DE LA LIGNE TOUCHEE
                    padded = False #La balle n'a pas touché de la pad
                    sprtBalle.color=couleur[l] #La balle prend la couleur de la brique cassée
                    balleAngle= -balleAngle #L'angle est modifié pour que la balle rebondisse sur la brique
                    score += (5-l) #On augmente le score en fonction de la hauteur de la brique cassée
                    scoreText.string = ("Score : " + str(score)) #On affiche le score sur la surface de rendu
                ligne[l][i] = 0 #On supprime la brique du tableau
    fenetre.draw(sprtBalle) #On déssine la balle sur la surface de rendu
    
# - Création de la fenêtre -
fenetre = sf.RenderWindow(sf.VideoMode(448, 300), "Kassbrik") #Création d'une fenêtre de 448px par 300px
fenetre.vertical_synchronization = True #Permet de limiter les FPS (images par seconde) en fonction de la charge du processeur

# - Variables de jeu -
padX = 192 #Position de départ du pad (centré)
balleAngle = (pi/3) #Angle de départ de la balle
score = 0 #Le score est nul au lancement du jeu
fini = False #La partie n'est pas terminée, elle commence
padded = False #On n'a pas encore touché le pad

# - Chargement des sons -
sonDefaite = sf.Sound(sf.SoundBuffer.from_file("Sons/gameover.wav")) #On charge le son de défaite en mémoire pour l'utiliser plus tard
sonVictoire = sf.Sound(sf.SoundBuffer.from_file("Sons/victoire.wav")) #On charge le son de victoire en mémoire pour l'utiliser plus tard
sonMur = sf.Sound(sf.SoundBuffer.from_file("Sons/mur.wav")) #On charge le son du mur/pad en mémoire pour l'utiliser plus tard
for i in range(0, 5):
    sonLigne.append(sf.Sound(sf.SoundBuffer.from_file("Sons/ligne" + str(i) +".wav"))) #On charge le son de chaque ligne en mémoire pour les utiliser plus tard

# - Initialisation du moteur de texte -
police = sf.Font.from_file("C:\Windows\Fonts\Arial.ttf") #Chargement de la police d'écriture
scoreText = sf.Text() #Création de l'objet texte pour le score
scoreText.font = police #Définition de sa police (c'est celle chargée)
scoreText.character_size = 15 #Définition de la taille des caractères
scoreText.position = (0,0) #Définition de sa position
scoreText.color = sf.Color.WHITE #Définition de sa couleur
scoreText.string = "Score : 0" #Définition du texte de départ
statutText = sf.Text() #Création de l'objet texte pour afficher la victoire/défaite
statutText.font = police #Définition de sa police (c'est celle chargée)
statutText.character_size = 40 #Définition de la taille des caractères
statutText.position = (0,0) #Définition de sa position de départ
statutText.color = sf.Color.WHITE #Définition de sa couleur de départ

# - Initialisation des textures et sprites -
briqueSprt.append(sf.Sprite(sf.Texture.from_file("Briques/violette.png"))) #Ajoute les sprites des briques à la liste briqueSprt
briqueSprt.append(sf.Sprite(sf.Texture.from_file("Briques/bleue.png"))) 
briqueSprt.append(sf.Sprite(sf.Texture.from_file("Briques/verte.png")))
briqueSprt.append(sf.Sprite(sf.Texture.from_file("Briques/orange.png")))
briqueSprt.append(sf.Sprite(sf.Texture.from_file("Briques/rouge.png")))

sprtPad = sf.Sprite(sf.Texture.from_file("pad.png")) #Créé le sprite du pad

sprtBalle = sf.Sprite(sf.Texture.from_file("balle.png")) #Créé le sprite de la balle
sprtBalle.position = sf.Vector2(170,200) #Défini la position de départ de la balle

# - Initialisation des couleurs -
couleur.append(sf.Color(164,71,61)) #Ajoute les couleurs des briques dans la liste couleur
couleur.append(sf.Color(216,115,35))
couleur.append(sf.Color(71,171,126))
couleur.append(sf.Color(54,111,180))
couleur.append(sf.Color(143,81,167))

# - Rafraichissement de la surface de jeu -
while fenetre.is_open: #Tant que la fenêtre SFML est ouvert...
 
	# Gestion des évènements SFML
    for event in fenetre.events: #Scane tous les évènements 1 par 1 pour les traiter
	    # Fermeture
            if type(event) is sf.CloseEvent:
                fenetre.close()
    	    
            # Touches
            if type(event) is sf.KeyEvent and event.pressed and event.code is sf.Keyboard.RIGHT: #flèche droite
                if (padX < 383) and  (fini == False): #Peut-on déplacer la balle (la balle ne va pas sortir par la droite et la partie n'est pas finie)
                    padX=padX+12

            if type(event) is sf.KeyEvent and event.pressed and event.code is sf.Keyboard.LEFT: #flèche gauche
                if (padX > 0) and (fini == False): #Peut-on déplacer la balle (la balle ne va pas sortir par la gauche et la partie n'est pas finie)
                    padX=padX-12


    fenetre.clear(sf.Color(120, 120, 120)) #Vide la fenêtre avec du gris
    afficherBriques() #Lance l'affichage des briques
    afficherPad() #Lance l'affichage du pad
    afficherBalle() #Lance l'affichage de la balle
    fenetre.draw(scoreText) #Affiche le score
    fenetre.draw(statutText) #Affiche le statut de la partie (même s'il est vide)

    # Affiche le rendu à l'utilisateur
    fenetre.display() #Affiche d'un seul coup la surface de rendu sur laquelle l'ensemble des élements a été dessiné

    if (score == 105) and (fini == False): #Vérifie si on a gagné (score max + partie pas encore finie)
        fini = True #Partie finie
        sonVictoire.play() #Joue le son de victoire
        statutText.string = "Victoire !" #Affiche "Victoire !" à l'écran
        statutText.position = (224 - statutText.global_bounds.width / 2, 130 - statutText.global_bounds.height / 2) #Positionne le texte sur la surface de rendu
        statutText.color = couleur[randint(0,4)] #Le message prend une couleur (de brique/balle) aléatoire
