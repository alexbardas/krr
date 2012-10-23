import sys

priority = ['not', 'and', 'or', '->', '<->']

tree = {}

propositions = [] # the set of propositions for each formula

def read_formulas(input):
    """
    Given an input file, read multiple formulas from it
    :param str input: the name of the input file
    """
    assert isinstance(input, str)

    try:
        f = open(input, 'U')
    except IOError, e:
        raise Exception('Invalid file!')

    lines = f.readlines()

    formulas = []
    maps = {'&': 'and', '|': 'or', '!': 'not'}

    for line in lines:
        formula = ''
        iterator = iter(line)

        prop = set()
        ws = ''
        for c in iterator:
            if c in ['p', 'q', 'r', 's', 't', 'u', 'v']:
                formula += ws + c
                prop.add(c)
            elif c == ' ':
                continue
            elif c == '\n':
                continue
            elif c in ['!', '&', '|']:
                formula += ws + maps[c]
            elif c == '-' and iterator.next() == '>':
                # We don't have to check for IndexError because we know that
                # the input is valid
                formula += ws + '->'
            elif c == '<' and iterator.next() == '-' and iterator.next() == '>':
                formula += ws + '<->'
            elif c == '(':
                formula += ws + '('
            elif c == ')':
                formula += ')'
            ws = '' if c == '(' else ' '

        formulas.append(formula)
        propositions.append(prop)
    f.close()

    return formulas

def parse_formula(formula):
    """
    :params list formula: a list of strings forming a formula
    """
    assert isinstance(formula, list)

    length = len(formula)
    for idx in xrange(0, len(formula)):
        try:
            if formula[idx].startswith('('):
                formula = match_parentheses(formula, idx)
                # After we grup a part of the formula, which is between
                # brackets into a single position, a new `inside_formula` is
                # formed at that position
                # For evaluating that and adding the necessary brackets to it
                # we must recursively evaluate it (and also another sub formula)
                # which may be trapped in it
                inside_formula = formula[idx].split(' ')
                assert inside_formula[0].startswith('(')
                assert inside_formula[-1].endswith(')')
                inside_formula[0] = inside_formula[0][1:]
                inside_formula[-1] = inside_formula[-1][:-1]
                formula = formula[:idx] + parse_formula(inside_formula) + \
                        formula[idx+1:]
        except IndexError, e:
            # We are at the end of the formula and some open parentheses were
            # found
            pass

    for token in priority:
        while 1:
            if token == 'not':
                # `not` can be preceded by multiple '(', while the other tokens can't
                # e.g: ['not', 'q'] -> ['not q']
                # Get the first position of not
                found_token = False
                for idx in range(0, len(formula)):
                    if formula[idx].endswith('not'):
                        found_token = True
                        formula = add_parentheses(formula, idx)
                        break

                if not found_token: break

            else:
                # 'and' , 'or', '->' and '<->' cases are all the same
                # e.g: ['p', 'and', 'q'] -> ['(p and q)']
                try:
                    idx = formula.index(token)
                except ValueError, e:
                    # The token doesn't exist in the formula so get to the next one
                    break
                formula = add_parentheses(formula, idx)

    return formula


def match_parentheses(formula, pos=0):
    """
    Transforms a list of strings delimited by parentheses into a single string

    Given the first position of an open bracket, it finds its closing bracket and
    tranforms the list between them into a string, without modifying the rest
    of the formula

    :param list formula: list of strings from a formula
    :param int pos: the position of the first '('
    """
    assert formula[pos].startswith('(')

    # Count the number of open parentheses between the first one and its match
    open_parentheses = -1

    for idx in range(pos, len(formula)):
        c = formula[idx].count('(')
        if c:
            open_parentheses += c
        c = formula[idx].count(')')
        if c:
            if open_parentheses -c + 1 <= 0:
                formula = formula[0:pos] + [' '.join(formula[pos:idx+1])] + formula[idx+1:]
                return formula
            else:
                open_parentheses -= c

    return formula


def add_parentheses(formula, idx=0):
    """
    Given a formula and an operator index for it, close the closest matching
    expression in a set of brackets
    :param int idx: the position of the operator for which we want to add
            parenthesess
    """
    token = formula[idx]

    assert token in ['and', 'or', '->', '<->'] or token.endswith('not')

    if token.endswith('not'):
        right = formula.pop(idx + 1)
        formula[idx] = '(%s %s)' % (token, right)
    else:
        formula = formula[:idx-1] + ['(%s %s %s)' % (formula[idx-1],
                        formula[idx], formula[idx+1])] + formula[idx+2:]
        # Same as
        # right = formula.pop(idx + 1)
        # left = formula.pop(idx - 1)
        # formula[idx-1] = '(%s %s %s)' % (left, token, right)

    return formula

def main(formulas):
    for formula in formulas:
        formula = parse_formula(formula.split(' '))
        print formula


if __name__ == '__main__':

    input_file = sys.argv[1]
    formulas = read_formulas(input_file)
    main(formulas)