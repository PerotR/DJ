################ Question 1 ################

import copy
import random
import time
import numpy as np


class JeuSequentiel:
    """
    Represente un jeu sequentiel, a somme
    nulle, a information parfaite
    """
    def __init__(self):
        pass

    def joueurCourant(self, C):
        """
        Rend le joueur courant dans la
        configuration C
        """
        raise NotImplementedError

    def coupsPossibles(self, C):
        """
        Rend la liste des coups possibles dans
        configuration C
        """
        raise NotImplementedError

    def f1(self, C):
        """
        Rend la valeur de l'evaluation de la
        configuration C pour le joueur 1
        """
        raise NotImplementedError

    def joueLeCoup(self, C, coup):
        """
        Rend la configuration obtenue apres
        que le joueur courant ait joue le coup
        dans la configuration C
        """
        raise NotImplementedError

    def estFini(self, C):
        """
        Rend True si la configuration C est
        une configuration finale
        """
        raise NotImplementedError


################ Question 2 ################

class Morpion(JeuSequentiel):
    """
    Represente le jeu du morpion (3x3)
    """


    def __init__(self):
        super().__init__()
        # Initialisation spécifique au Morpion, par exemple, un plateau vide
        self.plateau = [[' ' for _ in range(3)] for _ in range(3)]

    def joueurCourant(self, C):
        """
        Rend le joueur courant dans la configuration C
        """
        return C['prochain_joueur']

    def coupsPossibles(self, C):
        """
        Rend la liste des coups possibles dans la configuration C
        """
        coups = []
        for i in range(3):
            for j in range(3):
                if C['plateau'][i][j] == ' ':
                    coups.append((i, j))
        return coups

    def f1(self, C):
        """
        Rend la valeur de l'evaluation de la configuration C pour le joueur 1
        """
        # Pour le Morpion, une évaluation simple peut être le nombre de lignes, colonnes ou diagonales complétées pour J1
        return self._evaluer(C)

    def joueLeCoup(self, C, coup):
        """
        Rend la configuration obtenue apres que le joueur courant ait joue le coup dans la configuration C
        """
        # Copie de la configuration actuelle
        nouvelle_configuration = C.copy()
        # Obtention du joueur courant
        joueur_actuel = self.joueurCourant(C)
        # Mise à jour du plateau avec le coup joué
        if joueur_actuel=='J1':
            nouvelle_configuration['plateau'][coup[0]][coup[1]] = 'X'

        else:
            nouvelle_configuration['plateau'][coup[0]][coup[1]] = 'O'

        # Vérification si la partie est terminée après le coup joué
        nouvelle_configuration['est_fini'] = self.estFini(nouvelle_configuration)
        if not nouvelle_configuration['est_fini']:
            nouvelle_configuration['prochain_joueur'] = 'J1' if joueur_actuel == 'J2' else 'J2'

        return nouvelle_configuration

    def estFini(self, C):
        """
        Rend True si la configuration C est une configuration finale
        """
        # Vérification des lignes
        for i in range(3):
            if C['plateau'][i][0] == C['plateau'][i][1] == C['plateau'][i][2] != ' ':
                return True
        # Vérification des colonnes
        for j in range(3):
            if C['plateau'][0][j] == C['plateau'][1][j] == C['plateau'][2][j] != ' ':
                return True
        # Vérification des diagonales
        if (C['plateau'][0][0] == C['plateau'][1][1] == C['plateau'][2][2] != ' ') or \
           (C['plateau'][0][2] == C['plateau'][1][1] == C['plateau'][2][0] != ' '):
            return True
        # Si aucun alignement n'est trouvé, vérifie si le plateau est rempli
        for row in C['plateau']:
            if ' ' in row:
                return False
        # Si le plateau est rempli et aucun joueur n'a gagné, la partie est terminée en match nul
        return True

    def _evaluer(self, C):
        """
        Évalue la configuration C pour le joueur donné
        """
        score = 0

        # Compter les lignes, colonnes et diagonales complétées ou presque complétées pour chaque joueur
        for joueur in ['X', 'O']:
            point = 1 if joueur == 'X' else -1

            for i in range(3):
                if C['plateau'][i].count(joueur) == 2 and C['plateau'][i].count(' ') == 1:
                    score += point
                if [C['plateau'][j][i] for j in range(3)].count(joueur) == 2 and [C['plateau'][j][i] for j in range(3)].count(' ') == 1:
                    score += point

            if [C['plateau'][i][i] for i in range(3)].count(joueur) == 2 and [C['plateau'][i][i] for i in range(3)].count(' ') == 1:
                score += point
            if [C['plateau'][i][2 - i] for i in range(3)].count(joueur) == 2 and [C['plateau'][i][2 - i] for i in range(3)].count(' ') == 1:
                score += point

        return score


