# get generated puzzles from a text file
def load_puzzles(filename):
    puzzles = {'very easy':[],'easy':[],'medium':[],'hard':[],'fiendish':[]}
    difficulty = None
    puzzle = []
    for line in open(filename):
        if len(line) == 0:
            continue
        elif line[0] == '%':
            if difficulty and len(puzzle) == 81:
                puzzles[difficulty].append(puzzle)
            puzzle = []
            difficulty = line.split('-')[-1].strip()
        else:
            puzzle += [int(x) for x in line.strip().replace('.','0')]
        puzzles[difficulty].append(puzzle)
    return puzzles

