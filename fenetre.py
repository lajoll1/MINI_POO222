import tkinter  as tk 
from tkinter import ttk
from tkinter import filedialog

root = tk.Tk()
root.geometry("400x200")  

def openfile2():
    filedialog.askopenfilename(filetypes = (("Text files","*.xml"),("all files","*.*"))) #restreindre à fichier XML seulement

#Création des zones d'import fichiers
tk.Label(root,text="chemin du fichier de séquence:").grid(row=0,column=0)
root_txt_zone_1=tk.Entry(root)
root_txt_zone_1.grid(row=0,column=1)

root_button_1=tk.Button(root, text = "Importer", command = openfile2)
root_button_1.grid(row=0,column=2)

tk.Label(root,text="chemin du fichier de règles:").grid(row=1,column=0)

root_txt_zone_2=tk.Entry(root)
root_txt_zone_2.grid(row=1,column=1)

root_button_2=tk.Button(root,text="importer")
root_button_2.grid(row=1,column=2)

#Création des onglets
my_tabs = ttk.Notebook(root) # declaring 

tab1 = ttk.Frame(my_tabs)
tab2 = ttk.Frame(my_tabs)
tab3 = ttk.Frame(my_tabs)

my_tabs.add(tab1, text ='Affichage') # adding tab
my_tabs.add(tab2, text ='Plot-evolution') # adding tab 
my_tabs.add(tab3, text ='Test') # adding tab 

my_tabs.grid(row=2,column=0,columnspan=3)

#Passage à 0 pcq row et column du tab1
tab1_left_frame = tk.Frame(tab1)
tab1_left_frame.grid(row=0,column=0)


tab_1_button_1=tk.Button(root,text="importer")
tab_1_button_1.grid(row=1,column=2)

tab_2_button_1=tk.Button(root,text="importer")
tab_2_button_1.grid(row=1,column=2)
#Ici inclusion du plot matplotlib


#Zone droite du tab1
tab_1_right_frame= tk.Frame(tab1)
tab_1_right_frame.grid(row=0,column=1)

tab_1_rad_but_1=ttk.Checkbutton(tab_1_right_frame,text='Afficher Vitesses')
tab_1_rad_but_1.grid(row=0,column=0)
tab_1_rad_but_2=ttk.Checkbutton(tab_1_right_frame,text='Afficher accélérations')
tab_1_rad_but_2.grid(row=1,column=0)
tab_1_but_1=ttk.Button(tab_1_right_frame,text='Lancer affichage')
tab_1_but_1.grid(row=2,column=0)

#Création zones tab2
tab_2_left_frame = tk.Frame(tab2)
tab_2_left_frame.grid(row=0,column=0)

tab_2_right_frame= tk.Frame(tab2)
tab_2_right_frame.grid(row=0,column=1)
#Zone droite tab2

listeProduits=["Laptop", "Imprimante","Tablette","SmartPhone"] #A modifier avec la liste des articulations
tab_2_combobox_1 = ttk.Combobox(tab_2_right_frame, values=listeProduits)
tab_2_combobox_1.grid(row=0,column=0)

tab_2_rad_but_1=ttk.Checkbutton(tab_2_right_frame,text='Angle')
tab_2_rad_but_1.grid(row=1,column=0)
tab_2_rad_but_2=ttk.Checkbutton(tab_2_right_frame,text='Position')
tab_2_rad_but_2.grid(row=2,column=0)
tab_2_but_1=ttk.Button(tab_2_right_frame,text="Tracer l'évolution")
tab_2_but_1.grid(row=3,column=0)

#tab 3

tab_3_left_frame = tk.Frame(tab3)
tab_3_left_frame.grid(row=0,column=0)

tab_3_center_frame = tk.Frame(tab3)
tab_3_center_frame.grid(row=0,column=1)

tab_3_right_frame= tk.Frame(tab3)
tab_3_right_frame.grid(row=0,column=2)

#Remplissage tab3
#left_frame
tab_3_left_spnbox_1=ttk.Spinbox(tab_3_left_frame, from_=0, to=15) # A modifier selon nb articulion avec un len
tab_3_left_spnbox_1.grid(row=0,column=0)

tab_3_left_but_1=ttk.Button(tab_3_left_frame,text="Lancer la recherche")
tab_3_left_but_1.grid(row=1,column=0)

tab_3_left_lstbox_1=tk.Listbox(tab_3_left_frame)
tab_3_left_lstbox_1.insert(1,"élément 1") #(index, valeur)
tab_3_left_lstbox_1.grid(row=2,column=0)

#center_frame
listeProduits2=["Laptop", "Imprimante","Tablette","SmartPhone"] #A modifier avec la liste des articulations
tab_3_center_combobox_1 = ttk.Combobox(tab_3_center_frame, values=listeProduits2)
tab_3_center_combobox_1.grid(row=0,column=0)

tab_3_center_but_1=ttk.Button(tab_3_center_frame,text="Lancer la recherche")
tab_3_center_but_1.grid(row=1,column=0)

tab_3_center_lstbox_1=tk.Listbox(tab_3_center_frame)
tab_3_center_lstbox_1.grid(row=2,column=0)
tab_3_center_lstbox_1.insert(1,"élément 1") #(index, valeur)


#right_frame
tab_3_right_but_1=tk.Button(tab_3_right_frame,text="Lister et Enregistrer les règles activées")
tab_3_right_but_1.grid(row=0,column=0)





root.mainloop()  # Keep the window open