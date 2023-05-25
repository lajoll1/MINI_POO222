import xml.etree.ElementTree as ET
'_______________________Règles________________________''_______________________Règles________________________''_______________________Règles________________________'



class Regle():
    def __init__(self,mon_nom,ma_description,ma_condition):
        if isinstance(mon_nom, str) and isinstance(ma_description, str) and (isinstance(ma_condition, Condition_Simple) or isinstance(ma_condition, Condition_Composee)):
            self._nom_regle = mon_nom
            self._description_regle = ma_description
            self._condition_associe = ma_condition

    def posture_activees():
        pass

    def is_activated(self,posture):
        if isinstance(posture, Posture) or isinstance(posture, Posture):
            print("Vérification de l'activation de la règle {} ".format(posture))
        return self._condition_associe.is_activated(posture) 
   
'________Definition_classe_Condition_Simple________'

class Condition_Simple():

    # Valeur par défaut pour le seuil si domaine préféré
    #liste retenue plutôt que *var et nombre infini de tuples en entrée
    def __init__(self, parameters_list):
        #Pas de vérification des types car le fichier est supposé idéal
        self._param_dict=dict()
        for mon_tuple in parameters_list:
            duo_modifiable=list(mon_tuple)
            #conversion des types
            if duo_modifiable[0] == "threshold":
                duo_modifiable[1]=float(mon_tuple[1])
                print("threshold converted. New value {} and type {}".format(duo_modifiable[1],type(duo_modifiable[1])))
            if duo_modifiable[0] == "domain":
                duo_modifiable[1]=str(duo_modifiable[1]).removeprefix('(').removesuffix(")")
                duo_modifiable[1] = tuple([float (x) for x in duo_modifiable[1].split(",")])
                print("domain converted. New value {} and type {}".format(duo_modifiable[1],type(duo_modifiable[1][0])))
            
            if duo_modifiable[0]== "first_corner":
                duo_modifiable[1]=str(duo_modifiable[1]).removeprefix('(').removesuffix(")")
                duo_modifiable[1] = tuple([float (x) for x in duo_modifiable[1].split(",")])
                print("domain converted. New value {} and type {}".format(duo_modifiable[1],type(duo_modifiable[1][0])))
            
            if duo_modifiable[0]== "second_corner":
                duo_modifiable[1]=str(duo_modifiable[1]).removeprefix('(').removesuffix(")")
                duo_modifiable[1] = tuple([float (x) for x in duo_modifiable[1].split(",")])               

            self._param_dict.update({duo_modifiable[0]:duo_modifiable[1]})
            print("Dictionnaire mis à jour avec la clef {} et la valeur {} de type {}".format(duo_modifiable[0],duo_modifiable[1],type(duo_modifiable[1])))

    def _obtenir_depuis_posture(self,posture):
        if self._param_dict.get("target") == "angle": return posture.obtenir(self._param_dict.get("target_joint")).angle
        elif self._param_dict.get("target") == "pos":
            #projection ou vérification 3D?
            if "direction" in self._param_dict.keys():
                #Implique une projection donc disjonction de cas selon l'axe
                #cas avec un angle ?
                #TODO: tratier le cas Domain si projection
                if self._param_dict.get("direction") == "X":
                    return posture.obtenir(self._param_dict.get("target_joint")).position[0]
                elif self._param_dict.get("direction") == "Y":
                    return posture.obtenir(self._param_dict.get("target_joint")).position[1]
                    #Récupère la 2e coordonnée et la return
                elif self._param_dict.get("direction") == "Z":
                    return posture.obtenir(self._param_dict.get("target_joint")).position[2]
                else:
                    return "Axe non-reconnu"
            else: #forcément de type "belongs to the volume"
                return posture.obtenir(self._param_dict.get("target_joint")).position

    # bool is_activated(class self, posture posture_a_verifier)
    def is_activated(self, posture_a_verifier):
        if isinstance(posture_a_verifier, Posture): 
            
                # Droit d'accéder par élément car dans la classe
                #obtenir_angle_depuis_posture doit être complexifié et prendre en compte le cas où projection
                if self._param_dict.get("condition_type") == "lower than":
                    if self._obtenir_depuis_posture(posture_a_verifier) < self._param_dict.get("threshold"): return True
                elif self._param_dict.get("condition_type") == "greater than":
                    if  self._obtenir_depuis_posture(posture_a_verifier) > self._param_dict.get("threshold"): return True
                elif self._param_dict.get("condition_type") == "belongs to": 
                    if  self._param_dict.get("domain")[0] < self._obtenir_depuis_posture(posture_a_verifier) < self._param_dict.get("domain")[1]: return True
                elif self._param_dict.get("condition_type") == "belongs to the volume":
                    print("Coordonnées de la posture obtenues {}".format(self._obtenir_depuis_posture(posture_a_verifier)))
                    x,y,z = self._obtenir_depuis_posture(posture_a_verifier)[0],self._obtenir_depuis_posture(posture_a_verifier)[1],self._obtenir_depuis_posture(posture_a_verifier)[2]
                    print("Test de l'appartenance au volume")
                    print("Valeurs de x,y,z {} {} {}".format(x,y,z))
                    print("First corner {} and second corner {}".format(self._param_dict.get("first_corner"),self._param_dict.get("second_corner")))
                    if self._param_dict.get("first_corner")[0] < x < self._param_dict.get("second_corner")[0] and \
                       self._param_dict.get("first_corner")[1] < y < self._param_dict.get("second_corner")[1] and \
                       self._param_dict.get("first_corner")[2] < z <  self._param_dict.get("second_corner")[2]:
                        return True
                #Nouveau if selon les éléments présents dans le dictionnaire
        return False # Si l'on arrive ici, aucune des conditions précédentes n'est vérifiée
        # bool superieur_A_Un_Seuil()

    def _get_param_dict(self):
        print("Passage par l'accesseur de dictionnaire")
        return self._param_dict

    param_dict_val = property(_get_param_dict)
