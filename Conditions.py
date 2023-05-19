##Imports
import xml.etree.ElementTree as ET



class Regle():
    def __init__(self,mon_nom, ma_description,ma_condition):
        mon_nom=str(mon_nom)
        ma_description=str(ma_description)
        if isinstance(mon_nom, str) and isinstance(ma_description, str) and (isinstance(ma_condition, Condition_Simple) or isinstance(ma_condition, Conditions_composee)):
            self._nom_regle=mon_nom
            self._description_regle=ma_description
            self._condition_associe=ma_condition


class Conditions_composees():
    """.DS_Store"""

    #condition_composée __init__(class self, string operateur, list ma_condition_composee)
    def __init__(self, mon_operateur,ma_condition_composee):
        if mon_operateur in {"or","and"}:
            _operator=mon_operateur
        #Prendre en compte le fait qu'il y a potentiellement n codnitions simples dans la condition complexe
            _liste_conditions_simples=[] #liste en partaeg de pointeurs
            for x in ma_condition_composee:
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
                self._threshold=mon_seuil_ou_domaine
            else: return "Domaine invalide"
        elif mon_type_de_condition == "belongs to the volume":
            pass
        
        #A compléter selon futures règles ?
        if ma_zone_du_corps in {"Neck","RightForeArm","Spine"}:
            self._target_joint=ma_zone_du_corps

    #int obtenir_angle_depuis_posture(posture posture_a_verifier)
    #2-tuple obtenir_seuil_par_projection_depuis_posture(class posture)
    #N2cessité e la méthode is_activated dans condition ?

    #bool is_activated(class self, posture posture_a_verifier)

    def is_activated(self, posture_a_verifier):
        if isinstance(posture_a_verifier, Posture): #vérifier l'orthographe choisi pour la classe
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
                    obtenir_angle_depuis_posture(posture_a_verifier)< self._threshold: return True
                elif self._condition_type =="greater than":
                    if  obtenir_angle_depuis_posture(posture_a_verifier)> self._threshold: return True
                elif self._condition_type =="belongs to":
                    if  self._domain[0] < obtenir_angle_depuis_posture(posture_a_verifier) < self._domain[1]: return True
                return False #Si l'on arrive ici, aucune des conditions précédentes n'est vérifiée
        #bool superieur_A_Un_Seuil()
   
       