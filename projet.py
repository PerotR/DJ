################ Question 1 ################

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
        return C['joueur']

    def coupsPossibles(self, C):
        """
        Rend la liste des coups possibles dans
        configuration C
        """
        return C['coups_possibles']

    def f1(self, C):
        """
        Rend la valeur de l'evaluation de la
        configuration C pour le joueur 1
        """
        return C['evaluation_joueur1']

    def joueLeCoup(self, C, coup):
        """
        Rend la configuration obtenue apres
        que le joueur courant ait joue le coup
        dans la configuration C
        """
        nouvelle_configuration = C.copy()
        # Mise à jour du joueur courant
        nouvelle_configuration['joueur'] = 1 if C['joueur'] == 2 else 2
        nouvelle_configuration['prochainJoueur'] = 1 if nouvelle_configuration['joueur'] == 2 else 2
        nouvelle_configuration['historique_coups'].append(coup)

        return nouvelle_configuration

    def estFini(self, C):
        """
        Rend True si la configuration C est
        une configuration finale
        """
        # Exemple de logique pour déterminer si la configuration est finale (à remplacer par votre propre logique)
        return C['est_fini']


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
                if self.plateau[i][j] == ' ':
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


if __name__ == "__main__":
    # Création d'une instance de jeu de Morpion
    morpion = Morpion()
    # Configuration initiale
    config_initiale = {
        'plateau': [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
        'prochain_joueur': 'J1',
        'est_fini': False
    }
    print("Configuration initiale du Morpion:", config_initiale)

    print("C'est au tour de", morpion.joueurCourant(config_initiale));

    # Exemple d'appel des méthodes pour jouer un coup
    coup_joue = (0, 0)
    nouvelle_config = morpion.joueLeCoup(config_initiale, coup_joue)

    print("Nouvelle configuration après avoir joué le coup", coup_joue, ":", nouvelle_config)
    print("Est-ce que la nouvelle configuration est finale ?", morpion.estFini(nouvelle_config))


    coup_joue = (1, 1)
    nouvelle_config1 = morpion.joueLeCoup(nouvelle_config, coup_joue)

    print("Nouvelle configuration après avoir joué le coup", coup_joue, ":", nouvelle_config1)
    print("Est-ce que la nouvelle configuration est finale ?", morpion.estFini(nouvelle_config1))