'_______Definition_classe_Condition_Composee_______'


class Condition_Composee():
    
    # Condition_composée __init__(class self, string operateur, list ma_condition_composee)
    def __init__(self, mon_operateur,ma_liste_de_conditions_simples):
        if mon_operateur in {"or","and"}:
            self._operator = mon_operateur
        # Prendre en compte le fait qu'il y ait potentiellement n conditions simples dans la condition complexe
            self._liste_conditions_simples=[] # Liste en partaeg de pointeurs
            for x in ma_liste_de_conditions_simples:
                if isinstance(x, Condition_Simple):
                    self._liste_conditions_simples.append(x)

    # bool is_activated(class self, class posture)                
    def is_activated(self, ma_posture):
        if isinstance(ma_posture, Posture):
            # Assez flexible pour supporter de nouveaux opérateurs en ajoutant en elif
            if self._operator == "and":
                for condition_simple in self._liste_conditions_simples:
                    if condition_simple.is_activated(ma_posture) == False: return False
                    return True
            # Vérifier toutes les conditions les unes après les autres et renvoyer False si l'une n'est pas vérifiée     
            elif self._operator == "or":
                for condition_simple in self._liste_conditions_simples:
                    if condition_simple.is_activated(ma_posture): return True
                return False
                # Renvoyer true à la premirèe condition vérifiée


'_____________Importation_des_règles______________'
    
def importer_regle(chemin_d_acces_fichier_regles):
    arbreXML= ET.parse(chemin_d_acces_fichier_regles)
    tronc = arbreXML.getroot()

    # Dictionnaire de la forme {"nom_règle" : pointeur_de_la_règle_associée}
    regles = dict()

    for rule in tronc.iter('rule'):

        if rule[0].tag == "simple_condition":

            print("argument envoyé {}".format([mon_tuple for mon_tuple in rule[0].items()]))
            ma_condition_simple=Condition_Simple([mon_tuple for mon_tuple in rule[0].items()])   #conversion de type à vérifier  
            #dictionnaire qui prend des arguments au format {nom_variable_initialisée:valeur_variable_initialisée}
            print("Condition simple {} de paramètres {} générée".format(ma_condition_simple,ma_condition_simple.param_dict_val))
            regles.update({rule.get('name'):Regle(rule.get('name'),rule.get('description'),ma_condition_simple)})
            
        elif rule[0].tag == "composed_condition":
           
            liste_conditions_simples = []
            
            print("Début de la règle composée {} de description {}".format(rule.get('name'),rule.get("description")))

            for simple_condition in rule[0].iter("simple_condition"):
                    
                    print("argument envoyé {}".format([mon_tuple for mon_tuple in simple_condition.items()]))
                    ma_condition_simple=Condition_Simple([mon_tuple for mon_tuple in simple_condition.items()])
                    liste_conditions_simples.append(ma_condition_simple) #Liste de dictionnaire. Oui c'est moche.
                    print("Fait")

            print("Opérateur logique: {}".format(rule[0].get("operator")))
            print("liste de conditions simples finale: {}".format(liste_conditions_simples)) 
            ma_condition_composee=Condition_Composee(rule[0].get("operator"),liste_conditions_simples)
            regles.update({rule.get('name'):Regle(rule.get('name'),rule.get('description'),ma_condition_composee)})
            
            


    print(regles)
    return regles





import math
import numpy as np

'________________Ouverture_fichier_XML________________'

xml_file = "/Users/virgilejamot/Documents/GitHub/MINI_POO222/Postures_captures.xml"

arbreXML = ET.parse(xml_file)
tronc = arbreXML.getroot()



'____________Definition_classe_Articulation___________'

