import argparse
import os
import subprocess

#définir les arguments
ap = argparse.ArgumentParser()
ap.add_argument("-mot", "--mot", required = True, type = str)
ap.add_argument("-lire_grille", "--lire_grille", action="store_true")
args = ap.parse_args()
detect_grille, mot = args.lire_grille, args.mot

#lancer le script pour numériser la grille
if detect_grille:
    subprocess.run("python .\scan_grille.py")

#lancer le script pour trouver le mot recherché
if "array.npy" in os.listdir():
    subprocess.run(f"python .\montre_mot.py --mot {mot}")
else:
    print("Avez-vous bien pensé à lancer la numérisation de la grille ?")