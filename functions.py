def can_kill(checker1, checker2, all_checkers):
    if not (checker1.is_king):
        if abs(checker1.x - checker2.x) == abs(checker1.y - checker2.y) == 1 and \
                checker2.x not in (0, 7) and checker2.y not in (0, 7):
            return True
    else:
        if abs(checker1.x - checker2.x) == abs(checker1.y - checker2.y) and \
                checker2.x not in (0, 7) and checker2.y not in (0, 7):
            return True


def is_killing_possible(moving_checkers, not_moving_checkers):
    for checker1 in moving_checkers:
        for checker2 in not_moving_checkers:
            if can_kill(checker1, checker2, moving_checkers + not_moving_checkers):
                return True
    return False


def can_move(checker, x, y, moving_checkers, not_moving_checkers):
    if not(is_killing_possible(moving_checkers, not_moving_checkers)):
        if not(checker.is_king):
            if checker.color == 'white':
                if abs(checker.x - x) == 1 and y - checker.y == 1:
                    checker.move(x, y)
            else:
                if abs(checker.x - x) == 1 and y - checker.y == -1:
                    checker.move(x, y)
        else:
            if abs(checker.x - x) == abs(checker.y - y):
                checker.move(x, y)
    else:
        pass