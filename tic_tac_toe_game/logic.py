class TicTacToe:
    def __init__(self):
        self.size = 15
        self.board = [None] * self.size ** 2

    def check_winner(self, x, y, player):
        """
        Проверяет, победил ли игрок после совершения хода.
        """
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # вертикаль, горизонталь, две диагонали
        for dx, dy in directions:
            count = 1
            for dir in [1, -1]:  # Проверяем в обе стороны от последнего хода
                step = 1
                while True:
                    nx, ny = x + step * dx * dir, y + step * dy * dir
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        index = nx + ny * self.size
                        if self.board[index] == player:
                            count += 1
                            if count == 5:  # Нужно 5 подряд для победы
                                return True
                        else:
                            break
                    else:
                        break
                    step += 1
        return False
