class TicTacToe:
    def __init__(self):
        self.size = 15
        self.board = [None] * self.size ** 2
        self.__game_win_lenght = 5

    def get_decart_coordinate(self, ind):
        """Return x, y coordinate."""
        return ind // self.size, ind % self.size - 1

    def get_index_from_coordinate(self, x, y):
        return x * 15 + y

    def check_winner(self, player, ind):
        cur_x, cur_y = self.get_decart_coordinate(ind)
        going_up, going_down, k, counter = True, True, 0, 0

        while going_up or going_down:
            if going_up and self.get_index_from_coordinate(cur_x + k, cur_y) == 'X':
                counter += 1
            else:
                going_up = False
            if going_down and self.get_index_from_coordinate(cur_x - k, cur_y) == 'X':
                counter += 1
            else:
                going_down = False
            k += 1

        if counter >= self.__game_win_lenght:
            return True

        while going_up or going_down:
            if going_up and self.get_index_from_coordinate(cur_x, cur_y + k) == 'X':
                counter += 1
            else:
                going_up = False
            if going_down and self.get_index_from_coordinate(cur_x, cur_y - k) == 'X':
                counter += 1
            else:
                going_down = False
            k += 1

        if counter >= self.__game_win_lenght:
            return True

        while going_up or going_down:
            if going_up and self.get_index_from_coordinate(cur_x + k, cur_y + k) == 'X':
                counter += 1
            else:
                going_up = False
            if going_down and self.get_index_from_coordinate(cur_x - k, cur_y + k) == 'X':
                counter += 1
            else:
                going_down = False
            k += 1

        if counter >= self.__game_win_lenght:
            return True

        return False
