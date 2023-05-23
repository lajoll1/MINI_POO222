import xml.etree.ElementTree as ET
import math
import numpy as np

'________________Ouverture_fichier_XML________________'

xml_file = "/Users/thomas/Documents/GitHub/MINI_POO222/Postures_captures.xml"

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
        for i in [-2,-1,1,2]:
            for articulation in sequence.postures[self.posture + i].articulations:
                if articulation.nom == self.nom:
                    voisins.append(articulation)
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
        angle_0 = self.voisins_t[1].angle
        angle_1 = self.voisins_t[2].angle
        
        vitesse_ang = (angle_1-angle_0)/(2*dt)

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
            
        else: vitesse = None

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
            
        else: acceleration = None

        return vitesse,acceleration,norme_vitesse,norme_acceleration

    va_moy = property(_calculer_v_a_moyenne)


    
'______________Definition_classe_Posture_____________'

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as mp

class Posture():
    def __init__(self,tonnumero,tesarticulations):
        self._tonnumero = int(tonnumero)
        self._tesarticulations = list(tesarticulations)

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
    
        for articulation in self.articulations: # On parcourt l'ensemble des articulations de la posture considérée

            # Affichage de l'articulation considérée
            ax.scatter(articulation.position[0],articulation.position[2],articulation.position[1],c='r', marker='o') 

            # Liaison de l'articulation avec ses voisins
            if len(articulation.voisinsPOO[1]) != 0:
                for enfant in articulation.voisinsPOO[1]:
                    x1,x2 = enfant.position[0],articulation.position[0]
                    y1,y2 = enfant.position[2],articulation.position[2] 
                    z1,z2 = enfant.position[1],articulation.position[1]
                    ax.scatter([x1,x2], [y1,y2], [z1,z2], c='r', marker='o')
                    ax.plot([x1,x2], [y1,y2], [z1,z2], c='b')

            
                    
            # Tracé du vecteur vitesse si demandé 
            origine = articulation.position
            if call in ("v","b") and articulation.va_moy[0] != None:
                vitesse = articulation.va_moy[0]
                ax.quiver(origine[0], origine[2], origine[1], vitesse[0], vitesse[2], vitesse[1], color='green')



            # Tracé du vecteur acceleration si demandé
            origine = articulation.position
            if call in ("a","b") and articulation.va_moy[1] != None:
                acceleration = articulation.va_moy[1]
                ax.quiver(origine[0], origine[2], origine[1], acceleration[0], acceleration[2], acceleration[1], color='magenta')
                        
        # Configuration des axes
        ax.set_xlabel('X')
        ax.set_ylabel('Z')               
        ax.set_zlabel('Y')

        # Orientation de la vue
        ax.view_init(elev=15, azim=135)        
           
        # Affichage de la figure
        set_axes_equal(ax)
        plt.show()      
      


'______________Definition_classe_Sequence_____________'

class Sequence():
    def __init__(self,tespostures):
        self._tespostures = list(tespostures) 

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



'_______________________Règles________________________''_______________________Règles________________________''_______________________Règles________________________'



'______________Definition_classe_Regle_____________'

class Regle():
    def __init__(self,mon_nom,ma_description,ma_condition):
        if isinstance(mon_nom, str) and isinstance(ma_description, str) and (isinstance(ma_condition, Condition_Simple) or isinstance(ma_condition, Condition_Composee)):
            self._nom_regle = mon_nom
            self._description_regle = ma_description
            self._condition_associe = ma_condition
    def is_activated(self,posture):
        if isinstance(posture, Posture) or isinstance(posture, Posture):
            print("Vérification de l'activation de la règle {} ".format(posture))
        return self._condition_associe.is_activated(posture) 
    

   
'________Definition_classe_Condition_Simple________'

