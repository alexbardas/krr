from bnf import match_parentheses, add_parentheses, parse_formula

formulas = \
    [
        'p and q and r or s -> t',
        'p and not q -> s <-> t or r',
        'not (p or r) or not q',
        '(p and (q or r and (s or t)) <-> (not (p -> (q or r))))',
    ]

def test():
    """
    A set of tests for checking the bnf methods functionality
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


    print '\n'
    print 'Testing parse_formula()'

    f = parse_formula
    print  f(formulas[0].split(' '))
    assert f(formulas[0].split(' ')) == ['((((p and q) and r) or s) -> t)']

    print  f(formulas[1].split(' '))
    assert f(formulas[1].split(' ')) == ['(((p and (not q)) -> s) <-> (t or r))']

    print  f(formulas[2].split(' '))
    assert f(formulas[2].split(' ')) == ['((not (p or r)) or (not q))']

    print  f(formulas[3].split(' '))
    assert f(formulas[3].split(' ')) == ['((p and (q or (r and (s or t)))) <-> (not (p -> (q or r))))']


def main():
    test()

if __name__ == '__main__':
    main()