import csv
import dataclasses
from typing import Optional


@dataclasses.dataclass
class PersonDict:
    id: int
    name: str
    family_name: str
    number: str
    patronymic: str
    _last_year: set[str]
    this_year: Optional[str] = None

    @property
    def full_name(self) -> str:
        return f"{self.name} {self.family_name}"

    def __repr__(self) -> str:
        return f"{self.id}: {self.name} {self.family_name}"

    @property
    def last_year(self) -> str:
        return ",".join(self._last_year)

    def to_dict(self) -> dict[str, [str | int]]:
        as_dict = dataclasses.asdict(self)
        as_dict['last_year'] = self.last_year
        return as_dict


def process_match(match: tuple[PersonDict, PersonDict]) -> PersonDict:
    gifter, giftee = match
    gifter._last_year.add(giftee.full_name)
    gifter.this_year = giftee.full_name
    return gifter


def read_file(file_name: str) -> list[PersonDict]:
    person_list = []
    with open(file_name) as people:
        for row in csv.DictReader(people):
            last_year_set = set([elem.strip() for elem in row['last_year'][1:-1].replace("'", "").split(",")])
            person_list.append(PersonDict(
                row['id'],
                row['name'],
                row['family_name'],
                row['number'],
                row['patronymic'],
                last_year_set
            ))
        return person_list


def write_file(year: str, outcomes: list[PersonDict]):
    outcomes_as_dicts = [person.to_dict() for person in outcomes]
    with open(f"./{year}-outcomes.csv", "w+") as outcome_file:
        writer = csv.DictWriter(outcome_file, fieldnames=outcomes_as_dicts[0].keys())
        writer.writeheader()
        for row in outcomes_as_dicts:
            writer.writerow(row)