class Condition_Simple():

    # Valeur par défaut pour le seuil si domaine préféré
    def __init__(self,ma_cible,mon_type_de_condition,mon_seuil_ou_domaine_ou_volume,ma_zone_du_corps="",direction=""):
        
        # Début des tests
        if ma_cible in {"angle","position","pos"}: #Faire un fichier de génération auto ici
            self._target = ma_cible
        else:
            pass
            # return "type de cible incorrect"
        #Replacer les conditions proprement
        if mon_type_de_condition in {"lower than","greater than","belongs to","belongs to the volume"}:
            self._condition_type = mon_type_de_condition
        

        # Selon le type de condition
        if self._condition_type in {"lower than","greater than"}:
             #fichier considéré sans erreur donc pas de test
             #if isinstance(mon_seuil_ou_domaine,int):
             #Prise en compte de la conversion du format anglophone ver
            self._threshold = float(mon_seuil_ou_domaine_ou_volume)
            print("seuil initialisé")
           
        elif self._condition_type == "belongs to":
            #if isinstance(mon_seuil_ou_domaine,tuple) and len(mon_seuil_ou_domaine) == 2:
            #Formattage des données nécessaire car lu comme string
            mon_seuil_ou_domaine_ou_volume= mon_seuil_ou_domaine_ou_volume.removeprefix("(")
            mon_seuil_ou_domaine_ou_volume=mon_seuil_ou_domaine_ou_volume.removesuffix(")")
            self._domain = tuple(mon_seuil_ou_domaine_ou_volume.split(","))
            self._domain =tuple([int (x) for x in self._domain])
            print("Tuple converti vaut {} et est de type {} et chaque donnée est de type {}".format(self._domain,type(self._domain),type(self._domain[0])))
        
                # return "Domaine invalide"
        elif self._condition_type == "belongs to the volume":
            #Donnée importée sous la forme (corner1,corner2)
            self._first_corner=mon_seuil_ou_domaine_ou_volume[0]
            on_seuil_ou_domaine_ou_volume= mon_seuil_ou_domaine_ou_volume.removeprefix("(")
            mon_seuil_ou_domaine_ou_volume=mon_seuil_ou_domaine_ou_volume.removesuffix(")")
            self._first_corner = tuple(self._first_corner.split(","),type=float)
            self._second_corner=mon_seuil_ou_domaine_ou_volume[1]
            self._second_corner = tuple(self._second_corner.split(","),type=float)
            print("Tuple converti first_corner vaut {} et est de type {} et chaque donnée est de type {}".format(self._first_corner,type(self._first_corner),type(self._first_corner[0])))
            #Code cette nouvelle partie avec les règles

        # A compléter selon futures règles ?
        if ma_zone_du_corps in {"Neck","RightForeArm","Spine"}:
            self._target_joint = ma_zone_du_corps

    #int obtenir_angle_depuis_posture(posture posture_a_verifier)
    #int obtenir_angle_depuis_projection_posture(posture_a_verifier,axe)
    #2-tuple obtenir_seuil_par_projection_depuis_posture(class posture)
    #Nécessité de la méthode is_activated dans condition ?

    def _obtenir_angle_depuis_posture(self,posture):

        print("Demande de l'angle de l'articulation {} pour la posture {}".format(self._target_joint,posture))
        return posture.obtenir(self._target_joint).angle
   
    def _obtenir_coordonnees_depuis_posture(self,posture):
        print("Demande de la position de l'articulation {} pour la posture {}".format(self._target_joint,posture))
        return posture.obtenir(self._target_joint).position
   
    def _obtenir_angle_depuis_projection_posture(self,posture,axe):
        
        pass

    # bool is_activated(class self, posture posture_a_verifier)
    def is_activated(self, posture_a_verifier):
        if isinstance(posture_a_verifier, Posture): 
            if self._target == "angle":
                # Droit d'accéder par élément car dans la classe
                if self._condition_type == "lower than":
                    if self._obtenir_angle_depuis_posture(posture_a_verifier) < self._threshold: return True
                elif self._condition_type == "greater than":
                    if  self._obtenir_angle_depuis_posture(posture_a_verifier) > self._threshold: return True
                elif self._condition_type == "belongs to":
                    print("premier membre du domaine {}".format(self._domain))
                    if  self._domain[0] < self._obtenir_angle_depuis_posture(posture_a_verifier) < self._domain[1]: return True
                return False # Si l'on arrive ici, aucune des conditions précédentes n'est vérifiée

            elif self._target == "pos": # Changer l'intitulé
                if self._condition_type == " belongs to the volume":
                    x,y,z = self._obtenir_coordonnees_depuis_posture(posture_a_verifier)
                    if cond1 == 'val1' and \
                       cond3 == 'val3' and \
                       cond4 == 'val4':
                        pass
                elif self._condition_type == "lower than":
                    if self._obtenir_angle_depuis_projection_posture(posture_a_verifier,axe) < self._threshold: return True
                elif self._condition_type == "greater than":
                    if  self.obtenir_angle_depuis_projection_posture(posture_a_verifier,axe) > self._threshold: return True
                elif self._condition_type == "belongs to":
                    if  self._domain[0] < obtenir_angle_depuis_projection_posture(posture_a_verifier,axe) < self._domain[1]: return True
                return False # Si l'on arrive ici, aucune des conditions précédentes n'est vérifiée
        # bool superieur_A_Un_Seuil()



'_______Definition_classe_Condition_Composee_______'

