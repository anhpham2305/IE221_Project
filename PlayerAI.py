import itertools
import numpy as np
from Game import Grid, Game
from Constants import *

config = Base()


def get_grid(tiles, directions):
    """
    Get the grid after applying the given directions on the tiles.
    """
    g = Grid(config.SIZE)
    g.tiles = tiles.copy()
    for direction in directions:
        g.run(direction)
        g.add_random_tile()
    return g.tiles


def printf(tiles):
    """
    Print the tiles in a formatted way.
    """
    for row in tiles:
        for i in row:
            print("{:^6}".format(i), end='')
        print()


def my_log2(z):
    """
    Custom implementation of logarithm base 2.
    """
    if z == 0:
        return 0
    else:
        return z
        # return np.math.log2(z)


class Ai:
    """
    AI player for the 2048 game.
    """

    def __init__(self):
        self.g = Grid(config.SIZE)

    def get_next(self, tiles):
        """
        Get the next move for the AI player based on the current tiles configuration.
        """
        score_list = []
        tn = self.get_tile_num(tiles)
        if tn >= self.g.size ** 2 / 3:
            return "RD"[np.random.randint(0, 2)], 0
        kn = min(max(tn ** 2, 20), 40)
        for directions in itertools.product("ULRD", repeat=3):
            fen = []
            for i in range(kn):
                t_g = get_grid(tiles, directions)
                fen.append(self.get_score(t_g))
            print(directions, min(fen))
            score_list.append([directions, min(fen)])
        score_list = sorted(score_list, key=(lambda x: [x[1]]))
        # print(score_list)
        for d in score_list[::-1]:
            self.g.tiles = tiles.copy()
            if self.g.run(d[0][0], is_fake=False) != 0:
                return d[0][0], d[1] / kn
        self.g.tiles = tiles.copy()
        return score_list[-1][0][0], score_list[-1][1] / kn

    def get_score(self, tiles):
        """
        Calculate the score for a given tiles configuration.
        """
        a = self.get_bj2__4(tiles)
        b = self.get_bj__4(tiles)
        print(a, b)
        return a * 2.8 + b

    def debug(self, tiles):
        """
        Debug function to print and analyze tile configurations.
        """
        print('\n=======Start Debugging========')
        print('Grid before movement:')
        printf(tiles)
        score_list = []
        for directions in itertools.product("ULRD", repeat=2):
            t_g = get_grid(tiles, directions)
            fen = self.get_score(t_g)
            score_list.append([directions, fen])
            print('==={}=={}=='.format(directions, fen))
            printf(t_g)
        score_list = sorted(score_list, key=(lambda x: [x[1]]))
        for d in score_list[::-1]:
            self.g.tiles = tiles.copy()
            if self.g.run(d[0][0], is_fake=True) != 0:
                self.g.run(d[0][0])
                return d[0][0]
        return score_list[-1][0][0]

    def get_tile_num(self, tiles):
        """
        Get the number of empty tiles on the grid.
        """
        n = 0
        for row in tiles:
            for i in row:
                if i == 0:
                    n += 1
        return n

    def get_bj(self, tiles):
        """
        Get the evaluation scores for each quadrant of the grid.
        """
        gjs = [
            self.get_bj__1(tiles),
            self.get_bj__2(tiles),
            self.get_bj__3(tiles),
            self.get_bj__4(tiles)
        ]
        return gjs

    def get_bj__4(self, tiles):
        """
        Get the evaluation score for the fourth quadrant of the grid.
        """
        bj = 0
        l = len(tiles)
        size = self.g.size - 1
        for y in range(l):
            for x in range(l):
                z = tiles[y][x]
                if z != 0:
                    z_log = z - 2
                    bj += z_log * (x + y - (size * 2 - 1))
                else:
                    bj += (100 - 20 * (x + y - (size * 2 - 1)))
        return bj

    # Implement the other get_bj__ functions similarly

    def get_bj2(self, tiles):
        """
        Get the second evaluation scores for each quadrant of the grid.
        """
        gjs = [
            self.get_bj2__1(tiles),
            self.get_bj2__2(tiles),
            self.get_bj2__3(tiles),
            self.get_bj2__4(tiles)
        ]
        return gjs

    # Implement the get_bj2__ functions similarly

    def get_bj2__4(self, tiles):
        """
        Get the second evaluation score for the fourth quadrant of the grid.
        """
        bj = 0
        l = len(tiles)
        for y in range(l - 1, 0, -1):
            for x in range(l - 1, 0, -1):
                z = tiles[y][x]
                if z < tiles[y][x - 1]:
                    bj -= abs(my_log2(tiles[y][x - 1]) - z)
                if z < tiles[y - 1][x]:
                    bj -= abs(my_log2(tiles[y - 1][x]) - z)
                if z < tiles[y - 1][x - 1]:
                    bj -= abs(my_log2(tiles[y - 1][x - 1]) - z)
        return bj


if __name__ == '__main__':
    game = Game(4)
    game.grid.tiles = np.array([
        [0, 0, 0, 0],
        [0, 32, 64, 128],
        [256, 512, 1024, 1024],
        [1024, 1024, 1024, 1024]
    ])
    ai = Ai()
    print(game.grid)

    a = ai.get_next(game.grid.tiles)
    print(a)
    game.run(a[0])
    print(game.grid)
