import re


if __name__ == "__main__":

    # with open('example.txt', 'r') as h:
    #     example = h.readlines()
    # example = [l.rstrip('\n') for l in example]
    #


    def data_ls_to_dict(data_ls):
        out = {}
        for i, row in enumerate(data_ls):
            for j, val in enumerate(row):
                out[f'{i}_{j}'] = val

        return out


    def iter_numbers(data_ls):
        pattern = re.compile(f'\d+')
        for i, line in enumerate(data_ls):
            for j, match in enumerate(pattern.finditer(line)):
                yield i, match

    def iter_asts(data_ls):
        pattern = re.compile(f'\*')
        for i, line in enumerate(data_ls):
            for j, match in enumerate(pattern.finditer(line)):
                yield i, match

    def get_idxs(i, match):
        return [f'{i}_{j}' for j in range(match.start(), match.end())]


    def coord_valid(coord, verbose=False):  # return True if next to symbol, False otherwise
        if verbose: print(f'doing {coord=}')
        i, j = coord.split('_')
        i, j = int(i), int(j)
        s = []
        for new_i in range(i - 1, i + 2):
            for new_j in range(j - 1, j + 2):

                check = f'{new_i}_{new_j}'

                if check == coord:
                    continue

                try:
                    point = grid[check]
                except KeyError:  # boundary
                    if verbose: print(f'hit boundary at {check}')
                    s.append('b')
                    continue

                if point.isdigit():
                    if verbose: print(f'found digit ({point}) at {check}')
                    s.append('d')
                    continue
                elif point == '.':
                    if verbose: print(f'found point at {check}')
                    s.append('.')
                    continue
                else:
                    if verbose: print(f'found symbol ({point}) at {check}')
                    if point not in ['*', '-', '/', '@', '&', '+', '=', '%', '#', '$']:
                        print(point)
                    return True, point

        return False, s

    def coords_valid(coords, verbose=False):
        return any([coord_valid(coord, verbose)[0] for coord in coords])


    use_example = False
    if use_example:
        fname = 'example.txt'
    else:
        fname = 'data.txt'

    with open(fname, 'r') as h:
        data = h.readlines()


    data = [l.rstrip('\n') for l in data]

    grid = data_ls_to_dict(data)

    # numbers = [x for x in iter_numbers(example)]
    numbers = { f'{match.group()}_{c}': get_idxs(i, match) for c, (i, match) in enumerate(iter_numbers(data))}
    invalid_numbers = []
    valid_numbers = []
    for number, coords in numbers.items():
        if coords_valid(coords):
            valid_numbers.append(eval(number.split('_')[0]))
        else:
            invalid_numbers.append(eval(number.split('_')[0]))
            print(f'Not including {number}')#: {[coord_valid(coord)[1] for coord in coords]}]')

    # valid_numbers = [eval(number.split('_')[0]) for number, coords in numbers.items() if coords_valid(coords)]
    print('Part 1')
    print(sum(valid_numbers))


    print('Part 2')
    def get_neighbours_from_coord(coord):
        i, j = coord.split('_')
        i, j = int(i), int(j)

        out = []
        for new_i in range(i - 1, i + 2):
            for new_j in range(j - 1, j + 2):

                new_coord = f'{new_i}_{new_j}'

                if new_coord == coord:
                    continue

                out.append(new_coord)

        return out

    def get_neighbours_from_coords(coords):
        out = []
        for coord in coords:
            out.extend(get_neighbours_from_coord(coord))

        # remove duplicates
        out = list(set(out))
        return out




    # find asts, find index
    # find numbers, find coords
    # for every ast, see if its index is in the coords of 2 numbers

    asts = [get_idxs(*a)[0] for a in iter_asts(data)]
    ratios = []
    for ast_idx in asts:

        # ast adjacent numbers
        ast_numbers = []

        for number_key, coords in numbers.items():

            number = eval(number_key.split('_')[0])

            neighbours = get_neighbours_from_coords(coords)

            if ast_idx in neighbours:
                ast_numbers.append(number)

        if len(ast_numbers) == 1:
            print(f'Skipping {ast_numbers[0]}')
        elif len(ast_numbers) == 2:
            ratio = ast_numbers[0] * ast_numbers[1]
            ratios.append(ratio)

    print(sum(ratios))









