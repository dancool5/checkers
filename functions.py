def can_kill(checker, x, y, color, all_checkers):
    if color == checker.color and abs(checker.x - x) == 2 and abs(checker.y - y) == 2:
        for ch in all_checkers:
            if ch.color != color and abs(ch.x - checker.x) == 1 and abs(ch.y - checker.y) == 1:
                return ch
    return None


def is_killing_possible(moving_checkers, not_moving_checkers):
    for checker1 in moving_checkers:
        for checker2 in not_moving_checkers:
            if can_kill(checker1, checker2, moving_checkers + not_moving_checkers):
                return True
    return False


def select(pos, all_checkers, color):
    for checker in all_checkers:
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