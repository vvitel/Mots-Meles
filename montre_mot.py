import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np

#argument pour récupérer le mot
ap = argparse.ArgumentParser()
ap.add_argument("-mot", "--mot", required = True, type = str)
args = ap.parse_args()
mot = args.mot

#charger la grille
letters = np.load("./array.npy")


#cases dans la grille des premieres & dernieres lettres
pos_premiere_lettre = np.argwhere(letters == mot[0])
pos_derniere_lettre = np.argwhere(letters == mot[-1])

#on calcul la distance de tchebychev
distance_tchebychev = []
for i in pos_premiere_lettre:
    for j in pos_derniere_lettre:
        dist = max(abs(i[0] - j[0]), abs(i[1] - j[1]))
        distance_tchebychev.append([i, j, dist])

#on garde que les distances égales à nb lettre-1
list_flr = [lst for lst in distance_tchebychev if lst[2] == len(mot)-1]

#on garde que les élements sur la même ligne ou même colonne ou écart de nb lettre-1 diago
fltr_list = [lst for lst in list_flr if (lst[0][0] == lst[1][0]) or (lst[0][1] == lst[1][1]) or ((abs(lst[0][0] - lst[1][0]) == len(mot)-1) and (abs(lst[0][1] - lst[1][1]) == len(mot)-1))]

#si un seul résultat
if len(fltr_list) == 1:
    res = fltr_list[0]
    print("resultat: ", fltr_list)
elif len(fltr_list) == 0:
    print("resultat: désolé je trouve pas ...")
elif len(fltr_list) > 1:
    for i in fltr_list:
        #sur la même ligne
        if i[0][0] == i[1][0]:
            mini, maxi = min(i[0][1], i[1][1]), max(i[0][1], i[1][1])
            string = ""
            for c in range(mini, maxi):
                string = string + letters[i[0][0], c]
            if (string == mot[:-1]) or (string == mot[::-1][:-1]):
                res = i
        #sur la même colonne
        if i[0][1] == i[1][1]:
            mini, maxi = min(i[0][0], i[1][0]), max(i[0][0], i[1][0])
            string = ""
            for c in range(mini, maxi):
                string = string + letters[c, i[0][1]]
            if (string == mot[:-1]) or (string == mot[::-1][:-1]):
                res = i
        #si diagonale
        if (i[0][0] != i[1][0]) and (i[0][1] != i[1][1]):
            dico_seek = {0: [-1, -1], 1: [-1, 1], 2: [1, -1], 3:[1, 1]}
            for dk in dico_seek:
                string = ""
                for c in range(len(mot)):
                    deplace_row, deplace_col = c * dico_seek[dk][0], c * dico_seek[dk][1]
                    try:
                        string = string + letters[i[0][0] + deplace_row, i[0][1] + deplace_col]
                    except:
                        pass
                print(string)
                if string == mot:
                    res = i
                    break

print(res)
            
#ouvrir image
im = cv2.imread("./image.png")
vertical, horizontal = im.shape[0], im.shape[1]
nb_lettre_hor, nb_lettre_ver = 14, 14

#tracer le mot    
if res != "":
    x0 = (vertical / nb_lettre_ver) + (res[0][1] * vertical / nb_lettre_ver) - 20
    y0 = (horizontal / nb_lettre_hor) + (res[0][0] * horizontal / nb_lettre_hor) - 20
    x1 = (vertical / nb_lettre_ver) + (res[1][1] * vertical / nb_lettre_ver) - 20
    y1 = (horizontal / nb_lettre_hor) + (res[1][0] * horizontal / nb_lettre_hor) - 20
    

plt.imshow(im)
plt.plot([x0, x1], [y0, y1], color="magenta", linewidth=5, alpha=0.5)
plt.show()           
            
            
            
            
            
            
            
            
            















#print(fltr_list)

"""
#plusieurs possibilités
if len(fltr_list) == 1:
    res = fltr_list[0]
    print("resultat: ", fltr_list)
elif len(fltr_list) == 0:
    print("resultat: désolé je trouve pas ...")
elif len(fltr_list) > 1:
    dico = {}
    for i in fltr_list:
        #si même ligne
        string = ""
        if i[0][0] == i[1][0]:
            mini, maxi = min(i[0][1], i[1][1]), max(i[0][1], i[1][1])
            for c in range(mini, maxi):
                string = string + letters[i[0][0], c]
            dico[string] = i
        #si même colonne
        string = ""
        if i[0][1] == i[1][1]:
            mini, maxi = min(i[0][0], i[1][0]), max(i[0][0], i[1][0])
            for c in range(mini, maxi):
                string = string + letters[i[0][1], c]
            dico[string] = i

print(dico)
"""






