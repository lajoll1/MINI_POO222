import xml.etree.ElementTree as ET


chemin_d_acces_fichier_regles="/Users/thomas/Documents/GitHub/MINI_POO222/rules_angles_v1.2.xml"
arbreXML= ET.parse(chemin_d_acces_fichier_regles)
tronc = arbreXML.getroot()
print(tronc[0])
for rule in tronc.iter('rule'):
    print(rule.get('name'))
    print(rule.get('description'))
    print(rule[0])

