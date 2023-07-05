import random

from datetime import datetime


def generate_random_data():
    birthday: datetime = _generate_random_birthday()
    race: str = _generate_random_race()
    name: str = _generate_random_name(race=race)
    gil: int = random.randint(-10000, 10000)

    return {"birthday": birthday, "race": race, "name": name, "gil": gil}


def _generate_random_birthday():
    current_year: int = datetime.now().year
    min_birth_year: int = current_year - 200
    max_birth_year: int = current_year - 18

    # generate random birth year within the range
    birth_year: int = random.randint(min_birth_year, max_birth_year)

    # generate random birth month
    birth_month: int = random.randint(1, 12)
    birth_day: int
    # generate random birth day based on the month
    if birth_month in [1, 3, 5, 7, 8, 10, 12]:
        birth_day = random.randint(1, 31)
    elif birth_month in [4, 6, 9, 11]:
        birth_day = random.randint(1, 30)
    else:
        # february
        if birth_year % 4 == 0 and (birth_year % 100 != 0 or birth_year % 400 == 0):
            # leap years
            birth_day = random.randint(1, 29)
        else:
            birth_day = random.randint(1, 28)
    return datetime(birth_year, birth_month, birth_day)


def _generate_random_race():
    race: str = random.choice(["Hyur", "Elezen", "Miqo'te", "Roegadyn", "Au Ra"])
    # race: str = random.choice(["Miqo'te", "Au Ra"])
    return race


def _generate_random_name(race: str):
    name: str = ""
    match race:
        case "Hyur":
            name += random.choice(["Hy", "Fu", "Tha", "Ra", "El"]) + random.choice(
                ["an", "is", "el", "en", "on"]
            )
        case "Elezen":
            name += random.choice(["E", "The", "Fe", "Ha", "Ba"]) + random.choice(
                ["n", "s", "r", "l"]
            )
            name += random.choice(
                ["dir", "zir", "lar", "rand", "wald", "land", "breath"]
            )
        case "Miqo'te":
            name += random.choice(["Mi", "Na", "Ti", "Ra", "Ho"]) + random.choice(
                ["qo", "ki", "la", "to", "si"]
            )
            name += random.choice(["'te", "le", "ri", "me", "ne"])
        case "Roegadyn":
            name += random.choice(["Ro", "Ga", "Br", "Za", "Lo"]) + random.choice(
                ["e", "m", "g", "f", "r"]
            )
            name += random.choice(["gad", "gar", "garl", "dur", "dyn", "gyn", "lad"])
        case "Au Ra":
            name += random.choice(["A", "Xae", "Zae", "Yu", "Zo"]) + random.choice(
                ["u", "l", "n", "r"]
            )
            name += random.choice(["'ra", "'no", "'zu", "'li", "'ha"])
        case _:
            # Default to Hyur if the race is not recognized
            name += random.choice(["Hy", "Fu", "Tha", "Ra", "El"]) + random.choice(
                ["an", "is", "el", "en", "on"]
            )
    return name
