from munkres import DISALLOWED

from .file_actions import PersonDict


def score(person_one: PersonDict, person_two: PersonDict) -> int:
    if any(map(lambda f: f(person_one, person_two), (same_person, same_family, parents, same_as_last_year))):
        return DISALLOWED
    else:
        return 0


def same_family(p1: PersonDict, p2: PersonDict) -> bool:
    return p1.patronymic == p2.patronymic


def parents(p1: PersonDict, p2: PersonDict) -> bool:
    """
    Return `True` if p1 is p2's parent or vice versa
    :param p1:
    :param p2:
    :return:
    """
    return p1.name in p2.patronymic or p2.name in p1.patronymic


def same_person(p1: PersonDict, p2: PersonDict) -> bool:
    return p1 == p2


def same_as_last_year(p1: PersonDict, p2: PersonDict) -> bool:
    return p2.full_name in p1._last_year
