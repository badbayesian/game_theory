import numpy as np
import pandas as pd


class game():
    """Method to solve games in game theory.

    Currently able to solve and find nash equilibriums for any two player game
    with finite choices and deterministic strategies given player preferences
    and actions sets (player payoffs)

    Parameter:
    ----------
    payoffs : list of list of each player's payoffs
        payoff matrix inputed as a list of list of each players payoffs read
        clockwise starting from the top-right sector (quadrant)
    name : string
        Name of game played
    mixed : bool
        If true, game is solved using mixed strategies
        If false, game is solved with only deterministic strategies

    Results:
    --------
    self.name : string
        Name of the game played
    self.players : int
        Number of players in game (#TODO expand number of players)
    self.dim : list of int
        List of number of choices each player has in game
    self.payoffs : matrix of tuples (#TODO expand number of players)
        Stores payoffs as matrix of tuples as commonly stored in game theory
    self.nash : list of tuples
        Locations of all nash equilibriums in game
    """

    def __init__(self, payoffs, name='game', mixed=False):
        """Initializes game."""
        self.name = name
        self.players = 2
        self.dim = [len(payoffs[0]), len(payoffs[0][1])]
        self.payoffs = self.translate_payoffs(payoffs)
        self.nash = self.find_nash(mixed)

    def __repr__(self):
        """Pandas looks nicer when presenting, only 26 max choices for now."""
        name = [[chr(i) for i in range(ord('A'), ord('Z') + 1)][0:self.dim[0]],
                [chr(i) for i in range(ord('A'), ord('Z') + 1)][0:self.dim[1]]]
        df = pd.DataFrame([self.payoffs[i] for i in range(0, self.dim[0])],
                          index=name[0], columns=name[1])
        return(self.name + '\n\n' + str(df) + '\n\n' +
               'Nash Equilibrum(s) at:' + str(self.nash))

    def translate_payoffs(self, payoffs):
        """Manipulates payoffs arrays into matrix of tuples."""
        payoff_matrix = np.zeros((self.dim[0], self.dim[1]), dtype='int,int')

        for i in range(0, self.dim[0]):
            for j in range(0, self.dim[1]):
                payoff_matrix[i][j][0] = payoffs[0][i][j]
                payoff_matrix[i][j][1] = payoffs[1][i][j]

        return(payoff_matrix)

    def find_nash(self, mixed):
        """Solves for the nash equilibrium coordinates.

        Currently information is saved as a matrix of tuples. Unclear if that
        will remain if multiagents are added.
        #TODO mixed strategies
        #TODO multiagents
        """
        if not mixed:
            nash = np.zeros((self.dim[0], self.dim[1]), dtype='int,int')

            player_1_choices = []
            for i in range(0, self.dim[1]):
                payoffs_per_column = [payoff[0] for payoff in
                                      [column[i] for column in self.payoffs]]
                player_1_choices.append(
                    np.argwhere(
                        payoffs_per_column == np.amax(payoffs_per_column)))

            for i in range(0, self.dim[1]):
                if len(player_1_choices[i].flatten()) == 1:
                    nash[player_1_choices[i].flatten()[0]][i][0] = 1
                else:
                    for j in range(0, len(player_1_choices[i].flatten())):
                        nash[player_1_choices[i].flatten()[j]][i][0] = 1

            player_2_choices = []
            for i in range(0, self.dim[0]):
                payoffs_per_row = [row[1] for row in self.payoffs[i]]
                player_2_choices.append(
                    np.argwhere(payoffs_per_row == np.amax(payoffs_per_row)))

            for i in range(0, self.dim[0]):
                if len(player_2_choices[i].flatten()) == 1:
                    nash[i][player_2_choices[i].flatten()[0]][1] = 1
                else:
                    for j in range(0, len(player_2_choices[i].flatten())):
                        nash[i][player_2_choices[i].flatten()[j]][1] = 1

        coords = []
        for i in range(0, self.dim[0]):
            for j in range(0, self.dim[1]):
                if nash[i][j][0] == 1 and nash[i][j][1] == 1:
                    coords.append([i, j])

        return(coords)
