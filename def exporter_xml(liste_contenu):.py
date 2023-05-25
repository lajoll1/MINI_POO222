 def exporter_xml(liste_contenu):
        # Create root element.
        root = ET.Element("root")
        
        # Add sub element.
        #country = ET.SubElement(root, "country", name="Canada")
        country = ET.SubElement(root, "regle_activee", name="rule_1") # a remplacer par la regle en question
        ontario = ET.SubElement(rule_1, "posture1")# a adatper également

        # Add sub-sub element.
        ontario = ET.SubElement(country, "province")
        ontario.text = "Ontario"
        ontario.set("rank", "2")    # Set attribute rank="2"
        
        # One-liner to create Alberta province.
        ET.SubElement(country, "province", rank="3", category="oil").text = "Alberta"
        
        # Write XML file.
        tree = ET.ElementTree(root)
        tree.write("export.xml")
