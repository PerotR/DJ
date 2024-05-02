################ Question 1 ################

import random


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
        return self._evaluer(C, 'J1')

    def joueLeCoup(self, C, coup):
        """
        Rend la configuration obtenue apres que le joueur courant ait joue le coup dans la configuration C
        """
        # Copie de la configuration actuelle
        nouvelle_configuration = C.copy()
        # Obtention du joueur courant
        joueur_actuel = self.joueurCourant(C)
        # Mise à jour du plateau avec le coup joué
        nouvelle_configuration['plateau'][coup[0]][coup[1]] = joueur_actuel
        # Vérification si la partie est terminée après le coup joué
        nouvelle_configuration['est_fini'] = self.estFini(nouvelle_configuration)
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

    def _evaluer(self, C, joueur):
        """
        Évalue la configuration C pour le joueur donné
        """
        score = 0
        # Compter les lignes complétées pour le joueur donné
        for i in range(3):
            if all(cell == joueur for cell in C['plateau'][i]):
                score += 1
        # Compter les colonnes complétées pour le joueur donné
        for j in range(3):
            if all(C['plateau'][i][j] == joueur for i in range(3)):
                score += 1
        # Compter les diagonales complétées pour le joueur donné
        if all(C['plateau'][i][i] == joueur for i in range(3)):
            score += 1
        if all(C['plateau'][i][2 - i] == joueur for i in range(3)):
            score += 1
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
    while not jeu.estFini(C):
        coup = strategie_j1.choisirProchainCoup(C) if jeu.joueurCourant(C) == 'J1' else strategie_j2.choisirProchainCoup(C)
        C = jeu.joueLeCoup(C, coup)
        print('\n', C['plateau'][0],'\n', C['plateau'][1],'\n', C['plateau'][2])

    return jeu.f1(C)


################ Exercice 3 ################

class StrategieMinMax(Strategie):
    """
    Represente une strategie utilisant un arbre min-max de profondeur k
    """

    def __init__(self,jeu:JeuSequentiel, k:int):
        super().__init__(jeu,k)

    def noeudsEnfant(self,coups,C):

        coups_restant=[]

        for c in self.jeu.coupsPossibles(C):
            if c != coups:
                coups_restant.append(c)

        return  coups_restant
    

    def MinMax(self,profondeur,coups,C):

        if profondeur == self.k or len(self.noeudsEnfant(self,coups,C))==0:
            return None
        
        return None
    

################ Exercice 4 ################


class Allumettes(JeuSequentiel):
    """
    Represente la strategie optimale pour le jeu des allumettes
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
    
    def plateauttt(self,coup):
        print(self.plateau[coup[0]])

    """def f1(self, C):
        
        #Rend la valeur de l'evaluation de la configuration C pour le joueur 1

        # Pour le Morpion, une évaluation simple peut être le nombre de lignes, colonnes ou diagonales complétées pour J1
        return self._evaluer(C, 'J1')"""



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

    """def _evaluer(self, C, joueur):
        
        Évalue la configuration C pour le joueur donné
        
        score = 0
        # Compter les lignes complétées pour le joueur donné
        for i in range(3):
            if all(cell == joueur for cell in C['plateau'][i]):
                score += 1
        # Compter les colonnes complétées pour le joueur donné
        for j in range(3):
            if all(C['plateau'][i][j] == joueur for i in range(3)):
                score += 1
        # Compter les diagonales complétées pour le joueur donné
        if all(C['plateau'][i][i] == joueur for i in range(3)):
            score += 1
        if all(C['plateau'][i][2 - i] == joueur for i in range(3)):
            score += 1
        return score"""


    






