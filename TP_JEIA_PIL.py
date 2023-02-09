########################################################
#   ATELIER CHIFFREMENT MULTIMEDIA - Pauline PUTEAUX
#   Contact : pauline.puteaux@cnrs.fr
########################################################


########################################################
#   PACKAGES
########################################################
import matplotlib.pyplot as plt
from PIL import Image
from math import *
import random

########################################################
#   CHARGEMENT D'UNE IMAGE ET ANALYSE
########################################################

# a) Ouvrir une image en niveaux de gris et l'afficher.

def ouvrirImageGris(cheminImage):
    image = Image.open(cheminImage).convert('L')
    return image

def afficherImage(image):
    image.show()

cheminImage = "image.png" # à compléter avec votre image
image = ouvrirImageGris(cheminImage)
afficherImage(image)

############################

# b) Afficher les dimensions de l'image.

tailleImage = image.size
print("Les dimensions de l'image sont : ", tailleImage)

############################

# c) Ecrire une fonction pour afficher l'histogramme d'une image.

def calculHistogramme(image):
    return image.histogram()

def afficherHistogramme(histogrammeImage):
    plt.bar(range(len(histogrammeImage)), histogrammeImage)

histogrammeImage = calculHistogramme(image)
afficherHistogramme(histogrammeImage)

############################

# d) Ecrire une fonction pour calculer l'entropie d'une image. 
def entropieImage(histogrammeImage):
    nbPixels = sum(histogrammeImage)
    entropie = 0
    for val in histogrammeImage:
        if val != 0:
            entropie += (val/nbPixels) * log2(val/nbPixels)
    return (-1) * entropie


entropie = entropieImage(histogrammeImage)
print("L'entropie de l'image est de : ", entropie, "bits par pixel (bpp).")

############################

# e) Ecrire une fonction pour calculer le PSNR entre deux images.

def erreurQuadratiqueMoyenne(image1, image2):
    somme = 0
    for i in range(image1.size[0]):
        for j in range(image1.size[1]):
            difference = image1.getpixel((i,j)) - image2.getpixel((i,j))
            carreDifference = difference ** 2
            somme += carreDifference
    return somme / (image1.size[0] * image1.size[1])

def psnr(image1, image2):
    erreur = erreurQuadratiqueMoyenne(image1, image2)
    if erreur == 0:
        return "inf"
    return 10 * log10((255 ** 2) / erreur)

############################

# Fonctions auxiliaires utiles pour la suite

def image2Dto1D(image):
    listePixels = []
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            listePixels.append(image.getpixel((i,j)))
    return listePixels

def image1Dto2D(listePixels, tailleImage):
    image = Image.new('L', tailleImage)
    k = 0
    for i in range(tailleImage[0]):
        for j in range(tailleImage[1]):
            image.putpixel((i,j), listePixels[k])
            k += 1
    return image

########################################################
#   CHIFFREMENT PAR PERMUTATION
########################################################

# a) Ecrire une fonction qui prend en entrée un nombre n et une clé k, crée une liste [0, n-1]
#  et retourne la liste mélangée en utilisant k en tant que graine d'initialisation.

def melangeIndices(n, k):
    indices = list(range(n))
    random.seed(k)
    random.shuffle(indices)
    return indices

n = 4 # tester plusieurs paramètres
k = 3 # tester plusieurs paramètres
indicesMelanges = melangeIndices(n, k)
print(indicesMelanges)

############################

# b) Ecrire une fonction pour mélanger les pixels d'une image.

def melangeImage(image, k):
    # passage de la 2D à la 1D
    listePixels = image2Dto1D(image)

    # calcul du nombre de pixels 
    n = len(listePixels)

    # generation de la liste d'indices melangés
    indicesMelanges = melangeIndices(n, k)

    # initialisation de l'image chiffrée en 1D
    listePixelsChiffres = [0] * n

    # melange des pixels de l'image originale en utilisant la liste des indices melanges
    for i in range(n):
        nouvelIndice = indicesMelanges[i]
        listePixelsChiffres[i] = listePixels[nouvelIndice]

    # passage de la 1D à la 2D
    imageChiffree = image1Dto2D(listePixelsChiffres, image.size)

    return imageChiffree
    

k = 3 # la valeur de la clé peut être modifiée
imageChiffree1 = melangeImage(image, k)
afficherImage(imageChiffree1)

############################

# c) Afficher l'histogramme et calculer l'entropie de l'image ainsi chiffrée. Que constatez-vous ?

histogrammeImageChiffree1 = calculHistogramme(imageChiffree1)
afficherHistogramme(histogrammeImageChiffree1)

entropieImageChiffree1 = entropieImage(histogrammeImageChiffree1)
print("L'entropie de l'image est de : ", entropieImageChiffree1, "bits par pixel (bpp).")

############################

# d) Ecrire une fonction pour "démélanger" les pixels de l'image.

