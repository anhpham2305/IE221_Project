import random
import numpy as np


class Grid:
    """Class representing the game grid."""

    size = 4
    tiles = []
    max_tile = 0

    def __init__(self, size=4):
        """
        Initialize the grid.

        Args:
            size (int): The size of the grid (default: 4).
        """
        self.size = size
        self.score = 0
        self.tiles = np.zeros((size, size)).astype(np.int32)

    def is_zero(self, x, y):
        """
        Check if the tile at the given coordinates is zero.

        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.

        Returns:
            bool: True if the tile is zero, False otherwise.
        """
        return self.tiles[y][x] == 0

    def is_full(self):
        """
        Check if the grid is full.

        Returns:
            bool: True if the grid is full, False otherwise.
        """
        return 0 not in self.tiles

    def set_tiles(self, xy, number):
        """
        Set the value of a tile at the given coordinates.

        Args:
            xy (tuple): The coordinates of the tile as a tuple (x, y).
            number (int): The value to set on the tile.
        """
        self.tiles[xy[1]][xy[0]] = number

    def get_random_xy(self):
        """
        Get random empty coordinates on the grid.

        Returns:
            tuple: The coordinates of an empty tile as a tuple (x, y), or (-1, -1) if the grid is full.
        """
        if not self.is_full():
            while 1:
                x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
                if self.is_zero(x, y):
                    return x, y
        return -1, -1

    def add_tile_init(self):
        """Add two random tiles to the grid at the start of the game."""
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        """Add a random tile (either 2 or 4) to the grid at an empty position."""
        if not self.is_full():
            value = 2 if random.random() < 0.9 else 4
            self.set_tiles(self.get_random_xy(), value)

    def run(self, direction, is_fake=False):
        """
        Run the game in the given direction.

        Args:
            direction (str): The direction to move the tiles ('U', 'D', 'L', 'R').
            is_fake (bool): Whether the move is fake (default: False).

        Returns:
            int: The score obtained from the move.
        """
        if isinstance(direction, int):
            direction = nmap[direction]
        self.score = 0
        if is_fake:
            t = self.tiles.copy()
        else:
            t = self.tiles
        if direction == 'U':
            for i in range(self.size):
                self.move_hl(t[:, i])
        elif direction == 'D':
            for i in range(self.size):
                self.move_hl(t[::-1, i])
        elif direction == 'L':
            for i in range(self.size):
                self.move_hl(t[i, :])
        elif direction == 'R':
            for i in range(self.size):
                self.move_hl(t[i, ::-1])
        return self.score

    def move_hl(self, hl):
        """
        Move a single row or column.

        Args:
            hl (list): The row or column to be moved.

        Returns:
            list: The moved row or column.
        """
        len_hl = len(hl)
        for i in range(len_hl - 1):
            if hl[i] == 0:
                for j in range(i + 1, len_hl):
                    if hl[j] != 0:
                        hl[i] = hl[j]
                        hl[j] = 0
                        self.score += 1
                        break
            if hl[i] == 0:
                break
            for j in range(i + 1, len_hl):
                if hl[j] == hl[i]:
                    hl[i] += hl[j]
                    self.score += hl[j]
                    hl[j] = 0
                    break
                if hl[j] != 0:
                    break
        return hl

    def is_over(self):
        """
        Check if the game is over (no more valid moves).

        Returns:
            bool: True if the game is over, False otherwise.
        """
        if not self.is_full():
            return False
        for y in range(self.size - 1):
            for x in range(self.size - 1):
                if self.tiles[y][x] == self.tiles[y][x + 1] or self.tiles[y][x] == self.tiles[y + 1][x]:
                    return False
        return True

    def is_win(self):
        """
        Check if the player has won the game (reached the maximum tile).

        Returns:
            bool: True if the player has won, False otherwise.
        """
        if self.max_tile > 0:
            return self.max_tile in self.tiles
        else:
            return False

    def __str__(self):
        """
        Return a string representation of the grid.

        Returns:
            str: The string representation of the grid.
        """
        str_ = '====================\n'
        for row in self.tiles:
            str_ += '-' * (5 * self.size + 1) + '\n'
            for i in row:
                str_ += '|{:4d}'.format(int(i))
            str_ += '|\n'
        str_ += '-' * (5 * self.size + 1) + '\n'
        str_ += '==================\n'
        return str_


nmap = {0: 'U', 1: 'R', 2: 'D', 3: 'L'}
fmap = dict([val, key] for key, val in nmap.items())


class Game:
    """Class representing the game logic and state."""

    score = 0
    env = 'testing'
    state = 'start'
    grid = None

    def __init__(self, grid_size=4, env='production'):
        """
        Initialize the game.

        Args:
            grid_size (int): The size of the game grid (default: 4).
            env (str): The environment of the game ('production' or 'testing') (default: 'production').
        """
        self.env = env
        self.grid_size = grid_size
        self.start()

    def start(self):
        """Start or restart the game."""
        self.grid = Grid(self.grid_size)
        if self.env == 'production':
            self.grid.add_tile_init()
        self.state = 'run'

    def run(self, direction):
        """
        Run the game by making a move in the given direction.

        Args:
            direction (str): The direction to move the tiles ('U', 'D', 'L', 'R').

        Returns:
            Grid: The updated game grid after the move.
        """
        if self.state in ['over', 'win']:
            return None
        if isinstance(direction, int):
            direction = nmap[direction]

        self.grid.run(direction)
        self.score += self.grid.score

        if self.grid.is_over():
            self.state = 'over'

        if self.grid.is_win():
            self.state = 'win'

        if self.env == 'production':
            self.grid.add_random_tile()
        return self.grid

    def printf(self):
        """Print the game grid."""
        print(self.grid)


if __name__ == '__main__':
    game = Game(env='testing')
    print(game.grid)
    print(game.run('D'))
