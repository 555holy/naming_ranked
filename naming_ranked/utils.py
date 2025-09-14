"""
functions for getting the baby names
"""


def add_name(name_dict: dict[str, dict[int, int]],
             year: int,
             rank: int,
             name: str
             ) -> None:
    """
    add name, year, rank in the name_dict dictionary
    """
    if name not in name_dict:
        name_dict[name] = {year: rank}
    elif year not in name_dict[name]:
        name_dict[name][year] = rank
    elif rank < name_dict[name][year]:
        name_dict[name][year] = rank


def add_names_from_file(
        filepath: str,
        name_dict: dict[str, dict[int, int]]
) -> None:
    """
    reads a file and add names, years, ranks into name_dict
    """
    first_line = True
    with open(filepath, 'r') as f:
        for line in f:
            tokens = [token.strip() for token in line.strip().split(',')]
            if tokens:
                if first_line:
                    year = int(tokens[0])
                    first_line = False
                else:
                    rank = int(tokens[0])
                    name1 = tokens[1]
                    name2 = tokens[2]
                    add_name(name_dict, year, rank, name1)
                    add_name(name_dict, year, rank, name2)
