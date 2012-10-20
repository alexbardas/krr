formulas = \
    [
        #['p and q and r or s -> t'],
        #['p and not q -> s <-> t or r'],
        #['not (p or r) or not q'],
        ['(p and (q or r and (s or t)) <-> (not (p -> (q or r))))'],
    ]

priority = ['not', 'and', 'or', '->', '<->']

tree = {}

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
                #print idx, formula[idx],': ', formula
                formula = formula[:idx] + parse_formula(formula[idx].split(' ')[1:]) + \
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
        formula = parse_formula(formula[0].split(' '))
        print formula


def test():
    """
    A set of program tests
    """
    print 'Testing match_parentheses()'

    f = match_parentheses
    print  f(['(p', 'or', 'q)'])
    assert f(['(p', 'or', 'q)']) == ['(p or q)']

    print  f(['(p', 'or', 'q)', 'and', 's', '->', 't'])
    assert f(['(p', 'or', 'q)', 'and', 's', '->', 't']) == \
            ['(p or q)', 'and', 's', '->', 't']

    print  f(['(q', 'or', 'r', 'and', '(s', 'or', 't))'])
    assert f(['(q', 'or', 'r', 'and', '(s', 'or', 't))']) == \
            ['(q or r and (s or t))']

    print  f(['(q', 'or', '(r', 'and', '(s', 'or', 't)))'])
    assert f(['(q', 'or', '(r', 'and', '(s', 'or', 't)))']) == \
            ['(q or (r and (s or t)))']

    print  f(['((q', 'or', 'r)', 'and', '(s', 'or', 't))'])
    assert f(['((q', 'or', 'r)', 'and', '(s', 'or', 't))']) == \
            ['((q or r) and (s or t))']

    print  f(['not', 's', 'and', '((q', 'or', 'r)', 'and', '(s', 'or', 't))'], 3)
    assert f(['not', 's', 'and', '((q', 'or', 'r)', 'and', '(s', 'or', 't))'], 3) == \
            ['not', 's', 'and', '((q or r) and (s or t))']

    print  f('not (p or r) or not q'.split(' '), 1)
    assert f('not (p or r) or not q'.split(' '), 1) == \
            ['not', '(p or r)', 'or', 'not', 'q']

    print  f('(not (p -> (q or r)))'.split(' '))
    assert f('(not (p -> (q or r)))'.split(' ')) == \
            ['(not (p -> (q or r)))']

    print  f(['(p', 'and', '(q or r and (s or t))', '<->', '(not', '(p', '->', '(q', 'or', 'r))))'], 4)
    assert f(['(p', 'and', '(q or r and (s or t))', '<->', '(not', '(p', '->', '(q', 'or', 'r))))'], 4) == \
             ['(p', 'and', '(q or r and (s or t))', '<->', '(not (p -> (q or r))))']


    print '\n'
    print 'Testing add_parentheses()'

    f = add_parentheses
    print  f(['p', 'or', 'q'], 1)
    assert f(['p', 'or', 'q'], 1) == ['(p or q)']

    print  f(['p', 'or', 'q', 'and', 's'], 3)
    assert f(['p', 'or', 'q', 'and', 's'], 3) == ['p', 'or', '(q and s)']

    print  f(['(p', 'and', 'q', 'and', '(not', '(p and q)))'], 4)
    assert f(['(p', 'and', 'q', 'and', '(not', '(p and q)))'], 4) == \
            ['(p', 'and', 'q', 'and', '((not (p and q))))']

    print  f(['p', 'and', 'q', 'and', 'r', 'or', 's', '->', 't'], 1)
    assert f(['p', 'and', 'q', 'and', 'r', 'or', 's', '->', 't'], 1) == \
            ['(p and q)', 'and', 'r', 'or', 's', '->', 't']


if __name__ == '__main__':
    main(formulas)
    #test()
