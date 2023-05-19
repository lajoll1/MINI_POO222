##Imports
import xml.etree.ElementTree as ET



class Regle():
    def __init__(self,mon_nom, ma_description,ma_condition):
        if isinstance(mon_nom, str) and isinstance(ma_description, str) and (isinstance(ma_condition, Condition_Simple) or isinstance(ma_condition, Conditions_composee)):
            self._nom_regle=mon_nom
            self._description_regle=ma_description
            self._condition_associe=ma_condition

    def importer_regle(self,chemin_d_acces_fichier_regles):
        arbreXML= ET.parse(chemin_d_acces_fichier_regles)
        tronc = arbreXML.getroot()


        regles=dict()

        for rule in tronc.iter('rule'):

            if rule[0].tag == "simple_condition":
                #On suppose le fichier xml bien formatté
                if rule[0].get('condition_type') in {"lower than","greater than"}:
                    ma_condition_simple=Condition_Simple(rule[0].get('target'),rule[0].get('condition_type'),rule[0].get("threshold"),rule[0].get('target_joint'))
                elif rule[0].get('condition_type') == "belongs to":
                    ma_condition_simple=Condition_Simple(rule[0].get('target'),rule[0].get('condition_type'),rule[0].get("domain"),rule[0].get('target_joint'))
            
                regles[rule.get('name')]=Regle(rule.get('name'),rule.get('description'),ma_condition_simple)

                print("On ajoute la règle simple {}, de description {} et associée à la condition simple qui a pour éléments constitutifs sa cible {}, un type de conditions {}, un seuil {} et une zone du corps {}".format(rule.get('name'),rule.get('description'),rule[0].get('target'),rule[0].get('condition_type'),rule[0].get("threshold"),rule[0].get('target_joint')))

            #Faut-il tout mettre en managé ?
            elif rule[0].tag == "composed_condition":
                print("Début de la règle composée {} de description {}".format(rule.get('name'),rule.get("description")))
                print("Associée à la condition simple qui a pour éléments constitutifs sa cible {}, un type de conditions {}, un seuil {} et une zone du corps {}".format(simple_condition.get('target'),simple_condition.get('condition_type'),simple_condition.get("threshold"),simple_condition.get('target_joint')))

                liste_conditions_simples=[]

                for simple_condition in rule[0].iter("simple_condition"):
                    if rule[0].get('condition_type') in {"lower than","greater than"}:
                        ma_condition_simple=Condition_Simple(simple_condition.get('target'),simple_condition.get('condition_type'),simple_condition.get("threshold"),simple_condition.get('target_joint'))
                        liste_conditions_simples.append(ma_condition_simple)
                    elif rule[0].get('condition_type') == "belongs to":
                        ma_condition_simple=Condition_Simple(simple_condition.get('target'),simple_condition.get('condition_type'),simple_condition.get("domain"),simple_condition.get('target_joint'))
                        liste_conditions_simples.append(ma_condition_simple)
                        
                regles[rule.get('name')]=Regle(rule.get('name'),rule.get('description'),liste_conditions_simples)

        print(regles)

class Condition_Simple(Regle):

    #valeur par défaut pour le seuil si domaine préféré
    def __init__(self,ma_cible,mon_type_de_condition,mon_seuil_ou_domaine,ma_zone_du_corps=""):
        
        #Début des test
        if ma_cible in {"angle","position"}: 
            self._target=ma_cible
        else:
            return "type de cible incorrect"

        if mon_type_de_condition in {"lower than","greater than","belongs to","belongs to the volume"}:
            self._condition_type=mon_type_de_condition
        else:
            return  "type de condition inconnue"

        #Selon le type de condition
        if mon_type_de_condition in {"lower than","greater than"}:
            if isintance(mon_seuil_ou_domaine,int):
                self._threshold=mon_seuil_ou_domaine
            else: return "Seuil invalide"
        elif mon_type_de_condition == "belongs to":
            if isintance(mon_seuil_ou_domaine,tuple) and len(mon_seuil_ou_domaine) == 2:
                self._domain=mon_seuil_ou_domaine
            else: return "Domaine invalide"
        elif mon_type_de_condition == "belongs to the volume":
            pass

        #A compléter selon futures règles ?
        if ma_zone_du_corps in {"Neck","RightForeArm","Spine"}:
            self._target_joint=ma_zone_du_corps

    #int obtenir_angle_depuis_posture(posture posture_a_verifier)
    #int obtenir_angle_depuis_projection_posture(posture_a_verifier,axe)
    #2-tuple obtenir_seuil_par_projection_depuis_posture(class posture)
    #N2cessité e la méthode is_activated dans condition ?

    #bool is_activated(class self, posture posture_a_verifier)

    def is_activated(self, posture_a_verifier):
        if isinstance(posture_a_verifier, Posture): #vérifier l'orthographe choisi pour la classe Posture
            if self._target == "angle":
                #Droit d'accéder par élément car dans la classe
                if self._condition_type =="lower than":
                    if  obtenir_angle_depuis_posture(posture_a_verifier)< self._threshold: return True
                elif self._condition_type =="greater than":
                    if  obtenir_angle_depuis_posture(posture_a_verifier)> self._threshold: return True
                elif self._condition_type =="belongs to":
                    if  self._domain[0] < obtenir_angle_depuis_posture(posture_a_verifier) < self._domain[1]: return True
                return False #Si l'on arrive ici, aucune des conditions précédentes n'est vérifiée

            elif self._target == "posture": #Changer l'intitulé
                if self._condition_type ==" belongs to the volume":
                    pass
                elif self._condition_type =="lower than":
                    if obtenir_angle_depuis_projection_posture(posture_a_verifier,axe)< self._threshold: return True
                elif self._condition_type =="greater than":
                    if  obtenir_angle_depuis_projection_posture(posture_a_verifier,axe)> self._threshold: return True
                elif self._condition_type =="belongs to":
                    if  self._domain[0] < obtenir_angle_depuis_projection_posture(posture_a_verifier,axe) < self._domain[1]: return True
                return False #Si l'on arrive ici, aucune des conditions précédentes n'est vérifiée
        #bool superieur_A_Un_Seuil()
   
class Condition_composee():
    """.DS_Store"""

    #condition_composée __init__(class self, string operateur, list ma_condition_composee)
    def __init__(self, mon_operateur,ma_liste_de_conditions_simples):
        if mon_operateur in {"or","and"}:
            _operator=mon_operateur
        #Prendre en compte le fait qu'il y a potentiellement n codnitions simples dans la condition complexe
            _liste_conditions_simples=[] #liste en partaeg de pointeurs
            for x in ma_liste_de_conditions_simples:
                if isinstance(x, Condition_Simple):
                    _liste_conditions_simples.append(x)

    #bool is_activated(class self, class posture)
    #                 
    def is_activated(self, ma_posture):
        if isinstance(ma_posture, posture):
            #Assez flexible pour supporter de nouveaux opérateurs en ajoutant en elif
            if self._operator == "and":
                for condition_simple in self._condition_list:
                    if condition_simple.is_activated(ma_posture) == False: return False
            #Verifier toutes les conditions les unes après les autres et renvoyer False si l'une n'est pas vérifiée     
            elif self._operator == "or":
                for condition_simple in self._condition_list:
                    if condition_simple.is_activated(ma_posture): return True
                #renvoyer true à la premirèe condition vérifiée
    