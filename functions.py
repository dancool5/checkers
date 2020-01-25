from os import path
import pygame
import settings as s


def can_kill(checker1, checker2, all_checkers, x, y, flag):
    if flag:
        # эти условия проверяются в случае, если нужно рассмотреть конкретную
        # ситуацию с рубкой, которую выделил сам игрок
        for ch in all_checkers:
            if ch.x == x and ch.y == y:
                return False

    if not checker1.is_king:
        if (checker1.x - checker2.x < 0 and checker1.x + 2 > 7) or (checker1.x - 2 < 0 and checker1.x - checker2.x > 0):
            return False

        if (checker1.y - checker2.y < 0 and checker1.y + 2 > 7) or (checker1.y - checker2.y > 0 and checker1.y - 2 < 0):
            return False

        if abs(checker1.x - checker2.x) != 1 or abs(checker1.y - checker2.y) != 1:
            return False

        x_now, y_now = 2 * (checker2.x - checker1.x) + checker1.x, 2 * (checker2.y - checker1.y) + checker1.y
        for ch in all_checkers:
            if ch.x == x_now and ch.y == y_now:
                return False
        return True
    else:
        if flag:
            # эти условия проверяются в случае, если нужно рассмотреть конкретную
            # ситуацию с рубкой, которую выделил сам игрок
            checking = special_check(checker1.x, checker1.y, x, y, all_checkers)
            if checking is None or type(checking) is list:
                return False

            if abs(checker1.x - x) != abs(checker1.y - y):
                return False

        if special_check(checker1.x, checker1.y, checker2.x, checker2.y, all_checkers) is not None:
            return False

        if abs(checker2.x - checker1.x) != abs(checker2.y - checker1.y):
            return False

        if checker1.x > checker2.x:
            x = checker2.x - 1
        else:
            x = checker2.x + 1

        if checker1.y > checker2.y:
            y = checker2.y - 1
        else:
            y = checker2.y + 1

        if x in (-1, 8) or y in (-1, 8):
            return False

        for check in all_checkers:
            if check.x == x and check.y == y:
                return False

        return True


def is_killing_possible(moving_checkers, not_moving_checkers, all_checkers, is_AI=False):
    possible_killings = []
    for checker1 in moving_checkers:
        for checker2 in not_moving_checkers:
            if can_kill(checker1, checker2, all_checkers, None, None, False):
                if is_AI:
                    possible_killings.append((checker1, checker2))
                else:
                    return True
    if is_AI:
        return possible_killings

    return False


def can_move(checker, x, y, color, board):
    all_checkers = board.board

    if x % 2 == y % 2:
        return False
    if checker.is_king:
        if abs(checker.x - x) != abs(checker.y - y):
            return False

        for ch in all_checkers:
            if ch.x == x and ch.y == y:
                return False

        if special_check(checker.x, checker.y, x, y, all_checkers) is not None:
            return False

        return True
    else:
        if checker.x - x > 0:
            if checker.x - 1 < 0:
                return False
        elif checker.x + 1 > 7:
            return False

        if checker.y - y > 0:
            if checker.y - 1 < 0:
                return False
        elif checker.y + 1 > 7:
            return False

        for ch in all_checkers:
            if ch.x == x and ch.y == y:
                return False

        if ((color == checker.color == 'white' and not board.is_rotate) or
                (color == checker.color == 'black' and board.is_rotate)):
            if abs(checker.x - x) == 1 and y - checker.y == -1:
                return True
        elif ((color == checker.color == 'white' and board.is_rotate) or
              (color == checker.color == 'black' and not board.is_rotate)):
            if abs(checker.x - x) == 1 and checker.y - y == -1:
                return True
        return False


def check_winning(black_ch, white_ch):
    if len(black_ch) == 0:
        return 'white'
    if len(white_ch) == 0:
        return 'black'
    return None


def change_status(checker, images, need_changing=True):
    checker.is_king = True

    if need_changing:
        FPS = 10
        clock = pygame.time.Clock()
        w_images, b_images = images[0], images[1]
        if checker.color == 'white':
            for image in w_images:
                checker.image = image
                clock.tick(FPS)
        else:
            for image in b_images:
                checker.image = image
                clock.tick(FPS)


def special_check(x1, y1, x2, y2, all_checkers):
    # эта функция нужна для проверки есть ли между двумя клетками по диагонали другие шашки
    ch = []
    for i in range(1, abs(x1 - x2)):
        if x2 > x1:
            x = x1 + i
        else:
            x = x1 - i

        if y2 > y1:
            y = y1 + i
        else:
            y = y1 - i

        for check in all_checkers:
            if check.x == x and check.y == y:
                ch.append(check)

    if len(ch) == 1:
        return ch[0]
    if len(ch) == 0:
        return None
    return ch


def load_image(name):
    fullname = path.join('data/Images', name)
    im = pygame.image.load(fullname).convert_alpha()
    return im


def select(x, y, all_checker, color, pos):
    if x is not None:
        if x % 2 != y % 2:
            for checker in all_checker:
                if checker.rect.collidepoint(pos):
                    if checker.color == color:
                        return checker
                    else:
                        return 'false_color'
    return None


def find_killed_checker(sel_checker, all_checkers, x, y, not_moving_ch):
    if sel_checker.is_king:
        killed_checker = special_check(sel_checker.x, sel_checker.y, x, y, all_checkers)
        if not killed_checker:
            killed_checker = sel_checker
        elif type(killed_checker) == list:
            killed_checker = killed_checker[0]
    else:
        for ch in not_moving_ch:
            if (abs(x - ch.x) == 1 and abs(ch.y - y) == 1 and abs(sel_checker.x - ch.x) == 1 and
                    abs(ch.y - sel_checker.y) == 1):
                killed_checker = ch
                break
        else:
            killed_checker = sel_checker
    return killed_checker


