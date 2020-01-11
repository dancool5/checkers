def can_kill(checker1, checker2, all_checkers):
    if abs(checker1.x - checker2.x) != 1 or abs(checker1.y - checker2.y) != 1:
        return False

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

    for ch in all_checkers:
        if checker2.x - checker1.x == ch.x - checker2.x and ch.y - checker2.y == checker2.y - checker1.y:
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


def can_move(checker, x, y, color):
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
    if [1 for check in all_checkers if check.color == color] == []:
        return 'White wins'
    color = 'white'
    if [1 for check in all_checkers if check.color == color] == []:
        return 'Black wins'
    return None