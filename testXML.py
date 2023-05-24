import xml.etree.ElementTree as ET

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


class Condition_Simple():

    # Valeur par défaut pour le seuil si domaine préféré
    #liste retenue plutôt que *var et nombre infini de tuples en entrée
    def __init__(self, parameters_list):
        _param_dict=dict()
        for mon_tuple in parameters_list:
            duo_modifiable=list(mon_tuple)
            #conversion des types
            if duo_modifiable[0] == "threshold":duo_modifiable[1]=float(mon_tuple[1])
            if duo_modifiable[0] == "domain":
                duo_modifiable[1]=str(duo_modifiable[1]).removeprefix('(').removesuffix(")")
                duo_modifiable[1] = tuple([float (x) for x in duo_modifiable[1].split(",")])
            if duo_modifiable[0]== "first_corner":
                duo_modifiable[1]=str(duo_modifiable[1]).removeprefix('(').removesuffix(")")
                duo_modifiable[1] = tuple([float (x) for x in duo_modifiable[1].split(",")])
            if duo_modifiable[0]== "second_corner":
                duo_modifiable[1]=str(duo_modifiable[1]).removeprefix('(').removesuffix(")")
                duo_modifiable[1] = tuple([float (x) for x in duo_modifiable[1].split(",")])               
            
            _param_dict.update({duo_modifiable[0]:duo_modifiable[1]})
            print("Dictionnaire mis à jour avec la clef {} et la valeur {} de type {}".format(duo_modifiable[0],duo_modifiable[1],type(duo_modifiable[1])))

    # bool is_activated(class self, posture posture_a_verifier)
    def is_activated(self, posture_a_verifier):
        if isinstance(posture_a_verifier, Posture): 
            
                # Droit d'accéder par élément car dans la classe
                #obtenir_angle_depuis_posture doit être complexifié et prendre en compte le cas où projection
                if self._condition_type == "lower than":
                    if self._obtenir_depuis_posture(posture_a_verifier) < self._param_dict.get("threshold"): return True
                elif self._condition_type == "greater than":
                    if  self._obtenir_depuis_posture(posture_a_verifier) > self._param_dict.get("threshold"): return True
                elif self._condition_type == "belongs to": 
                    if  self._param_dict.get("domain")[0] < self._obtenir_depuis_posture(posture_a_verifier) < self._param_dict.get("domain")[1]: return True
                elif self._condition_type == " belongs to the volume":
                    x,y,z = self._obtenir_depuis_posture(posture_a_verifier)
                    if self._param_dict.get("_first_corner")[0] < x < self._param_dict.get("_second_corner")[0] and \
                       self._param_dict.get("_first_corner")[1] < y < self._param_dict.get("_second_corner")[1] and \
                       self._param_dict.get("_first_corner")[2] < z <  self._param_dict.get("_second_corner")[2]:
                        return True
                #Nouveau if selon les éléments présents dans le dictionnaire
        return False # Si l'on arrive ici, aucune des conditions précédentes n'est vérifiée
        # bool superieur_A_Un_Seuil()

def _obtenir_depuis_posture(self,posture):
    if self._param_dict.get("target") == "angle": return posture.obtenir(self._target_joint).angle
    elif self._param_dict.get("target") == "pos":
        #projection ou vérification 3D?
        if "direction" in self._param_dict.keys:
            #Implique une projection donc disjonction de cas selon l'axe
            #cas avec un angle ?
            #TODO: tratier le cas Domain si projection
            if self._direction == "X":
                return posture.obtenir(self._param_dict.get("_target_joint")).position[0]
            elif self._direction == "Y":
                return posture.obtenir(self._param_dict.get("_target_joint")).position[1]
                #Récupère la 2e coordonnée et la return
            elif self._direction == "Z":
                return posture.obtenir(self._param_dict.get("_target_joint")).position[2]
            else:
                return "Axe non-reconnu"
        else: #forcément de type "belongs to the volume"
            return posture.obtenir(self._param_dict.get("_target_joint"))
            
    
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
            regles.update({rule.get('name'):Regle(rule.get('name'),rule.get('description'),ma_condition_simple)})
            
        elif rule[0].tag == "composed_condition":
           
            liste_conditions_simples = []
            
            print("Début de la règle composée {} de description {}".format(rule.get('name'),rule.get("description")))

            for simple_condition in rule[0].iter("simple_condition"):
                    print("argument envoyé {}".format([mon_tuple for mon_tuple in rule[0].items()]))
                    la_condition_simple=Condition_Simple([mon_tuple for mon_tuple in rule[0].items()]) 
                    liste_conditions_simples.append(ma_condition_simple) #Liste de dictionnaire. Oui c'est moche.

            print("liste de conditions simples finale: {}".format(liste_conditions_simples))  
            regles.update({rule.get('name'):Regle(rule.get('name'),rule.get('description'),liste_conditions_simples)})
            
            


    print(regles)
    return regles

regles = importer_regle("/Users/thomas/Documents/GitHub/MINI_POO222/rules_angles_et_positions_v1.3.xml")
print("test de la règle {}".format(regles["Bac_1"].is_activated(sequence.postures[15])))


