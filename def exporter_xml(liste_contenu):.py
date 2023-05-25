import xml.etree.ElementTree as ET

def exporter_xml(dico_postures_activees_pour_regle_donnee):
    #prend un argument de la forme dictionnaire {nom_règle_activation:[liste_posture activées]}
    # Create root element.
    root = ET.Element("root")
    
    # Add sub element.
    #country = ET.SubElement(root, "country", name="Canada")
    for regle in dico_postures_activees_pour_regle_donnee.keys():
       
        regle_activee = ET.SubElement(root, "regle_activee", name=regle)
        regle_activee.text=regle # a remplacer par la regle en question
        for posture in dico_postures_activees_pour_regle_donnee.get(regle_activee.text):
            # Add sub-sub element.
            ET.SubElement(regle_activee, "posture").text = posture #remplacer test par le numero de posture

    # Write XML file.
    tree = ET.ElementTree(root)
    tree.write("export.xml")

exporter_xml({"rule1":["posture1","posture2"]})

