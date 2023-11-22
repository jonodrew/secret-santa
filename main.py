import csv
import itertools
from typing import Iterable, Optional, Generator

from munkres import Munkres, DISALLOWED


class Person:

    def __init__(self, **kwargs):
        self.id = int(kwargs['id'])
        self.name: str = kwargs['name']
        self.family_name: str = kwargs['family_name']
        self.number = kwargs["number"]
        self.patronymic: str = kwargs['patronymic']
        self.last_year: set[str] = set(kwargs['last_year'].split(","))
        self.giftee: Optional['Person'] = None

    @property
    def full_name(self):
        return f"{self.name} {self.family_name}"

    def __repr__(self):
        return f"{self.id}: {self.name} {self.family_name}"


def score(person_one: Person, person_two: Person) -> int:
    if any(map(lambda f: f(person_one, person_two), (same_person, same_family, partners, same_as_last_year))):
        return DISALLOWED
    else:
        return 0


def same_family(p1: Person, p2: Person) -> bool:
    return p1.patronymic == p2.patronymic


def partners(p1: Person, p2: Person) -> bool:
    return p1.name in p2.patronymic or p2.name in p1.patronymic


def same_person(p1: Person, p2: Person) -> bool:
    return p1 == p2


def same_as_last_year(p1: Person, p2: Person) -> bool:
    return p2.full_name in p1.last_year


def convert_to_csv(filename: str, complete_set):
    """You did this with Excel last time"""
    with open(filename) as people:
        pass


def read_file(file_name: str) -> list[Person]:
    with open(file_name) as people:
        return [Person(**data) for data in csv.DictReader(people)]


def batched(iterable, n) -> Generator[list[tuple[Person, Person]], None, None]:
    "Batch data into lists of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    it = iter(iterable)
    while True:
        batch = list(itertools.islice(it, n))
        if not batch:
            return
        yield batch


def main(file_name: str):
    with open(file_name) as my_file:
        reader: Iterable[dict] = csv.DictReader(my_file)
        people = [Person(**data) for data in reader]
    all_pairs = [batch for batch in batched(itertools.product(people, repeat=2), len(people))]
    scores = [[score(*pair) for pair in row] for row in all_pairs]
    solver = Munkres()
    matches = solver.compute(scores)
    match_list = []
    for row, column in matches:
        paired_match = all_pairs[row][column]
        gifter, giftee = paired_match
        gifter.giftee = giftee
        gifter_as_dict = {fieldname: getattr(gifter, fieldname) for fieldname in reader.fieldnames}
        gifter_as_dict["this_year"] = giftee.full_name
        match_list.append(gifter_as_dict)
        print(f"{gifter} paired with {giftee}")
    print(match_list)
    fieldnames = list(reader.fieldnames)
    fieldnames.append("this_year")
    with open("2023-outcomes.csv", "w") as out:
        writer = csv.DictWriter(out, fieldnames)
        writer.writeheader()
        for row in match_list:
            writer.writerow(row)


main("2023-participants.csv")
