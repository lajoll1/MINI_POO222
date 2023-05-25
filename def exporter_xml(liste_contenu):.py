import xml.etree.ElementTree as ET

def exporter_xml(dico_regle):
    #prend un argument de la forme dictionnaire {nom_règle_activation:[liste_posture activées]}
    # Create root element.
    root = ET.Element("root")
    
    # Add sub element.
    #country = ET.SubElement(root, "country", name="Canada")
    for regle in liste_regle:
       
        regle_activee = ET.SubElement(root, "regle_activee", name=regle) # a remplacer par la regle en question
        # Add sub-sub element.
        posture = ET.SubElement(regle_activee, "posture").text = "test" #remplacer test par le numero de posture
    
    # Write XML file.
    tree = ET.ElementTree(root)
    tree.write("export.xml")

exporter_xml("z")
