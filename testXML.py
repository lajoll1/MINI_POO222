import xml.etree.ElementTree as ET


chemin_d_acces_fichier_regles="/Users/thomas/Documents/GitHub/MINI_POO222/rules_angles_v1.2.xml"
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