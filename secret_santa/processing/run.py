import itertools
import random
from typing import Iterable, Generator

from munkres import Munkres

from .file_actions import PersonDict, process_match, write_file, read_file
from .scoring import score
from send import make_client, send


def batched(iterable: Iterable[PersonDict], n: int) -> Generator[list[tuple[PersonDict, PersonDict]], None, None]:
    """Batch data into lists of length n. The last batch may be shorter."""
    # batched('ABCDEFG', 3) --> ABC DEF G
    it = iter(iterable)
    while True:
        batch = list(itertools.islice(it, n))
        if not batch:
            return
        yield batch


def generate_matches(file_name: str) -> list[PersonDict]:
    people = read_file(file_name)
    random.shuffle(people)
    all_pairs = [batch for batch in batched(itertools.product(people, repeat=2), len(people))]
    scores = [[score(*pair) for pair in row] for row in all_pairs]
    solver = Munkres()
    matches = solver.compute(scores)
    match_list = []
    for row, column in matches:
        paired_match = all_pairs[row][column]
        gifter = process_match(paired_match)
        match_list.append(gifter)
        print(f"{gifter} paired with {paired_match[1]}")
    write_file("2024", match_list)
    return match_list


def send_matches(list_of_matches: list[PersonDict], dry_run: bool = True):
    twilio_client = make_client()
    for person in list_of_matches:
        if not dry_run:
            send(person.number, person.name, person.this_year, twilio_client)


