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


def can_move(checker, x, y, moving_checkers, not_moving_checkers):
    if not(is_killing_possible(moving_checkers, not_moving_checkers)):
        if not(checker.is_king):
            if checker.color == 'white':
                if abs(checker.x - x) == 1 and y - checker.y == -1:
                    for checker in moving_checkers + not_moving_checkers:
                        if (checker.x, checker.y) == (x, y):
                            return False
                    return True
            else:
                if abs(checker.x - x) == 1 and y - checker.y == 1:
                    for checker in moving_checkers + not_moving_checkers:
                        if (checker.x, checker.y) == (x, y):
                            return False
                    return True
        else:
            if abs(checker.x - x) == abs(checker.y - y):
                for checker in moving_checkers + not_moving_checkers:
                    if (checker.x, checker.y) == (x, y):
                        return False
                return True
    else:
        pass