class Condition_Composee():
    
    # Condition_composée __init__(class self, string operateur, list ma_condition_composee)
    def __init__(self, mon_operateur,ma_liste_de_conditions_simples):
        if mon_operateur in {"or","and"}:
            _operator = mon_operateur
        # Prendre en compte le fait qu'il y ait potentiellement n conditions simples dans la condition complexe
            _liste_conditions_simples=[] # Liste en partaeg de pointeurs
            for x in ma_liste_de_conditions_simples:
                if isinstance(x, Condition_Simple):
                    _liste_conditions_simples.append(x)

    # bool is_activated(class self, class posture)                
    def is_activated(self, ma_posture):
        if isinstance(ma_posture, posture):
            # Assez flexible pour supporter de nouveaux opérateurs en ajoutant en elif
            if self._operator == "and":
                for condition_simple in self._condition_list:
                    if condition_simple.is_activated(ma_posture) == False: return False
            # Vérifier toutes les conditions les unes après les autres et renvoyer False si l'une n'est pas vérifiée     
            elif self._operator == "or":
                for condition_simple in self._condition_list:
                    if condition_simple.is_activated(ma_posture): return True
                # Renvoyer true à la premirèe condition vérifiée



'_____________Importation_des_règles______________'

def importer_regle(chemin_d_acces_fichier_regles):
    arbreXML= ET.parse(chemin_d_acces_fichier_regles)
    tronc = arbreXML.getroot()

    # Dictionnaire de la forme {"nom_règle" : pointeur_de_la_règle_associée}
    regles = dict()

    for rule in tronc.iter('rule'):

        if rule[0].tag == "simple_condition":
            print("On ajoute la règle simple {}, de description {}".format(rule.get('name'),rule.get('description')))
            print("et associée à la condition simple qui a pour éléments constitutifs sa cible {}, un type de conditions {}, un seuil {} et une zone du corps {}".format(rule[0].get('target'),rule[0].get('condition_type'),rule[0].get("threshold"),rule[0].get('target_joint')))
            # On suppose le fichier xml bien formaté
            if rule[0].get('condition_type') in {"lower than","greater than"}:
                ma_condition_simple = Condition_Simple(rule[0].get('target'),rule[0].get('condition_type'),rule[0].get("threshold"),rule[0].get('target_joint'))
                # ma_condition_simple = Condition_Simple("angle","lower than","3","RightForeArm")

            elif rule[0].get('condition_type') == "belongs to":
                ma_condition_simple = Condition_Simple(rule[0].get('target'),rule[0].get('condition_type'),rule[0].get("domain"),rule[0].get('target_joint'))
        
            regles[rule.get('name')] = Regle(rule.get('name'),rule.get('description'),ma_condition_simple)


        # Faut-il tout mettre en managé ?
        elif rule[0].tag == "composed_condition":
           
            liste_conditions_simples = []

            for simple_condition in rule[0].iter("simple_condition"):
                if simple_condition.get('condition_type') in {"lower than","greater than"}:
                    ma_condition_simple=Condition_Simple(simple_condition.get('target'),simple_condition.get('condition_type'),simple_condition.get("threshold"),simple_condition.get('target_joint'))
                    #print("Condition simple qui a pour éléments constitutifs sa cible {}, un type de conditions {}, un seuil {} et une zone du corps {}".format(simple_condition.get('target'),simple_condition.get('condition_type'),simple_condition.get("threshold"),simple_condition.get('target_joint')))
                    liste_conditions_simples.append(ma_condition_simple)
                elif simple_condition.get('condition_type') == "belongs to":
                    ma_condition_simple=Condition_Simple(simple_condition.get('target'),simple_condition.get('condition_type'),simple_condition.get("domain"),simple_condition.get('target_joint'))
                    liste_conditions_simples.append(ma_condition_simple)
            print("liste de conditions simples finale: {}".format(liste_conditions_simples))        
            regles[rule.get('name')]=Regle(rule.get('name'),rule.get('description'),liste_conditions_simples)
            
            print("Début de la règle composée {} de description {}".format(rule.get('name'),rule.get("description")))
            print("Associée à la condition simple qui a pour éléments constitutifs sa cible {}, un type de conditions {}, un seuil {} et une zone du corps {}".format(simple_condition.get('target'),simple_condition.get('condition_type'),simple_condition.get("threshold"),simple_condition.get('target_joint')))

    print(regles)
    return regles

regles = importer_regle("/Users/thomas/Documents/GitHub/MINI_POO222/rules_angles_et_positions_v1.3.xml")
print("test de la règle {}".format(regles["Ohhhh"].is_activated(sequence.postures[15])))