class Articulation():
    def __init__(self,tonnom,taposition,taposture,tonvoisindavant,tesvoisinsdapresXML):
        self._tonnom = str(tonnom)
        self._taposition = [float(num) for num in taposition.strip('()').split(',')]
        self._taposture = int(taposture)
        self._voisinsXML = {"P":tonvoisindavant,"N":tesvoisinsdapresXML}
        
        
    def _lire_nom(self):
        return self._tonnom
    def _lire_position(self):
        return self._taposition
    def _lire_posture(self):
        return self._taposture
    def _lire_voisinsXML(self):
        return self._voisinsXML
    
    nom = property(_lire_nom)
    position = property(_lire_position)
    posture = property(_lire_posture)
    voisinsXML = property(_lire_voisinsXML)

    def _trouver_voisinsPOO(self):
        parent = None
        enfants = []
        for articulation in sequence.postures[self.posture].articulations:
            if _trouver_parent(tronc,self.voisinsXML["P"])!=tronc:
                if articulation.nom == self.voisinsXML["P"].attrib["Name"]:
                    parent = articulation
            else:
                parent = None
                
            for enfantXML in self.voisinsXML["N"]:
                if articulation.nom == enfantXML.attrib["Name"]:
                    enfants.append(articulation)
        return (parent,enfants)
    voisinsPOO = property(_trouver_voisinsPOO)

    def _trouver_voisins_temporels(self):
        voisins = []
        if self.posture == 0:
            voisins.append(None)
            voisins.append(None)
            voisins.append(sequence.search(self.nom,1))
            voisins.append(None)
            
        elif self.posture == 1:
            voisins.append(None)
            voisins.append(sequence.search(self.nom,0))
            voisins.append(sequence.search(self.nom,2))
            voisins.append(sequence.search(self.nom,3))
            
        elif self.posture == len(sequence.postures)-1:
            voisins.append(None)
            voisins.append(sequence.search(self.nom,len(sequence.postures)-2))
            voisins.append(None)
            voisins.append(None)

        elif self.posture == len(sequence.postures)-2:
            voisins.append(sequence.search(self.nom,len(sequence.postures)-4))
            voisins.append(sequence.search(self.nom,len(sequence.postures)-3))
            voisins.append(sequence.search(self.nom,len(sequence.postures)-1))
            voisins.append(None)

        else :
            voisins.append(sequence.search(self.nom,self.posture-2))
            voisins.append(sequence.search(self.nom,self.posture-1))
            voisins.append(sequence.search(self.nom,self.posture+1))
            voisins.append(sequence.search(self.nom,self.posture+2))
      
        return voisins
    voisins_t = property(_trouver_voisins_temporels)

    def _calculer_angle(self):
        if len(self.voisinsPOO) == 2 and len(self.voisinsPOO[1])==1 :
            x1,y1,z1 = ((self.voisinsPOO[0]).position)[0],((self.voisinsPOO[0]).position)[1],((self.voisinsPOO[0]).position)[2]
            x2,y2,z2 = (self.position)[0],(self.position)[1],(self.position)[2]
            x3,y3,z3 = ((self.voisinsPOO[1][0]).position)[0],((self.voisinsPOO[1][0]).position)[1],((self.voisinsPOO[1][0]).position)[2]

            # Calcule les vecteurs AB et BC
            AB = (x2 - x1, y2 - y1, z2 - z1)
            BC = (x3 - x2, y3 - y2, z3 - z2)

            # Calcule les normes des vecteurs AB et BC
            norm_AB = math.sqrt(AB[0]**2 + AB[1]**2 + AB[2]**2)
            norm_BC = math.sqrt(BC[0]**2 + BC[1]**2 + BC[2]**2)

            # Calcule le produit scalaire des vecteurs AB et BC
            dot_product = AB[0] * BC[0] + AB[1] * BC[1] + AB[2] * BC[2]

            # Calcule l'angle entre les vecteurs AB et BC en radians
            angle_rad = math.acos(dot_product / (norm_AB * norm_BC))

            # Convertit l'angle en degrés
            angle_deg = math.degrees(angle_rad)
            return 180 - angle_deg

        else :
            print("Extrémité ou main !")
            return None
        
    angle = property(_calculer_angle)

    def _calculer_v_a_angulaire(self):
        dt = 1/1.2
        vitesse_ang,acceleration_ang = 0,0

        if self.posture not in [0,len(sequence.postures)-1]:
            angle_0 = self.voisins_t[1].angle
            angle_1 = self.voisins_t[2].angle
        
            vitesse_ang = (angle_1 - angle_0)/(2*dt)

        if self.posture not in [0,1,len(sequence.postures)-1,len(sequence.postures)-2]:
            angle_0 = self.voisins_t[0].angle
            angle_1 = self.angle
            angle_2 = self.voisins_t[3].angle

            acceleration_ang = (angle_2 + angle_0 - 2*angle_1)/(4*dt)

        return vitesse_ang,acceleration_ang

    va_ang = property(_calculer_v_a_angulaire)

    def _calculer_v_a_moyenne(self):    # Détermination des vecteurs vitesse et accélération 
        dt = 1/1.2
        
        if self.posture != 0 and self.posture != 57: # Ne fonctionne pas pour les postures extrémales
            
            # Coordonnées 3D des points dans le temps
            x = [self.voisins_t[1].position[0],self.voisins_t[2].position[0]]
            y = [self.voisins_t[1].position[1],self.voisins_t[2].position[1]]
            z = [self.voisins_t[1].position[2],self.voisins_t[2].position[2]]

            # Calcul des vecteurs vitesse
            vitesse = []
            vitesse.append((x[1]-x[0])/(2*dt))
            vitesse.append((y[1]-y[0])/(2*dt))
            vitesse.append((z[1]-z[0])/(2*dt))
            norme_vitesse = np.sqrt(vitesse[0]**2+vitesse[1]**2+vitesse[2]**2)
            
        else:
            vitesse = [0,0,0]
            norme_vitesse = 0

        if self.posture > 1 and self.posture < 56:

            # Coordonnées 3D des points dans le temps
            x = [self.voisins_t[0].position[0],self.position[0],self.voisins_t[3].position[0]]
            y = [self.voisins_t[0].position[1],self.position[1],self.voisins_t[3].position[1]]
            z = [self.voisins_t[0].position[2],self.position[2],self.voisins_t[3].position[2]]
            # Calcul des vecteurs accélération
            acceleration = []
            acceleration.append((x[0]+x[2]-2*x[1])/(4*dt))
            acceleration.append((y[0]+y[2]-2*y[1])/(4*dt))
            acceleration.append((z[0]+z[2]-2*z[1])/(4*dt))
            norme_acceleration = np.sqrt(acceleration[0]**2+acceleration[1]**2+acceleration[2]**2)
            
        else:
            acceleration = [0,0,0]
            norme_acceleration = 0
        return vitesse, acceleration, norme_vitesse, norme_acceleration

    va_moy = property(_calculer_v_a_moyenne)


    
