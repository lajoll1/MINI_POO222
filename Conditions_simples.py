Class ConditionSimple():
    #valeur par défaut pour le seuil si domaine préféré
    def __init__(self,ma_cible,mon_tye_de_condition,mon_seuil=-1,mon_domaine,ma_zone_du_corps):
        #Conversion des types:
        ma_cible=str(ma_cible)
        mon_tye_de_condition= str(mon_tye_de_condition)
        mon_seuil=int(mon_seuil)
        ma_zone_du_corps=str(ma_zone_du_corps)
        
        #Début des test
        if ma_cible in {"angle","position"}: 
            self.target=str(ma_cible)
        else:
            return "type de cible incorrect"

        if mon_tye_de_condition in {"lower than","greater than","belongs to","belongs to the volume"}:
            self.condition_type=mon_tye_de_condition
        else:
            return  "type de condition inconnue"
        
        if isinstance(mon_seuil,int) and mon_seuil != -1:
            self.threshold=int(mon_seuil)
        elif isinstance(mon_domaine,tuple) and len(mon_domaine)==2:
            self.domain=mon_domaine
        #A compléter selon futures règles ?
        if ma_zone_du_corps in {"Neck","RightForeArm","Spine"}:
            self.target_joint=ma_zone_du_corps

    #bool superieur_A_Un_Seuil()
    def angle_superieur_a_un_seuil(angle_articulation,seuil):
            if angle_articulation > seuil: return True
            return False
        elif isinstance

    def angle_inferieur_a_un_seuil(angle_articulation, seuil):
        if isinstance(angle_articulation, angle):
            if angle_articulation < seuil: return True
            return False

    def angle_appartient_a_un_domaine(angle, borne_inf, borne_sup):
        if isinstance(angle_articulation, angle):
            if borne_inf < angle > borne_sup: return True
            return False
            
    def appartient_a_un_volume(position, sommet1, sommet2):
        pass

    def projection_sur_un_axe(position,axe):
        pass

    def volume_superieur_a_un_seuil():
        pass

    def volume_inferieur_a_un_seuil(angle_articulation, seuil):
        pass
#N2cessité e la méthode is_activated dans condition ?

    def is_activated(condition_a_verifier):
        if isinstance(angle_articulation, angle):

        elif isinstance(position, poisition_articulaire):

        else:
            return -1
        pass
