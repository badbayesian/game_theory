import copy
import itertools
import numpy as np
import pandas as pd


class game():
    """Collection of methods to solve games in game theory.

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
    self.nash_location : list of tuples
        Locations of all nash equilibriums in game
    self.nash : tuple
        Nash Equilibrium values #TODO multi nash and mixed nash
    """

    def __init__(self, payoffs, name='game', mixed=False):
        """Initialize and run game."""
        self.name = name
        self.players = 2
        self.dim = [len(payoffs[0]), len(payoffs[0][1])]
        self.payoffs = self.translate_payoffs(payoffs)
        self.nash_location = self.find_nash(mixed)
        self.nash = self.payoffs[self.nash_location[0][0],
                                 self.nash_location[0][1]]

    def __repr__(self):
        """Print game with pandas, only 26 max choices for now."""
        name = [[chr(i) for i in range(ord('A'), ord('Z') + 1)][0:self.dim[0]],
                [chr(i) for i in range(ord('A'), ord('Z') + 1)][0:self.dim[1]]]
        df = pd.DataFrame([self.payoffs[i] for i in range(0, self.dim[0])],
                          index=name[0], columns=name[1])
        return(self.name + '\n\n' + str(df) + '\n\n' +
               'Nash Equilibrum(s) at: ' + str(self.nash_location))

    def translate_payoffs(self, payoffs):
        """Manipulate payoffs arrays into matrix of tuples."""
        payoff_matrix = np.zeros((self.dim[0], self.dim[1]), dtype='int,int')

        for i in range(0, self.dim[0]):
            for j in range(0, self.dim[1]):
                payoff_matrix[i][j][0] = payoffs[0][i][j]
                payoff_matrix[i][j][1] = payoffs[1][i][j]

        return(payoff_matrix)

    def find_nash(self, mixed):
        """Solve for the nash equilibrium coordinates.

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


class evolution():
    """Simulated iterative, non-memory games.

    This method follows an evolutionary game theory flavor where each there are
    different types of agents, each playing different games depending which
    other agent they find. In each round, all agents are paired up with another
    agent (same or different type) randomly. They play their game and are given
    points accordingly. One can see how the scores evolve over time.

    #TODO Population dynamics within game e.g. after a certain score the pop
    either grows or diminishes.

    Parameters:
    -----------
    games : dict
        Dictionary of games with payoffs
        Example:
        X = [[-5, 5], [10, 8]]
        Y = [[2, 3], [1, 1]]
        games = {"X X": [X, X], "X Y": [X, Y], "Y Y": [Y, Y]}
    player_pop : dict
        Dictionary of agents and number of agents
    number_of_games : int
        Number of games
    init_scores : #TODO
    name : string
        Name of enviroment of games
    mixed : bool
        If true, games are solved using mixed strategies
        If false, games are solved with only deterministic strategies

    Results:
    --------
    self.name : str
        Name of enviroment
    self.player_pop : dict
        Dictionary of agents and number of agents
    self.games :
    self.number_of_games : int
    self.mixed : bool
        If true, games are solved using mixed strategies
        If false, games are solved with only deterministic strategies
    self.scores : array of dict
    """

    def __init__(self, games, player_pop, number_of_games, init_scores=0,
                 name='env', mixed=False):
        """Initialize and run enviroment of games."""
        self.name = name
        self.player_pop = player_pop
        self.games = games
        self.number_of_games = number_of_games
        self.mixed = mixed
        self.scores = self.score_games()

    def __repr__(self):
        """Print information of each different game."""
        return(str([game(name='\n\n' + key, payoffs=values)
                    for (key, values) in self.games.items()]))

    def score_games(self):
        """Run x games recording the score at after each game.

        In this version, only two agents can meet each other to create a game.
        As such, if there is an odd number of players, on player does not play
        that round. The scores are saved as an array of dictonaries for easy
        slicing.\n

        Example: \n
        [{'X': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'Y': [0, 0, 0, 0, 0],
        'Z': [0, 0, 0, 0, 0]}, \n
        {'X': [0, 0, 1, 0, 0, 0, 0, 0, 0, -2],
        'Y': [-1, -1, -1, -2, 2],
        'Z': [0, -1, 2, 2, 2]}]
        """
        scores = [copy.deepcopy({key: [0] * values for (key, values)
                                 in self.player_pop.items()})
                  for x in range(self.number_of_games)]

        player_id = [item for sublist in [
            [key + str(s) for s in list(range(0, values))] for
            (key, values) in self.player_pop.items()] for item in sublist]

        if len(player_id) % 2 != 0:
            player_id = [None] + player_id

        for i in range(1, self.number_of_games):

            length = len(player_id)
            index = np.random.choice(length, size=length, replace=False)

            paired_list = list(zip([player_id[i] for i in index[::2]],
                                   [player_id[i] for i in index[1::2]]))

            for j in range(0, int(length / 2)):
                if not all(paired_list[j]):
                    continue
                players = [["".join(x) for _, x in
                            itertools.groupby(paired_list[j][0],
                                              key=str.isdigit)],
                           ["".join(x) for _, x in
                           itertools.groupby(paired_list[j][1],
                                             key=str.isdigit)]]
                try:
                    g = game(payoffs=self.games[str(players[0][0] +
                                                    " " + players[1][0])])
                except KeyError:
                    g = game(payoffs=self.games[str(players[1][0] +
                                                    " " + players[0][0])])

                scores[i][players[0][0]][int(players[0][1])] = (
                    scores[i - 1][players[0][0]][int(players[0][1])] +
                    g.nash[0])
                scores[i][players[1][0]][int(players[1][1])] = (
                    scores[i - 1][players[1][0]][int(players[1][1])] +
                    g.nash[1])
        return(scores)
