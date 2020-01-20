from os import path
import pygame
import settings as s


def can_kill(checker1, checker2, all_checkers, x, y, flag):
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
            # ситуацию с рубкой, котороую выделил сам игрок
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


def is_killing_possible(moving_checkers, not_moving_checkers, all_checkers):
    for checker1 in moving_checkers:
        for checker2 in not_moving_checkers:
            if can_kill(checker1, checker2, all_checkers, None, None, False):
                return True
    return False


def can_move(checker, x, y, color, board):
    all_checkers = board.board

    if x % 2 == y % 2:
        return False
    if checker.is_king:
        if abs(checker.x - x) != abs(checker.y - y):
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
        return 'White wins'
    if len(white_ch) == 0:
        return 'Black wins'
    return None


def change_status(checker, images):
    checker.is_king = True
    w_image, b_image = images[0], images[1]
    if checker.color == 'white':
        checker.image = w_image
    else:
        checker.image = b_image


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
    fullname = path.join('data', name)
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
