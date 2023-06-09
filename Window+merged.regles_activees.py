import xml.etree.ElementTree as ET
'_______________________Règles________________________''_______________________Règles________________________''_______________________Règles________________________'



class Regle():
    def __init__(self,mon_nom,ma_description,ma_condition):
        if isinstance(mon_nom, str) and isinstance(ma_description, str) and (isinstance(ma_condition, Condition_Simple) or isinstance(ma_condition, Condition_Composee)):
            self._nom_regle = mon_nom
            self._description_regle = ma_description
            self._condition_associe = ma_condition

    def is_activated(self,posture):
        if isinstance(posture, Posture) or isinstance(posture, Posture):
            #print("Vérification de l'activation de la règle {} ".format(posture))
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
                duo_modifiable[1]=str(duo_modifiable[1])[1:-1]
                duo_modifiable[1] = tuple([float (x) for x in duo_modifiable[1].split(",")])
                print("domain converted. New value {} and type {}".format(duo_modifiable[1],type(duo_modifiable[1][0])))
            
            if duo_modifiable[0]== "first_corner":
                duo_modifiable[1]=str(duo_modifiable[1])[1:-1]
                duo_modifiable[1] = tuple([float (x) for x in duo_modifiable[1].split(",")])
                print("domain converted. New value {} and type {}".format(duo_modifiable[1],type(duo_modifiable[1][0])))
            
            if duo_modifiable[0]== "second_corner":
                duo_modifiable[1]=str(duo_modifiable[1])[1:-1]
                duo_modifiable[1] = tuple([float (x) for x in duo_modifiable[1].split(",")])               

            self._param_dict.update({duo_modifiable[0]:duo_modifiable[1]})
            print("Dictionnaire mis à jour avec la clef {} et la valeur {} de type {}".format(duo_modifiable[0],duo_modifiable[1],type(duo_modifiable[1])))

    def _articulation_seeker(self,articulation_cible,posture):
        for articulation in posture.articulations:
            if articulation.nom == articulation_cible:
                return articulation
        return -1

    def _obtenir_depuis_posture(self,posture):
        if self._param_dict.get("target") == "angle": return self._articulation_seeker(self._param_dict.get("target_joint"),posture).angle
        elif self._param_dict.get("target") == "pos":
            #projection ou vérification 3D?
            if "direction" in self._param_dict.keys():
                #Implique une projection donc disjonction de cas selon l'axe
                #cas avec un angle ?
                #TODO: tratier le cas Domain si projection
                if self._param_dict.get("direction") == "X":
                    return self._articulation_seeker(self._param_dict.get("target_joint"),posture).position[0]
                elif self._param_dict.get("direction") == "Y":
                    return self._articulation_seeker(self._param_dict.get("target_joint"),posture).position[1]
                    #Récupère la 2e coordonnée et la return
                elif self._param_dict.get("direction") == "Z":
                    return self._articulation_seeker(self._param_dict.get("target_joint"),posture).position[2]
                else:
                    return "Axe non-reconnu"
            else: #forcément de type "belongs to the volume"
                return self._articulation_seeker(self._param_dict.get("target_joint"),posture).position

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


import math
import numpy as np



'____________Definition_classe_Articulation___________'

