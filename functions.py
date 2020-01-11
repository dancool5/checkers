from os import path
import pygame


def can_kill(checker1, checker2, all_checkers):
    if not checker1.is_king:
        if checker1.x - checker2.x < 0:
            if checker1.x + 2 > 7:
                return False
        elif checker1.x - 2 < 0:
            return False

        if checker1.y - checker2.y < 0:
            if checker1.y + 2 > 7:
                return False
        elif checker1.y - 2 < 0:
            return False

        if abs(checker1.x - checker2.x) != 1 or abs(checker1.y - checker2.y) != 1:
            return False

        for ch in all_checkers:
            if checker2.x - checker1.x == ch.x - checker2.x and ch.y - checker2.y == checker2.y - checker1.y:
                return False
        return True
    else:
        if abs(checker1.x - checker2.x) != abs(checker1.y - checker2.y):
            return False

        if special_check(checker1.x, checker1.y, checker2.x, checker2.y, all_checkers):
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
            if can_kill(checker1, checker2, all_checkers):
                return True
    return False


def select(pos, all_checkers, color):
    for checker in all_checkers:
        if checker.rect.collidepoint(pos) and checker.color == color:
            return checker
    return None


def can_move(checker, x, y, color, all_checkers):
    if checker.is_king:
        if abs(checker.x - x) != abs(checker.y - y):
            return False
        if type(special_check(checker.x, checker.y, x, y, all_checkers)) == int:
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

        if color == checker.color == 'white':
            if abs(checker.x - x) == 1 and y - checker.y == -1:
                return True
        elif color == checker.color == 'black':
            if abs(checker.x - x) == 1 and checker.y - y == -1:
                return True
        return False


def check_winning(all_checkers):
    color = 'black'
    if not [1 for check in all_checkers if check.color == color]:
        return 'White wins'
    color = 'white'
    if not [1 for check in all_checkers if check.color == color]:
        return 'Black wins'
    return None


def change_status(checker, images):
    checker.is_king = True
    w_image, b_image = images[0], images[1]
    if checker.color == 'white':
        checker.image = w_image
    else:
        checker.image = b_image


def special_check(x1, y1, x2, y2, all_checkers):  # эта функция нужна для проверки
    ch = []
    for i in range(1, abs(x1 - x2)):  # есть ли между двумя клетками по диагонали другие шашки
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