def start_game(old_width, old_height):
    s.state = 'game'
    s.width = old_width
    s.height = old_height

    pygame.time.wait(250)
    return [], pygame.sprite.Group()


def declination(checkers, color):  # функция для правильного склонения слова 'шашка' в зависимости от числительного
    count = len(checkers)
    if count == 1:
        return str(count) + ' ' + color[0] + ' шашка'
    elif count > 4 or count == 0:
        return str(count) + ' ' + color[0] + ' шашек'
    return str(count) + ' ' + color[0] + ' шашки'

move_ = ()
score = -1000
best_score = 0
best_move = ()

def AI_turn(board, depth):
    global score, best_score, move_, best_move
    moves, is_killing = collect_moves(board)

    for move in moves:
        if is_killing:
            checker1, checker2, x_kill, y_kill = move[0], move[1], move[2][0], move[2][1]
            if can_kill(checker1, checker2, board.board, x_kill, y_kill, True):
                # если данная рубка возможна
                board.board.remove(checker2)
                if s.moving_color == s.player_color:
                    score -= 10
                else:
                    score += 10

                flag_king = checker1.make_move(x_kill, y_kill, board.is_rotate)

                if flag_king:
                    if s.moving_color == s.player_color:
                        score -= 5
                    else:
                        score += 5

                    change_status(checker1, [], False)

                moves, is_killing = collect_moves(board)
                if not is_killing:
                    s.moving_color = 'black' if s.moving_color == 'white' else 'white'
                    if depth == 0:
                        if best_score < score:
                            best_score = score
                            best_move = move
                    elif depth == 6:
                        move_ = (checker1, checker2, x_kill, y_kill)
                    else:
                        AI_turn(board, depth - 1)
                else:
                    AI_turn(board, depth)

        else:
            checker1, x_move, y_move = move[0], move[1][0], move[1][1]
            if s.moving_color != s.player_color:
                score -= 1
            flag_king = checker1.make_move(x_move, y_move, board.is_rotate)

            if flag_king:
                change_status(checker1, [], False)

            s.moving_color = 'black' if s.moving_color == 'white' else 'white'

            if depth == 0:
                if best_score < score:
                    best_score = score
                    best_move = move
            elif depth == 6:
                move_ = (checker1, x_move, y_move)
            else:
                AI_turn(board, depth - 1)

    return best_move


def collect_moves(board, moving_ch, not_moving_ch):
    moves = []
    kills = is_killing_possible(moving_ch, not_moving_ch, board.board, True)


    if kills:
        # если возможна рубка
        for kill in kills:
            checker1, checker2 = kill[0], kill[1]
            if checker1.is_king:
                if checker2.x > checker1.x:
                    x = checker2.x + 1
                else:
                    x = checker2.x - 1

                if checker2.y > checker1.y:
                    y = checker2.y + 1
                else:
                    y = checker2.y - 1

                while can_kill(checker1, checker2, board.board, x, y, True) and 0 <= x < s.cols and 0 <= y < s.lines:
                    moves.append((checker1, checker2, (x, y)))
                    if checker2.x > checker1.x:
                        x += 1
                    else:
                        x -= 1

                    if checker2.y > checker1.y:
                        y += 1
                    else:
                        y -= 1

            else:
                moves.append((checker1, checker2, ((checker2.x - checker1.x) * 2 + checker1.x,
                                                   (checker2.y - checker1.y) * 2 + checker1.y)))
    else:
        # если рубка невозможна
        for checker in moving_ch:
            if checker.is_king:
                # если текущая шашка - дамка, то в каждую из 4х сторон
                # проверяем насколько клеток по-диагонали можно сходить
                x, y = checker.x + 1, checker.y + 1
                while (can_move(checker, x, y, s.moving_color, board) and
                       0 <= x < s.cols and 0 <= y < s.lines):
                    moves.append((checker, (x, y)))
                    x += 1
                    y += 1

                x, y = checker.x - 1, checker.y + 1
                while (can_move(checker, x, y, s.moving_color, board) and
                       0 <= x < s.cols and 0 <= y < s.lines):
                    moves.append((checker, (x, y)))
                    x -= 1
                    y += 1

                x, y = checker.x - 1, checker.y - 1
                while (can_move(checker, x, y, s.moving_color, board) and
                       0 <= x < s.cols and 0 <= y < s.lines):
                    moves.append((checker, (x, y)))
                    x -= 1
                    y -= 1

                x, y = checker.x + 1, checker.y - 1
                while (can_move(checker, x, y, s.moving_color, board) and
                       0 <= x < s.cols and 0 <= y < s.lines):
                    moves.append((checker, (x, y)))
                    x -= 1
                    y += 1

            else:
                # если текущая шашка - недамка, то проверяем можно ли
                # сходить в каждую из 4х ближайших клеток по-диагонали
                if can_move(checker, checker.x + 1, checker.y + 1, s.moving_color, board):
                    moves.append((checker, (checker.x + 1, checker.y + 1)))

                if can_move(checker, checker.x - 1, checker.y + 1, s.moving_color, board):
                    moves.append((checker, (checker.x - 1, checker.y + 1)))

                if can_move(checker, checker.x + 1, checker.y - 1, s.moving_color, board):
                    moves.append((checker, (checker.x + 1, checker.y - 1)))

                if can_move(checker, checker.x - 1, checker.y - 1, s.moving_color, board):
                    moves.append((checker, (checker.x - 1, checker.y - 1)))

    return moves, (kills != [])
