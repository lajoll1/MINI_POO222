import xml.etree.ElementTree as ET

class Condition_Simple():

    # Valeur par défaut pour le seuil si domaine préféré
    #liste retenue plutôt que *var et nombre infini de tuples en entrée
    def __init__(self, parameters_list):
        param_dict=dict()
        for mon_tuple in parameters_list:
            param_dict.update({mon_tuple[0]:mon_tuple[1]})

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
                    if self._first_corner[0] < x < self._second_corner[0] and \
                       self._first_corner[1] < y < self._second_corner[1] and \
                       self._first_corner[2] < z <  self._second_corner[2]:
                        return True
                elif self._condition_type == "lower than":
                    pass
                    #
                    if self._obtenir_angle_depuis_projection_posture(posture_a_verifier) < self._threshold: return True
                elif self._condition_type == "greater than":
                    if  self.obtenir_angle_depuis_projection_posture(posture_a_verifier,axe) > self._threshold: return True
                elif self._condition_type == "belongs to":
                    if  self._domain[0] < obtenir_angle_depuis_projection_posture(posture_a_verifier,axe) < self._domain[1]: return True
                return False # Si l'on arrive ici, aucune des conditions précédentes n'est vérifiée
        # bool superieur_A_Un_Seuil()


def importer_regle(chemin_d_acces_fichier_regles):
    arbreXML= ET.parse(chemin_d_acces_fichier_regles)
    tronc = arbreXML.getroot()

    # Dictionnaire de la forme {"nom_règle" : pointeur_de_la_règle_associée}
    regles = dict()

    for rule in tronc.iter('rule'):

        if rule[0].tag == "simple_condition":

            print("argument envoyé {}".format([mon_tuple for mon_tuple in rule[0].items()]))
            ma_condition_simple=Condition_Simple([mon_tuple for mon_tuple in rule[0].items()])   #conversion de type à vérifier  
            regles[rule.get('name')] = Regle(rule.get('name'),rule.get('description'),ma_condition_simple)
            #dictionnaire qui prend des arguments au format {nom_variable_initialisée:valeur_variable_initialisée}

        # Faut-il tout mettre en managé ?
        elif rule[0].tag == "composed_condition":
           
            liste_conditions_simples = []

            for simple_condition in rule[0].iter("simple_condition"):
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


