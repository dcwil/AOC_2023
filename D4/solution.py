import re
from functools import reduce

if __name__ == "__main__":
    use_example = False
    if use_example:
        fname = 'example.txt'
    else:
        fname = 'data.txt'

    with open(fname, 'r') as h:
        data = h.readlines()
    data = [l.rstrip('\n') for l in data]

    pattern = re.compile(r'(\d+):\s+(\d+(?:\s+\d+)*)\s+\|\s+(\d+(?:\s+\d+)*)')

    cards = {}
    points_ls = []
    for line in data:

        match = pattern.search(line)
        card_no = int(match.group(1))
        winners = list(map(int, re.findall(r'\b\d+\b', match.group(2))))
        entries = list(map(int, re.findall(r'\b\d+\b', match.group(3))))
        
        winning_entries = list(filter(lambda x: x in winners, entries))

        cards[card_no] = {
            'copies': 1,
            'winners': winners,
            'entries': entries,
            'winning_entries': winning_entries
        }


        if len(winning_entries) > 0:
            points = 2 ** (len(winning_entries) - 1)

            points_ls.append(points)

    print(sum(points_ls))


    for i in range(1, len(cards) + 1):

        card = cards[i]

        no_wins = len(card['winning_entries'])

        for j in range(i + 1, i + no_wins + 1):
            cards[j]['copies'] += card['copies']

    print(reduce(lambda x, y: x + y, [cards[i]['copies'] for i in range(1, len(cards) + 1)]))
        
        # cards[card_no] = {
        #     'winners': ,
        #     'entries':
        # }
        
        
        


