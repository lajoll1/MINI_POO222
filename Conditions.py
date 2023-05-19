class Conditions_composees():
    """.DS_Store"""

#condition_composée __init__(class self, string operateur, list ma_condition_composee)
def __init__(self, mon_operateur,ma_condition_composee):
    if mon_operateur in {"or","and"}:
        _operator=mon_operateur
    #Prendre en compte le fait qu'il y a potentiellement n codnitions simples dans la condition complexe
        _condition_list=[]
        for x in ma_condition_composee:
            if isinstance(x, Condition_Simple):
                condition_list.append(x)

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

    <composed_condition operator="and">
			<simple_condition target="angle" condition_type="lower than" threshold="120" target_joint="Spine"/>
			<simple_condition target="angle" condition_type="lower than" threshold="160" target_joint="Neck"/>
		</composed_condition>

class Condition_Simple():

"""
La classe position simple 


"""

    #valeur par défaut pour le seuil si domaine préféré
    def __init__(self,ma_cible,mon_tye_de_condition,mon_seuil,mon_domaine=-1,ma_zone_du_corps):
        #Conversion des types:
        ma_cible=str(ma_cible)
        mon_tye_de_condition= str(mon_tye_de_condition)
        mon_seuil=int(mon_seuil)
        ma_zone_du_corps=str(ma_zone_du_corps)
        
        #Début des test
        if ma_cible in {"angle","position"}: 
            self._target=ma_cible
        else:
            return "type de cible incorrect"

        if mon_tye_de_condition in {"lower than","greater than","belongs to","belongs to the volume"}:
            self._condition_type=mon_tye_de_condition
        else:
            return  "type de condition inconnue"
        
        if isinstance(mon_seuil,int): #Prise en compte des angles négatifs ?
            self._threshold=int(mon_seuil)
        elif isinstance(mon_domaine,tuple) and len(mon_domaine)==2:
            self._domain=mon_domaine
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
                    if  obtenir_angle_depuis_posture(posture_a_verifier)< _threshold: return True
                elif self._condition_type =="greater than":
                    if  obtenir_angle_depuis_posture(posture_a_verifier)> _threshold: return True
                elif self._condition_type =="belongs to":
                    if  self._domain[0] < obtenir_angle_depuis_posture(posture_a_verifier) < self._domain[1]: return True
                return False #Si l'on arrive ici, aucune des conditions précédentes n'est vérifiée
            elif self._target == "posture" #Changer l'intitulé
                if self._condition_type ==" belongs to the volume":
                    pass
                elif self._condition_type =="lower than":
                    obtenir_angle_depuis_posture(posture_a_verifier)< _threshold: return True
                elif self._condition_type =="greater than":
                    if  obtenir_angle_depuis_posture(posture_a_verifier)> _threshold: return True
                elif self._condition_type =="belongs to":
                    if  self._domain[0] < obtenir_angle_depuis_posture(posture_a_verifier) < self._domain[1]: return True
                return False #Si l'on arrive ici, aucune des conditions précédentes n'est vérifiée
        #bool superieur_A_Un_Seuil()
   
       