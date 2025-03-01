import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
from tqdm import tqdm

#configurer pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
config_tesseract = "--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0"

#fonction pour détecter les lettres
def find_letter(image, nb_case):
    im = image[case[nb_case][0]:case[nb_case][1], case[nb_case][2]:case[nb_case][3]]
    im_gray = cv2.cvtColor(im, cv2.IMREAD_GRAYSCALE)
    text = pytesseract.image_to_string(im_gray, config=config_tesseract, lang="eng")
    
    #si pas de détection
    if text == "":
        for t in range(10, 230, 10):
            im_tresh = cv2.threshold(im_gray, t, 255, cv2.THRESH_BINARY)[1]
            text2 = pytesseract.image_to_string(im_tresh, config=config_tesseract, lang="eng")
            if text2 != "":
                text = text2
                break
    
    #lister cases erreurs
    pb = "OK"
    if text == "": pb = nb_case
    
    return text.strip(), pb

#ouvrir image
im = cv2.imread("./image.png")
vertical, horizontal = im.shape[0], im.shape[1]
nb_lettre_hor, nb_lettre_ver = 14, 14

#découper la grille en cases
case_ver = [int(vertical/nb_lettre_ver) * i for i in range(1, nb_lettre_ver+1)]
case_hor = [int(horizontal/nb_lettre_hor) * i for i in range(1, nb_lettre_hor+1)]
case_ver, case_hor = [0] + case_ver, [0] + case_hor

case = []
for v in range(1, len(case_ver)):
    for h in range(1, len(case_hor)):
        case.append((case_ver[v-1], case_ver[v], case_hor[h-1], case_hor[h]))

#appliquer la fonction de détection
letters, probleme = [], []
for i in tqdm(range(nb_lettre_hor * nb_lettre_ver)):
    l, p = find_letter(im, i)
    letters.append(l), probleme.append(p)
    
letters = np.array(letters, dtype=str).reshape(nb_lettre_ver, nb_lettre_hor)
letters = np.char.upper(letters)

#cas des problèmes de détection
probleme = [i for i in probleme if isinstance(i, int)]
print("case non détectées:",  probleme)
    
#appliquer corrections probable
letters = np.char.replace(letters, "0", "O")

#afficher et enregistrer la grille
print("#######DÉTECTÉ#######")
print(letters)
np.save("./array.npy", letters)

"""
#visualisation découpage grille
plt.imshow(im)
#nb_case = 84
#plt.imshow(im[case[nb_case][0]:case[nb_case][1], case[nb_case][2]:case[nb_case][3]])
plt.hlines(case_ver, 0, horizontal)
plt.vlines(case_hor, 0, vertical)
plt.show()
"""