'______________Definition_classe_Posture_____________'

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as mp

class Posture():
    def __init__(self,tonnumero,tesarticulations):
        self._tonnumero = int(tonnumero)
        self._tesarticulations = list(tesarticulations)

    def regles_activees(self):
        liste_regles_activees_par_posture=list()
        for regle in regles.values():
            print("règle utilisée: {}".format(regle))
            if regle.is_activated(self):
                liste_regles_activees_par_posture.append(regle)
        return liste_regles_activees_par_posture 

    def _lire_numero(self):
        return self._tonnumero
    def _lire_articulations(self):
        return self._tesarticulations

    numero = property(_lire_numero)
    articulations = property(_lire_articulations)
    
    def obtenir(self,nom_articulation):
        for articulation in self.articulations :
            if articulation.nom == nom_articulation:
                return articulation

    def tracer(self,call):

        # Création de la figure
        def set_axes_equal(ax):
            
            x_limits = ax.get_xlim3d()
            y_limits = ax.get_ylim3d()
            z_limits = ax.get_zlim3d()

            x_range = abs(x_limits[1] - x_limits[0])
            x_middle = np.mean(x_limits)
            y_range = abs(y_limits[1] - y_limits[0])
            y_middle = np.mean(y_limits)
            z_range = abs(z_limits[1] - z_limits[0])
            z_middle = np.mean(z_limits)
                
            plot_radius = 0.5*max([x_range, y_range, z_range])

            ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
            ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
            ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.set_xlim(0, 1)
        ax.set_ylim(-0.6, 0.6) 
        ax.set_zlim(0, 2)
    
        bras_droit = ['Spine2','RightShoulder','RightArm','RightForeArm','RightHand']
        bras_gauche = ['Spine2','LeftShoulder','LeftArm','LeftForeArm','LeftHand']
        jambe_droite = ['Hips','RightUpLeg','RightLeg','RightFoot']
        jambe_gauche = ['Hips','LeftUpLeg','LeftLeg','LeftFoot']
        colonne = ['Hips','Spine','Spine1','Spine2','Neck','Neck1','Head']

        main_droite_pouce = ['RightHand','RightHandThumb1','RightHandThumb2','RightHandThumb3']
        main_droite_index = ['RightHand','RightInHandIndex','RightHandIndex1','RightHandIndex2','RightHandIndex3']
        main_droite_majeur = ['RightHand','RightInHandMiddle','RightHandMiddle1','RightHandMiddle2','RightHandMiddle3']
        main_droite_annulaire = ['RightHand','RightInHandRing','RightHandRing1','RightHandRing2','RightHandRing3']
        main_droite_petit = ['RightHand','RightInHandPinky','RightHandPinky1','RightHandPinky2','RightHandPinky3']

        main_gauche_pouce = ['LeftHand','LeftHandThumb1','LeftHandThumb2','LeftHandThumb3']
        main_gauche_index = ['LeftHand','LeftInHandIndex','LeftHandIndex1','LeftHandIndex2','LeftHandIndex3']
        main_gauche_majeur = ['LeftHand','LeftInHandMiddle','LeftHandMiddle1','LeftHandMiddle2','LeftHandMiddle3']
        main_gauche_annulaire = ['LeftHand','LeftInHandRing','LeftHandRing1','LeftHandRing2','LeftHandRing3']
        main_gauche_petit = ['LeftHand','LeftInHandPinky','LeftHandPinky1','LeftHandPinky2','LeftHandPinky3']

        chemin1 = [bras_droit,bras_gauche,jambe_droite,jambe_gauche,colonne]
        chemin2 = [main_droite_pouce,main_droite_index,main_droite_majeur,main_droite_annulaire,main_droite_petit]
        chemin3 = [main_gauche_pouce,main_gauche_index,main_gauche_majeur,main_gauche_annulaire,main_gauche_petit]   
        chemin = chemin1 + chemin2 + chemin3

        
        for ligne in chemin :
            x = [self.obtenir(articulation).position[0] for articulation in ligne]
            y = [self.obtenir(articulation).position[2] for articulation in ligne]
            z = [self.obtenir(articulation).position[1] for articulation in ligne]
            ax.scatter(x,y,z,c='r',marker = 'o')
            ax.plot(x,y,z,c='b')
                        
        # Configuration des axes
        ax.set_xlabel('X')
        ax.set_ylabel('Z')               
        ax.set_zlabel('Y')

        # Orientation de la vue
        ax.view_init(elev=15, azim=135)        
           
        # Affichage de la figure
        set_axes_equal(ax)
##        plt.show()

        return ax


'______________Definition_classe_Sequence_____________'

