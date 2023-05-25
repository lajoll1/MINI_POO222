import xml.etree.ElementTree as ET

class Articulation:
    def __init__(self, tonnom,taposition,taposture):
        self._tonnom = str(tonnom)
        self._taposture_num = taposture.numero
        self._tesneighbors = {"N":[]}
        self._taposition = taposition #[float(num) for num in taposition.strip('()').split(',')]
        self._taposture = taposture
        
    def _lire_nom(self):
        return self._tonnom
    def _lire_position(self):
        return self._taposition
    def _lire_posture(self):
        return self._taposture
    def _lire_voisins(self):
        return self._tesneighbors
    
    nom = property(_lire_nom)
    position = property(_lire_position)
    posture_num = property(_lire_posture)
    voisins = property(_lire_voisins)

    def add_neighbor_child(self, neighbor):
        self._tesneighbors["N"].append(neighbor)

    def add_neighbor_parent(self, neighbor):
        self._tesneighbors["P"] = neighbor

class Posture:
    def __init__(self, frame_number):
        self.frame_number = frame_number
        self._articulations = []
        self._previous_posture = None
        self._next_posture = None

    def _lire_numero(self):
        return self.frame_number
    numero = property(_lire_numero)

    def _lire_articulations(self):
        return self._articulations
    articulations = property(_lire_articulations)

    def _lire_voisins(self):
        return self._previous_posture,self._next_posture
    voisins = property(_lire_voisins)
    
    def add_articulation(self, articulation):
        self._articulations.append(articulation)

    def set_previous_posture(self, posture):
        self._previous_posture = posture

    def set_next_posture(self, posture):
        self._next_posture = posture

class Sequence:
    def __init__(self):
        self.postures = []

    def add_posture(self, posture):
        self.postures.append(posture)

    def set_posture_neighbors(self):
        num_postures = len(self.postures)
        for i in range(num_postures):
            if i > 0:
                self.postures[i].set_previous_posture(self.postures[i-1])
            if i < num_postures - 1:
                self.postures[i].set_next_posture(self.postures[i+1])

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
##        if child_elem.tag == 'Joint':
        child_articulation = parse_joint_element(child_elem,joint_elem,posture)
        articulation.add_neighbor_child(child_articulation)

    parent_articulation = trouver_parent(frame_elem, joint_elem)
    if parent_articulation is not None and parent_articulation.tag == 'Joint':
        parent_articulation = parse_joint_element(parent_articulation, frame_elem, posture)
        articulation.add_neighbor_parent(parent_articulation)
    return articulation

def parse_frame_element(frame_elem,c):
    frame_number = c
    posture = Posture(frame_number)
    for joint_elem in frame_elem.iter('Joint'):
        articulation = parse_joint_element(joint_elem,frame_elem,posture)
        posture.add_articulation(articulation)
    return posture

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    sequence = Sequence()
    c=0
    for frame_elem in root.findall('Frame'):
        posture = parse_frame_element(frame_elem,c)
        sequence.add_posture(posture)
        c+=1

    sequence.set_posture_neighbors()

    return sequence

# Exemple d'utilisation
sequence = parse_xml('/Users/virgilejamot/Desktop/Postures_captures.xml')

# Accéder aux postures et à leurs articulations
##for posture in sequence.postures:
##    print("Frame:", posture.frame_number)
##    for articulation in posture.articulations:
##        print("Articulation:", articulation.name)