class Articulation:
    def __init__(self, tonnom,taposition,taposture):
        self._tonnom = str(tonnom)
        self._taposture_num = taposture.numero
        self._tesneighbors = {"N":[],"P":None}
        self._taposition = taposition
        self._taposture = taposture
        
        
    def _lire_nom(self):
        return self._tonnom
    def _lire_position(self):
        return self._taposition
    def _lire_posture(self):
        return self._taposture
    def _lire_voisins(self):
        return self._tesneighbors
    def _lire_posture_num(self):
        return self._taposture_num
    
    nom = property(_lire_nom)
    position = property(_lire_position)
    posture = property(_lire_posture)
    voisins = property(_lire_voisins)
    posture_num = property(_lire_posture_num)

    def _convertir(self):
        ma_variable = str(self._taposition)[1:-1]
        ma_variable = tuple([float (x) for x in ma_variable.split(",")])
        return ma_variable
    vposition = property(_convertir)
    def _add_neighbor_child(self, neighbor):
        self._tesneighbors["N"].append(neighbor)

    def _add_neighbor_parent(self, neighbor):
        self._tesneighbors["P"] = neighbor

    def _trouver_voisins_temporels(self):
        voisins_t = []
        if self.posture_num == 0:
            voisins_t.append(None)
            voisins_t.append(None)
            for articulation in self.posture.voisins[1].articulations:
                if articulation.nom == self.nom:
                    voisins_t.append(articulation)
            for articulation in (self.posture.voisins[1]).voisins[1].articulations:
                if articulation.nom == self.nom:
                    voisins_t.append(articulation)
            
        elif self.posture == 1:
            voisins_t.append(None)
            for articulation in self.posture.voisins[0].articulations:
                if articulation.nom == self.nom:
                    voisins_t.append(articulation)
            for articulation in self.posture.voisins[1].articulations:
                if articulation.nom == self.nom:
                    voisins_t.append(articulation)
            for articulation in (self.posture.voisins[1]).voisins[1].articulations:
                if articulation.nom == self.nom:
                    voisins_t.append(articulation)
            
        elif self.posture == 57 :
            for articulation in (self.posture.voisins[0]).voisins[0].articulations:
                if articulation.nom == self.nom:
                    voisins_t.append(articulation)
            for articulation in self.posture.voisins[0].articulations:
                if articulation.nom == self.nom:
                    voisins_t.append(articulation)
            voisins_t.append(None)
            voisins_t.append(None)

        elif self.posture == 56 :
            for articulation in (self.posture.voisins[0]).voisins[0].articulations:
                if articulation.nom == self.nom:
                    voisins_t.append(articulation)
            for articulation in self.posture.voisins[0].articulations:
                if articulation.nom == self.nom:
                    voisins_t.append(articulation)
            for articulation in self.posture.voisins[1].articulations:
                if articulation.nom == self.nom:
                    voisins_t.append(articulation)
            voisins_t.append(None)

        else :
            postures_voisines = [(self.posture.voisins[0]).voisins[0],self.posture.voisins[0],self.posture.voisins[1],(self.posture.voisins[1]).voisins[1]]
            for posture in posture_voisines:
                for articulation in posture.articulations:
                    if articulation.nom == self.nom:
                        voisins_t.append(articulation)
        return voisins_t
    voisins_t = property(_trouver_voisins_temporels)

    def _calculer_angle(self):
        if len(self.voisins['N']) == 1 and self.voisins['P']!= None :
            x1,y1,z1 = self.voisins['P'].vposition[0],self.voisins['P'].vposition[1],self.voisins['P'].vposition[2]
            x2,y2,z2 = (self.position)[0],(self.position)[1],(self.position)[2]
            x3,y3,z3 = self.voisins['N'][0].vposition[0],self.voisins['N'][0].vposition[1],self.voisins['N'][0].vposition[2]

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

        if self.posture not in [0,57]:
            angle_0 = self.voisins_t[1].angle
            angle_1 = self.voisins_t[2].angle
        
            vitesse_ang = (angle_1 - angle_0)/(2*dt)

        if self.posture not in [0,1,57,56]:
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
    def __init__(self, frame_number):
        self._frame_number = frame_number
        self._articulations = []
        self._previous_posture = None
        self._next_posture = None

    def regles_activees(self,regles):
        liste_regles_activees_par_posture=list()
        for regle in regles.values():
            print("règle utilisée: {}".format(regle))
            if regle.is_activated(self):
                liste_regles_activees_par_posture.append(regle)
        return liste_regles_activees_par_posture 

    def _lire_numero(self):
        return self._frame_number
    numero = property(_lire_numero)

    def _lire_articulations(self):
        return self._articulations
    articulations = property(_lire_articulations)

    def _lire_voisins(self):
        return self._previous_posture,self._next_posture
    voisins = property(_lire_voisins)
    
    def _add_articulation(self, articulation):
        self._articulations.append(articulation)

    def _set_previous_posture(self, posture):
        self._previous_posture = posture

    def _set_next_posture(self, posture):
        self._next_posture = posture


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
##        return fig

        return ax


'______________Definition_classe_Sequence_____________'

