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
            return angle_deg

        else :
            print("Extrémité ou main !")
            return None
        
    angle = property(_calculer_angle)



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
    
    def _tracer_posture(self):
            instruction = 'b'

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
            
            for articulation in self.articulations:
                # Affichage de la liaison considérée
                ax.scatter(articulation.position[0],articulation.position[2],articulation.position[1],c='r', marker='o') 

                # Liaison de l'articulation avec ses voisins
                if len(articulation.voisinsPOO[1])!=0:
                    for enfant in articulation.voisinsPOO[1]:
                        x1,x2 = enfant.position[0],articulation.position[0]
                        y1,y2 = enfant.position[2],articulation.position[2] 
                        z1,z2 = enfant.position[1],articulation.position[1]
                        ax.scatter([x1,x2], [y1,y2], [z1,z2], c='r', marker='o')
                        ax.plot([x1,x2], [y1,y2], [z1,z2], c='b')

            # Détermination des vecteurs vitesse et accélération
            dt = 1/1.2

            if self.numero != 0 and self.numero != 57: # Ne fonctionne pas pour les postures extrémales
                for articulation in self.articulations: 

                    # Coordonnées 3D des points dans le temps
                    x = [obtenir(articulation.nom,articulation.posture-1).position[0],obtenir(articulation.nom,articulation.posture+1).position[0]]
                    y = [obtenir(articulation.nom,articulation.posture-1).position[1],obtenir(articulation.nom,articulation.posture+1).position[1]]
                    z = [obtenir(articulation.nom,articulation.posture-1).position[2],obtenir(articulation.nom,articulation.posture+1).position[2]]

                    # Calcul des vecteurs vitesse
                    vitesse = []
                    vitesse.append((x[1]-x[0]/(2*dt)))
                    vitesse.append((y[1]-y[0]/(2*dt)))
                    vitesse.append((z[1]-z[0]/(2*dt)))
                    
                    # Tracé du vecteur vitesse si demandé 
                    origine = articulation.position
                    if instruction in ("v","b"):
                        ax.quiver(origine[0], origine[2], origine[1], vitesse[0], vitesse[2], vitesse[1], color='green')


            if self.numero > 1 and self.numero < 56:
                for articulation in self.articulations:

                    # Coordonnées 3D des points dans le temps
                    x = [obtenir(articulation.nom,articulation.posture-2).position[0],obtenir(articulation.nom,articulation.posture).position[0],obtenir(articulation.nom,articulation.posture+2).position[0]]
                    y = [obtenir(articulation.nom,articulation.posture-2).position[1],obtenir(articulation.nom,articulation.posture).position[1],obtenir(articulation.nom,articulation.posture+2).position[1]]
                    z = [obtenir(articulation.nom,articulation.posture-2).position[2],obtenir(articulation.nom,articulation.posture).position[2],obtenir(articulation.nom,articulation.posture+2).position[2]]

                    # Calcul des vecteurs accélération
                    acceleration = []
                    acceleration.append((x[0]+x[2]-2*x[1])/(4*dt))
                    acceleration.append((y[0]+y[2]-2*y[1])/(4*dt))
                    acceleration.append((z[0]+z[2]-2*z[1])/(4*dt))

                    # Tracé du vecteur acceleration si demandé
                    origine = articulation.position
                    if instruction in ("a","b"):
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

    tracer = property(_tracer_posture)


'______________Definition_classe_Séquence_____________'

class Sequence():
    def __init__(self,tespostures):
        self._tespostures = list(tespostures) 

    def _lire_postures(self):
        return self._tespostures
    postures = property(_lire_postures)



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
    
def obtenir(nom_articulation,numero_posture):
    for articulation in sequence.postures[numero_posture].articulations:
        if articulation.nom == nom_articulation:
            return articulation