class Sequence():
    def __init__(self,tespostures):
        self._tespostures = list(tespostures) 

    def posture_activees(self,regle_a_tester):
        liste_postures_activant_la_regle=list()
        # Vérifier comment Virgile récupère chacune des postures de la séquence
        
        for posture in self.postures:
            if regle_a_tester.is_activated(posture):
                    liste_postures_activant_la_regle.append(posture)
            print("Vérification de l'activation de la règle à tester {} pour la posture {}".format(regle_a_tester,posture))
        return liste_postures_activant_la_regle

    def _lire_postures(self):
        return self._tespostures
    postures = property(_lire_postures)

    def search(self,nom_articulation,posture):
        for articulation in self.postures[posture].articulations:
            if articulation.nom == nom_articulation:
                return articulation



'________________________Main_________________________'

def _trouver_parent(tronc, element):    # Permet de trouver le parent XML d'un objet XML dans le fichier de Postures_captures.xml
    for enfant in tronc:
        if enfant is element:
            return tronc
        parent = _trouver_parent(enfant, element)
        if parent is not None:
            return parent
    return None

def _creer_postures_list():
    postures_list = []
    _posturePOO = 0
    c=0
    for _postureXML in tronc:
        articulations_list = []
        for _articulationXML in _postureXML.iter("Joint"):
            above_voisin = _trouver_parent(_postureXML,_articulationXML)
            below_voisin = _articulationXML.findall("Joint")
            _articulationPOO = Articulation(_articulationXML.get("Name"),_articulationXML.get("Position"),c,above_voisin,below_voisin)
            articulations_list.append(_articulationPOO)
        _posturePOO = Posture(c,articulations_list)
        postures_list.append(_posturePOO)
        c+=1
    return postures_list
    
sequence = Sequence(_creer_postures_list()) # Instanciation d'un objet sequence contenant toutes les postures

regles = importer_regle("/Users/virgilejamot/Documents/GitHub/MINI_POO222/rules_angles_et_positions_v1.3.xml")

print("test de la règle {}".format(regles["Bac_1"].is_activated(sequence.postures[15])))

print(sequence.postures[16].regles_activees())

print(sequence.posture_activees(regles.get("rule_2")))


