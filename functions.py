def can_kill(checker1, checker2, all_checkers):
    if 2 * checker1.x - checker2.x not in [checker.x for checker in all_checkers] + [0, 7] or \
            2 * checker1.y - checker2.y not in [checker.y for checker in all_checkers] + [0, 7]:
        if not(checker1.is_king):
            if abs(checker1.x - checker2.x) == abs(checker1.y - checker2.y) == 1:
                    return True
        else:
            if abs(checker1.x - checker2.x) == abs(checker1.y - checker2.y):
                    return True
    return False


def is_killing_possible(moving_checkers, not_moving_checkers):
    for checker1 in moving_checkers:
        for checker2 in not_moving_checkers:
            if can_kill(checker1, checker2, moving_checkers + not_moving_checkers):
                return True
    return False


def select(pos, board, color):
    for checker in board:
        if checker.rect.collidepoint(pos) and checker.color == color:
            return checker
    return None


def can_move(checker, x, y, color):
    if color == checker.color == 'white':
        if abs(checker.x - x) == 1 and y - checker.y == -1:
            return True
    elif color == checker.color == 'black':
        if abs(checker.x - x) == 1 and checker.y - y == -1:
            return True
    return False