class Sequence():
    def __init__(self):
        self._postures = []

    def _lire_postures(self):
        return self._postures
    postures = property(_lire_postures)

    def _add_posture(self, posture):
        self._postures.append(posture)

    def _set_posture_neighbors(self):
        num_postures = len(self._postures)
        for i in range(num_postures):
            if i > 0:
                self._postures[i]._set_previous_posture(self._postures[i-1])
            if i < num_postures - 1:
                self._postures[i]._set_next_posture(self._postures[i+1])
                
    def posture_activees(self,regle_a_tester):
        liste_postures_activant_la_regle=list()
        # Vérifier comment Virgile récupère chacune des postures de la séquence
        
        for posture in self.postures:
            print("règle à tester est: {}".format(regle_a_tester))
            if regle_a_tester.is_activated(posture):
                    liste_postures_activant_la_regle.append(posture)
            print("Vérification de l'activation de la règle à tester {} pour la posture {}".format(regle_a_tester._nom_regle,posture))
        return liste_postures_activant_la_regle

'________________________Classe_Chargement_________________________'

class Chargement():
    def __init__(self,chemin_sequence,chemin_regles):
        self._chemin_seq = str(chemin_sequence)
        self._chemin_reg = str(chemin_regles)

    def _lire_chemin(self):
        return self._chemin_seq,self._chemin_reg
    chemin = property(_lire_chemin)

    def _creer_sequence(self):
        def parse_joint_element(joint_elem,frame_elem,posture):

            def trouver_parent(tronc, element):    
                    for enfant in tronc:
                        if enfant is element:
                            return tronc
                        parent = trouver_parent(enfant, element)
                        if parent is not None:
                            return parent
                    return None

            name = joint_elem.get('Name')
            position = eval(joint_elem.get('Position'))
            articulation = Articulation(name, position, posture)
            for child_elem in joint_elem.findall("Joint"):
                child_articulation = parse_joint_element(child_elem,joint_elem,posture)
                articulation._add_neighbor_child(child_articulation)

            parent_articulation = trouver_parent(frame_elem, joint_elem)
            if parent_articulation is not None and parent_articulation.tag == 'Joint':
                parent_articulation = Articulation(parent_articulation.get('Name'), parent_articulation.get('Position'), posture)
                articulation._add_neighbor_parent(parent_articulation)

            return articulation

        def parse_frame_element(frame_elem,c):
            frame_number = c
            posture = Posture(frame_number)
            for joint_elem in frame_elem.iter('Joint'):
                articulation = parse_joint_element(joint_elem,frame_elem,posture)
                posture._add_articulation(articulation)
            return posture

        def parse_xml(file_path):
            tree = ET.parse(file_path)
            root = tree.getroot()

            sequence = Sequence()
            c=0
            for frame_elem in root.findall('Frame'):
                posture = parse_frame_element(frame_elem,c)
                sequence._add_posture(posture)
                c+=1

            sequence._set_posture_neighbors()

            return sequence

        return parse_xml(self.chemin[0])

    obtenir_sequence = property(_creer_sequence)

    def _importer_regle(self):
        arbreXML = ET.parse(self.chemin[1])
        tronc = arbreXML.getroot()

        # Dictionnaire de la forme {"nom_règle" : pointeur_de_la_règle_associée}
        regles = dict()

        for rule in tronc.iter('rule'):

            if rule[0].tag == "simple_condition":

        ##            print("argument envoyé {}".format([mon_tuple for mon_tuple in rule[0].items()]))
                ma_condition_simple=Condition_Simple([mon_tuple for mon_tuple in rule[0].items()])   #conversion de type à vérifier  
                #dictionnaire qui prend des arguments au format {nom_variable_initialisée:valeur_variable_initialisée}
     ##            print("Condition simple {} de paramètres {} générée".format(ma_condition_simple,ma_condition_simple.param_dict_val))
                regles.update({rule.get('name'):Regle(rule.get('name'),rule.get('description'),ma_condition_simple)})
                
            elif rule[0].tag == "composed_condition":
               
                liste_conditions_simples = []
                
     ##            print("Début de la règle composée {} de description {}".format(rule.get('name'),rule.get("description")))

                for simple_condition in rule[0].iter("simple_condition"):
                        
      ##                    print("argument envoyé {}".format([mon_tuple for mon_tuple in simple_condition.items()]))
                        ma_condition_simple=Condition_Simple([mon_tuple for mon_tuple in simple_condition.items()])
                        liste_conditions_simples.append(ma_condition_simple) #Liste de dictionnaire. Oui c'est moche.
     ##                    print("Fait")

        ##            print("Opérateur logique: {}".format(rule[0].get("operator")))
        ##            print("liste de conditions simples finale: {}".format(liste_conditions_simples)) 
                ma_condition_composee=Condition_Composee(rule[0].get("operator"),liste_conditions_simples)
                regles.update({rule.get('name'):Regle(rule.get('name'),rule.get('description'),ma_condition_composee)})
            
            


        ##    print(regles)
        return regles
    obtenir_regles = property(_importer_regle)
    
    def exporter_xml(self, dico_postures_activees_pour_regle_donnee):
        #prend un argument de la forme dictionnaire {nom_règle_activation:[liste_posture activées]}
        # Create root element.
        rootXMLElt = ET.Element("root")
        
        # Add sub element.
        #country = ET.SubElement(root, "country", name="Canada")
        for regle in dico_postures_activees_pour_regle_donnee.keys():
        
            regle_activee = ET.SubElement(rootXMLElt, "regle_activee", name=regle)
            regle_activee.text=regle # a remplacer par la regle en question

            for posture in dico_postures_activees_pour_regle_donnee.get(regle_activee.text):
                # Add sub-sub element.
                ET.SubElement(regle_activee, "posture").text = posture #remplacer test par le numero de posture

        # Write XML file.
        tree = ET.ElementTree(rootXMLElt)
        print(rootXMLElt) 
        tree.write("export2.xml")


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


