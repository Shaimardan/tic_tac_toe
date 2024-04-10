class TicTacToe:
    def __init__(self):
        self.size = 15
        self.board = [None] * self.size ** 2
        self.__game_win_lenght = 5

    def get_decart_coordinate(self, ind):
        """Return x, y coordinate."""
        return ind // self.size, ind % self.size

    @staticmethod
    def __get_index_from_coordinate(x, y):
        return x * 15 + y

    def __get_position_from_coordinate(self, x, y):
        ind = TicTacToe.__get_index_from_coordinate(x, y)
        if 0 <= ind <= len(self.board):
            return self.board[ind]
        else:
            return None

    def check_winner(self, player, ind):
        cur_x, cur_y = self.get_decart_coordinate(ind)

        directions = [
            (1, 0),  # horizontal right
            (-1, 0),  # horizontal left
            (0, 1),  # vertical up
            (0, -1),  # vertical down
            (1, 1),  # diagonal bottom-right
            (-1, 1),  # diagonal top-right
            (1, -1),  # diagonal bottom-left
            (-1, -1)  # diagonal top-left
        ]

        def count_in_direction(_dx, _dy):
            count = 0
            step = 1
            while True:
                new_x = cur_x + _dx * step
                new_y = cur_y + _dy * step
                if self.__get_position_from_coordinate(new_x, new_y) == player:
                    count += 1
                    step += 1
                else:
                    break
            return count

        for dx, dy in directions:
            if count_in_direction(dx, dy) >= self.__game_win_lenght - 1:
                return True

        return False