##'_______________________Règles________________________''_______________________Règles________________________''_______________________Règles________________________'
##
##
##
##class Regle():
##    def __init__(self,mon_nom,ma_description,ma_condition):
##        if isinstance(mon_nom, str) and isinstance(ma_description, str) and (isinstance(ma_condition, Condition_Simple) or isinstance(ma_condition, Condition_Composee)):
##            self._nom_regle = mon_nom
##            self._description_regle = ma_description
##            self._condition_associe = ma_condition
##
##    def posture_activees():
##        pass
##
##    def is_activated(self,posture):
##        if isinstance(posture, Posture) or isinstance(posture, Posture):
##            print("Vérification de l'activation de la règle {} ".format(posture))
##        return self._condition_associe.is_activated(posture) 
##   
##'________Definition_classe_Condition_Simple________'
##
##class Condition_Simple():
##
##    # Valeur par défaut pour le seuil si domaine préféré
##    #liste retenue plutôt que *var et nombre infini de tuples en entrée
##    def __init__(self, parameters_list):
##        #Pas de vérification des types car le fichier est supposé idéal
##        self._param_dict=dict()
##        for mon_tuple in parameters_list:
##            duo_modifiable=list(mon_tuple)
##            #conversion des types
##            if duo_modifiable[0] == "threshold":
##                duo_modifiable[1]=float(mon_tuple[1])
##                print("threshold converted. New value {} and type {}".format(duo_modifiable[1],type(duo_modifiable[1])))
##            if duo_modifiable[0] == "domain":
##                duo_modifiable[1]=str(duo_modifiable[1]).removeprefix('(').removesuffix(")")
##                duo_modifiable[1] = tuple([float (x) for x in duo_modifiable[1].split(",")])
##                print("domain converted. New value {} and type {}".format(duo_modifiable[1],type(duo_modifiable[1][0])))
##            
##            if duo_modifiable[0]== "first_corner":
##                duo_modifiable[1]=str(duo_modifiable[1]).removeprefix('(').removesuffix(")")
##                duo_modifiable[1] = tuple([float (x) for x in duo_modifiable[1].split(",")])
##                print("domain converted. New value {} and type {}".format(duo_modifiable[1],type(duo_modifiable[1][0])))
##            
##            if duo_modifiable[0]== "second_corner":
##                duo_modifiable[1]=str(duo_modifiable[1]).removeprefix('(').removesuffix(")")
##                duo_modifiable[1] = tuple([float (x) for x in duo_modifiable[1].split(",")])               
##
##            self._param_dict.update({duo_modifiable[0]:duo_modifiable[1]})
##            print("Dictionnaire mis à jour avec la clef {} et la valeur {} de type {}".format(duo_modifiable[0],duo_modifiable[1],type(duo_modifiable[1])))
##
##    def _obtenir_depuis_posture(self,posture):
##        if self._param_dict.get("target") == "angle": return posture.obtenir(self._param_dict.get("target_joint")).angle
##        elif self._param_dict.get("target") == "pos":
##            #projection ou vérification 3D?
##            if "direction" in self._param_dict.keys():
##                #Implique une projection donc disjonction de cas selon l'axe
##                #cas avec un angle ?
##                #TODO: tratier le cas Domain si projection
##                if self._param_dict.get("direction") == "X":
##                    return posture.obtenir(self._param_dict.get("target_joint")).position[0]
##                elif self._param_dict.get("direction") == "Y":
##                    return posture.obtenir(self._param_dict.get("target_joint")).position[1]
##                    #Récupère la 2e coordonnée et la return
##                elif self._param_dict.get("direction") == "Z":
##                    return posture.obtenir(self._param_dict.get("target_joint")).position[2]
##                else:
##                    return "Axe non-reconnu"
##            else: #forcément de type "belongs to the volume"
##                return posture.obtenir(self._param_dict.get("target_joint")).position
##
##    # bool is_activated(class self, posture posture_a_verifier)
##    def is_activated(self, posture_a_verifier):
##        if isinstance(posture_a_verifier, Posture): 
##            
##                # Droit d'accéder par élément car dans la classe
##                #obtenir_angle_depuis_posture doit être complexifié et prendre en compte le cas où projection
##                if self._param_dict.get("condition_type") == "lower than":
##                    if self._obtenir_depuis_posture(posture_a_verifier) < self._param_dict.get("threshold"): return True
##                elif self._param_dict.get("condition_type") == "greater than":
##                    if  self._obtenir_depuis_posture(posture_a_verifier) > self._param_dict.get("threshold"): return True
##                elif self._param_dict.get("condition_type") == "belongs to": 
##                    if  self._param_dict.get("domain")[0] < self._obtenir_depuis_posture(posture_a_verifier) < self._param_dict.get("domain")[1]: return True
##                elif self._param_dict.get("condition_type") == "belongs to the volume":
##                    print("Coordonnées de la posture obtenues {}".format(self._obtenir_depuis_posture(posture_a_verifier)))
##                    x,y,z = self._obtenir_depuis_posture(posture_a_verifier)[0],self._obtenir_depuis_posture(posture_a_verifier)[1],self._obtenir_depuis_posture(posture_a_verifier)[2]
##                    print("Test de l'appartenance au volume")
##                    print("Valeurs de x,y,z {} {} {}".format(x,y,z))
##                    print("First corner {} and second corner {}".format(self._param_dict.get("first_corner"),self._param_dict.get("second_corner")))
##                    if self._param_dict.get("first_corner")[0] < x < self._param_dict.get("second_corner")[0] and \
##                       self._param_dict.get("first_corner")[1] < y < self._param_dict.get("second_corner")[1] and \
##                       self._param_dict.get("first_corner")[2] < z <  self._param_dict.get("second_corner")[2]:
##                        return True
##                #Nouveau if selon les éléments présents dans le dictionnaire
##        return False # Si l'on arrive ici, aucune des conditions précédentes n'est vérifiée
##        # bool superieur_A_Un_Seuil()
##
##    def _get_param_dict(self):
##        print("Passage par l'accesseur de dictionnaire")
##        return self._param_dict
##
##    param_dict_val = property(_get_param_dict)
##'_______Definition_classe_Condition_Composee_______'
##
##
##class Condition_Composee():
##    
##    # Condition_composée __init__(class self, string operateur, list ma_condition_composee)
##    def __init__(self, mon_operateur,ma_liste_de_conditions_simples):
##        if mon_operateur in {"or","and"}:
##            self._operator = mon_operateur
##        # Prendre en compte le fait qu'il y ait potentiellement n conditions simples dans la condition complexe
##            self._liste_conditions_simples=[] # Liste en partaeg de pointeurs
##            for x in ma_liste_de_conditions_simples:
##                if isinstance(x, Condition_Simple):
##                    self._liste_conditions_simples.append(x)
##
##    # bool is_activated(class self, class posture)                
##    def is_activated(self, ma_posture):
##        if isinstance(ma_posture, Posture):
##            # Assez flexible pour supporter de nouveaux opérateurs en ajoutant en elif
##            if self._operator == "and":
##                for condition_simple in self._liste_conditions_simples:
##                    if condition_simple.is_activated(ma_posture) == False: return False
##                    return True
##            # Vérifier toutes les conditions les unes après les autres et renvoyer False si l'une n'est pas vérifiée     
##            elif self._operator == "or":
##                for condition_simple in self._liste_conditions_simples:
##                    if condition_simple.is_activated(ma_posture): return True
##                return False
##                # Renvoyer true à la premirèe condition vérifiée
##
##
##'_____________Importation_des_règles______________'
##    
##def importer_regle(chemin_d_acces_fichier_regles):
##    arbreXML= ET.parse(chemin_d_acces_fichier_regles)
##    tronc = arbreXML.getroot()
##
##    # Dictionnaire de la forme {"nom_règle" : pointeur_de_la_règle_associée}
##    regles = dict()
##
##    for rule in tronc.iter('rule'):
##
##        if rule[0].tag == "simple_condition":
##
##            print("argument envoyé {}".format([mon_tuple for mon_tuple in rule[0].items()]))
##            ma_condition_simple=Condition_Simple([mon_tuple for mon_tuple in rule[0].items()])   #conversion de type à vérifier  
##            #dictionnaire qui prend des arguments au format {nom_variable_initialisée:valeur_variable_initialisée}
##            print("Condition simple {} de paramètres {} générée".format(ma_condition_simple,ma_condition_simple.param_dict_val))
##            regles.update({rule.get('name'):Regle(rule.get('name'),rule.get('description'),ma_condition_simple)})
##            
##        elif rule[0].tag == "composed_condition":
##           
##            liste_conditions_simples = []
##            
##            print("Début de la règle composée {} de description {}".format(rule.get('name'),rule.get("description")))
##
##            for simple_condition in rule[0].iter("simple_condition"):
##                    
##                    print("argument envoyé {}".format([mon_tuple for mon_tuple in simple_condition.items()]))
##                    ma_condition_simple=Condition_Simple([mon_tuple for mon_tuple in simple_condition.items()])
##                    liste_conditions_simples.append(ma_condition_simple) #Liste de dictionnaire. Oui c'est moche.
##                    print("Fait")
##
##            print("Opérateur logique: {}".format(rule[0].get("operator")))
##            print("liste de conditions simples finale: {}".format(liste_conditions_simples)) 
##            ma_condition_composee=Condition_Composee(rule[0].get("operator"),liste_conditions_simples)
##            regles.update({rule.get('name'):Regle(rule.get('name'),rule.get('description'),ma_condition_composee)})
##            
##            
##
##
##    print(regles)
##    return regles


