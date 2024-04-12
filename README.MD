Test readme

First, before launching the program you have to install some librarys :

    pip install customtkinter
    pip install CTkMessagebox
    pip install pillow
    pip install threading

You have to set the python in your environnements variables (name: python or python3) 


The score received by each line clear is dependent on the level. Each type of clear, being a single, double, triple, or Tetris, has a base value which is multiplied by the number 1 higher than the current level. For any level 
A single will give 
40∗(n+1)
A double will give 
100∗(n+1)
A triple will give 
300∗(n+1)
A Tetris will give 
1200∗(n+1)
The game also awards points for holding the down key to make pieces fall faster, awarding 1 point for every grid cell that a piece is continuously soft dropped.Unlike line clears, this does not scale by level.

Vitesse = Vitesse_de_base × (1 + Coefficient_d’acceleration × (Niveau−1))

Dans cette équation :
Vitesse
Vitesse représente la vitesse de descente des pièces à un niveau donné.
Vitesse_de_base
Vitesse_de_base est la vitesse initiale de descente des pièces.
Coefficient_d’acceleration
Coefficient_d’acceleration est un nombre positif qui détermine à quel point la vitesse augmente à chaque niveau.
Niveau
Niveau est le niveau actuel du joueur.


Niveau=⌊ 
Lignes_par_niveau
Nombre_total_de_lignes_effac 
e
ˊ
 es
​
 ⌋+1

Dans cette équation :

Niveau
Niveau représente le niveau actuel du joueur.
Nombre_total_de_lignes_effac
e
ˊ
es
Nombre_total_de_lignes_effac 
e
ˊ
 es est le nombre total de lignes que le joueur a effacées depuis le début de la partie.
Lignes_par_niveau
Lignes_par_niveau est le nombre de lignes que le joueur doit effacer pour passer au niveau suivant.
⌊
�
⌋
⌊x⌋ représente la fonction plancher, qui arrondit un nombre réel 
�
x à l'entier le plus proche inférieur.
