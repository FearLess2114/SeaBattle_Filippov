import random as rnd
import copy

class Pos:
    """
    x - row number
    y - column number
    """
    def __init__(self, x, y) -> None:
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @x.setter
    def x(self, x):
        self.__x = x

    @y.setter
    def y(self, y):
        self.__y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"


class ShipDeck:
    """
    status: True - whole deck
            False - destroyed deck
    """
    def __init__(self, pos, status=True):
        self.__pos = pos
        self.__status = status

    @property
    def pos(self):
        return self.__pos

    @property
    def status(self):
        return self.__status


class Ship:
    def __init__(self, pos_1, pos_2=None) -> None:
        self.__decks = []
        if pos_2 is None:
            self.__decks.append(ShipDeck(pos_1, True))
        elif pos_1.x == pos_2.x:
            for i in range(min(pos_1.y, pos_2.y), max(pos_1.y, pos_2.y)+1):
                self.__decks.append(ShipDeck(Pos(pos_1.x, i)))
        else:
            for j in range(min(pos_1.x, pos_2.x), max(pos_1.x, pos_2.x)+1):
                self.__decks.append(ShipDeck(Pos(j, pos_1.y)))

    @property
    def decks(self):
        return self.__decks

    @property
    def length(self):
        return len(self.__decks)


class GameBoard:
    def __init__(self, width, height) -> None:
        __str1 = []
        self.__board = []
        for i in range(height):
            self.__board.append([])
            for j in range(width):
                self.__board[i].append(0)
        self.__width = width
        self.__height = height
        self.__ships = []
        self.__deck_count = 0

    def add_ship(self, ship) -> None:
        self.__ships.append(ship)
        for i in ship.decks:
            self.__board[i.pos.x][i.pos.y] = "■"
        self.__deck_count += ship.length

    def permission_add(self, ship) -> bool:
        permission = True
        if (ship.decks[0].pos.x >= 0) and (ship.decks[-1].pos.x < self.height) and (ship.decks[0].pos.y >= 0) and (ship.decks[-1].pos.y < self.width):
            for i in range(max(0, ship.decks[0].pos.x-1), min(self.height-1, ship.decks[-1].pos.x+1)+1):
                for j in range(max(0, ship.decks[0].pos.y-1), min(self.width-1, ship.decks[-1].pos.y+1)+1):
                    if self.__board[i][j] != 0:
                        permission = False
                        break
                if not permission:
                    break
        else:
            permission = False
        return permission

    def print_board(self, opponent=False) -> None:
        print("  ", end="|")
        for i in range(1, self.width+1):
            print(f" {i} ", end="|")
        print()
        for i, str_board in enumerate(self.__board):
            print(f"{i+1} ", end="|")
            for j in str_board:
                if j == "■" and opponent:
                    symbol = "0"
                else:
                    symbol = j
                print(f" {symbol} ", end="|")
            print()
        print()

    def shot(self, pos):
        """
        :return: False - repeated shot at the coordinate
        """
        if self.__board[pos.x][pos.y] == 0:
            self.__board[pos.x][pos.y] = "T"
            return "Miss"
        elif self.__board[pos.x][pos.y] == "■":
            self.__board[pos.x][pos.y] = "X"
            self.__deck_count -= 1
            if self.__deck_count == 0:
                return "Last Hit"
            else:
                return "Hit"
        elif self.__board[pos.x][pos.y] == "X" or self.__board[pos.x][pos.y] == "T":
            return False

    @property
    def board(self):
        return self.__board

    # @board.setter
    # def board(self, board):
    #     self.__board = board

    @property
    def ships(self):
        return self.__ships

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