################ Exercice 2 ################

class Strategie:
    """
    Represente une strategie de jeu
    """
    def __init__(self, jeu:JeuSequentiel):
        self.jeu = jeu
        pass

    def choisirProchainCoup(self, C):
        """
        Choisit un coup parmi les coups possibles dans la configuration C
        """
        raise NotImplementedError
    

class StrategieAleatoire(Strategie):
    """
    Represente une strategie de jeu aleatoire pour tout jeu sequentiel
    """

    def __init__(self, jeu:JeuSequentiel):
        super().__init__(jeu)

    def choisirProchainCoup(self, C):
        """
        Choisit un coup aleatoire suivant une distribution uniforme sur tous les coups
        possibles dans la configuration C        
        """
        coups_possibles = self.jeu.coupsPossibles(C)
        return coups_possibles[random.randint(0, len(coups_possibles) - 1)]
    


def morpionAleatoire():
    """
    Joue une partie de Morpion avec une strategie aleatoire pour chaque joueur
    """
    jeu = Morpion()
    strategie_j1 = StrategieAleatoire(jeu)
    strategie_j2 = StrategieAleatoire(jeu)

    
    C = {'plateau': jeu.plateau, 'prochain_joueur': 'J1', 'est_fini': False}
    print("Le joueur J1 joue les X")
    print("Le joueur J2 joue les O")
    while not jeu.estFini(C):
        coup = strategie_j1.choisirProchainCoup(C) if jeu.joueurCourant(C) == 'J1' else strategie_j2.choisirProchainCoup(C)
        C = jeu.joueLeCoup(C, coup)
        print('\n',C['plateau'][0],'\n', C['plateau'][1],'\n', C['plateau'][2],'\n')

    return C['prochain_joueur']


def morpionMinMax():
    """
    Joue une partie de Morpion avec une strategie aleatoire pour chaque joueur
    """
    jeu = Morpion()
    strategie_j1 = StrategieMinMax(jeu,3)
    strategie_j2 = StrategieMinMax(jeu,3)

    
    C = {'plateau': jeu.plateau, 'prochain_joueur': 'J1', 'est_fini': False}
    print("Le joueur J1 joue les X")
    print("Le joueur J2 joue les O")
    while not jeu.estFini(C):
        coup = strategie_j1.choisirProchainCoup(C) if jeu.joueurCourant(C) == 'J1' else strategie_j2.choisirProchainCoup(C)
        C = jeu.joueLeCoup(C, coup)
        print('\n',C['plateau'][0],'\n', C['plateau'][1],'\n', C['plateau'][2],'\n')

    return C['prochain_joueur']


################ Exercice 3 ################

class StrategieMinMax(Strategie):
    """
    Represente une strategie utilisant un arbre min-max de profondeur k
    """
    def __init__(self,jeu:JeuSequentiel, k:int):
        super().__init__(jeu)
        self.k = k

    def choisirProchainCoup(self, C):
        """
        Choisit un coup parmi les coups possibles dans la configuration C
        """

        return self.MinMax(C, self.k)[1]


    
    def MinMax(self, C, k, coup_joue=None):

        if self.jeu.coupsPossibles(C) == []:
            return self.jeu.f1(C), coup_joue

        if k==0 or C['est_fini']:
            if coup_joue ==None:
                coup_joue = self.jeu.coupsPossibles(C)[0]
            return self.jeu.f1(C), coup_joue
        
        if C['prochain_joueur'] == 'J1':
            val = float('-inf')
            cp = None
            for coup in self.jeu.coupsPossibles(C):
                
                C_copy = copy.deepcopy(C)
                self.jeu.joueLeCoup(C_copy,coup)
                next_value, next_coup = self.MinMax(C_copy, k-1, coup)
                if next_value > val:
                    val = next_value
                    cp = next_coup
            
            return val, cp
        else:
            val = float('inf')
            cp = None
            for coup in self.jeu.coupsPossibles(C):
                C_copy = copy.deepcopy(C)
                self.jeu.joueLeCoup(C_copy,coup)
                next_value, next_coup = self.MinMax(C_copy, k-1, coup)
                if next_value < val:
                    val = next_value
                    cp = next_coup
            return  val, cp
        
    def toString(self):
        return "MinMax"
    
################ Exercice 4 ################


