import numpy as np
import pandas as pd
import operator

class game():
    """
    Method for individual game which finds nash equilibrium(s) given player
    preferences and actions sets (player payoffs)
    """

    def __init__(self, payoffs, name='game'):
        self.name = name
        self.players = 2
        self.dim = [len(payoffs[0]), len(payoffs[0][1])]
        self.payoffs = self.translate_payoffs(payoffs)
        self.nash = self.find_nash()


    def __repr__(self):
        """
        Pandas looks nicer when presenting, unclear if its too costly to create
        a DataFrame. Only 26 max choices for now.
        """
        names = [[chr(i) for i in range(ord('A'), ord('Z')+1)][0:self.dim[0]],
                 [chr(i) for i in range(ord('A'), ord('Z')+1)][0:self.dim[1]]]
        df = pd.DataFrame([self.payoffs[i] for i in range(0, self.dim[0])],
                          index=names[0], columns=names[1])
        return(self.name + '\n\n' + str(df) + '\n\n' +
               "Nash Equilibrum(s) at:"+ str(self.nash))

    def translate_payoffs(self, payoffs):
        """
        Manipulates payoffs arrays into matrix of tuples
        """
        payoff_matrix = np.zeros((self.dim[0], self.dim[1]),dtype='int,int')

        for i in range(0, self.dim[0]):
            for j in range(0, self.dim[1]):
                payoff_matrix[i][j][0] = payoffs[0][i][j]
                payoff_matrix[i][j][1] = payoffs[1][i][j]

        return(payoff_matrix)


    def find_nash(self):
        """
        Solves for the nash equilibrium coordinates
        """
        nash = np.zeros((self.dim[0], self.dim[1]),dtype='int,int')

        player_1_choices = []
        for i in range(0, self.dim[1]):
            payoffs_per_column = [payoff[0] for payoff in
                                  [column[i] for column in self.payoffs]]
            player_1_choices.append(
                np.argwhere(payoffs_per_column == np.amax(payoffs_per_column)))

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