'_______________________Interface________________________''_______________________Interface________________________''_______________________Interface________________________'

import tkinter  as tk 
from tkinter import ttk
from tkinter import filedialog as fd

#importer le matplotlib.pyplot.plt dans tintker
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


def fentre():
    root = tk.Tk()

    # Fonction d'import doublée faute de mieux
    # Possibilité de complexifier si on sait quel bouton a appelé
    def open_postures_file():
        root_txt_zone_1.insert(0, fd.askopenfilename(filetypes = (("Text files","*.xml"),("all files","*.*")))) #restreindre à fichier XML seulement)

    def open_rules_file():
        root_txt_zone_2.insert(0, fd.askopenfilename(filetypes = (("Text files","*.xml"),("all files","*.*")))) #restreindre à fichier XML seulement)

    # Création des zones d'import fichiers
    tk.Label(root,text="chemin du fichier de séquence:").grid(row=0,column=0)
    root_txt_zone_1=tk.Entry(root)
    root_txt_zone_1.grid(row=0,column=1)

    root_button_1=tk.Button(root, text = "Importer", command = open_postures_file)
    root_button_1.grid(row=0,column=2)

    print(root_button_1)

    tk.Label(root,text="chemin du fichier de règles:").grid(row=1,column=0)

    root_txt_zone_2=tk.Entry(root)
    root_txt_zone_2.grid(row=1,column=1)

    root_button_2=tk.Button(root, text = "Importer", command = open_rules_file)
    root_button_2.grid(row=1,column=2)

    # lien avec les classes


    # Création des onglets
    my_tabs = ttk.Notebook(root) # declaring 

    tab1 = ttk.Frame(my_tabs)
    tab2 = ttk.Frame(my_tabs)
    tab3 = ttk.Frame(my_tabs)

    my_tabs.add(tab1, text ='Affichage') # adding tab
    my_tabs.add(tab2, text ='Plot-evolution') # adding tab 
    my_tabs.add(tab3, text ='Test') # adding tab 

    my_tabs.grid(row=2,column=0,columnspan=3)

    # Passage à 0 pcq row et column du tab1
    tab1_left_frame = tk.Frame(tab1)
    tab1_left_frame.grid(row=0,column=0)



    # Ici inclusion du plot matplotlib onglet 1
    # Taille de la fenêtre

    fig = Figure(figsize=(5, 4), dpi=100)

##    fig.add_subplot(111).plot(Lx,Ly)

    
    canvas = FigureCanvasTkAgg(fig, master=tab1_left_frame)  # A tk.DrawingArea.
    canvas.get_tk_widget().grid(row=0,column=1)
    canvas.draw()
##    del(canvas)
    


    def afficher_sequence(posture):
##        del(canvas)
        # On détermine en fonction des boutons pressés les vecteurs à tracer
        print(tab_1_check_but_1_var,tab_1_check_but_2_var)
        if tab_1_check_but_1_var and tab_1_check_but_2_var:  call = 'b'

        elif tab_1_check_but_1_var and not tab_1_check_but_2_var: call = 'v'
            
        elif tab_1_check_but_2_var and not tab_1_check_but_1_var: call = 'a'

        else: call = 'r'

        ax = sequence.postures[posture].tracer(call)
        canvas = FigureCanvasTkAgg(ax, master=tab1_left_frame)  # A tk.DrawingArea.
        canvas.get_tk_widget().grid(row=0,column=1)
        canvas.draw()
        

    #Zone droite du tab1
    tab_1_right_frame= tk.Frame(tab1)
    tab_1_right_frame.grid(row=0,column=1)

    
    tab_1_check_but_1_var = 1
    tab_1_check_but_1 = ttk.Checkbutton(tab_1_right_frame,text='Afficher Vitesses',variable = tab_1_check_but_1_var)
##    tab_1_check_but_1.deselect
    tab_1_check_but_1.grid(row=0,column=0)

    tab_1_check_but_2_var = 0
    tab_1_check_but_2 = ttk.Checkbutton(tab_1_right_frame,text='Afficher accélérations',variable = tab_1_check_but_2_var)
