#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Récupère Nom/Prénom dans un fichier csv et écrit un nouveau fichier CSV
    avec une colonne supplémentaire : le code AMC. Vous pouvez paramétrer :
    - le nombre de lettres à extraire du nom
    - le nombre de lettres à extraire du prénom
    Attention à bien renseigner le fichier csv où chercher les informations.
    Ce fichier doit comporter au moins ces colonnes (en majuscule) :
    - NOM
    - PRENOM
"""


#Nom du fichier csv d'entrée
csvFile = "chemin/vers/liste.etudiants.csv"

#Nom du fichier de sortie
csvOut = "chemin/vers/liste.avec.codes.csv"

#Séparateur utilisé dans le csv
sep = ","

#Nombre de lettres à extraire au début du nom de famille
nb_nom = 3

#Nombre de lettres à extraire au début du prénom
nb_prenom = 3



import unidecode
import unicodedata


def readCSV(csvFile, sep):
    """Va chercher le fichier csv et créé une liste de dictionnaires.
       Chaque dictionnaire correspond à un étudiant avec toutes les
       informations données sur la première ligne du csv
       Renvoie aussi la ligne d'en-tête pour respecter l'ordre.
    """
    with open(csvFile,"r") as f:
        header = next(f) #on récupère l'en-tête
        header = header[:-1].split(sep)
        plop = []
        for etudiant in f:
            plop.append({}) #on créé un dictionnaire par étudiant
            etudiant = etudiant[:-1].split(sep)
            for j in range(len(etudiant)):
                s = etudiant[j].replace(" ","").replace("-","").lower()
                plop[-1][header[j]] = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('ascii') #Supprime les accents
    return plop, header


def createSetFromName(etudiant, nb_nom, nb_prenom):
    """ Récupère les nb_nom premières lettres du nom et les nb_prenom
        premières lettres du prénom d'un étudiant. Créé un ensemble
        avec (supprime les lettres en double)
    """
    # On créé un ensemble et on y ajoute les lettres
    x = set()
    for i in etudiant['NOM'][:nb_nom]:
        x.add(i)
    for i in etudiant['PRENOM'][:nb_prenom]:
        x.add(i)
    # On trie la liste et on met en majuscules
    return ''.join(sorted(x)).upper()


def createFinalSet(header, etudiants, nb_nom, nb_prenom):
    """ Créé un ensemble avec tous les codes. 
        Affiche un étudiant en cas de doublon.
    """
    for i in range(len(etudiants)):
         x = createSetFromName(etudiants[i], nb_nom, nb_prenom)
         etudiants[i]["CODE"] = x
         etudiants[i]["NUMERO"] = ""
         nb = 0
         for j in range(i-1):
             if etudiants[j]["CODE"] == x:
                nb += 1
                etudiants[j]["NUMERO"] = str(nb)
         if nb:
            etudiants[i]["NUMERO"] = str(nb+1)
    return None


def createCSV(etudiants, nb_nom, nb_prenom, header):
    """ Créé un fichier csv avec les codes (sans doublon, à mettre à jour plus tard)"""
    with open(csvOut, "w") as f:
        header.append('CODE')
        for key in sorted(header):
            f.write(key)
            f.write(',')
        f.write('\n')
        for etudiant in etudiants:
            etudiant["CODE"] = etudiant["CODE"] + etudiant["NUMERO"]
            etudiant["NOM"] = etudiant["NOM"].upper()
            etudiant["PRENOM"] = etudiant["PRENOM"].capitalize()
            if etudiant["NUMERO"]:
                print(etudiant["NOM"] + " " + etudiant["PRENOM"] + " : " + etudiant["NUMERO"])
            del etudiant["NUMERO"]
            for key in sorted(etudiant):
                f.write(etudiant[key])
                f.write(',')
            f.write('\n')    


if __name__ == '__main__':
    print('Ouverture du fichier csv')
    etudiants, header = readCSV(csvFile, sep)
    print('Extraction des premières lettres des noms/prénoms')
    createFinalSet(header, etudiants, nb_nom, nb_prenom)
    print('Recherche de doublons, et affichage ci-dessous le cas échéant')
    print('-'*40)
    createCSV(etudiants, nb_nom, nb_prenom, header)
    print('-'*40)
    print('Terminé !')