# доски должны быть одинаковой высоты
def print_game_boards(game_board_1, game_board_2, opponent_1=False, opponent_2=True):
    print("Игрок 1"+25*" "+"Игрок 2")
    print("  ", end="|")
    for i in range(1, game_board_1.width+1):
        print(f" {i} ", end="|")
    print(7*" ", end="|")
    for i in range(1, game_board_2.width+1):
        print(f" {i} ", end="|")
    print()
    for i in range(game_board_1.height):
        print(f"{i+1} ", end="|")
        for j in game_board_1.board[i]:
            if j == "■" and opponent_1:
                symbol = "0"
            else:
                symbol = j
            print(f" {symbol} ", end="|")
        print(5*" " + f"{i + 1} ", end="|")
        for j in game_board_2.board[i]:
            if j == "■" and opponent_2:
                symbol = "0"
            else:
                symbol = j
            print(f" {symbol} ", end="|")
        print()
    print()

class StrategyUser:

    def __init__(self, own_board=None, game_board=None):
        self.__game_board = game_board
        self.__own_board = own_board

    # метод, возвращающий позицию следующего выстрела
    def pos_shot(self):
        if self.__game_board != None:
            while True:
                pos_str = input('Введите позицию выстрела в формате "номер_строки номер_столбца": ').split()
                try:
                    pos_list = list(map(int, pos_str))
                except ValueError:
                    print("Необходимо ввести числа: ")
                else:
                    if len(pos_list) == 2:
                        if (0 <= pos_list[0]-1 < self.__game_board.height) and (0 <= pos_list[1]-1 < self.__game_board.width):
                            if self.__game_board.shot(Pos(pos_list[0]-1, pos_list[1]-1)):
                                return Pos(pos_list[0]-1, pos_list[1]-1)
                            else:
                                print("Выстрел по этой позиции был совершен ранее")
                        else:
                            print("Значения не должны выходить за границы игрового поля")
                    else:
                        print("Должно быть 2 значения через пробел")
        else:
            raise ValueError("Не задана игровая доска оппонента для используемой стратегии")

    def add_opponent_board(self, game_board):
        self.__game_board = game_board

    def add_own_board(self, game_board):
        self.__own_board = game_board

    # возвращает список кораблей для добавления на собственную доску игрока
    def place_ships(self, ships={1: 4, 2: 2, 3: 1}):
        new_placing = True
        while new_placing:
            count_ships = copy.deepcopy(ships)
            ship_list = []
            new_placing = False
            unacceptable_fields = []
            own_board = copy.deepcopy(self.__own_board)
            print("Новая расстановка")
            while count_ships:
                pos_1, pos_2 = None, None
                print("Новый корабль")
                pos_str = input('Введите первую позицию корабля в формате "номер_строки номер_столбца": ').split()
                try:
                    pos_list = list(map(int, pos_str))
                except ValueError:
                    print("Необходимо ввести числа: ")
                else:
                    if len(pos_list) == 2:
                        if (0 <= pos_list[0] - 1 < own_board.height) and (
                                0 <= pos_list[1] - 1 < own_board.width):
                            pos_1 = Pos(pos_list[0] - 1, pos_list[1] - 1)
                            if pos_1 in unacceptable_fields:
                                pos_1 = None
                                answer = input("Недопустимая позиция корабля.\n"
                                               "Введите любой текст, если хотите заново разместить все корабли\n"
                                               "или введите пустую строчку, чтобы заново ввести координаты корабля: ")
                                if answer:
                                    new_placing = True
                                    count_ships = False
                        else:
                            print("Значения не должны выходить за границы игрового поля")
                    else:
                        print("Должно быть 2 значения через пробел")
                if (pos_1 is not None) and not(new_placing):
                    pos_str = input('Введите последнюю позицию корабля в формате "номер_строки номер_столбца"\n'
                                    'если корабль однопалубный, введите пустую строку: ').split()
                    if pos_str:
                        try:
                            pos_list = list(map(int, pos_str))
                        except ValueError:
                            print("Необходимо ввести числа: ")
                        else:
                            if len(pos_list) == 2:
                                if (0 <= pos_list[0] - 1 < own_board.height) and (
                                        0 <= pos_list[1] - 1 < own_board.width):
                                    if pos_list[0] - 1 == pos_1.x or pos_list[1] - 1 == pos_1.y:
                                        pos_2 = Pos(pos_list[0] - 1, pos_list[1] - 1)
                                        if pos_2 in unacceptable_fields:
                                            pos_2 = None
                                            answer = input("Недопустимая позиция корабля.\n"
                                                           "Введите любой текст, если хотите заново разместить все корабли\n"
                                                           "или введите пустую строку, чтобы заново ввести координаты корабля: ")
                                            if answer:
                                                new_placing = True
                                                count_ships = False
                                    else:
                                        print("Одна из координат должна быть одинаковой для первой и последней позиции")
                                else:
                                    print("Значения не должны выходить за границы игрового поля")
                            else:
                                print("Должно быть 2 значения через пробел")
                    if not(new_placing) and ((pos_str and pos_2) or (not pos_str and not pos_2)) and pos_1:
                        ship = Ship(pos_1, pos_2)
                        if ship.length in count_ships:
                            permission = True
                            if ship.length > 3:
                                for i in range(0, ship.length, 3):
                                    if ship.decks[i].pos in unacceptable_fields:
                                        permission = False
                            if permission:
                                ship_list.append(ship)
                                if count_ships[ship.length] > 1:
                                    count_ships[ship.length] -= 1
                                else:
                                    count_ships.pop(ship.length)
                                own_board.add_ship(ship)
                                own_board.print_board()
                            else:
                                answer = input("Недопустимая позиция корабля.\n"
                                               "Введите любой текст, если хотите заново разместить все корабли\n"
                                               "или введите пустую строку, чтобы заново ввести координаты корабля: ")
                                if answer:
                                    new_placing = True
                                    count_ships = False
                            if not (new_placing):
                                for a in range(max(ship.decks[0].pos.x - 1, 0),
                                               min(ship.decks[-1].pos.x + 1, own_board.height - 1) + 1):
                                    for b in range(max(ship.decks[0].pos.y - 1, 0),
                                                   min(ship.decks[-1].pos.y + 1, own_board.width - 1) + 1):
                                        # if not(Pos(i,j) in acceptable_fields):
                                        unacceptable_fields.append(Pos(a, b))
                        else:
                            print("Введите корабль другого размера ")
        return ship_list


