# Code étudiant 

Le script python présent dans ce dossier permet de générer un fichier csv avec les codes de vos étudiants.

Un code étudiant est composé : 
* des n premières lettres du nom
* des p premières lettres du prénom

Les lettres présentes à la fois dans le nom et le prénom ne sont pas répétées. Par défaut, le script récupère 3 lettres dans le nom et 3 lettres dans le prénom. Après plusieurs essais, ce système fonctionne très bien.

Exemple : 
Alexis Flesch -> AEFL

Si deux étudiants obtiennent le même code, un chiffre supplémentaire leur est attribué automatiquement et le script vous donne alors la liste des étudiants concernés.

Sur une promo de 600 étudiants, on observe de l'ordre d'une dizaine de doublons seulement avec les paramètres par défaut.