##    tab_1_check_but_2.deselect
    tab_1_check_but_2.grid(row=1,column=0)

    tab_1_right_spnbox_1_var = tk.StringVar(value=0)
    tab_1_right_spnbox_1=ttk.Spinbox(tab_1_right_frame, from_=0, to = len(sequence.postures)-1, textvariable = tab_1_right_spnbox_1_var,wrap = True) 
    tab_1_right_spnbox_1.grid(row=3,column=0)

    tab_1_check_1 = ttk.Button(tab_1_right_frame,text='Lancer affichage')
    #, command = afficher_sequence(int(tab_1_right_spnbox_1.get()))
    tab_1_check_1.grid(row=2,column=0)

    

    

        
    #Création zones tab2
    tab_2_left_frame = tk.Frame(tab2)
    tab_2_left_frame.grid(row=0,column=0)

    tab_2_right_frame = tk.Frame(tab2)
    tab_2_right_frame.grid(row=0,column=1)

    #Zone gauche tab2

    fig = Figure(figsize=(5, 4), dpi=100)
    

    canvas = FigureCanvasTkAgg(fig, master=tab_2_left_frame )  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().grid(row=0,column=1)

   
    #Zone droite tab2


    liste_articulations=[articulation.nom for articulation in sequence.postures[0].articulations] #A modifier avec la liste des articulations DONE
    tab_2_combobox_1 = ttk.Combobox(tab_2_right_frame, values=liste_articulations)
    tab_2_combobox_1.grid(row=0,column=0)

    liste_demandes = ['Angle','Vitesse_moy','Acceleration_moy','Vitesse_ang','Acceleration_ang']
    tab_2_combobox_2 = ttk.Combobox(tab_2_right_frame,values = liste_demandes)
    tab_2_combobox_2.grid(row=3,column=0)


    def determiner_coord_evolution():
        articulation = tab_2_combobox_1.get()
        demande = tab_2_combobox_2.get()
        dt = 1/1.2
        x = [i*dt for i in range(len(sequence.postures))]
        y = []
        for posture in sequence.postures:
            articulation_concernee = posture.obtenir(articulation)
            if demande == 'Angle':
                y.append(articulation_concernee.angle)
            if demande == 'Vitesse_moy':
                y.append(articulation_concernee.va_moy[2])
            if demande == 'Acceleration_moy':
                y.append(articulation_concernee.va_moy[3])
            if demande == 'Vitesse_ang':
                y.append(articulation_concernee.va_ang[0])
            if demande == 'Acceleration_ang':
                y.append(articulation_concernee.va_ang[1])
        return x,y

    def tracer_evolution():
        x,y = determiner_coord_evolution()
        fig.add_subplot(111).plot(x,y)

        canvas = FigureCanvasTkAgg(fig, master = tab_2_left_frame )  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().grid(row=0,column=0,columnspan = 2)

    def nettoyer():
        tab_2_left_frame.destroy
        fig = Figure(figsize=(5, 4), dpi=100)

        canvas = FigureCanvasTkAgg(fig, master=tab_2_left_frame)  # A tk.DrawingArea.
        canvas.get_tk_widget().grid(row=0,column=0,columnspan=2)
        canvas.draw()
        
    tab_2_but_1=ttk.Button(tab_2_right_frame,text="Tracer l'évolution", command = tracer_evolution)
    tab_2_but_1.grid(row=4,column=0,columnspan = 2)

    racine = ttk
    tab_2_but_2 = ttk.Button(tab_2_right_frame,text = "Clear", command = nettoyer)
    tab_2_but_2.grid(row=5,column=0,columnspan = 2)
    
    #tab 3

    tab_3_left_frame = tk.Frame(tab3)
    tab_3_left_frame.grid(row=0,column=0)

    tab_3_center_frame = tk.Frame(tab3)
    tab_3_center_frame.grid(row=0,column=1)

    tab_3_right_frame= tk.Frame(tab3)
    tab_3_right_frame.grid(row=0,column=2)

    #Remplissage tab3
    #left_frame
    tab_3_left_spnbox_1=ttk.Spinbox(tab_3_left_frame, from_=0, to = len(sequence.postures)-1) # A modifier selon nb articulion avec un len DONE
    tab_3_left_spnbox_1.grid(row=0,column=0)

    tab_3_left_but_1=ttk.Button(tab_3_left_frame,text="Lancer la recherche")
    tab_3_left_but_1.grid(row=1,column=0)

    tab_3_left_lstbox_1=tk.Listbox(tab_3_left_frame)
    tab_3_left_lstbox_1.insert(1,"élément 1") #(index, valeur)
    tab_3_left_lstbox_1.grid(row=2,column=0)

    #center_frame
    listeProduits2=[element for element in list(regles.keys())] #A modifier avec la liste des articulations DONE
    tab_3_center_combobox_1 = ttk.Combobox(tab_3_center_frame, values=listeProduits2)
    tab_3_center_combobox_1.grid(row=0,column=0)

    tab_3_center_but_1=ttk.Button(tab_3_center_frame,text="Lancer la recherche")
    tab_3_center_but_1.grid(row=1,column=0)

    tab_3_center_lstbox_1=tk.Listbox(tab_3_center_frame)
    tab_3_center_lstbox_1.grid(row=2,column=0)
    tab_3_center_lstbox_1.insert(1,"élément 1") #(index, valeur)


    #right_frame
    tab_3_right_but_1=tk.Button(tab_3_right_frame,text="Lister et Enregistrer les règles activées")
    tab_3_right_but_1.grid(row=0,column=0)





    root.mainloop()  # Keep the window open

fentre()