class StrategyBot:

    def __init__(self, own_board=None, game_board=None):
        # копия игровой доски оппонента по которой производятся выстрелы
        self.__game_board = game_board
        # создание словаря, где ключи размеры кораблей, значения кол-во кораблей данного размера
        self.__ships = {}
        if game_board is not None:
            for i in game_board.ships:
                if i.length in self.__ships:
                    self.__ships[i.length] += 1
                else:
                    self.__ships[i.length] = 1
            # создается список позиций полей, в которых может находится корабль
            self.__acceptable_shots = []
            for i in range(game_board.height):
                for j in range(game_board.width):
                    self.__acceptable_shots.append(Pos(i, j))
            # предстоящие выстрелы для проверки размера корабля
            self.__upcoming_shots = []
            # последний найденый корабль
            self.__last_ship = None
            # вычисление размера наибольшего корабля
            if len(self.__ships) == 0:
                raise ValueError("Создана игровая доска без кораблей")
            else:
                self.__size_max_ship = max(self.__ships.keys())
        self.__own_board = own_board

    def add_opponent_board(self, game_board):
        self.__game_board = game_board
        self.__ships = {}
        for i in game_board.ships:
            if i.length in self.__ships:
                self.__ships[i.length] += 1
            else:
                self.__ships[i.length] = 1
        # создается список позиций полей, в которых может находится корабль
        self.__acceptable_shots = []
        for i in range(game_board.height):
            for j in range(game_board.width):
                self.__acceptable_shots.append(Pos(i, j))
        # предстоящие выстрелы для проверки размера корабля
        self.__upcoming_shots = []
        # последний найденый корабль
        self.__last_ship = None
        # вычисление размера наибольшего корабля
        if len(self.__ships) == 0:
            raise ValueError("Создана игровая доска без кораблей")
        else:
            self.__size_max_ship = max(self.__ships.keys())

    def add_own_board(self, own_board):
        self.__own_board = own_board

    # метод, возвращающий позицию следующего выстрела
    def pos_shot(self) -> object:
        if self.__game_board != None:
            # проверка, что допустимые выстрелы есть
            if len(self.__acceptable_shots) > 0:
                # проверка предстоящих выстрелов для проверки, что корабль более длинный
                if len(self.__upcoming_shots) == 0:
                    # если предстоящие выстрелы проверки размеров корабля отсутствуют
                    # выстрел в свободное пространство не рядом с кораблями
                    pos_shooting = self.__acceptable_shots.pop(rnd.randint(0, len(self.__acceptable_shots)-1))
                    # проверка на результат выстрела
                    if self.__game_board.shot(pos_shooting) == "Hit":
                        self.__last_ship = Ship(pos_shooting)
                        # 4 проверки, стоит ли добавлять поля сверху и снизу в список предстоящих выстрелов
                        if (pos_shooting.x+1 < self.__game_board.height) and \
                                (Pos(pos_shooting.x+1, pos_shooting.y) in self.__acceptable_shots):
                            self.__upcoming_shots.append(Pos(pos_shooting.x+1, pos_shooting.y))
                        if (pos_shooting.x-1 >= 0) \
                                and (Pos(pos_shooting.x-1, pos_shooting.y) in self.__acceptable_shots):
                            self.__upcoming_shots.append(Pos(pos_shooting.x-1, pos_shooting.y))
                        if (pos_shooting.y+1 < self.__game_board.width) \
                                and (Pos(pos_shooting.x, pos_shooting.y+1) in self.__acceptable_shots):
                            self.__upcoming_shots.append(Pos(pos_shooting.x, pos_shooting.y+1))
                        if (pos_shooting.y-1 >= 0) \
                                and (Pos(pos_shooting.x, pos_shooting.y-1) in self.__acceptable_shots):
                            self.__upcoming_shots.append(Pos(pos_shooting.x, pos_shooting.y-1))
                # ветка, если предстоящие планируемые выстрелы есть
                else:
                    pos_shooting = rnd.choice(self.__upcoming_shots)
                    self.__upcoming_shots.remove(pos_shooting)
                    self.__acceptable_shots.remove(pos_shooting)
                    if self.__game_board.shot(pos_shooting) == "Hit":
                        if (pos_shooting.y > self.__last_ship.decks[0].pos.y) or \
                                (pos_shooting.x > self.__last_ship.decks[0].pos.x):
                            self.__last_ship = Ship(pos_shooting, self.__last_ship.decks[0].pos)
                        else:
                            self.__last_ship = Ship(pos_shooting, self.__last_ship.decks[-1].pos)
                        # если корабль максимального размера, то удаляем предстоящие выстрелы
                        if self.__last_ship.length == self.__size_max_ship:
                            for i in self.__upcoming_shots:
                                self.__acceptable_shots.remove(i)
                            self.__upcoming_shots.clear()
                        # если корабль не максимального размера
                        else:
                            # удаляем предстоящие выстрелы, в которых не может быть корабль
                            # если корабль горизонтальный
                            if pos_shooting.x == self.__last_ship.decks[0].pos.x:
                                for i in range(len(self.__upcoming_shots) - 1, -1, -1):
                                    if self.__upcoming_shots[i].x != pos_shooting.x:
                                        self.__acceptable_shots.remove(self.__upcoming_shots[i])
                                        self.__upcoming_shots.pop(i)
                                # добавляем предстоящий выстрел на конце корабля и обновляем данные последнего корабля
                                if pos_shooting.y > self.__last_ship.decks[0].pos.y:
                                    if Pos(pos_shooting.x, pos_shooting.y+1) in self.__acceptable_shots:
                                        self.__upcoming_shots.append(Pos(pos_shooting.x, pos_shooting.y+1))
                                else:
                                    if Pos(pos_shooting.x, pos_shooting.y-1) in self.__acceptable_shots:
                                        self.__upcoming_shots.append(Pos(pos_shooting.x, pos_shooting.y-1))
                            # если корабль вертикальный
                            else:
                                for i in range(len(self.__upcoming_shots) - 1, -1, -1):
                                    if self.__upcoming_shots[i].y != pos_shooting.y:
                                        self.__acceptable_shots.remove(self.__upcoming_shots[i])
                                        self.__upcoming_shots.pop(i)
                                # добавляем предстоящий выстрел и обновляем данные последнего корабля
                                # в конец корабля
                                if pos_shooting.x > self.__last_ship.decks[0].pos.x:
                                    if Pos(pos_shooting.x + 1, pos_shooting.y) in self.__acceptable_shots:
                                        self.__upcoming_shots.append(Pos(pos_shooting.x + 1, pos_shooting.y))
                                # в начало корабля
                                else:
                                    if Pos(pos_shooting.x - 1, pos_shooting.y) in self.__acceptable_shots:
                                        self.__upcoming_shots.append(Pos(pos_shooting.x - 1, pos_shooting.y))
                # если предстоящих выстрелов нет
                # т.е. последний найденный корабль уже уничтожен
                if (self.__last_ship is not None) and (len(self.__upcoming_shots) == 0):
                    self.__ships[self.__last_ship.length] -= 1
                    if self.__ships[self.__last_ship.length] == 0:
                        self.__ships.pop(self.__last_ship.length)
                    # Удаление всех полей вокруг корабля из возможных выстрелов
                    for i in range(max(0, self.__last_ship.decks[0].pos.x-1),
                                   min(self.__game_board.height-1, self.__last_ship.decks[-1].pos.x+1)+1):
                        for j in range(max(0, self.__last_ship.decks[0].pos.y-1),
                                       min(self.__game_board.width-1, self.__last_ship.decks[-1].pos.y+1)+1):
                            try:
                                self.__acceptable_shots.remove(Pos(i,j))
                            except ValueError:
                                pass
                    self.__size_max_ship = max(self.__ships.keys())
                    self.__last_ship = None
                return pos_shooting
            else:
                raise ValueError("Попытка выстрела на игровую доску, где игра уже закончена")
        else:
            raise ValueError("Не задана игровая доска оппонента для используемой стратегии")
    # возвращает список кораблей для добавления на собственную доску игрока
    def place_ships(self, own_ships={1: 4, 2: 2, 3: 1}):
        new_placing = True
        while new_placing:
            new_placing = False
            self.__own_ships = copy.deepcopy(own_ships)
            unacceptable_fields = []
            while self.__own_ships and not(new_placing):
                size_ship = max(self.__own_ships.keys())
                acceptable_fields = []
                # 0 - горизонтальный корабль, 1 - вертикальный
                if rnd.randint(0, 1):
                    # создание списка полей, в которые можно поставить корабль
                    for i in range(self.__own_board.height-size_ship+1):
                        for j in range(self.__own_board.width):
                            add_permission = True
                            for g in range(i, i+size_ship):
                                if Pos(g, j) in unacceptable_fields:
                                    add_permission = False
                                    break
                            if add_permission:
                                acceptable_fields.append(Pos(i, j))
                    if acceptable_fields:
                        pos_ship = rnd.choice(acceptable_fields)
                        ship = Ship(pos_ship, Pos(pos_ship.x+size_ship-1, pos_ship.y))
                    else:
                        new_placing = True
                else:
                    for i in range(self.__own_board.height):
                        for j in range(self.__own_board.width-size_ship+1):
                            add_permission = True
                            for g in range(j, j+size_ship):
                                if Pos(i, g) in unacceptable_fields:
                                    add_permission = False
                                    break
                            if add_permission:
                                acceptable_fields.append(Pos(i, j))
                    if acceptable_fields:
                        pos_ship = rnd.choice(acceptable_fields)
                        ship = Ship(pos_ship, Pos(pos_ship.x, pos_ship.y + size_ship - 1))
                    else:
                        new_placing = True
                if not(new_placing):
                    for a in range(max(ship.decks[0].pos.x-1, 0), min(ship.decks[-1].pos.x+1, self.__own_board.height-1)+1):
                        for b in range(max(ship.decks[0].pos.y-1, 0), min(ship.decks[-1].pos.y+1, self.__own_board.width-1)+1):
                            # if not(Pos(i,j) in acceptable_fields):
                            unacceptable_fields.append(Pos(a, b))
                    self.__own_board.add_ship(ship)
                    self.__own_ships[ship.length] -=1
                    if self.__own_ships[ship.length] == 0:
                        self.__own_ships.pop(ship.length)
        return self.__own_board.ships


