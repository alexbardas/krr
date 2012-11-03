from bnf import match_parentheses, add_parentheses, parse_formula, evaluate
from ftree import FTree

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


    print '\n'
    print 'Testing evaluate()'
    f = evaluate
    assert FTree.compare(f('(p and q)'), FTree('and', left=FTree('p'), right=FTree('q')))
    assert FTree.compare(f('(not p)'), FTree('not', left=FTree('p')))
    assert FTree.compare(f('((p and q) or p)'),
                         FTree('or',
                               left=FTree('and', left=FTree('p'), right=FTree('q')),
                               right=FTree('p')))
    assert FTree.compare(f('(p or (q and r))'),
                         FTree('or',
                               left=FTree('p'),
                               right=FTree('and', left=FTree('q'), right=FTree('r'))))
    assert FTree.compare(f('((p and q) or (q and r))'),
                         FTree('or',
                               left=FTree('and', left=FTree('p'), right=FTree('q')),
                               right=FTree('and', left=FTree('q'), right=FTree('r'))))
    assert FTree.compare(f('(((p and (not q)) -> s) <-> (t or r))'),
                         FTree('<->',
                               left=FTree('->',
                                          left=FTree('and',
                                                     left=FTree('p'),
                                                     right=FTree('not', left=FTree('q'))),
                                          right=FTree('s')),
                               right=FTree('or', left=FTree('t'), right=FTree('r'))))
    assert FTree.compare(f('((not (p or r)) or (not q))'),
                         FTree('or',
                               left=FTree('not',
                                          left=FTree('or', left=FTree('p'), right=FTree('r'))),
                               right=FTree('not', left=FTree('q'))))


def main():
    test()

if __name__ == '__main__':
    main()