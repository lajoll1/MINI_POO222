import xml.etree.ElementTree as ET
import math

'________________Ouverture_fichier_XML________________'

xml_file = "/Users/virgilejamot/Documents/GitHub/MINI_POO222/Postures_captures.xml"

arbreXML = ET.parse(xml_file)
tronc = arbreXML.getroot()



'____________Definition_classe_Articulation___________'

class Articulation():
    def __init__(self,tonnom,taposition):
        self._tonnom = str(tonnom)
        self._taposition = [float(num) for num in taposition.strip('()').split(',')]
        
    def _lire_nom(self):
        return self._tonnom
    def _lire_position(self):
        return self._taposition
    
    nom = property(_lire_nom)
    position = property(_lire_position)
    
    def trouver_voisins(self):
        index = Artics.index(self)
        neighbors = []
        if index > 0:
            neighbors.append(Artics[index-1])
        if index < len(Artics) - 1:
            neighbors.append(Artics[index+1])
        return neighbors
    voisins = property(trouver_voisins)

    def calculer_angle(self):
        if len(self.voisins) == 2:
            x1,y1,z1 = ((self.voisins[0]).position)[0],((self.voisins[0]).position)[1],((self.voisins[0]).position)[2]
            x2,y2,z2 = (self.position)[0],(self.position)[1],(self.position)[2]
            x3,y3,z3 = ((self.voisins[1]).position)[0],((self.voisins[1]).position)[1],((self.voisins[1]).position)[2]

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
        else :
            return ("Extrémité!")

        return angle_deg
    angle = property(calculer_angle)
    
def chargementXML_articulations():
    toutes_articulations = []
    for _articulationXML in tronc[0].iter("Joint"):
        _articulationPOO = Articulation(_articulationXML.get("Name"),_articulationXML.get("Position"))
        toutes_articulations.append(_articulationPOO)
    return toutes_articulations
artic_list = chargementXML_articulations()



'______________Definition_classe_Posture_____________'

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

    def tracer_posture(self):
            positions_articulations = [articulations.position for i in range(len(artic_list))]

            x = [point[0] for point in positions_articulations]
            z = [point[1] for point in positions_articulations]
            y = [point[2] for point in positions_articulations]

            # Création de la figure
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            # Affichage des points en 3D
            ax.scatter(x, y, z, c='r', marker='o')

            # Configuration des axes
            ax.set_xlabel('X')
            ax.set_ylabel('Z')
            ax.set_zlabel('Y')

            # Orientation de la vue
            ax.view_init(elev=8, azim=112)

            # Affichage de la figure
            plt.show()

def chargementXML = 


'______________Definition_classe_Séquence_____________'
class Sequence():
    def __init__(self,tespostures):
        self._tespostures = list(tespostures)

    def _lire_postures(self):
        return self._tesarticulations