class Allumettes(JeuSequentiel):
    """
    Represente le jeu des allumettes pour $g$ groupe de $m$ allumettes
    """

    def __init__(self, g:int,m:int):
        super().__init__()
        self.m=m
        self.g=g
        self.plateau = {}
        for i in range (self.g):
            self.plateau[i+1]=m

    def joueurCourant(self, C):
        """
        Rend le joueur courant dans la configuration C
        """
        return C['prochain_joueur']

    def coupsPossibles(self, C):
        """
        Rend la liste des coups possibles dans la configuration C
        """
        coups = []
        
        for i in (C['plateau']):
            for j in range(C['plateau'][i]):
                coups.append((i, j+1))
        return coups

    def f1(self, C):
        
        #Rend la valeur de l'evaluation de la configuration C pour le joueur 1

        return self._evaluer(C)



    def joueLeCoup(self, C, coup):
        """
        Rend la configuration obtenue apres que le joueur courant ait joue le coup dans la configuration C
        """
        # Copie de la configuration actuelle
        nouvelle_configuration = C.copy()
        # Obtention du joueur courant
        joueur_actuel = self.joueurCourant(C)
        # Mise à jour du plateau avec le coup joué
        if coup[1]<= C['plateau'][coup[0]]:
            nouvelle_configuration['plateau'][coup[0]] -= coup[1]
        # Vérification si la partie est terminée après le coup joué
        nouvelle_configuration['est_fini'] = self.estFini(nouvelle_configuration)
        if not nouvelle_configuration['est_fini']:
            nouvelle_configuration['prochain_joueur'] = 'J1' if joueur_actuel == 'J2' else 'J2'

        return nouvelle_configuration

    def estFini(self, C):
        """
        Rend True si la configuration C est une configuration finale
        """
        som=0
        for i in (C['plateau']):
            som+=C['plateau'][i]
        
        if som==0:
            return True
        return False

    def _evaluer(self, C):
        """
        Évalue la configuration C pour le joueur donné
        """
        score = 0
        somme_allumettes = sum(C['plateau'].values())

        if C['prochain_joueur'] == 'J1':
            score = 1 if somme_allumettes % 2 == 1 else -1
        else:
            score = -1 if somme_allumettes % 2 == 1 else 1

        return score
    

class StrategieAllumettes(Strategie):
    """
    Represente la strategie optimale pour le jeu des allumettes 
    """
    def __init__(self, jeu:Allumettes):
        super().__init__(jeu)

    def grundy(self,n):
        return [i for i in range(n+1)]
    def dec_to_bin(self,num):
        if num == 0:
            return '0'
        res = ''
        quot = num

        while quot > 0:
            res = str(quot % 2) + res
            quot = quot // 2
        return res
    def bin_to_dec(self,num):
        res = 0
        power = len(num) - 1

        for i in num:
            if i == '1':
                res += 2 ** power
            power -= 1
        return res

    def Som_Nim(self,num1,num2):

        a=self.dec_to_bin(num1)
        b=self.dec_to_bin(num2)

        i=min(len(a),len(b))
        j=max(len(a),len(b))
        r=j-i
        res=''

        if len(a)>len(b):
            while r>0:
                b='0'+b
                r-=1
        else:
            while r>0:
                a='0'+a
                r-=1

        for k in range(j):
            if ((a[k]=='1' and b[k]=='1') or (a[k]=='0' and b[k]=='0')):
                res+='0'

            elif ((a[k]=='1' and b[k]=='0') or (a[k]=='0' and b[k]=='1')) :
                res+='1'
        res=self.bin_to_dec(res)
        return res

    def gagnante(self,C):

        max=0

        for i in (C['plateau']):
            if C['plateau'][i]>max:
                max=C['plateau'][i]

        g=self.grundy(max)

        res=0

        for i in C['plateau']:
            res= self.Som_Nim(res,g[C['plateau'][i]])

        if res==0:
            return (False,0)
        else:
            return (True,res)
        
    def choisirProchainCoup(self, C):
        (b,g)=self.gagnante(C)
        coups_choisi=None
        g_choisi=None
        if b:
            res=0
            coupsTrouver=False
            coupsPossibles= self.jeu.coupsPossibles(C)

            while res < len(coupsPossibles) and not coupsTrouver:

                C['plateau'][coupsPossibles[res][0]]-=coupsPossibles[res][1]
                (bi,gi)=self.gagnante(C)
                C['plateau'][coupsPossibles[res][0]]+=coupsPossibles[res][1]

                if not bi:
                    coupsTrouver=True

                else:
                    res+=1
            g_choisi=coupsPossibles[res][0]
            coups_choisi=coupsPossibles[res][1]

        else:
            max=0
            coupsPossibles=self.jeu.coupsPossibles(C)
            for s,coups in coupsPossibles:

                C['plateau'][s]-=coups
                (bi,gi)=self.gagnante(C)
                C['plateau'][s]+=coups

                if gi>max:

                    g_choisi=s
                    coups_choisi=coups
                    max=gi
        return (g_choisi,coups_choisi)


