import xml.etree.ElementTree as ET


chemin_d_acces_fichier_regles="/Users/thomas/Documents/GitHub/MINI_POO222/rules_angles_v1.2.xml"
arbreXML= ET.parse(chemin_d_acces_fichier_regles)
tronc = arbreXML.getroot()
print(tronc[0])
regles=dict()
for rule in tronc.iter('rule'):
    if rule[0] == "simple_condition":
        ma_condition_simple=Condition_Simple()
        regles[rule.get('name')]=Regle(rule.get('name'),rule.get('description'),ma_condition_simple)
    #Faut-il tout mettre en managé ?
    elif rule[1] == "composed_condition":
        liste_conditions_simples=[]
        
        for condition in rule[1].iter():
            ma_condition_simple=Condition_Simple()
            liste_conditions_simples.append(ma_condition_simple) 
        ma_condition_composee=Condition_composee(rule.get("operator"),liste_conditions_simples) #Sur 2 lignes pour plus de visibilité
        regles[rule.get('name')]=Regle(rule.get('name'),rule.get('description'),ma_condition_composee)