def demelangeImage(imageChiffree, k):
    # passage de la 2D à la 1D
    listePixelsChiffres = image2Dto1D(imageChiffree)

    # calcul du nombre de pixels 
    n = len(listePixelsChiffres)

    # generation de la liste d'indices melangés
    indicesMelanges = melangeIndices(n, k)

    # initialisation de l'image déchiffrée en 1D
    listePixelsDechiffres = [0] * n

    # melange des pixels de l'image originale en utilisant la liste des indices melanges
    for i in range(n):
        nouvelIndice = indicesMelanges[i]
        listePixelsDechiffres[nouvelIndice] = listePixelsChiffres[i]

    # passage de la 1D à la 2D
    imageDechiffree = image1Dto2D(listePixelsDechiffres, imageChiffree.size)

    return imageDechiffree
    

k = 3 # la valeur de la clé peut être modifiée
imageDechiffree1 = demelangeImage(imageChiffree1, k)
afficherImage(imageDechiffree1)

############################

# e) Vérifier que l'image originale est bien reconstruite sans perte à l'aide du PSNR.

psnr1 = psnr(image, imageDechiffree1)
print("Le PSNR entre les deux images est de", psnr1, "dB.")

########################################################
#   CHIFFREMENT PAR SUBSTITUTION
########################################################

#  a) Ecrire une fonction qui prend en entrée un nombre n et une clé k et génère une séquence 
# pseudo-aléatoire de pixels (valeurs entre 0 et 255) en utilisant la clé comme graine d'initialisation.

def generationPseudoAleatoire(n, k):
    random.seed(k)
    seq = [] 
    for i in range(n):
        seq.append(random.randint(0, 255))
    return seq

n = 100  # le nombre de valeurs générées peut être modifié
k = 10  # la valeur de la clé peut être modifiée
octetsAleatoires = generationPseudoAleatoire(n, k)
print(octetsAleatoires)

############################

# b) En utilisant la fonction précédente, écrire une méthode de chiffrement basée sur 
# l'utilisation du ou-exclusif.

def substitutionImage(image, k):
    # passage de la 2D à la 1D
    listePixels = image2Dto1D(image)

    # calcul du nombre de pixels 
    n = len(listePixels)

    # generation de la liste d'octets pseudo-aléatoires
    octetsAleatoires = generationPseudoAleatoire(n, k)

    # initialisation de l'image chiffrée en 1D
    listePixelsChiffres = [0] * n

    # substitution des pixels de l'image originale en utilisant l'opérateur ou-exclusif (XOR)
    for i in range(n):
        listePixelsChiffres[i] = listePixels[i] ^ octetsAleatoires[i]

    # passage de la 1D à la 2D
    imageChiffree = image1Dto2D(listePixelsChiffres, image.size)

    return imageChiffree

k = 3
imageChiffree2 = substitutionImage(image, k)
afficherImage(imageChiffree2)

############################

# c) Afficher l'histogramme et calculer l'entropie de l'image ainsi chiffrée. Que constatez-vous ?

histogrammeImageChiffree2 = calculHistogramme(imageChiffree2)
afficherHistogramme(histogrammeImageChiffree2)

entropieImageChiffree2 = entropieImage(histogrammeImageChiffree2)
print("L'entropie de l'image est de : ", entropieImageChiffree2, "bits par pixel (bpp).")

############################

# d) L'opération ou-exclusif étant symétrique, vérifier que l'image originale est reconstruite en 
# réappliquant la fonction de chiffrement. 

k = 3
imageDechiffree2 = substitutionImage(imageChiffree2, k)
afficherImage(imageDechiffree2)

psnr2 = psnr(image, imageDechiffree2)
print("Le PSNR entre les deux images est de", psnr2, "dB.")

########################################################
#   CHIFFREMENT SELECTIF PAR PLAN BINAIRE
########################################################

# Utiliser la fonction ci-dessous en faisant varier l'emplacement du plan binaire chiffré.

def substitionPlanBinaire(image, indicePlan, k):
    # passage de la 2D à la 1D
    listePixels = image2Dto1D(image)

    # calcul du nombre de pixels 
    n = len(listePixels)

    # initialisation du générateur pseudo-aléatoire
    random.seed(k)

    # initialisation de l'image chiffrée en 1D
    listePixelsChiffres = [0] * n

    for i in range(n):
        # génération d'un bit (0 ou 1) et décalage à gauche
        bitAleatoire = random.randint(0, 1) << (7 - indicePlan)
        # opération ou-exclusif
        listePixelsChiffres[i] = listePixels[i] ^ bitAleatoire

    # passage de la 1D à la 2D
    imageChiffreeSelectivement = image1Dto2D(listePixelsChiffres, image.size)

    return imageChiffreeSelectivement

############################
    
# Chiffrement du plan binaire le plus significatif (MSB)

k = 3
imageChiffreeMSB = substitionPlanBinaire(image, 0, k)
afficherImage(imageChiffreeMSB)

psnrMSB = psnr(image, imageChiffreeMSB)
print("Le PSNR entre les deux images est de", psnrMSB, "dB.")

############################

# Chiffrement du plan binaire le moins significatif (LSB)

k = 3
imageChiffreeLSB = substitionPlanBinaire(image, 7, k)
afficherImage(imageChiffreeLSB)

psnrLSB = psnr(image, imageChiffreeLSB)
print("Le PSNR entre les deux images est de", psnrLSB, "dB.")