class Player:

    def __init__(self, game_board, strategy):
        self.__game_board = game_board
        self.__strategy = strategy

    @property
    def strategy(self):
        return self.__strategy

    @property
    def game_board(self):
        return self.__game_board


# ПРОЦЕСС ИГРЫ
player_1 = Player(GameBoard(6, 6), StrategyUser(GameBoard(6, 6)))
player_2 = Player(GameBoard(6, 6), StrategyBot(GameBoard(6, 6)))
player_1.game_board.print_board()
print("РАССТАНОВКА КОРАБЛЕЙ")
ships_2 = player_2.strategy.place_ships()
ships_1 = player_1.strategy.place_ships()
# ships_1 = [Ship(Pos(0, 0), Pos(0, 2)), Ship(Pos(2, 0), Pos(3, 0)), Ship(Pos(5, 0), Pos(5, 1)),
#            Ship(Pos(3, 3)), Ship(Pos(5, 3)), Ship(Pos(0, 5)), Ship(Pos(2, 5))]
for i in ships_1:
    player_1.game_board.add_ship(i)
for i in ships_2:
    player_2.game_board.add_ship(i)
player_1.strategy.add_opponent_board(copy.deepcopy(player_2.game_board))
player_2.strategy.add_opponent_board(copy.deepcopy(player_1.game_board))
print("ПРОЦЕСС ИГРЫ")
current_player = rnd.randint(0, 1)
while True:
    if current_player:
        pos_shot = player_1.strategy.pos_shot()
        shot_result = player_2.game_board.shot(pos_shot)
        if shot_result:
            if shot_result == "Miss":
                current_player = False
            elif shot_result == "Hit":
                # print("Попадание")
                pass
            elif shot_result == "Last Hit":
                print("КОНЕЦ ИГРЫ, ПОБЕДА ИГРОКА")
                break
            else:
                print("ОШИБКА МЕТОДА ВЫСТРЕЛА")
        else:
            print("ОШИБКА. Повторный выстрел в координату!")
            # print(shot_result)
        print(f"Выстрел игрока 1 по координатам ({pos_shot.x+1}; {pos_shot.y+1}): {shot_result}")
        # player_2.game_board.print_board(opponent=True)
    else:
        pos_shot = player_2.strategy.pos_shot()
        shot_result = player_1.game_board.shot(pos_shot)
        if shot_result:
            if shot_result == "Miss":
                current_player = True
            elif shot_result == "Hit":
                # print("Попадание")
                pass
            elif shot_result == "Last Hit":
                print("КОНЕЦ ИГРЫ, ПОБЕДА БОТА>")
                break
            else:
                print("ОШИБКА МЕТОДА ВЫСТРЕЛА")
        else:
            print("ОШИБКА. Повторный выстрел в координату!")
            # print(shot_result)
        print(f"Выстрел игрока 2 по координатам ({pos_shot.x+1}; {pos_shot.y+1}): {shot_result}")
        # player_1.game_board.print_board()
    print_game_boards(player_1.game_board, player_2.game_board)
print("Игровая доска игрока: ")
player_1.game_board.print_board()
print("Игровая доска оппонента: ")
player_2.game_board.print_board()