def Allumettes_Jeu_Nim(g,m):

    jeu=Allumettes(g,m)
    strategie_j1 = StrategieAllumettes(jeu)
    strategie_j2 = StrategieAllumettes(jeu)
    C = {'plateau': jeu.plateau, 'prochain_joueur': 'J1', 'est_fini': False}
    while not jeu.estFini(C):
        coup = strategie_j1.choisirProchainCoup(C) if jeu.joueurCourant(C) == 'J1' else strategie_j2.choisirProchainCoup(C)
        C = jeu.joueLeCoup(C, coup)
        print(C['plateau'])
    return C['prochain_joueur']


##############################################################################

morpion = Morpion()

strategie_j1 = StrategieAleatoire(morpion)
strategie_j2 = StrategieMinMax(morpion,6)



C = {'plateau': morpion.plateau, 'prochain_joueur': 'J1', 'est_fini': False}
while not morpion.estFini(C):
    coup = strategie_j1.choisirProchainCoup(C) if morpion.joueurCourant(C) == 'J1' else strategie_j2.choisirProchainCoup(C)
    C = morpion.joueLeCoup(C, coup)

print(C['prochain_joueur'])



def tournoiMorpion(k):

    victoire_J1=0
    victoire_J2=0
    temps_executions = []
    
    for _ in range(100):
        morpion = Morpion()
        strategie_j1 = StrategieAleatoire(morpion)
        strategie_j2 = StrategieMinMax(morpion,k)
        C = {'plateau': morpion.plateau, 'prochain_joueur': 'J2', 'est_fini': False}
        debut = time.time()
        while not morpion.estFini(C):
            coup = strategie_j1.choisirProchainCoup(C) if morpion.joueurCourant(C) == 'J1' else strategie_j2.choisirProchainCoup(C)
            C = morpion.joueLeCoup(C, coup)
        if C['prochain_joueur']=='J1':
            victoire_J1+=1
        else:
            victoire_J2+=1
        fin = time.time()
        temps_executions.append(fin - debut)

    return [victoire_J1,victoire_J2,np.sum(temps_executions), np.mean(temps_executions)]
            

def tournoiAllumette_Ale(g,m):


    victoire_J1=0
    victoire_J2=0
    temps_executions = []
    for _ in range (100):
        allumettes= Allumettes(g,m)

        strategie_j1 = StrategieAllumettes(allumettes)
        strategie_j2 = StrategieAleatoire(allumettes)
        C = {'plateau': allumettes.plateau, 'prochain_joueur': 'J1', 'est_fini': False}
        debut = time.time()
        while not allumettes.estFini(C):
            coup = strategie_j1.choisirProchainCoup(C) if allumettes.joueurCourant(C) == 'J1' else strategie_j2.choisirProchainCoup(C)
            C = allumettes.joueLeCoup(C, coup)
        if C['prochain_joueur']=='J1':
            victoire_J1+=1
        else:
            victoire_J2+=1
        fin = time.time()

        temps_executions.append(fin - debut)

    return [victoire_J1,victoire_J2,np.sum(temps_executions), np.mean(temps_executions)]


def tournoiAllumette_MinMax(g,m,k):

    victoire_J1=0
    victoire_J2=0
    temps_executions = []
    for _ in range (100):
        allumettes= Allumettes(g,m)

        strategie_j1 = StrategieAllumettes(allumettes)
        strategie_j2 = StrategieMinMax(allumettes,k)
        C = {'plateau': allumettes.plateau, 'prochain_joueur': 'J1', 'est_fini': False}
        debut = time.time()
        while not allumettes.estFini(C):
            coup = strategie_j1.choisirProchainCoup(C) if allumettes.joueurCourant(C) == 'J1' else strategie_j2.choisirProchainCoup(C)
            C = allumettes.joueLeCoup(C, coup)
        if C['prochain_joueur']=='J1':
            victoire_J1+=1
        else:
            victoire_J2+=1
        fin = time.time()

        temps_executions.append(fin - debut)

    return [victoire_J1,victoire_J2,np.sum(temps_executions), np.mean(temps_executions)]

def tournoiAllumette(g,m):

    victoire_J1=0
    victoire_J2=0
    temps_executions = []
    for _ in range (100):

        allumettes= Allumettes(g,m)

        strategie_j1 = StrategieAllumettes(allumettes)
        strategie_j2 = StrategieAllumettes(allumettes)
        C = {'plateau': allumettes.plateau, 'prochain_joueur': 'J1', 'est_fini': False}
        debut = time.time()
        while not allumettes.estFini(C):
            coup = strategie_j1.choisirProchainCoup(C) if allumettes.joueurCourant(C) == 'J1' else strategie_j2.choisirProchainCoup(C)
            C = allumettes.joueLeCoup(C, coup)
        if C['prochain_joueur']=='J1':
            victoire_J1+=1
        else:
            victoire_J2+=1
        fin = time.time()

        temps_executions.append(fin - debut)

    return [victoire_J1,victoire_J2,np.sum(temps_executions), np.mean(temps_executions)]