def main():

   
    def remplir_onglets(sequence,regles):
        tab_1_right_spnbox_1["to"]= len(sequence.postures)-1 
        
        #A modifier avec la liste des articulations DONE
        
        tab_2_combobox_1["values"]= [articulation.nom for articulation in sequence.postures[0].articulations] 
        tab_3_left_spnbox_1["to"]=len(sequence.postures)-1
        #A modifier avec la liste des articulations DONE
        tab_3_center_combobox_1["values"] = [element for element in list(regles.keys())]
        pass

    def open_postures_file():
        if root_txt_zone_1.get(): root_txt_zone_1.delete(0,"end")
        root_txt_zone_1.insert(0, fd.askopenfilename(filetypes = (("Text files","*.xml"),("all files","*.*")))) #restreindre à fichier XML seulement)

    def open_rules_file():
        if root_txt_zone_2.get(): root_txt_zone_2.delete(0,"end")
        root_txt_zone_2.insert(0, fd.askopenfilename(filetypes = (("Text files","*.xml"),("all files","*.*")))) #restreindre à fichier XML seulement)
    
    def start_analyzing_process():
        #On suppose les fichiers verslesquels on a pointé les bons.
        if root_txt_zone_1.get() and root_txt_zone_2.get():
            fichiers_charges= Chargement(root_txt_zone_1.get(), root_txt_zone_2.get())
            sequence = fichiers_charges.obtenir_sequence
           # print("Les chemins des fichiers d'imports sont: \n {} \n {}".format(root_txt_zone_1.get(), root_txt_zone_2.get()))
            remplir_onglets(fichiers_charges.obtenir_sequence,fichiers_charges.obtenir_regles)
            demo()
            return fichiers_charges    
        print("Fin de l'import")

    def ensemble_regles_activees_par_sequence(fichiers_charges):
        sequence,regles = fichiers_charges.obtenir_sequence,fichiers_charges.obtenir_regles
        dict_ensemble_regles_activees_par_sequence= dict()
        for regle in regles:
            dict_ensemble_regles_activees_par_sequence.update({"rule_2":sequence.posture_activees(regles.get("rule_2"))})
        print("Liste envoyée pour l'export est {} de type {}".format(dict_ensemble_regles_activees_par_sequence,type(dict_ensemble_regles_activees_par_sequence)))
        
        
        
        fichiers_charges.exporter_xml(dict_ensemble_regles_activees_par_sequence)

    def demo():
        if root_txt_zone_1.get() and root_txt_zone_2.get():
            fichiers_charges= Chargement(root_txt_zone_1.get(), root_txt_zone_2.get())
            sequence = fichiers_charges.obtenir_sequence
            regles=fichiers_charges.obtenir_regles
            print(sequence.postures[16].regles_activees(regles))
            #print(sequence.posture_activees(regles.get("rule_2")))
            #ensemble_regles_activees_par_sequence(fichiers_charges)
    
    root = tk.Tk()
    root.title("MINI_POO - 2022_S2")
    # Fonction d'import doublée faute de mieux
    # Possibilité de complexifier si on sait quel bouton a appelé
   
   

    tk.Label(root,text="chemin du fichier de règles:").grid(row=1,column=0)

    root_txt_zone_2=tk.Entry(root)
    root_txt_zone_2.grid(row=1,column=1)

    root_button_2=tk.Button(root, text = "Selectionner", command = open_rules_file)
    root_button_2.grid(row=1,column=2)

    root_button_3=tk.Button(root, text = "Lancer l'import", command = start_analyzing_process)
    root_button_3.grid(row=2,column=0,sticky="EW",columnspan=3)

   
    
    # Création des zones d'import fichiers
    tk.Label(root,text="chemin du fichier de séquence:").grid(row=0,column=0)
    root_txt_zone_1=tk.Entry(root)
    root_txt_zone_1.grid(row=0,column=1)

    root_button_1=tk.Button(root, text = "Sélectionner", command = open_postures_file)
    root_button_1.grid(row=0,column=2)

    # lien avec les classes

    # Création des onglets
    my_tabs = ttk.Notebook(root) # declaring 

    tab1 = ttk.Frame(my_tabs)
    tab2 = ttk.Frame(my_tabs)
    tab3 = ttk.Frame(my_tabs)

    my_tabs.add(tab1, text ='Affichage') # adding tab
    my_tabs.add(tab2, text ='Plot-evolution') # adding tab 
    my_tabs.add(tab3, text ='Test') # adding tab 

    my_tabs.grid(row=3,column=0,columnspan=3)

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
        
        # On détermine en fonction des boutons pressés les vecteurs à tracer
        print(tab_1_check_but_1_var,tab_1_check_but_2_var)
        if tab_1_check_but_1_var and tab_1_check_but_2_var:  call = 'b'

        elif tab_1_check_but_1_var and not tab_1_check_but_2_var: call = 'v'
            
        elif tab_1_check_but_2_var and not tab_1_check_but_1_var: call = 'a'

        else: call = 'r'

        ax = sequence.postures[posture].tracer(call)
        ##  fig = sequence.postures[posture].tracer(call)
        ax.savefig('image.png',format = 'png')
        canvas = FigureCanvasTkAgg(ax, master=tab1_left_frame)  # A tk.DrawingArea.

        canvas = Canvas(width=5, height=6, bg='black')
        # charger le fichier image .gif
        photo = PhotoImage(file='image.png')
        # mettre l'image sur le canvas
        canvas.create_image(5, 4, image=photo, anchor=NW)
        canvas.get_tk_widget().grid(row=0,column=1)
        canvas.draw()
        import os

        # Spécifier le chemin du fichier à supprimer
        chemin_fichier = 'chemin/vers/image.png'

        # Vérifier si le fichier existe avant de le supprimer
        if os.path.exists(chemin_fichier):
            os.remove(chemin_fichier)
        
    def determiner_coord_evolution(sequence):
        def obtenir(posture,articulation_nom):
                for articulation in posture.articulations:
                    if articulation.nom == articulation_nom:
                        return articulation
                    
        articulation = tab_2_combobox_1.get()
        demande = tab_2_combobox_2.get()
        dt = 1/1.2
        x = [i*dt for i in range(len(sequence.postures))]
        y = []
        for posture in sequence.postures:
            articulation_concernee = obtenir(posture,articulation)
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

    def tracer_evolution(sequence):
        
        x,y = determiner_coord_evolution(sequence)
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

    def lancer_recherche_regles_activees_posture(posture):
        if tab_3_check_but_1_var==1:
            #print("Valeur actuelle de la spnbox: {}".format(tab_3_left_spnbox_1.get()))
            print("Objet de type posture de valeur {}".format(sequence.postures[int(tab_3_left_spnbox_1.get())]))
            print("Posture is_activated ? {}".format(posture.regle_activee))
            if tab_3_left_spnbox_1.get():
                tab_3_left_lstbox_1.update()

    def _lancer_recherche_posture_activant_regle_selectionnee(sequence,regle):
        if tab_3_check_but_1_var==1:
            #La fonction se lance toute seule sans que je comprenne pourquoi
            print("commande lancer_recherche_posture_activant_regle_selectionnee lancée")
            #print(sequence.posture_activees(regle))
            print("Fin de la liste")
            #print("Valeur actuelle de la spnbox: {}".format(tab_3_left_spnbox_1.get()))
        #  print(sequence.posture_activees(regles.get(str(regle))))
            #Pas bsn de test pcq une sélection est forcée
            #tab_3_center_lstbox_1.update(tab_3_center_combobox_1.get()[1])

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
    tab_1_right_spnbox_1=ttk.Spinbox(tab_1_right_frame, from_=0, textvariable = tab_1_right_spnbox_1_var,wrap = True) 
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


    liste_articulations=[0] #A modifier avec la liste des articulations DONE
    tab_2_combobox_1 = ttk.Combobox(tab_2_right_frame, values=liste_articulations)
    tab_2_combobox_1.current(0)
    tab_2_combobox_1.grid(row=0,column=0)

    liste_demandes = ['Angle','Vitesse_moy','Acceleration_moy','Vitesse_ang','Acceleration_ang']
    tab_2_combobox_2 = ttk.Combobox(tab_2_right_frame,values = liste_demandes,state= "readonly")
    tab_2_combobox_2.current(0)
    tab_2_combobox_2.grid(row=3,column=0)
        
    tab_2_but_1=ttk.Button(tab_2_right_frame,text="Tracer l'évolution")
    #command = tracer_evolution())
    tab_2_but_1.grid(row=4,column=0,columnspan = 2)

    racine = ttk
    tab_2_but_2 = ttk.Button(tab_2_right_frame,text = "Clear", command = nettoyer)
    tab_2_but_2.grid(row=5,column=0,columnspan = 2)
    
    #tab 3
    tab_3_check_but_1_var=0

    tab_3_check_but_1 = tk.Checkbutton(tab3,variable=tab_3_check_but_1_var,text="Activer le traitement")
    tab_3_check_but_1.grid(row=0,column=0)

    tab_3_left_frame = tk.Frame(tab3)
    tab_3_left_frame.grid(row=1,column=0)

    tab_3_center_frame = tk.Frame(tab3)
    tab_3_center_frame.grid(row=1,column=1)

    tab_3_right_frame= tk.Frame(tab3)
    tab_3_right_frame.grid(row=1,column=2)

    #Remplissage tab3
    #left_frame
    tab_3_left_lbl_1 = ttk.Label(tab_3_left_frame, text="Sélectionner le numero de la posture:")
    tab_3_left_lbl_1.grid(row=0,column=0)

    tab_3_left_spnbox_1=ttk.Spinbox(tab_3_left_frame, from_=0, to = 0) # A modifier selon nb articulion avec un len DONE
    tab_3_left_spnbox_1.set(0)
    tab_3_left_spnbox_1.grid(row=1,column=0)

    tab_3_left_but_1=tk.Button(tab_3_left_frame,text="Lancer la recherche",command=print("TEST lancer recherche. Y aura-t-il un appel direct sans en comprendre la cause ?"))
    tab_3_left_but_1.bind('<Double-Button-1>', lancer_recherche_regles_activees_posture)
    #tab_3_left_but_1("<Button-1>", lancer_recherche_regles_activees_posture(tab_3_left_spnbox_1.get()))
    tab_3_left_but_1.grid(row=2,column=0)

    tab_3_left_lstbox_1=tk.Listbox(tab_3_left_frame)
    tab_3_left_lstbox_1.insert(1,"élément 1") #(index, valeur)
    tab_3_left_lstbox_1.grid(row=3,column=0)

    #center_frame
    tab_3_center_lbl_1 = ttk.Label(tab_3_center_frame, text="Sélectionner la règle:")
    tab_3_center_lbl_1.grid(row=0,column=0)

    listeProduits2=[0] #A modifier avec la liste des articulations DONE
    #listeProduits2=["ez"]
    tab_3_center_combobox_1 = ttk.Combobox(tab_3_center_frame, values=listeProduits2)
    tab_3_center_combobox_1.current(0)
    tab_3_center_combobox_1.grid(row=1,column=0)

    tab_3_center_but_1=tk.Button(tab_3_center_frame,text="Lancer la recherche de positions")
    tab_3_center_but_1.grid(row=2,column=0)

    tab_3_center_lstbox_1=tk.Listbox(tab_3_center_frame)
    tab_3_center_lstbox_1.grid(row=3,column=0)
    #tab_3_center_lstbox_1.insert(1,"élément 1") #(index, valeur)


    #right_frame
    tab_3_center_but_2=tk.Button(tab_3_right_frame,text="Exporter les règles activées")
    #,command=fichiers_charges.exporter_xml(tab_3_center_lstbox_1.get('1','end'))
    tab_3_center_but_2.grid(row=4,column=0)

    root.mainloop()  # Keep the window open

main()
