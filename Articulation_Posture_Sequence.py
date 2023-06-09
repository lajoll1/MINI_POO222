import xml.etree.ElementTree as ET
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
            if trouver_parent(tronc,self.voisinsXML["P"])!=tronc:
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

        # Test
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
            x = [articulation.position[0] for articulation in ligne]
            y = [articulation.position[2] for articulation in ligne]
            z = [articulation.position[1] for articulation in ligne]
            ax.scatter(x,y,z,c='r',marker = 'o')
            ax.plot(x,y,z,c='b')
                       
        
        for articulation in self.articulations:

            # Affichage de l'articulation considérée
            if articulation.nom == "RightArm":
                ax.scatter(articulation.position[0],articulation.position[2],articulation.position[1],c='k', marker='o')
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
            vitesse = articulation.va_moy[0]
            if call in ("v","b"):
                ax.quiver(origine[0], origine[2], origine[1], vitesse[0], vitesse[2], vitesse[1], color='green')



            # Tracé du vecteur acceleration si demandé
            origine = articulation.position
            acceleration = articulation.va_moy[1]
            if call in ("a","b"):
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



'______________Definition_classe_Séquence_____________'

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

def trouver_parent(tronc, element):
    for enfant in tronc:
        if enfant is element:
            return tronc
        parent = trouver_parent(enfant, element)
        if parent is not None:
            return parent
    return None

def creer_postures_list():
    postures_list = []
    _posturePOO = 0
    c=0
    for _postureXML in tronc:
        articulations_list = []
        for _articulationXML in _postureXML.iter("Joint"):
            above_voisin = trouver_parent(_postureXML,_articulationXML)
            below_voisin = _articulationXML.findall("Joint")
            _articulationPOO = Articulation(_articulationXML.get("Name"),_articulationXML.get("Position"),c,above_voisin,below_voisin)
            articulations_list.append(_articulationPOO)
        _posturePOO = Posture(c,articulations_list)
        postures_list.append(_posturePOO)
        c+=1
    return postures_list

sequence = Sequence(creer_postures_list())

